"""A captured descendant stays owned across a later census disappearance."""
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
    if change == 'reused-child': after[103] = row(103, 'other', 102)
    elif change == 'unknown-grandchild': after[104] = row(104, 'new-child', 103)
    elif change == 'missing-root': after.pop(100)
    elif change == 'reused-root': after[100]['birth_id'] = 'other'
    elif change == 'zombie-root': after[100]['status'] = 5
    elif change == 'empty-census': after = {}
    samples = iter((before, after))
    def fresh():
        value = next(samples)
        if value is after and change == 'changed-root-handle':
            owner._handles[100] = ('root', object())
        return value
    registered = []
    def register(pid, birth, **kwargs):
        registered.append((pid, birth))
        if change != 'missing-captured-handle': owner._handles[pid] = captured
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
