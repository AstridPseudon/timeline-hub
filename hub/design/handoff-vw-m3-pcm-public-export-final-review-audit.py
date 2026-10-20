from pathlib import Path
import hashlib, json, os, stat, subprocess, sys
O=Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
P=O/'design/handoff-vw-m3-pcm-public-export-final-review'
W=O/'workers/vw-m3-pcm-public-export-final-review'
S=Path('/home/user/work/wt/vw-m3-pcm-public-export-final-review')
G=O/'workers/vw-m3-app-private12-clean-install/clean-project/node_modules'
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def graph():
    manifest=json.loads((O/'design/handoff-vw-m3-app-private12-clean-install-manifest.json').read_text())
    root=Path(manifest['root'])
    expected={e['path']:e for e in manifest['entries'] if e['path']=='node_modules' or e['path'].startswith('node_modules/')}
    actual={}
    def visit(p):
        s=p.lstat(); rel=str(p.relative_to(root)); item={'mode':stat.S_IMODE(s.st_mode)}
        if stat.S_ISLNK(s.st_mode): item.update(kind='symlink',target=os.readlink(p))
        elif stat.S_ISDIR(s.st_mode):
            item.update(kind='directory')
            for child in p.iterdir(): visit(child)
        elif stat.S_ISREG(s.st_mode): item.update(kind='executable' if s.st_mode & 0o111 else 'file',bytes=s.st_size,sha256=digest(p))
        actual[rel]=item
    visit(G)
    changes=[k for k in sorted(set(expected)|set(actual)) if k not in expected or k not in actual or any(expected[k].get(a)!=b for a,b in actual[k].items())]
    assert not changes, changes
    return {'entries':len(actual),'changes':changes}
def inventory():
    archives={}; pins={}
    roots=[Path('/home/user/work'),Path('/home/user/peteromallet'),Path('/home/user/banodoco'),O]
    for root in roots:
        for directory,dirs,files in os.walk(root,followlinks=False):
            dirs[:]=[d for d in dirs if d not in {'.git','node_modules','__pycache__','.venv','venv','dist','test-dist'} and not d.startswith('venv-')]
            for name in files:
                if 'timeline-composition-0.0.11.tgz' in name or 'timeline-composition-0.0.12.tgz' in name:
                    f=Path(directory)/name
                    if f.is_file(): archives[str(f)]=digest(f)
    for repo in ['agent','runtime','app','composition']:
        root=Path('/home/user/work')/repo
        for name in ['package.json','package-lock.json','remotion/package.json','remotion/package-lock.json','pyproject.toml']:
            f=root/name
            if f.is_file(): pins[str(f)]=digest(f)
    for name in ['package.json','package-lock.json']:
        pins[str(S/name)]=digest(S/name)
    return {'archives':archives,'pins':pins}
phase=sys.argv[1]
result={'graph':graph(),**inventory()}
if phase=='before':
    nm=S/'node_modules'; nm.mkdir()
    for entry in G.iterdir():
        if entry.name.startswith('@'):
            scope=nm/entry.name; scope.mkdir()
            for pkg in entry.iterdir(): (scope/pkg.name).symlink_to(pkg,target_is_directory=True)
        elif not entry.name.startswith('.'): (nm/entry.name).symlink_to(entry,target_is_directory=entry.is_dir())
    (W/'tmp').mkdir(exist_ok=True)
    (W/'node_modules/@banodoco').mkdir(parents=True)
    (W/'node_modules/@banodoco/timeline-composition').symlink_to(S,target_is_directory=True)
else:
    old=json.loads(Path(str(P)+'-before.json').read_text())
    assert result==old, 'Archive, pin or graph changed'
Path(str(P)+'-'+phase+'.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'phase':phase,'graph':result['graph'],'archiveFiles':len(result['archives']),'pinFiles':len(result['pins'])}))
