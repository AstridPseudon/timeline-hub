# AM-footage qualified current-source owner packet

## Result

Prepared a small current-main patch from Agent `4467c1c1a9ed81fa7cd1b2d7687b8ada54dc216a`.
It carries the already-qualified AM-footage source seam and `2e9` missing-media
slot correction, the exact pack resource declarations, the public13 host inset/
SLOT proof, the resource-derived catalog revision, and direct typed-generator
assertions. The generator implementation itself was already present on this
base (`2b25a16ca`, the same three `as EffectComponent` joins), so it was
preserved rather than replayed.

The source keeps the old `x/y/scale` input out of geometry, reports a real
missing-media selection as the full slot field, preserves transparent inset
alpha as unknown, and leaves every existing assertion in place.

## Files and dependencies

Product files in `FILELIST` are the AM-footage component/helper/scene/direct
test, `pack.yaml`, `tests/packs/rendering/test_scene_host.py`, the focused
generator assertions, and the normally generated
`astrid/packs/rendering/elements/catalog.ts` revision.

The source donor was qualified at `2e9fb6e260778e0ae6dc4a39a498d0f36a837ef6`
(parent source seam `ac792e33cb05fa865cd8d726c5e1e371305ab778`). The typed
generator boundary is already an exact current-base ancestor at
`2b25a16cae6d1fdc5c3e6ab1d4883fab19bf7f90`; no generator implementation delta
is needed in this packet. Public-host qualification uses the existing
Composition 0.0.13 artifact, SHA-256
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, Node
20.19.4 SHA-256
`43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`, and
the read-only peer graph at
`/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/node_modules`.
Those are qualification inputs, not modified dependencies.

## Evidence

All commands used the private pinned Node and read-only peer graph; no install,
browser, renderer capture, physical media proof, full suite, caller
activation, or shared-dependency write was performed.

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m astrid.core.pack.cli validate astrid/packs/astrid_motion` — valid.
- Private pinned-Node AM-footage scene command — 5 passed, 0 failed.
- `node --test remotion/tests/am-footage-volume.test.cjs` — 1 test passed, 0 failed.
- Private public13 host command:
  `python -m pytest -q -p no:cacheprovider -o addopts= tests/packs/rendering/test_scene_host.py tests/packs/rendering/test_scene_answers.py` — 46 passed.
- Private generator/custom-owner/refusal command:
  `python -m pytest -q -p no:cacheprovider -o addopts= tests/packs/rendering/test_remotion_element_generation.py tests/packs/rendering/test_effect_registry_target.py` — 11 passed.
- Private source-closed normal `gen_remotion_types.py --include-element-registries`, followed by Root `tsc --noEmit` under the pinned peer graph — pass, zero diagnostics.
- Normal `scripts/gen_element_catalog.py` — generated the truthful AM-footage revision `sha256:4ed648625d0d37b6a98e0978613a9f9ee0213461c2eadfb46564685448809d41`; subsequent `--check` passed.
- `python -m ruff check tests/packs/rendering/test_scene_host.py tests/packs/rendering/test_remotion_element_generation.py` — all checks passed.
- `git diff --check` and `PATCH` application against a clean `HEAD` archive — pass.

An initial host attempt with `ASTRID_REMOTION_PROJECT_DIR` pointed at a
runtime root without its `remotion/` package produced setup errors; the
correct private package/peer scope above was then used and produced the 46-pass
result. No product change was made for that environment correction.

## Owner next step

Apply `PATCH` to the Agent owner integration branch, keep the already-present
typed generator boundary, and rerun the commands in `COMMAND` in the owner
environment. Do not hand-edit generated outputs or replay the old full-file
donor reset.
