from pathlib import Path
root=Path('/home/user/work/wt/vw-m3-pcm-admission-public-export-proposal')
graph=Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/clean-project/node_modules')
node=root/'node_modules'
node.mkdir()
for entry in graph.iterdir():
    if entry.name.startswith('@'):
        scope=node/entry.name
        scope.mkdir()
        for pkg in entry.iterdir(): (scope/pkg.name).symlink_to(pkg,target_is_directory=True)
    elif not entry.name.startswith('.'):
        (node/entry.name).symlink_to(entry,target_is_directory=entry.is_dir())
