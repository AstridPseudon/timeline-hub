import hashlib, json, os, shutil, subprocess, tarfile
from pathlib import Path
W=Path(__file__).parent
R=Path('/home/user/work/wt/vw-m3-live-source-label-native-join')
P=W/'runtime'/'remotion'
if not P.exists():
    shutil.copytree(R/'remotion', P)
    (P.parent/'astrid').symlink_to(R/'astrid', target_is_directory=True)
    shutil.copytree('/home/user/work/wt/vw-m1-ssr-snapshot/remotion/node_modules', P/'node_modules', symlinks=True)
    package=P/'node_modules/@banodoco/timeline-composition'
    shutil.rmtree(package)
    artifact=P/'artifacts/banodoco-timeline-composition-0.0.12.tgz'
    assert hashlib.sha256(artifact.read_bytes()).hexdigest()=='0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3'
    with tarfile.open(artifact) as archive:
        archive.extractall(W/'extract', filter='data')
    (W/'extract/package').rename(package)
    (W/'extract').rmdir()
if not (W/'node').exists():
    with tarfile.open('/tmp/node-v20.19.4-linux-x64.tar.xz') as archive:
        data=archive.extractfile('node-v20.19.4-linux-x64/bin/node').read()
    assert hashlib.sha256(data).hexdigest()=='43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490'
    (W/'node').write_bytes(data); (W/'node').chmod(0o755)
print(P)
