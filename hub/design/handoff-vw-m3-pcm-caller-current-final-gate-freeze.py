from pathlib import Path
import ast
import difflib
import hashlib
import importlib.util
import json
import subprocess

script = Path(__file__).with_name('handoff-vw-m3-pcm-caller-current-final-gate-prepare.py')
spec = importlib.util.spec_from_file_location('prepare', script)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
O, W, P, git = m.O, m.W, m.P, m.git
producer = O / 'workers/vw-m3-pcm-caller-current-land-unit'
assert (producer/'DONE').exists(), 'producer is not DONE'
assert not (producer/'running').exists(), 'producer still running'
assert (producer/'exit').read_text().strip() == '0'
ref = 'tl/vw-m3-pcm-caller-current-land-unit'
sha = git('rev-parse', ref).decode().strip()
assert sha != m.BASE and git('rev-parse', sha+'^').decode().strip() == m.BASE
candidate = W / 'candidate'
archive_hash = m.extract(sha, candidate)
entries = []
for entry in git('ls-tree','-r','-z',sha).split(b'\0'):
    if not entry:
        continue
    header, path = entry.split(b'\t',1)
    mode, kind, blob = header.decode().split()
    name = path.decode()
    dest = candidate/name
    data = dest.readlink().as_posix().encode() if mode == '120000' else dest.read_bytes()
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest() == blob
    entries.append(dict(path=name, mode=mode, blob=blob, sha256=hashlib.sha256(data).hexdigest()))
Path(str(P)+'-blobs.json').write_text(json.dumps(entries,indent=2)+'\n')
baseline = W/'baseline'
names = {row['path'] for row in entries} | {str(p.relative_to(baseline)) for p in baseline.rglob('*') if p.is_file()}
changed = sorted(name for name in names if not (baseline/name).exists() or not (candidate/name).exists() or (baseline/name).read_bytes() != (candidate/name).read_bytes())
caller = ['astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py',
          'astrid/packs/rendering/rendering/renderers/remotion/run.py',
          'tests/packs/rendering/test_normal_audio_http.py',
          'tests/packs/rendering/test_normal_audio_run.py']
assert changed == caller, changed
patch = ''.join(''.join(difflib.unified_diff((baseline/name).read_text().splitlines(keepends=True) if (baseline/name).exists() else [], (candidate/name).read_text().splitlines(keepends=True), fromfile='a/'+name if (baseline/name).exists() else '/dev/null', tofile='b/'+name)) for name in changed)
Path(str(P)+'-caller-only.patch').write_text(patch)
assert not any(p.suffix in ['.orig','.rej','.bak'] for p in candidate.rglob('*'))
assert not (candidate/'.git').exists()
assert not (candidate/'remotion/artifacts/banodoco-timeline-composition-0.0.10.tgz').exists()
run = caller[1]
def functions(path):
    return {f.name:ast.dump(f,include_attributes=False) for f in ast.parse(path.read_text()).body if isinstance(f,(ast.FunctionDef,ast.AsyncFunctionDef))}
old,new = functions(baseline/run),functions(candidate/run)
assert set(old)==set(new)
assert [name for name in old if old[name]!=new[name]] == ['_execute_remotion_locked']
http = (candidate/caller[2]).read_text()
for forbidden in ['/tmp/claude','/home/user/','scratchpad','ORCH','0.0.10']:
    assert forbidden not in http, forbidden
record = dict(producer_sha=sha, producer_tree=git('rev-parse',sha+'^{tree}').decode().strip(), base=m.BASE, extent=m.EXTENT,
              source_archive=str(W/'candidate-source.tar'), archive_sha256=archive_hash,
              blobs=len(entries), caller_only_paths=changed, caller_patch_sha256=hashlib.sha256(patch.encode()).hexdigest(),
              protected_all_other_paths_equal=True)
Path(str(P)+'-freeze.json').write_text(json.dumps(record,indent=2)+'\n')
Path(str(P)+'-whole.patch').write_bytes(git('diff','--binary',m.BASE,sha))
print(json.dumps(record,indent=2))
