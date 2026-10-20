import hashlib, json, os, stat, sys
from pathlib import Path
base = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
assert (base / 'design/handoff-vw-m3-app-private12-clean-install-READY').exists()
assert (base / 'workers/vw-m3-app-private12-clean-install/DONE').exists()
ready = json.loads((base / 'design/handoff-vw-m3-app-private12-clean-install-REPORT.json').read_text())
assert ready['status'] == 'READY' and ready['frozenProductRoot'] == '0ea988bdd2907c876b82fd2620820e3fb6d6ea84'
root = Path(ready['privateRoot'])
records = []
def sha(data):
    return hashlib.sha256(data).hexdigest()
def visit(path):
    info = path.lstat()
    record = {'path': path.relative_to(root).as_posix(), 'mode': stat.S_IMODE(info.st_mode)}
    if path.is_symlink():
        target = os.readlink(path)
        assert not target.startswith('/') and path.resolve().is_relative_to(root / 'node_modules') and path.resolve().is_file()
        record.update(kind='symlink', target=target, sha256=sha(target.encode()))
    elif path.is_dir():
        record['kind'] = 'directory'
    else:
        assert stat.S_ISREG(info.st_mode)
        record.update(kind='executable' if info.st_mode & 0o111 else 'file', bytes=info.st_size,
                      sha256=sha(path.read_bytes()), device=info.st_dev, inode=info.st_ino, links=info.st_nlink)
    records.append(record)
    if record['kind'] == 'directory':
        for child in sorted(path.iterdir()): visit(child)
visit(root / 'node_modules')
original = json.loads((base / 'design/handoff-vw-m3-app-private12-clean-install-manifest.json').read_text())
expected = [r for r in original['entries'] if r['path'] == 'node_modules' or r['path'].startswith('node_modules/')]
assert records == expected, 'physical graph differs from installer READY manifest'
result = {'root': str(root), 'entries': records, 'sha256': sha(json.dumps(records, separators=(',', ':'), ensure_ascii=False).encode())}
Path(sys.argv[1]).write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'entries': len(records), 'sha256': result['sha256'], 'output': sys.argv[1]}))
