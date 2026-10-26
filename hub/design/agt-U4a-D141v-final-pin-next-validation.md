$ /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/runtime
ok runtime.lock.json (matches producer manifest)
$ /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
artifacts.json is current
$ PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-U4a-D141v-final-pin-next:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -o cache_dir=/tmp/w-98688817f2/agt-U4a-D141v-validate-z0wVlD/cache --basetemp=/tmp/w-98688817f2/agt-U4a-D141v-validate-z0wVlD/basetemp tests/test_vendor_lock.py tests/test_artifact_manifest.py tests/test_installer_tools.py
......................................                                   [100%]
38 passed in 6.39s
$ /home/user/work/venv-agent/bin/ruff check scripts/refresh_runtime_client.py scripts/vendor_lock.py scripts/artifact_manifest.py tests/test_vendor_lock.py tests/test_artifact_manifest.py tests/test_installer_tools.py
All checks passed!
$ git diff --check
$ git status --short
PRIVATE_ROOT=/tmp/w-98688817f2/agt-U4a-D141v-validate-z0wVlD
EXIT=0
