"""Real paired synthetic task: invalid launch proposals never reach spawn."""
import pytest

from astrid.core.execution import generic_host as gh
from test_task_authority_host_canary import flow, submit, assert_probe


def test_paired_claim_rejects_unowned_launch_context_before_spawn(flow, tmp_path, monkeypatch):
    d, host, projects, sessions = flow
    task = submit(flow, 0, 'bound-launch-proposals')['data']['task_id']
    original = host._workload_launch_plan
    observed = []

    def bound_plan(argv, **context):
        # Exercise the actual claimed attempt, real executable and immutable
        # policy. No test-only allow authority or launch/broker substitute.
        claim = dict(host._attempt_claim_authority.fields)
        assert claim['task_id'] == task and claim['project_id'] == projects[0]
        grant = d.httpd.paired_sessions._sessions[sessions[0][1]['pair_id']]
        assert grant.actor == 'connector-0' and grant.connector_id == 'connector-0'
        assert grant.realm_id == d.service.realm['id'] and grant.project_id == projects[0]
        for field, value, reason in (
            ('attempt', tmp_path / 'unowned', 'different attempt'),
            ('cwd', tmp_path, 'cwd exceeds'),
            ('inherited_fds', (123,), 'descriptors'),
        ):
            assert not host._active_processes
            with pytest.raises(gh.HostError, match=reason):
                original(argv, **{**context, field: value})
            assert not host._active_processes
            assert d.service.store.list_managed_outputs(task) == []
            observed.append(field)
        return original(argv, **context)

    monkeypatch.setattr(host, '_workload_launch_plan', bound_plan)
    assert host.claim_once()
    assert observed == ['attempt', 'cwd', 'inherited_fds']
    assert d.service.task(task)['task']['status'] == 'completed'
    assert_probe(d, task)  # Actual child and descendant OS confinement denials.
