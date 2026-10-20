"""Replay the portable fixture with real Agent code and in-memory test ports.

Run from the Agent checkout with PYTHONPATH pointing at that checkout.
No local admission cache, build, service, sockets or dependency writes needed.
"""
from __future__ import annotations

import json
from pathlib import Path

from pytest import MonkeyPatch

from astrid.sdk.timeline.commit import _digest
from tests.sdk.test_timeline_commit_provider import DetachedRealm, runtime_abi
from tests.sdk.test_timeline_selected_param_authority import _commit, _source


def main():
    fixture = json.loads(Path(__file__).with_name(
        'selected-param-original-pin-counterexample.json').read_text())
    sources = []
    with MonkeyPatch.context() as patch:
        runtime_abi.__wrapped__(patch)
        for case in fixture['cases']:
            realm = DetachedRealm(fixture['input'])
            for verified, objects in fixture['schema_inputs']:
                realm.live_sources[_digest(verified['pin'])] = verified
                realm.snapshot_objects.update(objects)
            previous = case['initial_head']
            for entry in case['history']:
                assert entry['previous'] == previous
                previous = {key: entry[key] for key in ('publication_id', 'revision_id')}
                records = entry['records']['commands']
                _commit(realm, [record['command'] for record in records])
                assert realm.entries[-1]['records'] == entry['records']
            assert previous == case['head']
            document = realm.documents[realm.head['revision_id']]
            assert document == fixture['canonical_document']
            record = realm.entries[-1]['records']['commands'][0]
            source = _source(record, fixture['select'], fixture['element'])
            assert source == case['expected_schema_source']
            sources.append(source)
    assert sources[0] != sources[1]
    print(json.dumps({'cases': 2, 'accepted_effects': 6, 'record_envelopes_equal': True,
                      'entire_canonical_documents_equal': True,
                      'expected_next_sources_distinct': True}))


if __name__ == '__main__':
    main()
