"""Memory-only report declaration and exact published Proof receipt parser tests.
No Store/build/installer, fake environment, permission change or publication.
"""
import ast
import contextlib
import hashlib
import io
from pathlib import Path
import subprocess
import sys
import types

HERE = Path(__file__).resolve().parent
PREFIX = Path(__file__).name.removesuffix('test-receipts.py')
OLD = 'handoff-runtime-OPS-bench-store-creators-1850-'
PROOF = HERE / 'handoff-ap2-P1-current-diagnostic-OPS-1813.md'
proof = PROOF.read_text()
# Exact original production preflight commands, not a reimplemented regex.
commands = [
    'grep -Eiq "(status=(passed|success)|\\b(PASS|PASSED|SUCCESS|DONE|COMPLETE)\\b)" "$CR"',
    'grep -Eq "(agent|agent_sha)=$P1A" "$CR"',
    'grep -Eq "(runtime|runtime_sha)=$P1R" "$CR"',
]
for command in commands:
    assert command in proof, command

def parse(receipt):
    for command in commands:
        # Replace only the receipt file input with stdin; exact grep bytes remain.
        result = subprocess.run(['bash', '-c', command.replace('"$CR"', '')],
                                env={'PATH': '/usr/bin:/bin', 'P1A': 'a'*40, 'P1R': 'b'*40},
                                input=receipt, text=True, capture_output=True)
        if result.returncode:
            return False
    return True

def embedded(prefix):
    text = (HERE / (prefix + 'make-child-venv.sh')).read_text()
    return ast.parse(text.split("<<'STORE_PY'\n", 1)[1].split('\nSTORE_PY\n', 1)[0])

files = {}
class MemoryPath:
    def __init__(self, *parts): self.path = '/'.join(map(str, parts))
    def __truediv__(self, other): return MemoryPath(self.path, other)
    def __str__(self): return self.path
    def read_bytes(self): return files[self.path]
    def read_text(self): return self.read_bytes().decode()

agent, backend = 'a'*40, 'b'*40
client = 'packages/python/astrid_runtime_client/__init__.py=' + 'c'*64
entry_path = '/owned/entry'
name = 'venv-agent-child-requested'
report = ('status=passed\nagent_sha=' + agent + '\nruntime_sha=' + backend +
          '\nruntime_client_identity_sha256=' + hashlib.sha256(client.encode()).hexdigest() +
          '\nrequirements_path=requirements/proof.lock\nrequirements_lock_sha256=' + 'd'*64 +
          '\ninstalled_import_origins:\nastrid=/owned/entry/lib/site-packages/astrid/__init__.py\n'
          'installed_distribution_metadata:\npip_freeze:\n').encode()
files[entry_path + '/.provision-report'] = report
files[entry_path + '/.astrid-import-origins'] = b'astrid=/owned/entry/lib/site-packages/astrid/__init__.py\n'
files[entry_path + '/.astrid-distribution-metadata'] = b''
files[entry_path + '/.astrid-source-commit'] = (agent + '\n').encode()
files[entry_path + '/.astrid-runtime-source-commit'] = (backend + '\n').encode()
files['/tests/provision/' + name + '.txt'] = report
files['/tests/suites.conf'] = b''

def namespace(prefix):
    env = dict(hashlib=hashlib, pathlib=types.SimpleNamespace(Path=MemoryPath),
               agent=agent, backend=backend, client=client, tests='/tests', name=name,
               remotion='', base_suite='', managed_remotion=False,
               requirements='requirements/proof.lock', lock='d'*64,
               verified_reports={entry_path: report})
    tree = embedded(prefix)
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in
                 ('report_bytes', 'registration', 'success_receipt')]
    exec(compile(ast.Module(body=functions, type_ignores=[]), prefix, 'exec'), env)
    return env, tree

child_source = (HERE / (PREFIX + 'make-child-venv.sh')).read_text()
freeze_identity = child_source.split("\nIDENTITY_SCRIPT=" + "'", 1)[1].split("'\nrun_stage", 1)[0]
compile(freeze_identity, 'final-path-freeze-identity', 'exec')
print('PASS exact final-path freeze identity extraction/compile')

