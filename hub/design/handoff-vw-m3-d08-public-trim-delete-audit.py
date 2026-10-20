from pathlib import Path
import hashlib, json, os, tarfile, sys
graph = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/clean-project/node_modules')
root = Path('/home/user/work/wt/vw-m3-d08-public-trim-delete')
archive = root/'vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz'
composition = graph/'@banodoco/timeline-composition'
members = 0
with tarfile.open(archive) as tar:
    for member in tar:
        if not member.isfile(): continue
        relative = Path(member.name).relative_to('package')
        assert (composition/relative).read_bytes() == tar.extractfile(member).read(), str(relative)
        members += 1
assert members == 77
entries = []
for current, dirs, files in os.walk(graph, followlinks=False):
    for name in sorted(dirs + files):
        p = Path(current)/name
        st = p.lstat()
        value = os.readlink(p) if p.is_symlink() else hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else 'dir'
        entries.append([str(p.relative_to(graph)), st.st_mode, st.st_size, st.st_mtime_ns, value])
entries.sort()
digest = hashlib.sha256(json.dumps(entries, separators=(',', ':')).encode()).hexdigest()
print(json.dumps({'graph': str(graph), 'entries': len(entries), 'tree_sha256': digest, 'artifact_sha256': hashlib.sha256(archive.read_bytes()).hexdigest(), 'exact_tar_members': members}, indent=2))
