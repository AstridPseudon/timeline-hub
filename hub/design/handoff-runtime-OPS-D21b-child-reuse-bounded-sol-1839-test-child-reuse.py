import base64
import csv
import fnmatch
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import tarfile
import tempfile
import tomllib
import runpy

HERE = Path(__file__).resolve().parent
PREFIX = Path(__file__).name.removesuffix('test-child-reuse.py')
def artifact(name): return HERE / (PREFIX + name)
helpers = runpy.run_path(str(artifact('fixture-sources.py')))
footprint = helpers['footprint']
SESSION = tempfile.TemporaryDirectory(prefix='controls-', dir=os.environ['TMPDIR'])
ROOT = Path(SESSION.name).resolve()
assert ROOT.is_relative_to(Path(os.environ['TMPDIR']).resolve())
O = ROOT / 'orch'
W = ROOT / 'work'
for path in [O / 'queue/pending', O / 'queue/done', O / 'tests', W]:
    path.mkdir(parents=True)
A, R = helpers['make_sources'](ROOT)
SCRIPTS = ROOT / 'scripts'; SCRIPTS.mkdir()
for name in ['request-child-venv.sh', 'make-child-venv.sh', 'fixture-python.sh']:
    shutil.copyfile(artifact(name), SCRIPTS / name)
    (SCRIPTS / name).chmod(0o755)
def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])
agent = git(A, 'rev-parse', 'HEAD').decode().strip()
runtime = git(R, 'rev-parse', 'HEAD').decode().strip()
snapshot = W / '.child-venv-source-fixture'
files = {}
for name, repo, sha in [('agent', A, agent), ('runtime', R, runtime)]:
    source = snapshot / name
    source.mkdir(parents=True)
    files[name] = {}
    with tarfile.open(fileobj=io.BytesIO(git(repo, 'archive', sha))) as archive:
        for entry in archive:
            if entry.isdir():
                continue
            assert entry.isfile(), entry.name
            data = archive.extractfile(entry).read()
            files[name][entry.name] = data
            target = source / entry.name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)

def readonly(root):
    for path in [*root.rglob('*'), root]:
        path.chmod(stat.S_IMODE(path.stat().st_mode) & ~0o222)

def edit(path, data):
    path.chmod(stat.S_IMODE(path.stat().st_mode) | 0o200)
    path.write_bytes(data if isinstance(data, bytes) else data.encode())
    path.chmod(stat.S_IMODE(path.stat().st_mode) & ~0o222)

client = {p.removeprefix('packages/python/'): data for p, data in files['runtime'].items() if p.startswith('packages/python/astrid_runtime_client/')}
identity = '\n'.join('packages/python/' + p + '=' + hashlib.sha256(data).hexdigest() for p, data in sorted(client.items()))
base = W / 'venv-agent-child-base'
site_rel = Path('lib/python3.13/site-packages')
site = base / site_rel
(base / 'bin').mkdir(parents=True)
shutil.copyfile(artifact('fixture-python.sh'), base / 'bin/python')
(base / 'bin/python').chmod(0o755)
for name, distname in [('agent', 'astrid'), ('runtime', 'astrid-runtime')]:
    config = tomllib.loads(files[name]['pyproject.toml'].decode())
    discovery = config['tool']['setuptools']['packages']['find']
    installed = {}
    for rel, data in files[name].items():
        package = str(Path(rel).parent).replace('/', '.')
        if rel.endswith('.py') and any(fnmatch.fnmatch(package, pat) for pat in discovery['include']) and not any(fnmatch.fnmatch(package, pat) for pat in discovery.get('exclude', [])):
            installed[rel] = data
    if name == 'agent':
        installed.update(client)
    for rel, data in installed.items():
        target = site / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    dist = site / (distname.replace('-', '_') + '-0.1.0.dist-info')
    dist.mkdir(parents=True)
    (dist / 'METADATA').write_text(f'Name: {distname}\nVersion: 0.1.0\n')
    (dist / 'direct_url.json').write_text(json.dumps({'url': (snapshot / name).as_uri(), 'dir_info': {'editable': False}}))
    rows = []
    for target in [*(site / rel for rel in installed), dist / 'METADATA', dist / 'direct_url.json']:
        data = target.read_bytes()
        digest = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).decode().rstrip('=')
        rows.append([target.relative_to(site).as_posix(), 'sha256=' + digest, str(len(data))])
    rows.append([(dist / 'RECORD').relative_to(site).as_posix(), '', ''])
    with (dist / 'RECORD').open('w') as stream:
        csv.writer(stream).writerows(rows)

