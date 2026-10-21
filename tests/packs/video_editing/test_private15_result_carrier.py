"""Regression for the existing managed speech result carrier."""
from __future__ import annotations

from types import SimpleNamespace

from astrid.sdk.results import InvocationResult
from tests.packs.video_editing import test_outer_voiceover_native as native


def test_private15_speech_helper_selects_managed_output_port(monkeypatch):
    """Runtime ManagedOutput has ``output_port`` and no legacy ``name`` field."""
    row = {
        "association_id": "managed-output-speech",
        "output_port": "speech",
        "object_id": "sha256:" + "a" * 64,
        "digest": "sha256:" + "a" * 64,
    }
    result = InvocationResult(
        capability_id="generation.generate_speech",
        capability_type="executor",
        native_kind="executor",
        ok=True,
        outputs={"managed_outputs": [row]},
    )
    selection = {
        "asset": "asset-1",
        "generation_id": "generation-1",
        "variant_id": "variant-1",
        "object_id": row["object_id"],
        "catalog_digest": "catalog-1",
    }
    verified = {"media_type": "audio/wav", "duration_seconds": 4.0}
    seen = {}

    def read_authoritative_media_info(client, project, output):
        seen.update(client=client, project=project, output=output)
        return selection, verified

    monkeypatch.setattr(
        "astrid.packs.video_editing.shared.draft_voiceover._read_authoritative_media_info",
        read_authoritative_media_info,
    )
    client = SimpleNamespace(
        invoke_result=lambda *args, **kwargs: result,
    )

    returned, actual_selection, actual_verified = native._speech_result(
        client, "project-1", "hello", "carrier"
    )

    assert returned is result
    assert actual_selection == selection
    assert actual_verified == verified
    assert seen == {"client": client, "project": "project-1", "output": row}
