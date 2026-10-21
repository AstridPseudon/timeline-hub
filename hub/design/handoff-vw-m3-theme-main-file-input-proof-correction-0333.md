# Theme normal file-input correction

The normal imported-theme proof was corrected in
`tests/integrations/test_generic_host_remotion_render.py:491-579`.

It now follows `astrid/packs/rendering/actions/render/STAGE.md:26-40,123-151`:
the timeline, asset registry, and Theme are owner-imported managed descriptors;
the normal file-port object IDs are passed in `timeline`, `assets_registry`,
`theme` order, followed by the registry's existing `black`, `silence` media
objects; and `timeline_ref` is omitted. Existing props.Theme, omitted builtin
fallback, and forged-local-source assertions remain unchanged.

Exact future one-case command:

```bash
env -u NODE_OPTIONS -u NODE_PATH \
  ASTRID_TEST_REMOTION_DEPENDENCY_ROOT=/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/node_modules \
  ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b \
  ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8f105c26 \
  ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
  ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
  PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/home/user/work/venv-agent/bin:/usr/local/bin:/usr/bin:/bin \
  PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration --tb=short \
  tests/integrations/test_generic_host_remotion_render.py::test_generic_host_normal_imported_theme_reaches_props_and_rejects_local_source
```

Source-only checks passed: Ruff, compile, exact one-case collection, and
`git diff --check`. The actual proof and all service/render/browser work remain
unrun pending independent review.
