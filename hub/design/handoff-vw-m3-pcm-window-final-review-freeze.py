import hashlib
import json
import os
import shutil
import subprocess
import tarfile
from pathlib import Path

WORKER = Path(__file__).parent
ORCH = WORKER.parents[1]
REPO = Path('/home/user/work/wt/vw-m3-pcm-window-final-review')
PREFIX = ORCH / 'design/handoff-vw-m3-pcm-window-final-review'
SHARED = Path('/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules')


def manifest():
    result = {}
    for root in (SHARED, Path('/home/user/work/app/node_modules'), Path('/home/user/work/venv-agent')):
        rows = {}
        for directory, dirs, files in os.walk(root, followlinks=False):
            for name in sorted(dirs + files):
                path = Path(directory) / name
                stat = path.lstat()
                rows[str(path.relative_to(root))] = (
                    ['link', os.readlink(path)] if path.is_symlink() else
                    ['dir'] if path.is_dir() else ['file', stat.st_size, stat.st_mtime_ns]
                )
        result[str(root)] = rows
    return result


def verify(sha):
    snapshot = WORKER / 'candidate'
    entries = subprocess.check_output(['git', 'ls-tree', '-rz', sha], cwd=REPO).split(b'\0')
    count = 0
    paths = set()
    for entry in entries:
        if not entry:
            continue
        head, raw_path = entry.split(b'\t')
        mode, kind, oid = head.split()
        assert kind == b'blob', entry
        relative = os.fsdecode(raw_path)
        paths.add(relative)
        path = snapshot / relative
        payload = os.fsencode(os.readlink(path)) if mode == b'120000' else path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(payload)).encode() + b'\0' + payload).hexdigest()
        assert actual == oid.decode(), relative
        if mode != b'120000':
            assert bool(path.stat().st_mode & 0o111) == (mode == b'100755'), relative
        count += 1
    actual_paths = {str(path.relative_to(snapshot)) for path in snapshot.rglob('*') if path.is_file() or path.is_symlink()}
    assert paths == actual_paths, (actual_paths - paths, paths - actual_paths)
    return {'source_sha': sha, 'tree': subprocess.check_output(['git', 'rev-parse', sha + '^{tree}'], cwd=REPO, text=True).strip(), 'byte_equal_blobs': count, 'unexpected_files': []}


if __name__ == '__main__':
    import sys
    sha = subprocess.check_output(['git', 'rev-parse', 'tl/vw-m3-pcm-native-window-resume-r1'], cwd=REPO, text=True).strip()
    assert (ORCH / 'workers/vw-m3-pcm-native-window-resume-r1/exit').read_text().strip() == '0'
    assert sha != '2019d7e69ceb9b10f18cc311e570d635b16c15d8'
    if sys.argv[1:] == ['verify']:
        assert (WORKER / 'source-sha').read_text().strip() == sha
        result = verify(sha)
        copied = []
        for name in ('normal-audio-sources.mjs', 'attempt-envelope-pcm.mjs', 'compiled-audio-source-clock.mjs'):
            assert (WORKER / 'audio-project' / name).read_bytes() == (WORKER / 'candidate/remotion' / name).read_bytes()
            copied.append(name)
        for path in (WORKER / 'candidate/remotion/tests').rglob('*'):
            if path.is_file():
                relative = path.relative_to(WORKER / 'candidate/remotion')
                assert (WORKER / 'audio-project' / relative).read_bytes() == path.read_bytes()
                copied.append(str(relative))
        result['overlay_source_copies_byte_equal'] = len(copied)
        package_files = 0
        with tarfile.open(WORKER / 'candidate/remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz') as stream:
            for member in stream.getmembers():
                if member.isfile():
                    assert (WORKER / 'audio-project/public12' / member.name).read_bytes() == stream.extractfile(member).read()
                    package_files += 1
        result['public12_archive_files_byte_equal'] = package_files
        before = json.loads(Path(str(PREFIX) + '-shared-before.json').read_text())
        after = manifest()
        Path(str(PREFIX) + '-shared-after.json').write_text(json.dumps(after, sort_keys=True))
        result['shared_metadata_equal'] = before == after
        print(json.dumps(result, indent=2))
        assert before == after
        raise SystemExit()
    (WORKER / 'source-sha').write_text(sha + '\n')
    Path(str(PREFIX) + '-shared-before.json').write_text(json.dumps(manifest(), sort_keys=True))
    snapshot = WORKER / 'candidate'
    snapshot.mkdir()
    archive = subprocess.Popen(['git', 'archive', sha], cwd=REPO, stdout=subprocess.PIPE)
    with tarfile.open(fileobj=archive.stdout, mode='r|') as stream:
        stream.extractall(snapshot, filter='data')
    assert archive.wait() == 0
    result = verify(sha)
    project = WORKER / 'audio-project'
    project.mkdir()
    modules = project / 'node_modules'
    modules.mkdir()
    for leaf in SHARED.iterdir():
        if leaf.name.startswith('.') or leaf.name == '@banodoco':
            continue
        if leaf.name.startswith('@'):
            scope = modules / leaf.name
            scope.mkdir()
            for package in leaf.iterdir():
                (scope / package.name).symlink_to(package.resolve())
        else:
            (modules / leaf.name).symlink_to(leaf.resolve())
    scope = modules / '@banodoco'
    scope.mkdir()
    with tarfile.open(snapshot / 'remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz') as stream:
        stream.extractall(project / 'public12', filter='data')
    (scope / 'timeline-composition').symlink_to(project / 'public12/package')
    for name in ('normal-audio-sources.mjs', 'attempt-envelope-pcm.mjs', 'compiled-audio-source-clock.mjs'):
        shutil.copy2(snapshot / 'remotion' / name, project / name)
    shutil.copytree(snapshot / 'remotion/tests', project / 'tests')
    result['public12_sha256'] = hashlib.sha256((snapshot / 'remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz').read_bytes()).hexdigest()
    print(json.dumps(result, indent=2))
