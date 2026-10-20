from pathlib import Path
import subprocess, tarfile, io, json, hashlib
orch = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
work = orch / 'workers/vw-m3-app-delivered-theme-seam'
repo = Path('/home/user/work/wt/vw-m3-app-delivered-theme-seam')
base = 'd48b13beb2f2919d3372f4221154c13e6426ef03'
app = work / 'offline-app'
app.mkdir(exist_ok=True)
archive = subprocess.check_output(['git', 'archive', base, 'src', 'vendor/fake-indexeddb', 'vendor/astrid-browser', 'tsconfig.node.json', 'tsconfig.app.json', 'tsconfig.json', 'package.json'], cwd=repo)
with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
    tar.extractall(app, filter='data')
if not (app / 'node_modules').exists(): (app / 'node_modules').symlink_to('/home/user/work/app/node_modules', target_is_directory=True)
artifact = orch / 'artifacts/banodoco-timeline-composition-0.0.10.tgz'
assert hashlib.sha256(artifact.read_bytes()).hexdigest() == 'cd83b77f72ce436e25eef697b289d33adae2087d92035aa37a27a308975ddea7'
agent_source = work / 'agent-source'
agent_source.mkdir(exist_ok=True)
agent_archive = subprocess.check_output(['git','archive','384918908aa8c75229c2b6ccdd8fda03b7ce24a1','astrid','pyproject.toml'],cwd='/home/user/peteromallet/astrid-agent')
with tarfile.open(fileobj=io.BytesIO(agent_archive)) as tar:
    tar.extractall(agent_source, filter='data')
public = work / 'public10'
public.mkdir(exist_ok=True)
with tarfile.open(artifact) as tar:
    tar.extractall(public, filter='data')
renderer = app / 'src/tools/video-editor/compositions/TimelineRenderer.tsx'
s = renderer.read_text()
assert "<LocalFontFaces />\n      <AbsoluteFill style={{ backgroundColor: 'black', overflow: 'hidden' }}>" in s
# Independently accepted eeddb47c ground line, applied only to external overlay.
s = s.replace("<LocalFontFaces />\n      <AbsoluteFill style={{ backgroundColor: 'black', overflow: 'hidden' }}>", "<LocalFontFaces />\n      <AbsoluteFill style={{ backgroundColor: theme.visual.color.bg, overflow: 'hidden' }}>")
renderer.write_text(s)
# Record baseline after the policy-neutral ground fix; proposed patch excludes it.
(work / 'renderer-baseline.tsx').write_text(s)
(work / 'preview-baseline.tsx').write_text((app / 'src/tools/video-editor/components/PreviewPanel/RemotionPreview.tsx').read_text())
(work / 'source.json').write_text(json.dumps({'app_base': base, 'assigned_base': subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip(), 'ground': 'eeddb47c0c824a6639a310c9a6c4f70631f64ff2', 'public10_sha256': hashlib.sha256(artifact.read_bytes()).hexdigest()},indent=2)+'\n')
print(app)
