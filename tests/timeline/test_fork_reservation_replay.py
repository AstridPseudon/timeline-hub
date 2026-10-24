"""Reservation replay retains authenticated native fork provenance."""
from __future__ import annotations

from astrid.core.timeline.authoring_bundle import publish_authoring_candidate
from tests.timeline.test_authoring_publication_migrations import checkout


def test_production_fork_publication_replays_native_copy_provenance():
    candidate, writer = checkout(shared=True)
    local = candidate['placements'][0]['shot_id']
    candidate['shots'][local]['payload']['items'][0]['metadata']['opaque_literal'] = 'replayed'

    result = publish_authoring_candidate(candidate, writer, idempotency_key='fork-reservation')

    assert result['publication']['status'] == 'accepted'
    assert writer.realm.entries[-1]['records']['commands'][0]['command']['op'] == 'occurrence.fork'
    assert result['publication']['canonical_document']['parent_revision']['payload']['occurrences'][1] == (
        writer.document['parent_revision']['payload']['occurrences'][1]
    )