def origins(bench):
    return ''.join(f'{p}={bench / site_rel / p}/__init__.py\n' for p in ['astrid', 'astrid_runtime', 'runtime_protocol', 'astrid_runtime_client'])
(base / '.astrid-import-origins').write_text(origins(base))
(base / '.astrid-source-commit').write_text(agent + '\n')
(base / '.astrid-runtime-source-commit').write_text(runtime + '\n')
(base / '.astrid-runtime-client-identity').write_text(identity + '\n')
readonly(snapshot)
readonly(base)

count = 0
def run(label, script, work, name, expected, extra=None, minimal=False, sha=None):
    global count
    footprint(label + '-before')
    # This assertion is mandatory before EVERY requester/maker execution.
    for path in [O, work]:
        assert path.resolve().is_relative_to(ROOT) and not path.is_symlink()
    env = {'PATH': '/usr/bin:/bin', 'HOME': str(ROOT)} if minimal else dict(os.environ)
    env.update(CHILD_VENV_ORCH_ROOT=str(O), CHILD_VENV_WORK_ROOT=str(work), CHILD_VENV_AGENT_CHECKOUT=str(A), CHILD_VENV_RUNTIME_CHECKOUT=str(R), CHILD_VENV_PYTHON=str(SCRIPTS / 'fixture-python.sh'))
    env.update(extra or {})
    def manifest(bench):
        return [(str(p.relative_to(bench)), p.lstat().st_mode, os.readlink(p) if p.is_symlink() else hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else '') for p in sorted([bench, *bench.rglob('*')])]
    retained_before = manifest(work / name) if script == 'make-child-venv.sh' else None
    result = subprocess.run([str(SCRIPTS / script), name, sha or agent, 'base-suite', 'remotion-graph'], env=env, capture_output=True, text=True)
    (ROOT / (label + '.log')).write_text(result.stdout + result.stderr)
    if retained_before is not None:
        assert retained_before == manifest(work / name), 'maker mutated retained target: ' + label
    if expected == 'reuse':
        assert result.returncode == 0 and 'registration=existing' in result.stdout, (label, result)
    elif expected == 'queue':
        assert result.returncode == 0 and 'queued; result in' in result.stdout, (label, result)
    else:
        assert result.returncode != 0, (label, result)
    footprint(label + '-after')
    count += 1
    print(f'PASS {label} rc={result.returncode}', flush=True)
    return result

# Keep one immutable baseline and one mutable copy. Reset only private fixture
# bytes and permissions; move added entries aside rather than deleting anything.
bench = W / 'venv-agent-child-target'
shutil.copytree(base, bench)
quarantine = ROOT / 'mutated-entries'; quarantine.mkdir()
reset_count = 0
def reset_bench():
    global reset_count
    footprint('before-reset-group')
    reset_count += 1
    for path in [bench, *bench.rglob('*')]:
        if not path.is_symlink(): path.chmod(0o755 if path.is_dir() else 0o644)
    expected = {p.relative_to(base) for p in base.rglob('*')}
    for path in sorted(bench.rglob('*'), key=lambda p: len(p.parts)):
        if not path.exists() and not path.is_symlink(): continue
        rel = path.relative_to(bench)
        if rel not in expected:
            path.rename(quarantine / (str(reset_count) + '-' + str(rel).replace('/', '_')))
    for source in base.rglob('*'):
        target = bench / source.relative_to(base)
        if source.is_dir(): target.mkdir(exist_ok=True)
        else:
            target.write_bytes(source.read_bytes())
            target.chmod(stat.S_IMODE(source.stat().st_mode))
    edit(bench / '.astrid-import-origins', origins(bench))
    readonly(bench)
    footprint('after-reset-group')

def probe(label, mutate=None, expected='refuse', maker=True):
    reset_bench()
    if mutate: mutate(bench)
    extra = {'CHILD_VENV_REUSE_TARGET': str(bench)}
    run(label, 'request-child-venv.sh', W, bench.name, expected, extra)
    if maker: run(label + '-maker', 'make-child-venv.sh', W, bench.name, expected, extra)
    return bench