old, tree = namespace(OLD)
new, _ = namespace(PREFIX)
for reused in (False, True):
    entry = {'reused': reused, 'path': entry_path, 'key': 'e'*64}
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        # Actual old receipt print statement; proves old RED on original parser.
        print_node = next(n for n in tree.body if isinstance(n, ast.Expr) and
                          isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Name) and
                          n.value.func.id == 'print')
        exec(compile(ast.Module(body=[print_node], type_ignores=[]), 'old-receipt', 'exec'),
             {**old, 'entry': entry})
    assert not parse(output.getvalue()), 'original receipt unexpectedly passes'
    receipt = new['success_receipt'](entry, report)
    assert parse(receipt), receipt
    assert 'actual_agent=' + agent in receipt and 'actual_runtime=' + backend in receipt
    assert 'provision_report_sha256=' + hashlib.sha256(report).hexdigest() in receipt
    assert 'requested_name=' + name in receipt and entry_path in receipt
    print('PASS oldRED/newGREEN exact Proof parser:', 'reused' if reused else 'created')

old_decl = old['registration'](entry_path, entry_path, False)
assert 'report' not in old_decl, 'old contract unexpectedly projects report'
for reused in (False, True):
    declaration = new['registration'](entry_path, entry_path, reused)
    assert declaration['report'].encode() == report
    assert declaration['env'] == '' and declaration['suite'] == ''
print('PASS oldRED/newGREEN report contract: exact verified bytes, empty env/suite')

def refuses(fn):
    try: fn()
    except (RuntimeError, KeyError, UnicodeError): return
    raise AssertionError('expected refusal')

# No verified cache, changed bytes, failed status, false tuple, malformed encoding,
# absent/different public projection cannot produce a success receipt.
new['verified_reports'].clear()
refuses(lambda: new['registration'](entry_path, entry_path, True))
new['verified_reports'][entry_path] = report
for bad in (report.replace(b'status=passed', b'status=failed'), report + b'status=passed\n',
            report.replace(agent.encode(), b'f'*40), report + b'\xff'):
    files[entry_path + '/.provision-report'] = bad
    refuses(lambda: new['registration'](entry_path, entry_path, True))
    refuses(lambda: new['success_receipt'](entry, report))
files[entry_path + '/.provision-report'] = report
for bad in (b'', report + b'altered'):
    files['/tests/provision/' + name + '.txt'] = bad
    refuses(lambda: new['success_receipt'](entry, report))
del files['/tests/provision/' + name + '.txt']
refuses(lambda: new['success_receipt'](entry, report))
assert not parse('status=failed agent=' + agent + ' runtime=' + backend)
assert not parse('status=passed agent=' + 'f'*40 + ' runtime=' + backend)
print('PASS failure/tamper/no-verification/no-projection controls')
print('Proof parser source SHA256=' + hashlib.sha256(PROOF.read_bytes()).hexdigest())
print('SOURCE fixtures only; combined child remains FAIL/UNQUALIFIED and STOPPED')

for prefix, expected in ((OLD, False), (PREFIX, True)):
    requester = (HERE / (prefix + 'request-child-venv.sh')).read_text()
    printf = next(line for line in requester.splitlines() if "printf 'reused child venv path=" in line)
    result = subprocess.run(['bash', '-c', 'qualified=(/owned/legacy)\n' + printf],
                            env={'PATH': '/usr/bin:/bin', 'S': agent, 'RUNTIME_SHA': backend},
                            text=True, capture_output=True, check=True)
    assert parse(result.stdout) == expected
print('PASS oldRED/newGREEN legacy verified-reuse receipt parser')

class RefusingStore:
    def ensure(self, component, identity, registration, build, verify):
        verify(entry_path)
        raise AssertionError('verify must refuse')
def failed_verify(path):
    raise RuntimeError('custody verification failed')
new.update(store=RefusingStore(), identity={}, build=None, verify=failed_verify, sys=sys)
tree = embedded(PREFIX)
flow = [n for n in tree.body if isinstance(n, ast.Try) or
        (isinstance(n, ast.Expr) and isinstance(n.value, ast.Call) and
         isinstance(n.value.func, ast.Name) and n.value.func.id == 'print')]
output = io.StringIO()
try:
    with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
        exec(compile(ast.Module(body=flow, type_ignores=[]), 'exact-maker-receipt-flow', 'exec'), new)
except SystemExit as error:
    assert error.code == 2
else:
    raise AssertionError('custody failure returned success')
assert 'REFUSED:' in output.getvalue() and not parse(output.getvalue())
print('PASS exact maker failure flow emits refusal and no success receipt')
