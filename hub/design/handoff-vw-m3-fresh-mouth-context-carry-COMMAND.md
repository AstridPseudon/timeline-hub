# Commands

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m py_compile \
  astrid/packs/rendering/actions/timeline_visualize/composed_frame.py \
  astrid/packs/rendering/actions/timeline_visualize/motion/sheet.py \
  astrid/packs/rendering/actions/timeline_visualize/layers/builtin.py \
  tests/packs/rendering/test_presenter_selected_cut_aggregate.py
git diff --check
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short \
  tests/packs/rendering/test_timeline_visualize_motion_views.py \
  tests/packs/rendering/test_timeline_visualize_labels.py -k 'not integration'
```

Pure lane result: `40 passed, 2 skipped`.