probe('positive', expected='reuse')
def standard_lib64(b):
    b.chmod(0o755)
    (b / 'lib64').symlink_to('lib')
    b.chmod(0o555)
probe('standard-lib64', standard_lib64, expected='reuse')
run('positive-env-i', 'request-child-venv.sh', W, 'venv-agent-child-base', 'reuse', {'CHILD_VENV_REUSE_TARGET': str(base)}, True)
probe('bad-agent-marker', lambda b: edit(b / '.astrid-source-commit', '0'*40))
probe('bad-runtime-marker', lambda b: edit(b / '.astrid-runtime-source-commit', '0'*40))
probe('partial-marker', lambda b: edit(b / '.astrid-runtime-client-identity', 'partial'))
probe('missing-marker', lambda b: (b.chmod(0o755), (b / '.astrid-source-commit').rename(b / '.missing'), b.chmod(0o555)))
probe('clientbyte', lambda b: edit(b / site_rel / 'astrid_runtime_client/generated.py', b'tamper'))
probe('agentbyte', lambda b: edit(b / site_rel / 'astrid/__init__.py', b'tamper'))
probe('runtimebyte', lambda b: edit(b / site_rel / 'astrid_runtime/__init__.py', b'tamper'))
probe('version', lambda b: edit(b / site_rel / 'astrid-0.1.0.dist-info/METADATA', 'Name: astrid\nVersion: 9.9.9\n'))
probe('url', lambda b: edit(b / site_rel / 'astrid-0.1.0.dist-info/direct_url.json', json.dumps({'url': 'file:///missing', 'dir_info': {}})))
probe('editable', lambda b: edit(b / site_rel / 'astrid-0.1.0.dist-info/direct_url.json', json.dumps({'url': (snapshot / 'agent').as_uri(), 'dir_info': {'editable': True}})))
for label, row in [('record-shape', 'broken\n'), ('record-absolute', '/unsafe,,\n'), ('record-blank', '\n'), ('record-size', 'astrid_runtime/__init__.py,sha256=bad,x\n'), ('record-duplicate', 'astrid_runtime/__init__.py,,\n')]:
    probe(label, lambda b, row=row: edit(b / site_rel / 'astrid_runtime-0.1.0.dist-info/RECORD', (b / site_rel / 'astrid_runtime-0.1.0.dist-info/RECORD').read_text() + row))
probe('writable-root', lambda b: b.chmod(0o755))
probe('writable-nested', lambda b: (b / site_rel / 'astrid').chmod(0o755))
probe('writable-file', lambda b: (b / site_rel / 'astrid/__init__.py').chmod(0o644))
def missing_module(b):
    path = b / site_rel / 'astrid/__init__.py'
    path.parent.chmod(0o755)
    path.rename(path.with_suffix('.missing'))
    path.parent.chmod(0o555)
probe('partial-package', missing_module)
def symlink(b):
    b.chmod(0o755)
    (b / 'escape').symlink_to(snapshot)
    b.chmod(0o555)
probe('symlink', symlink)
# Wrong/missing Agent checkouts must fail before lookup, even with valid bench markers.
for label, checkout in [('missing-checkout', ROOT / 'missing'), ('wrong-checkout', R)]:
    run(label, 'request-child-venv.sh', W, base.name, 'refuse', {'CHILD_VENV_AGENT_CHECKOUT': str(checkout)})
    run(label+'-maker', 'make-child-venv.sh', W, base.name, 'refuse', {'CHILD_VENV_AGENT_CHECKOUT': str(checkout)})
# Invalid existing destination must never reach venv/provisioning or mutate it.
partial = W / 'venv-agent-child-empty'
partial.mkdir()
run('same-name-empty', 'make-child-venv.sh', W, partial.name, 'refuse')
assert list(partial.iterdir()) == []
reset_bench()
run('ambiguity', 'request-child-venv.sh', W, 'venv-agent-child-new', 'refuse')
# Retained source tampering is checked independently of markers and distribution metadata.
source_file = snapshot / 'agent/pyproject.toml'
original = source_file.read_bytes()
edit(source_file, original + b'\n# tamper\n')
run('sourcebyte', 'request-child-venv.sh', W, base.name, 'refuse', {'CHILD_VENV_REUSE_TARGET': str(base)})
edit(source_file, original)
(snapshot / 'agent/astrid').chmod(0o755)
run('source-writable', 'request-child-venv.sh', W, base.name, 'refuse', {'CHILD_VENV_REUSE_TARGET': str(base)})
(snapshot / 'agent/astrid').chmod(0o555)

