"""Provider-only capture and explicit legacy load admission; no fake Runtime proof."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline.commit import _digest
from astrid.sdk.timeline.new_group_commands import capture_migrate_groups
from tests.editing_conformance.test_recipe_m2_group_migration import GROUPS, legacy_document
from tests.sdk.test_timeline_commit_provider import (
    CommitRejected,
    DetachedRealm,
    source_fixture,
)
from tests.sdk.test_timeline_commit_provider import (
    runtime_abi as runtime_abi,
)

pytestmark = pytest.mark.usefixtures('runtime_abi')


def test_provider_migration_preview_reads_exact_retained_transcript_and_media():
    document = legacy_document()
    transcript = source_fixture('transcript')
    document['dependency_manifest']['documents'] = [transcript['pin']]
    realm = DetachedRealm(document)
    realm.live_sources[_digest(transcript['pin'])] = transcript
    command = capture_migrate_groups(document, GROUPS)
    result = realm.call([command], dry_run=True)
    assert result['receipt'] is None
    assert realm.accepted == [] and realm.prepared == []
    assert ('transcript', transcript['pin']) in realm.reads
    canonical = result['data']['canonical_document']
    assert canonical['dependency_manifest']['documents'] == [transcript['pin']]
    assert canonical['dependency_manifest']['media'] == document['dependency_manifest']['media']
    assert canonical['parent_revision']['payload']['occurrences'][0]['duration_ms'] == 4000
    assert realm.documents[realm.head['revision_id']] == document


def test_provider_ordinary_edit_on_legacy_is_refused_before_preview():
    document = legacy_document()
    realm = DetachedRealm(document)
    before = copy.deepcopy(realm.documents)
    with pytest.raises(CommitRejected, match='explicit timeline.migrate-groups'):
        realm.call([{'schema_version': 1, 'op': 'track.create', 'version': '1',
                     'select': 'parent', 'args': {'row': {'id': 'x', 'kind': 'visual'}}}], dry_run=True)
    assert realm.documents == before and realm.prepared == []
