import os, subprocess, sys
from pathlib import Path
W=Path(__file__).parent
R=Path.cwd()
env={k:v for k,v in os.environ.items() if not k.startswith('GIT_') and k not in {'NODE_OPTIONS','NODE_PATH','PYTHONPYCACHEPREFIX'}}
env.update(PYTHONDONTWRITEBYTECODE='1', PYTHONPATH=str(R), ASTRID_RUNTIME_CHECKOUT=str(W/'runtime-source'),
           ASTRID_NODE_EXECUTABLE=str(W/'node'), ASTRID_REMOTION_PROJECT_DIR=str(W/'runtime/remotion'),
           ASTRID_TIMELINE_SCHEMA_PYTHONPATH=str(W/'python-overlay/lib/python3.11/site-packages'))
# Bind every native host source import to the actual test-service snapshot.
(W/'runtime/astrid').unlink()
(W/'runtime/astrid').symlink_to(R/'astrid', target_is_directory=True)
sys.exit(subprocess.call([str(W/'python-overlay/bin/python'),'-B','-m','pytest','-q','-o','addopts=',
                         '-p','no:cacheprovider','--tb=short','--basetemp='+str(W/'pytest-central'),
                         'tests/packs/rendering/test_live_source_label_native.py'],env=env))
