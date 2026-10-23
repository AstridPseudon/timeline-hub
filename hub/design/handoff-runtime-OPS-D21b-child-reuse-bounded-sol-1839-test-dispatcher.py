import os
from pathlib import Path
import re
import subprocess
import tempfile
import runpy

HERE = Path(__file__).resolve().parent
PREFIX = Path(__file__).name.removesuffix('test-dispatcher.py')
def artifact(name): return HERE / (PREFIX + name)
helpers = runpy.run_path(str(artifact('fixture-sources.py')))
footprint = helpers['footprint']
footprint('before-dispatcher-group')
SESSION = tempfile.TemporaryDirectory(prefix='dispatcher-', dir=os.environ['TMPDIR'])
ROOT = Path(SESSION.name).resolve()
assert ROOT.is_relative_to(Path(os.environ['TMPDIR']).resolve())
A, R = helpers['make_sources'](ROOT)
SHARED = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
expected = {'O': str(SHARED), 'W': '/home/user/work', 'A': '/home/user/work/agent', 'R': '/home/user/work/runtime'}
# Evaluate ONLY root assignments: no requester, maker, daemon, or shared writes.
for script in ['request-child-venv.sh', 'make-child-venv.sh']:
    text = (artifact(script)).read_text()
    assignments = '\n'.join(re.findall(r'^[OWAR]=.*$', text, re.M))
    check = subprocess.run(['/bin/bash', '-c', assignments + '\nprintf "%s\\n" "$O" "$W" "$A" "$R"'], env={'PATH': '/usr/bin:/bin'}, capture_output=True, text=True, check=True)
    assert check.stdout.splitlines() == [expected[k] for k in ['O', 'W', 'A', 'R']]
    print('PASS production-defaults ' + script)

raw = (SHARED / 'bin/dispatcher-daemon').read_text()
branch = next(line.strip() for line in raw.splitlines() if "'^CHILDVENV '" in line)
assert branch.startswith('elif ') and branch.endswith('rc=$?')
# Keep the real branch condition, command substitution, unquoted word splitting,
# stderr capture and exit status. O is faithfully taken from daemon context,
# with its sole hardcoded root rewritten to this private fixture.
context = next(line for line in raw.splitlines() if line.startswith('O='))
fixture_context = context.replace(str(SHARED), str(ROOT / 'orch'))
assert fixture_context != context
(root_orch := ROOT / 'orch/bin').mkdir(parents=True)
(ROOT / 'orch/queue/pending').mkdir(parents=True)
(ROOT / 'orch/queue/done').mkdir(parents=True)
(ROOT / 'work').mkdir()
requester = (artifact('request-child-venv.sh')).read_text()
requester = requester.replace(str(SHARED), str(ROOT / 'orch')).replace('W=${CHILD_VENV_WORK_ROOT:-/home/user/work}', 'W=${CHILD_VENV_WORK_ROOT:-' + str(ROOT / 'work') + '}')
requester = requester.replace('/home/user/work/agent', str(A)).replace('/home/user/work/runtime', str(R))
(ROOT / 'orch/bin/request-child-venv').write_text(requester)
(ROOT / 'orch/bin/request-child-venv').chmod(0o755)
# The only executed maker is a mock in the private installed layout.
(ROOT / 'orch/bin/make-child-venv').write_text('''#!/bin/bash
[ "$#" = 4 ] || exit 40
for key in CHILD_VENV_ORCH_ROOT CHILD_VENV_WORK_ROOT CHILD_VENV_AGENT_CHECKOUT CHILD_VENV_RUNTIME_CHECKOUT; do
  [ -z "${!key+x}" ] || exit 41
done
printf 'arg=%s\\n' "$@"
''')
(ROOT / 'orch/bin/make-child-venv').chmod(0o755)
body = '#!/bin/bash\n' + fixture_context + '\nf=$1\nif false; then :\n' + branch + '\nelse exit 42; fi\nprintf "%s\\n" "$out"\nexit "$rc"\n'
(ROOT / 'dispatch-branch.sh').write_text(body)
sha = subprocess.check_output(['git', '-C', str(A), 'rev-parse', 'HEAD'], text=True).strip()
for mode in ['normal', 'env-i']:
    # Assert private queue/work roots before EVERY requester execution.
    assert str(ROOT / 'orch') in requester and str(ROOT / 'work') in requester
    assert (ROOT / 'orch').resolve().is_relative_to(ROOT)
    assert (ROOT / 'work').resolve().is_relative_to(ROOT)
    name = 'venv-agent-child-call-' + mode
    args = [name, sha, 'base-suite', 'remotion-graph']
    env = dict(os.environ) if mode == 'normal' else {'PATH': '/usr/bin:/bin', 'HOME': str(ROOT)}
    env = {key: value for key, value in env.items() if not key.startswith('CHILD_VENV_')}
    cmd = [str(ROOT / 'orch/bin/request-child-venv'), *args]
    if mode == 'env-i':
        cmd = ['/usr/bin/env', '-i', 'PATH=/usr/bin:/bin', 'HOME=' + str(ROOT), *cmd]
    result = subprocess.run(cmd, env=env, capture_output=True, text=True)
    assert result.returncode == 0, result
    payload = ROOT / 'orch/queue/pending' / ('childvenv-' + name)
    assert payload.read_text() == 'CHILDVENV ' + ' '.join(args) + '\n'
    dispatch = ['/bin/bash', str(ROOT / 'dispatch-branch.sh'), str(payload)]
    if mode == 'env-i':
        dispatch = ['/usr/bin/env', '-i', 'PATH=/usr/bin:/bin', 'HOME=' + str(ROOT), *dispatch]
    result = subprocess.run(dispatch, env=env, capture_output=True, text=True)
    assert result.returncode == 0 and result.stdout == ''.join('arg=' + arg + '\n' for arg in args), result
    print('PASS exact-payload actual-branch mock-maker ' + mode)
(ROOT / 'extraction.txt').write_text('Original context:\n' + context + '\nOriginal branch:\n' + branch + '\n')
print('PASS default-root evaluation and private-only dispatcher fixtures roots=' + str(ROOT))

footprint('after-dispatcher-group')

# Restore permissions solely on this disposable fixture so cleanup is bounded.
for entry in [ROOT, *ROOT.rglob('*')]:
    if not entry.is_symlink(): entry.chmod(0o755 if entry.is_dir() else 0o644)
SESSION.cleanup()
footprint('after-disposable-fixture-release')
