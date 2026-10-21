# Public effect host type boundary

## Result

Applied the smallest private Agent-owner correction in
`scripts/gen_effect_registry.py`. Public Composition registry values are
admitted dynamically by the Composition registry and are declared as
`EffectComponent<never>` in public13; the generated host selector accepts the
host's `EffectComponent<unknown>`. The correction casts only at that
public-registry-to-host-map boundary, in the generated source expressions for

- the public symbol binding;
- the normal public winner and rendering owner;
- the bundled-only public winner path.

No public package, type, DTO, schema, generated output, any-cast,
ts-ignore, skipLibCheck, or strictness change was made. Local/custom owner
selection and unknown-owner diagnostics remain unchanged.

## Private source/type proof

The disposable stage was current Agent HEAD `5c5173dcb57669a9d43e5add2674543333f1c6d2`
with only approved AM-footage donor `2e9fb6e260778e0ae6dc4a39a498d0f36a837ef6`
overlaid. The current pack resource declaration was already identical to the
donor and was not changed.

Immutable inputs:

- Node SHA-256: `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`
- Runtime lock SHA-256: `c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24`
- Public Composition 0.0.13 artifact SHA-256: `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`

Normal generation passed with `--include-element-registries`; no generated file
was patched. The generated `text-card` entry was:

`selectOwnedEffect('text-card', PUBLIC_EFFECT_REGISTRY['text-card'] as EffectComponent, {'local': OwnerElement35, 'rendering': PUBLIC_EFFECT_REGISTRY['text-card'] as EffectComponent})`

Root typecheck passed with zero diagnostics (`tsc --noEmit`). This proves the
actual generated Root consumer, not a local public component substitute.

## Tests

- `PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q tests/packs/rendering/test_remotion_element_generation.py tests/packs/rendering/test_effect_registry_target.py` — initial invocation: 9 passed, 2 environment failures because this worker checkout has no local `remotion/node_modules` public package.
- Same command with `ASTRID_REMOTION_PROJECT_DIR` pointing at a private overlay leaf-linked to immutable public13 — **11 passed**.
- Same generator/custom-owner command against the source-closed private stage — **11 passed**. This includes missing custom-component and missing-public-component fail-closed diagnostics.
- AM-footage scene direct neighbor — **5/5 passed**.
- AM-footage volume direct neighbor — **5/5 passed**.

The negative controls still refuse admission when a custom component is missing
or a rendering component is absent from the installed public registry; the cast
does not bypass `_component_is_host_importable` or owner diagnostics.

## Scope and handoff

Only `scripts/gen_effect_registry.py` is changed in this worktree. No full,
browser, render, socket, install, physical, archive, pin, adoption, or
tracked generated-artifact/catalog refresh was run. The private stage and its
copied dependency graph are disposable and are removed before completion.
Agent owner should regenerate normal metadata/artifacts during integration.
