from pathlib import Path
import hashlib, json, os, stat, subprocess
base=Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
w=base/'workers/vw-m3-render-cap-consumer-review'
m=json.loads((base/'design/handoff-vw-m3-app-private12-clean-install-manifest.json').read_text())
root=Path(m['root'])
errors=[]
for e in m['entries']:
    p=root/e['path']; s=p.lstat()
    if stat.S_IMODE(s.st_mode)!=e['mode']: errors.append([e['path'],'mode'])
    if e['kind'] in ('file','executable'):
        if not stat.S_ISREG(s.st_mode) or hashlib.sha256(p.read_bytes()).hexdigest()!=e['sha256']: errors.append([e['path'],'file'])
    elif e['kind']=='symlink':
        if not stat.S_ISLNK(s.st_mode) or os.readlink(p)!=e['target']: errors.append([e['path'],'link'])
    elif not stat.S_ISDIR(s.st_mode):errors.append([e['path'],'directory'])
expected={e['path'] for e in m['entries'] if e['path']=='node_modules' or e['path'].startswith('node_modules/')}
actual={'node_modules'}
for directory, dirs, files in os.walk(root/'node_modules',followlinks=False):
    actual.update(str((Path(directory)/name).relative_to(root)) for name in dirs+files)
errors.extend([p,'extra-node_modules-path'] for p in sorted(actual-expected))
errors.extend([p,'missing-node_modules-path'] for p in sorted(expected-actual))
source_errors=[]
paths=['src/tools/video-editor/data/mainImageCap.fixture.json','src/tools/video-editor/data/shotCompositionProjection.test.ts','src/tools/video-editor/data/canonicalCompositionState.mainImageCap.test.ts','src/tools/video-editor/hooks/useTimelineCommandSession.ts','src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.ts','src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.tsx','src/tools/video-editor/components/PreviewPanel/RemotionPreview.tsx']
for path in paths:
    frozen=subprocess.check_output(['git','-C','/home/user/work/app','show','e6c4aae50ef2db89e482d28f25e742918530ce39:'+path])
    if frozen!=(w/'app-source-e6c4aae'/path).read_bytes():source_errors.append(path)
result={'dependency_manifest_entries_verified':len(m['entries']),'dependency_errors':errors,'source_errors':source_errors,'original_editor_suite_byte_equal':not source_errors,'fixture_sha256':hashlib.sha256((w/'app-source-e6c4aae/src/tools/video-editor/data/mainImageCap.fixture.json').read_bytes()).hexdigest()}
(w/'readonly-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
raise SystemExit(bool(errors or source_errors))
