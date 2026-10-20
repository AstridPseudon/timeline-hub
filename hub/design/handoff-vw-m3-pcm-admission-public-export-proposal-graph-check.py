from pathlib import Path
import json, hashlib, os, stat
r=Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
m=json.loads((r/'design/handoff-vw-m3-app-private12-clean-install-manifest.json').read_text())
root=Path(m['root'])
expected={e['path']:e for e in m['entries'] if e['path']=='node_modules' or e['path'].startswith('node_modules/')}
actual={}
def visit(path):
    s=path.lstat()
    rel=str(path.relative_to(root))
    item={'mode':stat.S_IMODE(s.st_mode)}
    if stat.S_ISLNK(s.st_mode):
        item.update(kind='symlink',target=os.readlink(path))
    elif stat.S_ISDIR(s.st_mode):
        item.update(kind='directory')
        for child in path.iterdir(): visit(child)
    elif stat.S_ISREG(s.st_mode):
        item.update(kind='executable' if s.st_mode & 0o111 else 'file',bytes=s.st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    actual[rel]=item
visit(root/'node_modules')
changes=[]
for key in sorted(set(expected)|set(actual)):
    old=expected.get(key)
    new=actual.get(key)
    if not old or not new or any(old.get(k)!=v for k,v in new.items()): changes.append(key)
result={'graph':str(root/'node_modules'),'entriesChecked':len(expected),'actualEntries':len(actual),'changes':changes}
(r/'design/handoff-vw-m3-pcm-admission-public-export-proposal-graph-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
assert not changes
