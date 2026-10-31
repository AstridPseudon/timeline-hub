"""Runtime refusals stay definitive and preserve the exact attempted request."""
from __future__ import annotations

import copy
import hashlib
import json

import pytest

from astrid.sdk import timeline
from astrid.sdk.timeline.sync import CommitConflict
from astrid_runtime_client import ApiError
from tests.sdk import test_timeline_sync as sync_test
from tests.sdk.test_timeline_sync import connected as connected_fixture  # noqa: F401


def test_runtime_refusal_is_not_retried_or_reclassified_and_saves_verified_payload(
    connected_fixture, monkeypatch, tmp_path,
):  # noqa: F811
    client, generated, path = connected_fixture
    editor = timeline.open("p", "t", client=client, outbox_path=path)

    source = tmp_path / "refused.png"
    payload = b"refused media"
    source.write_bytes(payload)
    digest = "sha256:" + hashlib.sha256(payload).hexdigest()
    pin = {
        "asset": "refused-asset",
        "object_id": digest,
        "generation_id": "refused-generation",
        "variant_id": "refused-variant",
        "catalog_digest": "sha256:" + "b" * 64,
    }
    verified = {
        "selection": copy.deepcopy(pin),
        "media_type": "image/png",
        "size": len(payload),
        "width": 1,
        "height": 1,
    }
    import_record = {
        "object_id": digest,
        "generation_id": pin["generation_id"],
        "variant_id": pin["variant_id"],
        "catalog_write": True,
        "retained_on_undo": True,
    }
    monkeypatch.setattr("astrid.sdk.authoring_media._metadata", lambda _path: {
        "digest": digest,
        "media_type": "image/png",
        "filename": source.name,
        "width": 1,
        "height": 1,
    })
    monkeypatch.setattr(
        "astrid.sdk.timeline.media_add._selection",
        lambda *_args: (copy.deepcopy(pin), copy.deepcopy(verified)),
    )
    execute = sync_test.execute
    monkeypatch.setattr(
        sync_test,
        "execute",
        lambda bundle, commands, **kwargs: execute(
            bundle, commands, verified_media=[verified], **kwargs,
        ),
    )

    # The 409 envelope and advanced current head must not turn this definitive
    # authority refusal into a retryable conflict.
    generated.refusal = ApiError(409, "conflict", "authority revoked", details={
        "status": "refused",
        "reason": "authority_revoked",
        "current": {"revision_id": "r1", "publication_id": "pub1"},
    })
    evaluations = []

    def edit(working):
        evaluations.append(True)
        working.add(source, at=0, hold=2, id="refused-clip")

    with pytest.raises(CommitConflict) as caught:
        editor.commit(edit, idempotency_key="refused-media-edit")

    assert caught.value.failure["details"]["status"] == "refused"
    assert caught.value.pending_id
    assert len(evaluations) == 1
    assert len(generated.calls) == 1

    saved = json.loads(path.read_text(encoding="utf-8"))
    assert saved["pending"] == [] and saved["flight"] is None
    assert "conflict" not in saved and "rejected" not in saved
    rejected = saved["pending_changes"][caught.value.pending_id]
    assert rejected["state"] == "pending"
    assert rejected["origin"] == "function"
    assert rejected["failure"] == caught.value.failure
    assert rejected["clash"]["pending_id"] == rejected["id"]
    assert rejected["clash"]["runtime"]["reason"] == "authority_revoked"
    packet = rejected["parts"][0]
    assert packet["imports"] == [import_record]
    assert packet["evaluation"]["media_cache"][digest]["imports"] == [import_record]
    assert rejected["parts"][0]["evaluation"]["count"] == 1

    assert packet["base"] == {"revision_id": "r0", "publication_id": "pub0"}
    assert any(command.get("args", {}).get("media") == pin for command in packet["commands"])
    assert caught.value.clash == rejected["clash"]


def test_explicit_retry_of_exhausted_function_reruns_saved_function(
    connected_fixture, monkeypatch,
):  # noqa: F811
    client, generated, path = connected_fixture
    editor = timeline.open("p", "t", client=client, outbox_path=path)
    evaluations, sent = [], []
    commit_timeline = generated.commit_timeline
    history = []

    def timeline_history(*_args, **_kwargs):
        from astrid.sdk.contracts import DomainResult

        return DomainResult.success({
            "head": copy.deepcopy(generated.head),
            "items": copy.deepcopy(history),
            "next_cursor": None,
        })

    monkeypatch.setattr(client.timelines, "history", timeline_history)

    def refuse_three_times(*args, **kwargs):
        sent.append(kwargs["idempotency_key"])
        if len(sent) <= 3:
            # Each conflict has a verified, advancing head, exhausting automatic
            # function retries while leaving an explicit retry available.
            ordinal = len(sent)
            previous = copy.deepcopy(generated.head)
            base = generated.bundles[generated.head["revision_id"]]
            command = {"schema_version": 1, "op": "clip.move", "version": "1",
                       "select": "parent/clip:a", "args": {"on": ordinal}}
            revision = f"retry-head-{ordinal}"
            generated.bundles[revision] = sync_test.execute(base, [command]).bundle
            generated.head = {"revision_id": revision, "publication_id": f"pub-{revision}"}
            generated.publications[revision] = generated.head["publication_id"]
            history.append({"revision_id": revision, "publication_id": generated.head["publication_id"],
                            "previous": previous})
            raise ApiError(409, "conflict", "head advanced", details={
                "status": "conflict", "reason": "guard_changed",
                "current": copy.deepcopy(generated.head),
            })
        return commit_timeline(*args, **kwargs)

    monkeypatch.setattr(generated, "commit_timeline", refuse_three_times)

    def edit(working):
        evaluations.append(working.bundle["parent"]["clips"][0]["at"])
        working.move("parent/clip:a", evaluations[-1] + 1)

    with pytest.raises(CommitConflict) as exhausted:
        editor.commit(edit)

    assert exhausted.value.pending_id
    assert evaluations == [0, 1, 2]
    record = json.loads(path.read_text(encoding="utf-8"))["pending_changes"][exhausted.value.pending_id]
    assert record["origin"] == "function"
    assert record["parts"][0]["evaluation"]["count"] == 3

    result = editor.retry(exhausted.value)

    assert result["status"] == "accepted"
    assert evaluations == [0, 1, 2, 3]
    assert len(sent) == 4
    assert editor.bundle["parent"]["clips"][0]["at"] == 4
    assert editor.pending_show(exhausted.value.pending_id)["state"] == "landed"


@pytest.mark.parametrize("status", ["refused", "invalid"])
def test_list_origin_runtime_refusal_suggests_fix_retry_or_drop(
    connected_fixture, status,
):  # noqa: F811
    client, generated, path = connected_fixture
    editor = timeline.open("p", "t", client=client, outbox_path=path)
    commands = editor.commit(lambda working: working.move("parent/clip:a", 4), dry_run=True)["data"]["commands"]
    generated.refusal = ApiError(409, status, "edit is not allowed", details={
        "status": status, "reason": "policy",
    })

    with pytest.raises(CommitConflict) as caught:
        editor.commit(commands, label="Reviewed move", idempotency_key="reviewed-move")

    assert caught.value.failure["details"]["status"] == status
    assert caught.value.pending_id
    assert all(word in caught.value.fix.lower() for word in ("fix", "retry", "drop"))
    state = json.loads(path.read_text(encoding="utf-8"))
    record = state["pending_changes"][caught.value.pending_id]
    assert record["origin"] == "list"
    assert record["parts"][0]["commands"] == commands
    assert record["failure"] == caught.value.failure
