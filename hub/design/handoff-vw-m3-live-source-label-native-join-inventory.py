import hashlib, json, os, subprocess, tarfile
from pathlib import Path
W=Path(__file__).parent
R=Path('/home/user/work/wt/vw-m3-live-source-label-native-join')
P=W/'runtime/remotion'
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def tree(root):
    return {str(p.relative_to(root)): ('link:'+os.readlink(p)) if p.is_symlink() else sha(p)
            for p in sorted(root.rglob('*')) if p.is_file() or p.is_symlink()}
with tarfile.open(R/'remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz') as archive:
    wanted={str(Path(m.name).relative_to('package')):hashlib.sha256(archive.extractfile(m).read()).hexdigest()
            for m in archive if m.isfile()}
assert len(wanted)==77
assert tree(P/'node_modules/@banodoco/timeline-composition')==wanted
tracked=subprocess.check_output(['git','-C',str(R),'ls-files','-z']).decode().split('\0')
sources={name:sha(R/name) for name in tracked if name and (R/name).is_file()}
sources['tests/packs/rendering/test_live_source_label_native.py']=sha(R/'tests/packs/rendering/test_live_source_label_native.py')
value={'public12':wanted,'source':sources,'peer_graph':tree(Path('/home/user/work/wt/vw-m1-ssr-snapshot/remotion/node_modules')),
       'private_graph':tree(P/'node_modules'),'node':sha(W/'node'),
       'runtime_source':tree(W/'runtime-source'),
       'python_toolchain':{str(p.relative_to(W/'python-overlay')):sha(p)
                           for p in (W/'python-overlay').rglob('*')
                           if p.is_file() and '__pycache__' not in p.parts},
       'runtime':subprocess.check_output(['git','-C','/home/user/work/runtime','rev-parse','HEAD']).decode().strip()}
file=W/(os.sys.argv[1]+'.json')
file.write_text(json.dumps(value,sort_keys=True,separators=(',',':')))
print(file,sha(file),len(value['peer_graph']),len(value['private_graph']),len(sources))
