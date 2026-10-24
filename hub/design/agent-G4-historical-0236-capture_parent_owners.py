import inspect
import json
from pathlib import Path

import pytest
from tests.helpers.runtime import use_runtime

use_runtime()
import runtime_protocol.timeline_commit_auth as auth

import astrid.sdk.timeline.native_occurrence_shared as shared
namespace = {'__name__': shared.__name__, '__package__': shared.__package__}
exec(compile(Path('/tmp/w-c3868a10ef/native_occurrence_shared.parent.py').read_text(),
             '/tmp/w-c3868a10ef/native_occurrence_shared.parent.py', 'exec'), namespace)
shared.prepare_shared_inverse = namespace['prepare_shared_inverse']
original = auth.validate
captured = []
evidence = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G4-historical-inverse-sol-0236')

def capture(*args, **kwargs):
    bound = inspect.signature(original).bind(*args, **kwargs)
    bound.apply_defaults()
    values = bound.arguments
    if any(command['op'] == 'timeline.inverse' for command in values['request']['commands']):
        path = evidence / f'owner-parent-auth-{len(captured)}.json'
        encoded = json.dumps(values, indent=2, sort_keys=True)
        path.write_text(encoded + '\n')
        assert json.loads(encoded) == values
        captured.append(str(path))
        print('PRE-VALIDATION CAPTURE:', path, len(encoded))
    return original(*args, **kwargs)

auth.validate = capture
result = pytest.main(['-q', '-oaddopts=', '-p', 'no:cacheprovider',
    'tests/editing_conformance/test_historical_shared_inverse_owners.py::test_inverse_retains_existing_destination_owner',
    '--basetemp=/tmp/w-c3868a10ef/owner-parent-red', '--timeout=45', '--tb=short', '-s'])
print('CAPTURES:', captured)
raise SystemExit(result)
