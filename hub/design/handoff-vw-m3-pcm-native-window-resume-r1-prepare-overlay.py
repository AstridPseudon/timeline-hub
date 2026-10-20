import hashlib
import json
import os
import shutil
import tarfile
from pathlib import Path

worker = Path(__file__).parent
repo = Path('/home/user/work/wt/vw-m3-pcm-native-window-resume-r1')
design = worker.parents[1] / 'design'
prefix = design / 'handoff-vw-m3-pcm-native-window-resume-r1'
shared = Path('/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules')

def manifest():
    result = {}
    for root in (shared, Path('/home/user/work/app/node_modules'), Path('/home/user/work/venv-agent')):
        rows = {}
        for directory, dirs, files in os.walk(root, followlinks=False):
            for name in sorted(dirs + files):
                path = Path(directory) / name
                stat = path.lstat()
                rows[str(path.relative_to(root))] = (
                    ['link', os.readlink(path)] if path.is_symlink() else
                    ['dir'] if path.is_dir() else
                    ['file', stat.st_size, stat.st_mtime_ns]
                )
        result[str(root)] = rows
    return result

if __name__ == '__main__':
    (Path(str(prefix) + '-shared-before.json')).write_text(json.dumps(manifest(), sort_keys=True))
    project = worker / 'audio-project'
    project.mkdir(exist_ok=True)
    modules = project / 'node_modules'
    modules.mkdir(exist_ok=True)
    for leaf in shared.iterdir():
        if leaf.name.startswith('.') or leaf.name == '@banodoco':
            continue
        if leaf.name.startswith('@'):
            scope = modules / leaf.name
            scope.mkdir(exist_ok=True)
            for package in leaf.iterdir():
                (scope / package.name).symlink_to(package.resolve())
        else:
            (modules / leaf.name).symlink_to(leaf.resolve())
    scope = modules / '@banodoco'
    scope.mkdir(exist_ok=True)
    with tarfile.open(repo / 'remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz') as archive:
        archive.extractall(project / 'public12', filter='data')
    (scope / 'timeline-composition').symlink_to(project / 'public12/package')
    for name in ('normal-audio-sources.mjs', 'attempt-envelope-pcm.mjs', 'compiled-audio-source-clock.mjs'):
        shutil.copy2(repo / 'remotion' / name, project / name)
    shutil.copytree(repo / 'remotion/tests', project / 'tests', dirs_exist_ok=True)
    print(project)
    print(hashlib.sha256((repo / 'remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz').read_bytes()).hexdigest())