# Re-sign a mutated file in RECORD to distinguish source authentication from
# merely detecting stale RECORD hashes.
def resign(b, dist, target):
    record = b / site_rel / dist / 'RECORD'
    rows = list(csv.reader(io.StringIO(record.read_text())))
    data = (b / site_rel / target).read_bytes()
    digest = 'sha256=' + base64.urlsafe_b64encode(hashlib.sha256(data).digest()).decode().rstrip('=')
    for row in rows:
        if row[0] == target:
            row[1:] = [digest, str(len(data))]
    stream = io.StringIO()
    csv.writer(stream).writerows(rows)
    edit(record, stream.getvalue())
def signed_client(b):
    edit(b / site_rel / 'astrid_runtime_client/generated.py', b'# wrong canonical client\n')
    resign(b, 'astrid-0.1.0.dist-info', 'astrid_runtime_client/generated.py')
probe('signed-clientbyte', signed_client)
def signed_agent(b):
    edit(b / site_rel / 'astrid/__init__.py', b'# wrong Agent bytes\n')
    resign(b, 'astrid-0.1.0.dist-info', 'astrid/__init__.py')
probe('signed-agentbyte', signed_agent)
def wrong_owner(b):
    a = b / site_rel / 'astrid-0.1.0.dist-info/RECORD'
    r = b / site_rel / 'astrid_runtime-0.1.0.dist-info/RECORD'
    rows = list(csv.reader(io.StringIO(a.read_text())))
    moved = [row for row in rows if row[0].startswith('astrid_runtime_client/')]
    keep = [row for row in rows if not row[0].startswith('astrid_runtime_client/')]
    stream = io.StringIO(); csv.writer(stream).writerows(keep); edit(a, stream.getvalue())
    stream = io.StringIO(); csv.writer(stream).writerows(moved); edit(r, r.read_text() + stream.getvalue())
probe('wrong-owner', wrong_owner)
def fake_launcher(b):
    edit(b / 'bin/python', '#!/bin/bash\nexit 0\n')
    edit(b / site_rel / 'astrid_runtime-0.1.0.dist-info/RECORD', 'malformed\n')
probe('fake-child-launcher', fake_launcher)
probe('fake-valid-launcher', lambda b: edit(b / 'bin/python', '#!/bin/bash\nexit 0\n'))
# Missing and malformed installed metadata and source snapshots fail closed.
probe('runtime-version', lambda b: edit(b / site_rel / 'astrid_runtime-0.1.0.dist-info/METADATA', 'Name: astrid-runtime\nVersion: 9.0\n'))
probe('runtime-url', lambda b: edit(b / site_rel / 'astrid_runtime-0.1.0.dist-info/direct_url.json', '{}'))
probe('missing-record', lambda b: edit(b / site_rel / 'astrid-0.1.0.dist-info/RECORD', ''))
probe('source-missing', lambda b: edit(b / site_rel / 'astrid-0.1.0.dist-info/direct_url.json', json.dumps({'url': (W / '.child-venv-source-deleted/agent').as_uri(), 'dir_info': {}})))
run('maker-env-i', 'make-child-venv.sh', W, base.name, 'reuse', {'CHILD_VENV_REUSE_TARGET': str(base)}, True)
# A private git shim changes observed source state only on the post-scan check.
# It delegates all real source reads to Git; no source checkout is changed.
shim = ROOT / 'shim'; shim.mkdir()
real_git = shutil.which('git')
script = '#!/bin/bash\n' + 'COUNT=' + str(shim / 'count') + '\n' + 'if [[ "$*" == *" status "* ]]; then\n n=0; [ ! -f "$COUNT" ] || n=$(cat "$COUNT"); n=$((n+1)); echo "$n" > "$COUNT"; [ "$n" -le 2 ] || { echo " M source-race"; exit 0; }; fi\nexec ' + real_git + ' "$@"\n'
(shim / 'git').write_text(script); (shim / 'git').chmod(0o755)
run('source-race', 'request-child-venv.sh', W, base.name, 'refuse', {'PATH': str(shim) + ':/usr/bin:/bin', 'CHILD_VENV_REUSE_TARGET': str(base)})
(shim / 'count').write_text('2')
run('dirty-source', 'request-child-venv.sh', W, base.name, 'refuse', {'PATH': str(shim) + ':/usr/bin:/bin'})

