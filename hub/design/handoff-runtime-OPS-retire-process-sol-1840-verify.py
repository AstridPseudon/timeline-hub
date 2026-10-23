"""Read-only source and exact-byte checks; never execute installed handlers."""
import hashlib
from pathlib import Path
import subprocess

O = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
D = O / 'design/handoff-runtime-OPS-retire-process-sol-1840'
T = Path('/tmp/w-ef8d3fdfde')
def artifact(suffix):
    return Path(str(D) + suffix)
script = artifact('-diagnostic.py').read_bytes()
command = artifact('-command.sh').read_bytes()
assert command == b"python3 - <<'PY'\n" + script + b"PY\n"
old = (O/'design/handoff-runtime-OPS-retire-process-return-1832.md').read_bytes().split(b"python3 - <<'PY'\n", 1)[1].split(b'\nPY\n', 1)[0]
assert hashlib.sha256(old).hexdigest() == '582405d5d6478e80560a35bb2cb523adae7b7a80e7dda4a068449ece69b2ff69'
for suffix in ('-diagnostic.py', '-checks.py', '-verify.py'):
    compile(artifact(suffix).read_bytes(), str(artifact(suffix)), 'exec')
print('PASS scoped in-memory compile: diagnostic, checks, verify')
for suffix, name in (('-diagnostic.py', 'diagnostic.py'), ('-command.sh', 'command.sh')):
    result = subprocess.run(['cmp', str(artifact(suffix)), str(T/name)])
    assert result.returncode == 0
    print('PASS cmp', suffix, 'exit 0')
doc = artifact('.md').read_bytes()
embedded = doc.split(b'```sh\n', 1)[1].split(b'```', 1)[0]
assert embedded == command
(T/'extracted-command.sh').write_bytes(embedded)
result = subprocess.run(['cmp', str(T/'extracted-command.sh'), str(artifact('-command.sh'))])
assert result.returncode == 0
print('PASS exact handoff first command fence extraction, cmp exit 0')
for name, expected in (
    ('retire-child-venv', '954d5d87fe2e6fcf42b34953ec0edc519a2eb97ade8f66f0f2f96f523516b791'),
    ('request-retire-venv', '21f61833a6718794ab2a06a3a96d34ca58c050ccd0151622e16866ac78758139'),
):
    path = O/'bin'/name
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected
    result = subprocess.run(['bash', '-n', str(path)])
    assert result.returncode == 0
    print('PASS unchanged source SHA256 and bash -n', name, 'exit 0')
handler = (O/'bin/retire-child-venv').read_text()
request = (O/'bin/request-retire-venv').read_text()
daemon = (O/'bin/dispatcher-daemon').read_text()
for snippet in ('wc -c < "$proc/cmdline"', 'if [ "$bytes" -eq 0 ]; then', 'process executable is unreadable', 'path_uses_candidate "$link"', 'process cwd is unreadable', 'process open files are unreadable', 'is_our_process "$pid" && continue'):
    assert snippet in handler, snippet
assert "printf 'RETIREVENV %s\\n'" in request
assert '^RETIREVENV ' in daemon and '$O/bin/retire-child-venv' in daemon
print('PASS source structure only: real cmdline byte count, empty/nonempty exe branches, own-process exclusion, target/cwd/fd checks, unchanged request route')
repo = '/home/user/work/wt/rt-OPS-retire-process-sol-1840'
for args in (['git', 'diff', '--check'], ['git', 'diff', '--exit-code'], ['git', 'status', '--porcelain']):
    result = subprocess.run(args, cwd=repo, capture_output=True, text=True)
    assert result.returncode == 0 and result.stdout == '' and result.stderr == ''
    print('PASS', ' '.join(args), 'exit 0; empty output')
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo, text=True).strip()
assert head == '2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d'
print('PASS Runtime HEAD', head)
for suffix in ('-diagnostic.py', '-command.sh', '-checks.py', '-verify.py'):
    data = artifact(suffix).read_bytes()
    print('SHA256', hashlib.sha256(data).hexdigest(), artifact(suffix).name, 'bytes', len(data))
print('Actual HOST/remote proc and installed handler/request execution: UNRUN')
