"""Gate 1: the SDK's attached source read against an exact transcript pin.

Run centrally with the paired Runtime95bd profile. This is deliberately one
focused read gate; it does not exercise browser, render, or the earlier
word-anchor case matrix.
"""
from __future__ import annotations

import pytest

from tests.editing_conformance import test_commit_runtime_m1 as m1

pytestmark = pytest.mark.integration


@pytest.fixture
def film(tmp_path, monkeypatch):
    return m1.film.__wrapped__(tmp_path, monkeypatch)


def test_verified_transcript_pin_reads_through_public_runtime_boundary(
        tmp_path, film, real_runtime,
):
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.timeline_commit_inputs import content_digest

    fixture, _, _ = film
    service = RuntimeService(fixture.duplicate_root)
    try:
        original = service.get_document(fixture.project_id, fixture.transcript_document_id)
    finally:
        service.close()
    pin = {
        "document_id": original["document_id"],
        "version": original["version"],
        "content_digest": content_digest(original["content"]),
    }

    daemon = real_runtime(fixture.duplicate_root, support_root=tmp_path / "support")
    try:
        client = m1.open_client(daemon)
        verified = client.timelines._client.get_project_verified_document(
            fixture.project_id, pin,
        )
        assert verified["pin"] == pin
        assert verified["document"]["content"] == original["content"]
    finally:
        daemon.stop()
