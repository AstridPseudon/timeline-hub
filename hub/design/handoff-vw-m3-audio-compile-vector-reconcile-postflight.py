import hashlib
import json
import subprocess
import tarfile
from pathlib import Path
P=Path(__file__).parent
ROOT=Path('/home/user/work/wt/vw-m3-audio-compile-vector-reconcile')
D=ROOT/'src/tools/video-editor/data'
AGENT=Path('/home/user/work/agent')
REF='fd82c36c7cd66d1d58aa0250a008245a43e6fbaa'
for name in ['shot_composition_projection.py','duration.py','shot_composition.py']:
    path='astrid/core/timeline/'+name
    assert (AGENT/path).read_bytes()==subprocess.check_output(['git','-C',str(AGENT),'show',REF+':'+path])
for repo,ref,source,target in [
    (ROOT,'1bfa51d5a','src/tools/video-editor/data/shotCompositionAudio.fixture.json','shotCompositionAudio.fixture.json'),
    (ROOT,'1bfa51d5a','src/tools/video-editor/data/shotComposition.fixture.json','shotComposition.fixture.json'),
    (AGENT,REF,'tests/editing_conformance/fixtures/audio_compile_contract.json','shotCompositionAudio.agent.fixture.json'),
    (AGENT,REF,'tests/fixtures/timeline/shot_composition.json','shotCompositionAudio.agentGraph.fixture.json'),
]:
    assert (D/target).read_bytes()==subprocess.check_output(['git','-C',str(repo),'show',ref+':'+source])
print('PASS: exact original corpora/base graphs and Agent projector/dependencies')
archive=P.parents[1]/'artifacts/banodoco-timeline-composition-0.0.11.tgz'
artifact=P.parent/'vw-m3-envelope-public-clock-join/artifact/package'
assert hashlib.sha256(archive.read_bytes()).hexdigest()=='dfa824a475737598477d98a2be2c2ad6ab9c3e6c8b0f967fad22e154afd74601'
with tarfile.open(archive) as tar:
    members=[m for m in tar.getmembers() if m.isfile()]
    for m in members:
        assert tar.extractfile(m).read()==(artifact/m.name.removeprefix('package/')).read_bytes()
print('PASS: public11 exact SHA256, 58344 bytes,',len(members),'archive/extracted files')
newfiles=subprocess.check_output(['git','-C',str(ROOT),'ls-files','--others','--exclude-standard'],text=True).splitlines()
assert len(newfiles)==6
for name in newfiles:
    data=(ROOT/name).read_text()
    assert data.endswith('\n') and all(line.rstrip()==line for line in data.splitlines()),name
assert subprocess.check_output(['git','-C',str(ROOT),'diff','--name-only'])==b''
print('PASS: six new test/fixture files only; tracked product files unchanged; new-file whitespace')
