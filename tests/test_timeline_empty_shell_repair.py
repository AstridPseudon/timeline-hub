"""Same-ID create repairs only an exact empty headless shell, atomically."""
from __future__ import annotations

import copy

import pytest

from runtime_protocol.errors import ConflictError
from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore
from runtime_protocol.timeline_commit_baseline import empty_bootstrap_document, verify_baseline
from test_timeline_commit_port import PreparedProvider


@pytest.fixture
def service(tmp_path):
    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    runtime = RuntimeService(root)
    project = runtime.create_project({"slug": "shell", "name": "Shell"}, idempotency_key="project")["id"]
    # Created before a commit provider exists, so no publication is installed.
    runtime.create_timeline(project, "main", idempotency_key="create-main")
    runtime.register_timeline_commit_provider(PreparedProvider())
    try:
        yield runtime, project
    finally:
        runtime.close()


def _shell(service, project, *, parent="empty-parent", payload=None, key="shell"):
    payload = payload or empty_bootstrap_document(project, "main", parent)["parent_revision"]["payload"]
    return service.publish_parent_composition(project, "main", {
        "project_id": project, "timeline_id": "main", "expected_head": None,
        "parent_revision_id": parent, "parent_composition": payload,
    }, idempotency_key=key)


def _dump(service):
    return tuple(service.store.conn.iterdump())


def _refused_untouched(service, call):
    before = _dump(service)
    with pytest.raises(ConflictError) as error:
        call()
    assert error.value.status == 409
    assert error.value.details == {"timeline_id": "main"}
    assert _dump(service) == before


def _head(service, project):
    return service.get_project_timeline(project, "main")


def test_empty_headless_shell_is_repaired_once_and_replays_identically(service):
    runtime, project = service
    _shell(runtime, project)
    assert _head(runtime, project)["head_publication_id"] is None

    first = runtime.create_timeline(project, "main", idempotency_key="adopt")
    head = _head(runtime, project)
    assert head["head_publication_id"] is not None
    assert head["head_revision_id"] == "empty-parent"
    history = runtime.list_timeline_commits(project, "main", authorize=lambda: None)
    assert [entry["intent"] for entry in history["items"]] == ["bootstrap"]
    assert verify_baseline(runtime.store.conn, project, "main", read_object=runtime.cas.read)["canonical_document"] \
        == empty_bootstrap_document(project, "main", "empty-parent")

    before = _dump(runtime)
    assert runtime.create_timeline(project, "main", idempotency_key="adopt") == first
    assert _dump(runtime) == before


def test_replayed_adoption_never_reapplies_over_later_writes(service):
    runtime, project = service
    _shell(runtime, project)
    first = runtime.create_timeline(project, "main", idempotency_key="adopt")
    runtime.rename_timeline(project, "main", {"name": "Later"}, idempotency_key="rename")
    history = runtime.list_timeline_commits(project, "main", authorize=lambda: None)

    assert runtime.create_timeline(project, "main", idempotency_key="adopt") == first
    assert runtime.list_timeline_commits(project, "main", authorize=lambda: None) == history
    _refused_untouched(runtime, lambda: runtime.create_timeline(project, "main", idempotency_key="second"))


def test_crash_before_commit_leaves_shell_and_retry_adopts_once(service, monkeypatch):
    runtime, project = service
    _shell(runtime, project)
    before = _dump(runtime)

    def crash(*args, **kwargs):
        raise RuntimeError("crash after adoption, before receipt")

    monkeypatch.setattr(runtime, "_command_record", crash)
    with pytest.raises(RuntimeError):
        runtime.create_timeline(project, "main", idempotency_key="adopt")
    monkeypatch.undo()
    assert _dump(runtime) == before
    assert _head(runtime, project)["head_publication_id"] is None

    first = runtime.create_timeline(project, "main", idempotency_key="adopt")
    assert runtime.create_timeline(project, "main", idempotency_key="adopt") == first
    assert len(runtime.list_timeline_commits(project, "main", authorize=lambda: None)["items"]) == 1


def test_original_create_replay_is_unchanged_by_adoption(service):
    runtime, project = service
    original = runtime.create_timeline(project, "main", idempotency_key="create-main")
    _shell(runtime, project)
    runtime.create_timeline(project, "main", idempotency_key="adopt")

    before = _dump(runtime)
    assert runtime.create_timeline(project, "main", idempotency_key="create-main") == original
    assert _dump(runtime) == before


def test_headed_timeline_is_refused_untouched(service):
    runtime, project = service
    _shell(runtime, project)
    runtime.create_timeline(project, "main", idempotency_key="adopt")
    _refused_untouched(runtime, lambda: runtime.create_timeline(project, "main", idempotency_key="other"))


def test_non_empty_headless_shell_is_refused_untouched(service):
    runtime, project = service
    payload = copy.deepcopy(empty_bootstrap_document(project, "main", "non-empty")["parent_revision"]["payload"])
    payload["config"] = {"clips": [], "tracks": [{"id": "picture", "kind": "visual", "role": "output", "opaque": [None, False]}]}
    _shell(runtime, project, parent="non-empty", payload=payload)
    _refused_untouched(runtime, lambda: runtime.create_timeline(project, "main", idempotency_key="adopt"))
    assert _head(runtime, project)["head_publication_id"] is None


def test_wrong_project_or_name_is_refused_untouched(service):
    runtime, project = service
    _shell(runtime, project)
    other = runtime.create_project({"slug": "other", "name": "Other"}, idempotency_key="other")["id"]
    _refused_untouched(runtime, lambda: runtime.create_timeline(other, "main", idempotency_key="foreign"))
    _refused_untouched(runtime, lambda: runtime.create_timeline(project, "main", name="Renamed", idempotency_key="renamed"))
