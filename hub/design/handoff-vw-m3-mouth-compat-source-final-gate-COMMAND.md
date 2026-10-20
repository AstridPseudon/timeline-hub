# Commands

The exact candidate source was extracted privately from Agent ref
`tl/vw-m3-mouth-partial-compat-source-unit` (`ee71010a0`). The retained public12
artifact and f816 peer modules were read-only; Node `v20.19.4` was copied into
the private temporary run directory.

```sh
ASTRID_NODE_EXECUTABLE=<private-node-v20.19.4> \
ASTRID_COMPOSITION_TEST_NODE_MODULES=/home/user/work/wt/vw-m1-ssr-snapshot/remotion/node_modules \
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<private-candidate-extract> \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short \
  tests/packs/rendering/test_presenter_scene_capability.py::test_presenter_existing_registered_ssr_markup \
  tests/packs/rendering/test_presenter_scene_capability.py::test_presenter_public_scene_contract \
  --basetemp=<private-temp>
```

Result: `6 passed in 8.27s`.

The complete targeted command and result are recorded in the report:
`55 passed, 2 skipped in 22.55s`.
