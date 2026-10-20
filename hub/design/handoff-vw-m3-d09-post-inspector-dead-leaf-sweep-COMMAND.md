`PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q tests/packs/rendering/test_timeline_visualize_model.py tests/packs/rendering/test_timeline_visualize_emit.py tests/packs/rendering/test_timeline_visualize_layout.py tests/packs/rendering/test_timeline_visualize_frozen_projection.py`

Result: `51 passed in 50.44s`.

Static audit and `git diff --check` passed. No full/browser/render/socket/
network/install run.
