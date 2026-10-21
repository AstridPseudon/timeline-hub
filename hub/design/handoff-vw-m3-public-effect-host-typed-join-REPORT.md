# Public effect host typed join

## Result

Applied the qualified, generator-only public registry boundary in
`scripts/gen_effect_registry.py`. The three generated expressions that cross
from Composition's public effect registry into the host's `EffectComponent`
surface now use `as EffectComponent`:

- the public symbol binding;
- the normal public winner and rendering owner;
- the bundled-only public winner path.

The existing registry discovery, canonical winner selection, custom/local
owner routing, transition defaults, and fail-closed component admission are
unchanged. No public declarations, package contents, pins, DTOs, runtime
shape, `any`, suppression, `skipLibCheck`, or strictness changes were made.
No generated output was hand-edited.

## Qualification inputs

The tests used a private staging directory. Its `node_modules` is a read-only
symlink to the existing immutable Agent Remotion public13 runtime; no shared
dependency or runtime file was modified.

- Node 20.19.4 binary SHA-256:
  `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`
- Agent Remotion lock SHA-256:
  `c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24`
- Composition 0.0.13 artifact SHA-256:
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`

Normal generation was run against the private stage, producing the actual
host generated registries. The generated `text-card` entry was:

`selectOwnedEffect('text-card', PUBLIC_EFFECT_REGISTRY['text-card'] as EffectComponent, {'local': OwnerElement35, 'rendering': PUBLIC_EFFECT_REGISTRY['text-card'] as EffectComponent})`

The generated Root consumer then passed TypeScript checking with Node 20.

## Exact checks

With `ASTRID_REMOTION_PROJECT_DIR` set to the private stage,
`ASTRID_NODE_EXECUTABLE=/opt/node20/bin/node`, and `PYTHONPATH` set to this
worktree:

```text
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/packs/rendering/test_remotion_element_generation.py \
  tests/packs/rendering/test_effect_registry_target.py
11 passed in 14.10s
```

The 11 controls cover normal generation, canonical owner/custom override and
default preservation, public-registry membership, missing custom-component
refusal, missing public-component refusal, and private host staging.

```text
/home/user/work/venv-agent/bin/python scripts/gen_effect_registry.py
PATH=/opt/node20/bin:$PATH \
  "$STAGE/node_modules/.bin/tsc" --noEmit -p "$STAGE/tsconfig.json"
NORMAL_ROOT_TYPECHECK=pass
```

No full, browser, render, socket, install, AM-footage source adoption, or
physical parity claim was made. Disposable staging was removed after the
checks.
