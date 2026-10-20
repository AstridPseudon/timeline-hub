# Commands

Working tree: `/home/user/work/wt/vw-m3-explicit-scene-root-lifetime-consumer`

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -o addopts= \
  tests/packs/rendering/test_scene_answers.py \
  -k 'prepared_host_query or invalid_runtime_context'
# 3 passed, 29 deselected in 0.39s

/home/user/work/venv-agent/bin/ruff check \
  astrid/core/timeline/scene_answers.py \
  tests/packs/rendering/test_scene_answers.py
# All checks passed!

git diff --check
# passed
```

Neighbor attempt (not a qualification; setup-only failure):

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -o addopts= \
  tests/packs/rendering/test_scene_answers.py \
  tests/packs/rendering/test_scene_host.py
# 3 passed, 44 setup errors: pinned Node v20.19.4 and renderer peers absent
```