for label, sha in [('wrong-commit', '0' * 40), ('malformed-commit', 'bad')]:
    run(label, 'request-child-venv.sh', W, base.name, 'refuse', sha=sha)
    run(label + '-maker', 'make-child-venv.sh', W, base.name, 'refuse', sha=sha)
probe('agent-record-shape', lambda b: edit(b / site_rel / 'astrid-0.1.0.dist-info/RECORD', (b / site_rel / 'astrid-0.1.0.dist-info/RECORD').read_text() + 'broken\n'))
probe('record-traversal', lambda b: edit(b / site_rel / 'astrid_runtime-0.1.0.dist-info/RECORD', (b / site_rel / 'astrid_runtime-0.1.0.dist-info/RECORD').read_text() + '../../../../escape,,\n'))
def ambiguous_dist(b):
    site = b / site_rel
    site.chmod(0o755)
    shutil.copytree(site / 'astrid-0.1.0.dist-info', site / 'astrid-9.9.9.dist-info')
    readonly(site)
probe('ambiguous-dist', ambiguous_dist)
# Missing non-package source files must refuse, even when every installed
# module and every distribution RECORD row is otherwise authentic.
for rel in ['agent/README.md', 'agent/astrid/nested/command.py', 'runtime/README.md']:
    path = snapshot / rel
    saved = ROOT / ('missing-' + rel.replace('/', '_'))
    path.parent.chmod(0o755); path.rename(saved); path.parent.chmod(0o555)
    run('source-partial-' + rel.replace('/', '-'), 'request-child-venv.sh', W, base.name, 'refuse', {'CHILD_VENV_REUSE_TARGET': str(base)})
    path.parent.chmod(0o755); saved.rename(path); path.parent.chmod(0o555)
# Signed backend mutations cannot bypass source custody either.
def signed_runtime(b):
    edit(b / site_rel / 'astrid_runtime/__init__.py', b'# wrong backend bytes\n')
    resign(b, 'astrid_runtime-0.1.0.dist-info', 'astrid_runtime/__init__.py')
probe('signed-runtimebyte', signed_runtime)
# Canonical client inventory and package ownership are complete, not just a
# comparison of the RECORD rows that happened to remain.
def drop_client_row(b):
    record = b / site_rel / 'astrid-0.1.0.dist-info/RECORD'
    rows = [row for row in csv.reader(io.StringIO(record.read_text())) if row[0] != 'astrid_runtime_client/generated.py']
    stream = io.StringIO(); csv.writer(stream).writerows(rows); edit(record, stream.getvalue())
probe('missing-client-row', drop_client_row)
def unowned_agent_file(b):
    folder = b / site_rel / 'astrid'; folder.chmod(0o755)
    (folder / 'extra.py').write_text('# unowned module\n'); readonly(folder)
probe('unowned-agent-module', unowned_agent_file)
# A symlinked retained name is never a qualified physical bench.
link = W / 'venv-agent-child-link'; link.symlink_to(base, target_is_directory=True)
run('same-name-symlink', 'request-child-venv.sh', W, link.name, 'refuse')
run('same-name-symlink-maker', 'make-child-venv.sh', W, link.name, 'refuse')
# Each source-byte and permission refusal also takes the maker's early path.
source_file = snapshot / 'agent/README.md'; original = source_file.read_bytes()
edit(source_file, b'tamper\n')
run('sourcebyte-maker', 'make-child-venv.sh', W, base.name, 'refuse')
edit(source_file, original)
(snapshot / 'runtime/runtime_protocol').chmod(0o755)
run('source-writable-maker', 'make-child-venv.sh', W, base.name, 'refuse')
(snapshot / 'runtime/runtime_protocol').chmod(0o555)

assert sorted(W.glob('.child-venv-source-*')) == [snapshot]
assert list((O / 'tests').iterdir()) == []
footprint('final-security-group')
print(f'PASS {count} custody controls; roots={ROOT}', flush=True)
(ROOT / 'result').write_text(f'{count} controls passed\n')

# Restore permissions solely on this disposable fixture so cleanup is bounded.
for entry in [ROOT, *ROOT.rglob('*')]:
    if not entry.is_symlink(): entry.chmod(0o755 if entry.is_dir() else 0o644)
SESSION.cleanup()
footprint('after-disposable-fixture-release')
