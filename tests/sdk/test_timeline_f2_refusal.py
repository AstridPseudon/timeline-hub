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
    assert len(evaluations) == 1
    assert len(generated.calls) == 1

    sent_body, sent_key = generated.calls[0]
    saved = json.loads(path.read_text(encoding="utf-8"))
    rejected = saved["rejected"]
    assert saved["pending"] == [] and saved["flight"] is None
    assert "conflict" not in saved
    assert saved.get("pending_changes", {}) == {}
    assert rejected["failure"]["details"]["status"] == "refused"
    assert rejected["flight"]["body"].encode() == sent_body
    assert rejected["flight"]["key"] == sent_key == "refused-media-edit"
    assert rejected["flight"]["imports"] == [import_record]
    assert rejected["evaluation"]["media_cache"][digest]["imports"] == [import_record]

    attempted = json.loads(rejected["flight"]["body"])
    assert attempted["base_revision_id"] == "r0"
    assert attempted["base_publication_id"] == "pub0"
    assert any(command.get("args", {}).get("media") == pin for command in attempted["commands"])
    assert rejected["commands"] == attempted["commands"]
