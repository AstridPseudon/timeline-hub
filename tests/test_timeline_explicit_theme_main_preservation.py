"""Preserve Main's normal imported Theme input through managed render admission.

The authored ``theme.json`` is imported into project CAS before admission.  It
is then carried as the ordinary named ``theme`` file input, alongside Runtime's
saved timeline snapshot, and materialized by the existing GenericPackHost.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from test_canonical_render_admission import _publish, _request
from test_canonical_render_admission import canonical_scene as _canonical_scene_fixture  # noqa: F401
from test_snapshot_authority_refusal import REFUSALS, _state

from runtime_protocol.service import RuntimeService

pytestmark = pytest.mark.integration


class _ObjectClient:
    """Expose only the existing CAS read used by GenericPackHost."""

    def __init__(self, service: RuntimeService):
        self.service = service

    def get_object(self, object_id: str) -> bytes:
        return self.service.object(object_id)[1]


def _theme_descriptor(service: RuntimeService, project: str, *, key: str) -> tuple[dict, bytes]:
    # Full authored Theme data, deliberately unlike the builtin default.  The
    # bytes are imported through Runtime's normal project-object API, not made
    # into an inline authority or a capture/snapshot certificate.
    authored = json.dumps(
        {
            "id": "worker-authored-cas-theme",
            "visual": {
                "canvas": {"width": 853, "height": 479, "fps": 23.976},
                "background": {"color": "#17243b", "opacity": 0.73},
                "font": {"family": "Author CAS Sans", "weight": 640},
                "accent": {"primary": "#d7ff42", "secondary": "#ff4f9a"},
            },
            "generation": {"references": [], "assets": []},
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    imported = service.ingest(
        project,
        authored,
        media_type="application/json",
        original_name="theme.json",
        idempotency_key=key,
    )["data"]
    descriptor = {
        "object_id": imported["object_id"],
        "digest": imported["digest"],
        "filename": "theme.json",
    }
    assert service.object(descriptor["object_id"])[1] == authored
    return descriptor, authored


def _managed_theme_request(fixture, descriptor: dict, *, key: str) -> dict:
    request = _request(fixture, key=key)
    request["input_object_ids"] = [descriptor["object_id"]]
    request["spec"]["inputs"] = {"theme": descriptor}
    request["spec"]["input_digests"] = [{"name": "theme", "digest": descriptor["digest"]}]
    return request


def _assert_refused_without_writes(service: RuntimeService, request: dict) -> None:
    before = _state(service)
    with pytest.raises(REFUSALS):
        service.create_task(request)
    assert _state(service) == before


def test_main_imported_theme_preserves_saved_snapshot_and_materializes_exact_bytes(
    _canonical_scene_fixture, tmp_path
):
    fixture = _canonical_scene_fixture
    _publish(fixture)
    descriptor, authored = _theme_descriptor(fixture["service"], fixture["project"], key="theme-main")
    task = fixture["service"].create_task(
        _managed_theme_request(fixture, descriptor, key="render-authored-theme")
    )["task"]

    canonical = [fixture[name]["object_id"] for name in ("package", "entry", "audio")]
    spec = task["spec"]["spec"]
    authority = spec["inputs"]["timeline_authority"]
    snapshot_ref = spec["timeline_snapshot_ref"]
    assert task["spec"]["input_object_ids"] == [
        descriptor["object_id"], *canonical, snapshot_ref["digest"]
    ]
    assert spec["inputs"]["theme"] == descriptor
    assert authority["parent_revision_id"] == "parent-1"
    assert authority["snapshot_digest"] == snapshot_ref["digest"]
    snapshot = json.loads(fixture["service"].object(snapshot_ref["digest"])[1])
    assert [clip["id"] for clip in snapshot["config"]["clips"]] == ["scene-a", "scene-b", "music"]
    assert snapshot["registry"]["assets"]["music"]["content_sha256"] == (
        fixture["audio"]["object_id"].removeprefix("sha256:")
    )

    claim = fixture["service"].claim_next(
        {
            "executor_id": "worker",
            "capability_ids": ["rendering.render"],
            "runtime_epoch": fixture["service"].health()["runtime_epoch"],
        }
    )
    assert claim["task_id"] == task["id"]

    from astrid.core.execution.generic_host import GenericPackHost

    values = GenericPackHost(pack_roots=[], client=_ObjectClient(fixture["service"]))._materialize_inputs(
        task["spec"], tmp_path / "attempt"
    )
    theme_path = Path(values["theme"])
    assert theme_path.name == "theme.json"
    assert theme_path.read_bytes() == authored
    assert Path(values["materialized_objects"]["theme"]).read_bytes() == authored


def test_explicit_theme_foreign_or_tampered_descriptor_refuses_without_writes(_canonical_scene_fixture):
    fixture = _canonical_scene_fixture
    _publish(fixture)
    service = fixture["service"]
    foreign = service.create_project({"slug": "foreign-theme", "name": "Foreign theme"})["id"]
    foreign_descriptor, _ = _theme_descriptor(service, foreign, key="foreign-theme")
    _assert_refused_without_writes(
        service,
        _managed_theme_request(fixture, foreign_descriptor, key="foreign-theme-render"),
    )

    valid, _ = _theme_descriptor(service, fixture["project"], key="tamper-theme")
    tampered = {**valid, "digest": "sha256:" + "0" * 64}
    _assert_refused_without_writes(
        service,
        _managed_theme_request(fixture, tampered, key="tampered-theme-render"),
    )
