from pathlib import Path
import difflib
import hashlib
import json
import subprocess
import tarfile

orch = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
work = orch / 'workers/vw-m3-app-delivered-theme-seam'
app = work / 'offline-app'
repo = Path('/home/user/work/wt/vw-m3-app-delivered-theme-seam')
paths = [('src/tools/video-editor/compositions/TimelineRenderer.tsx', 'renderer-baseline.tsx'),
         ('src/tools/video-editor/components/PreviewPanel/RemotionPreview.tsx', 'preview-baseline.tsx')]
check = work / 'patch-check'
actual = ''
for file, baseline in paths:
    target = check / file
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes((work / baseline).read_bytes())
    actual += ''.join(difflib.unified_diff((work / baseline).read_text().splitlines(True),
                                         (app / file).read_text().splitlines(True),
                                         fromfile='a/' + file, tofile='b/' + file))
patch = orch / 'design/handoff-vw-m3-app-delivered-theme-seam-UNAPPLIED.patch'
subprocess.run(['git', 'apply', '--check', '--whitespace=error-all', str(patch)], cwd=check, check=True)
assert actual == patch.read_text()
count = 0
with tarfile.open(orch / 'artifacts/banodoco-timeline-composition-0.0.10.tgz') as archive:
    for member in archive:
        if member.isfile():
            assert archive.extractfile(member).read() == (work / 'public10' / member.name).read_bytes()
            count += 1
source = json.loads((orch / 'design/handoff-vw-m3-app-delivered-theme-seam-source.json').read_text())['source']
for file, digest in source['sha256'].items():
    assert hashlib.sha256((work / 'agent-source' / file).read_bytes()).hexdigest() == digest
    original = subprocess.check_output(['git', 'show', source['agent_head'] + ':' + file], cwd='/home/user/peteromallet/astrid-agent')
    assert hashlib.sha256(original).hexdigest() == digest
status = subprocess.check_output(['git', 'status', '--porcelain'], cwd=repo, text=True)
assert not status, status
result = {'patch_check': 'PASS', 'restored_product_matches_published_patch': True,
          'public10_unchanged_files': count, 'agent_resolver_matches_frozen_git_objects': True,
          'assigned_worktree_status': status, 'full_suite_requested': False,
          'targeted': {'files': 7, 'passed': 132, 'seconds': 10.64},
          'red': {'selected': 7, 'failed': 6, 'passed': 1, 'filtered': 59},
          'type_probe': 'PASS', 'scoped_product_eslint': 'PASS'}
(orch / 'design/handoff-vw-m3-app-delivered-theme-seam-postflight.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
