"""Production reservation checks require the entire native ABI-1 binding set."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.timeline import commit
from tests.editing_conformance.test_doc_patch_v2 import submit
from tests.editing_conformance.test_provider_occurrence_fork import fork
from tests.editing_conformance.test_recipe_occurrence_fork import fork_document
from tests.sdk.test_timeline_commit_provider import (
    CommitRejected,
    DetachedRealm,
    inverse,
)
from tests.sdk.test_timeline_commit_provider import runtime_abi as runtime_abi


@pytest.mark.parametrize('legacy', [False, True])
@pytest.mark.parametrize('damage', [
    'reviewer-stripped-v2', 'partial', 'missing', 'duplicate', 'malformed',
    'policy', 'dependencies', 'ref', 'phase', 'extra',
])
def test_production_refuses_incomplete_abi1_and_mixed_v2(monkeypatch, legacy, damage):
    realm = DetachedRealm(fork_document())
    call = fork(realm)
    before = copy.deepcopy((realm.head, realm.entries, realm.documents, realm.prepared))
    check = commit._check_reservations
    observed = []

    def corrupt(port, plan, current, rejected, base):
        bindings = plan.records[0]['bindings']
        collection = bindings[0]
        assert collection['key'] == 'collection.owner:collection.clips'
        if damage == 'reviewer-stripped-v2':
            # Exact independent1350 attack: strip physical_ref everywhere,
            # reduce only fork.source/fork.owner to the four-key ABI-1 shape.
            for binding in bindings:
                binding.pop('physical_ref', None)
                if binding['key'] in ('fork.source', 'fork.owner'):
                    native = {key: binding[key] for key in ('key', 'ref', 'policy', 'dependencies')}
                    binding.clear()
                    binding.update(native)
            if legacy:
                collection['boundary'] = {'phase': 'input'}
        elif damage == 'partial':
            collection['physical_ref'] = 'parent' if legacy else None
        elif damage == 'missing':
            bindings.remove(collection)
        elif damage == 'duplicate':
            bindings.append(copy.deepcopy(collection))
        elif damage == 'malformed':
            bindings.append(None)
        elif damage == 'policy':
            collection['policy'] = 'caller'
        elif damage == 'dependencies':
            collection['dependencies'] = ['unproven']
        elif damage == 'ref':
            collection['ref'] = 'occurrence:occ-1'
        elif damage == 'phase':
            collection.setdefault('boundary', {})['phase'] = 'effect'
        else:
            bindings.append({'key': 'unknown', 'ref': 'parent', 'policy': 'fixed', 'dependencies': []})
        observed.append(damage)
        return check(port, plan, current, rejected, base)

    monkeypatch.setattr(commit, '_check_reservations', corrupt)
    with pytest.raises(CommitRejected):
        submit(realm, call, **({} if legacy else {'reads': []}))
    assert observed == [damage]
    assert (realm.head, realm.entries, realm.documents, realm.prepared) == before


def test_authentic_complete_abi1_binding_set_survives_history_and_inverse(monkeypatch):
    document = fork_document()
    realm = DetachedRealm(document)
    check = commit._check_reservations
    observed = []

    def observe(port, plan, current, rejected, base):
        record = plan.records[0]
        if record['command']['op'] == 'occurrence.fork':
            assert record['bindings'] == [
                {'key': key, 'ref': ref, 'policy': 'fixed', 'dependencies': []}
                for key, ref in (
                    ('collection.owner:collection.clips', 'occurrence:occ-0'),
                    ('collection.owner:collection.tracks', 'occurrence:occ-0'),
                    ('fork.source', 'occurrence:occ-0/source'),
                    ('fork.owner', 'occurrence:occ-0'))]
            observed.append(True)
        return check(port, plan, current, rejected, base)

    monkeypatch.setattr(commit, '_check_reservations', observe)
    # Omit v2 controls on the real production caller; no rewritten legacy flag.
    created = submit(realm, fork(realm))
    assert created['data']['status'] == 'accepted'
    undone = submit(realm, inverse([created['receipt']['receipt_id']]))
    assert undone['data']['canonical_document'] == document
    redone = submit(realm, inverse([undone['receipt']['receipt_id']]))
    assert redone['data']['canonical_document'] == created['data']['canonical_document']
    assert observed == [True]
