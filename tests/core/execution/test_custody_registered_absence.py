"""A captured descendant stays owned across a later census disappearance."""
import threading
from types import SimpleNamespace

import pytest

from astrid.core.execution import custody_broker as custody


@pytest.mark.parametrize('change', [None, 'reused-child', 'unknown-grandchild',
    'missing-root', 'reused-root', 'zombie-root', 'changed-actor',
    'changed-root-handle', 'missing-captured-handle', 'empty-census'])
def test_post_registration_absence_retains_only_the_exact_acquired_handle(tmp_path, monkeypatch, change):
    owner = object.__new__(custody.ProcessCustody)
    actor = {'pid': 10, 'uid': 501, 'birth_id': 'owner'}
    root_handle = ('root', object())
    parent_handle = ('parent', object())
    captured = ('child', object())
    owner._handles = {100: root_handle, 102: parent_handle}
    owner._unadmitted_absent = {}
    owner._uncertain = None
    owner.root = tmp_path
    owner.actor = SimpleNamespace(verify=lambda: {**actor, **({'birth_id': 'changed'}
        if change == 'changed-actor' else {})})
    def row(pid, birth, parent):
        return dict(pid=pid, uid=501, birth_id=birth, parent_pid=parent,
                    pgid=100, status=2, start_sec=1000+pid, start_usec=1)
    before = {100: row(100, 'root', 1), 102: row(102, 'parent', 100),
              103: row(103, 'child', 102)}
    after = {k: dict(v) for k, v in before.items() if k != 103}
    if change == 'reused-child':
        after[103] = row(103, 'other', 102)
    elif change == 'unknown-grandchild':
        after[104] = row(104, 'new-child', 103)
    elif change == 'missing-root':
        after.pop(100)
    elif change == 'reused-root':
        after[100]['birth_id'] = 'other'
    elif change == 'zombie-root':
        after[100]['status'] = 5
    elif change == 'empty-census':
        after = {}
    samples = iter((before, after))
    def fresh():
        value = next(samples)
        if value is after and change == 'changed-root-handle':
            owner._handles[100] = ('root', object())
        return value
    registered = []
    def register(pid, birth, **kwargs):
        registered.append((pid, birth))
        if change != 'missing-captured-handle':
            owner._handles[pid] = captured
    # Synthetic acquired handles exercise this caller's post-registration
    # control only. This test creates no native authority or exit certificate.
    owner.register = register
    owner._collect_census_candidates = lambda *args: {}
    observation = dict(outcome='LIVE', identity={'parent_pid': 102}, native=before[103])
    args = dict(census=before, root_pid=100, root_handle=root_handle, actor=actor,
        previously_admitted={100, 102}, census_round=0, new_absences=[],
        fresh_census=fresh, _collected_observation=observation)
    if change is None:
        owner._register_census_candidate(103, 'child', **args)
        assert owner._handles[103] is captured and owner._uncertain is None
        assert owner._unadmitted_absent == {} and args['new_absences'] == []
    else:
        with pytest.raises(custody.CustodyError):
            owner._register_census_candidate(103, 'child', **args)
    assert registered == [(103, 'child')]


@pytest.mark.parametrize('change', [None, 'still-live', 'observation-error', 'reused',
    'missing-parent', 'parent-microsecond', 'root-zombie', 'actor', 'root-handle',
    'unknown-child', 'reappeared', 'persistence'])
def test_pre_capture_disappearance_uses_native_absence_and_keeps_zero_authority(tmp_path, monkeypatch, change):
    owner = object.__new__(custody.ProcessCustody)
    actor = {'pid': 10, 'uid': 501, 'birth_id': 'owner'}
    broker = object.__new__(custody.RoleBoundCustodyBroker)
    broker.role = 'command'
    owner._launch_broker = broker
    def row(pid, parent):
        sec = 1700000000 + pid
        return dict(pid=pid, uid=501, birth_id=custody._ps_lstart_birth(sec),
                    parent_pid=parent, pgid=100, status=2, start_sec=sec, start_usec=123456)
    before = {100: row(100, 1), 102: row(102, 100), 103: row(103, 102)}
    after = {pid: dict(value) for pid, value in before.items() if pid != 103}
    owner._handles = {100: (before[100]['birth_id'], broker),
                      102: (before[102]['birth_id'], object())}
    original_handles = dict(owner._handles)
    owner._unadmitted_absent = {}
    owner._uncertain = None
    owner._lock = threading.RLock()
    owner._census_sequence = 0
    owner.root = tmp_path
    owner.process = SimpleNamespace(pid=100)
    owner.actor = SimpleNamespace(verify=lambda: dict(actor))
    owner._verify_root = lambda: None
    owner._collect_census_candidates = lambda members, census: dict(members)
    owner._observe_candidate_exits = lambda observations: None
    writes = []
    def persist():
        if change == 'persistence':
            raise OSError('test persistence failed')
        writes.append(True)
    owner._write_observed_containment = persist
    live = dict(outcome='LIVE', native=before[103], identity={key: before[103][key]
        for key in ('pid', 'uid', 'birth_id', 'parent_pid')})
    observed = []
    def observe(pid):
        observed.append(pid)
        if len(observed) == 1 or change == 'still-live':
            return live
        if change == 'observation-error':
            return dict(outcome='OBSERVATION_ERROR', error=OSError('test observation failed'))
        return dict(outcome='ABSENT')
    monkeypatch.setattr(custody.sys, 'platform', 'darwin')
    monkeypatch.setattr(custody, 'ordinary_candidate_observation', observe)
    monkeypatch.setattr(custody, 'current_process_audit_token',
                        lambda pid: pytest.fail('absent candidate attempted token acquisition'))
    samples = []
    def fresh():
        samples.append(True)
        if change == 'reused':
            return {**after, 103: {**before[103], 'birth_id': 'replacement'}}
        if change == 'missing-parent':
            after.pop(102, None)
        elif change == 'parent-microsecond':
            after[102]['start_usec'] = 234567
        elif change == 'root-zombie':
            after[100]['status'] = 5
        elif change == 'actor':
            owner.actor = SimpleNamespace(verify=lambda: {**actor, 'uid': 999})
        elif change == 'root-handle':
            owner._handles[100] = (before[100]['birth_id'], object())
        elif change == 'unknown-child':
            after[104] = row(104, 103)
        elif change == 'reappeared' and len(samples) > 1:
            return before
        return after
    if change is None:
        result = owner.observe_census({103: before[103]['birth_id']}, census=before, fresh_census=fresh)
        assert result == {pid: value['birth_id'] for pid, value in after.items()}
        record = owner._unadmitted_absent[103]
        assert record['stage'] == 'ancestry-recheck-no-authority-absence'
        assert record['disposition'] == 'UNADMITTED_ABSENT' and record['capability'] == 'NONE'
        assert record['exit_reap'] == record['subtree'] == 'UNPROVED'
        assert owner._uncertain is None and owner._handles == original_handles
        assert observed == [103, 103] and writes
    else:
        with pytest.raises((custody.CustodyError, OSError)):
            owner.observe_census({103: before[103]['birth_id']}, census=before, fresh_census=fresh)
        assert owner._uncertain is not None
    assert 103 not in owner._handles and not list(tmp_path.glob('designation-*'))
