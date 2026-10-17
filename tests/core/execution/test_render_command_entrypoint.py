"""The real V3 launch/pipe must reach the guarded pack, even after env filtering.

Only argparse help is requested: this is an entrypoint regression, not a render
or a Runtime/publication witness. No renderer or readiness response is supplied.
"""
import os
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

from astrid.core.contracts.schema import CommandSpec
from astrid.core.execution import generic_host as host
from tests.core.execution import test_confinement_launch_integration as confinement

launch = confinement.launch


def test_v3_render_command_restores_canonical_entrypoint_after_pipe(tmp_path, launch):
    policy, *_ = launch
    checkout = Path(host.__file__).resolve().parents[3]
    policy = replace(policy, bootstrap_roots=(*policy.bootstrap_roots, checkout),
        bootstrap_files=(*policy.bootstrap_files,
            Path('/opt/homebrew/opt/libb2/lib/libb2.1.dylib'),
            Path('/opt/homebrew/opt/openssl@3/lib/libcrypto.3.dylib'),
            Path('/opt/homebrew/opt/openssl@3/lib/libssl.3.dylib')))
    h = host.GenericPackHost(pack_roots=[checkout / 'astrid/packs/rendering'],
                             confinement_policy=policy)
    try:
        h.discover()
        record = h.capabilities['rendering.render']
        _, admission = h.admit('executor', record.id)
        admission = {**admission, 'capability_id': record.id,
                     'python_path_roots': list(host._admitted_python_roots(record.source_root, record.definition))}
        # Keep the actual module/source/guard and real Host stdio handshake.
        # Help avoids materialization, renderer calls and output publication.
        record = replace(record, definition=replace(record.definition,
            inputs=(), outputs=(),
            command=CommandSpec(argv=('{python_exec}', '-m',
                'astrid.packs.rendering.actions.render.run', '--help'))))
        plan = h._workload_launch_plan
        observed = []
        def observe(argv, **kwargs):
            result = plan(argv, **kwargs)
            assert 'ASTRID_INTERNAL_INVOCATION' not in result.environment
            observed.append(result)
            return result
        h._workload_launch_plan = observe
        result = h._run_command_definition(record, {}, policy.private_write_root,
                                            policy.attempt_root, admission=admission)
        assert result.returncode == 0
        assert result.process_id > 0 and len(observed) == 1
        assert not h._active_processes
    finally:
        h.shutdown()


def test_external_render_module_still_refuses_direct_entrypoint():
    checkout = Path(host.__file__).resolve().parents[3]
    environment = {key: value for key, value in os.environ.items()
                   if key != 'ASTRID_INTERNAL_INVOCATION'}
    result = subprocess.run([sys.executable, '-I', '-B', '-c',
        'import runpy,sys; sys.path.insert(0,sys.argv.pop(1)); '
        'runpy.run_module("astrid.packs.rendering.actions.render.run",run_name="__main__")',
        str(checkout), '--help'], env=environment, capture_output=True, text=True)
    assert result.returncode == 2
    assert 'not meant to be invoked directly' in result.stderr
