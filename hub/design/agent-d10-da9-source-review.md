# D10 Agent source-owner boundary review

## Verdict

**REJECT — exact generator defect; D10 remains HELD.** The candidate is not
safe to merge as the source deletion packet because it drops a valid custom
override when the canonical rendering descriptor is source-less and supplied
by Composition.

## Scope and bases

- Candidate: `da9a5bd860f3a16563bc2b0b0ef55ab042183091`.
- Actual merge-base with current `tl/integration`: `0b2f662e32e1a6818d58f9cf12130f0a89fb5a3b`.
- Reviewed delta: `merge-base..candidate`, four commits (`7aeda4d0`,
  `1e2de50d`, `e4d23250`, `da9a5bd8`), not an endpoint diff.
- Tree delta: exactly nine `component.tsx` implementations removed and their
  nine `pack.yaml` implementation resources removed. No `element.yaml`, local
  custom-pack, custom-asset, wire, DTO, or metadata-contract files changed.

The generated catalog still has 45 descriptors with unchanged IDs. For all
45 rows, descriptor/schema/defaults/pack identity/componentPath fields are
unchanged except for the nine retired public rows’ `revision` strings. Those
nine revisions changed because the source-byte digest now hashes an absent
component. That also conflicts with the requested unchanged revision
authority and must be resolved before approval.

## Blocking defect: valid custom override is lost

The current registry has this real boundary:

- canonical winner: `pack:rendering/effects/text-card`, source-less after the
  deletion, supplied by Composition’s public registry;
- valid shadow: `pack:local/effects/text-card`, with an existing
  `component.tsx` and the normal local pack identity.

In `scripts/gen_effect_registry.py:102-117`, `discover_plugins()` starts from
`registry.list(kind=kind)`, which is winners-only, then removes the source-less
public winner. In the effect owner pass at `:459-476`, the valid local shadow
is visible via `include_shadowed=True` but is discarded at `:462` because its
ID is no longer in `effects`. The generated map therefore has neither a
`text-card` public default entry nor a local owner entry. Host composition
resolution falls back to Composition and cannot honor the valid local
override selected by the existing registry semantics.

Focused counterexample (one bounded probe, with public membership supplied by
the existing Composition seam) returned:

```text
text-card id present: False
local text-card import present: False
rendering text-card import present: False
```

This is a source/catalog boundary failure, not a reason to add a second
priority chooser. The correction should retain the existing canonical winner
for the unqualified path while carrying valid shadow owners through the
existing registry owner-selection seam, with a permanent source-less-public
winner plus local-override regression test.

## What passed / was preserved

- The candidate uses the installed Composition registry API for dynamic
  membership; it does not hard-code a blanket `pack:rendering` omission.
- Unknown or missing non-public components fail closed in
  `_component_is_host_importable()`.
- The nine descriptors and schemas remain discoverable, and the three custom
  component/asset areas are untouched.
- Existing focused source tests: `18 passed`; two tests that require the
  installed Composition package could not run in this worktree because
  `remotion/node_modules/@banodoco/timeline-composition/package.json` is
  absent. A private overlay of the pinned Composition `0.0.13` artifact was
  used for the dynamic-membership/generator probe; no shared dependency was
  modified.

## Last consumer and release dependency

The last installed-host consumer is App’s Home public host at
`src/pages/Home/astrid-public-host.tsx`, whose nine direct wrapper imports were
already migrated to the existing public Composition registry bridge (Home
`4ab` handoff). The source deletion must remain held until:

1. the generator preserves valid custom overrides while retaining the
   canonical winner semantics;
2. the nine catalog revisions are reconciled with the settled unchanged-
   revision requirement; and
3. App runs the normal vendor refresh against this exact corrected Agent
   source commit and verifies generated provenance.

Do not mark the nine source/vendor rows `DELETED` before that consumer-first,
real-refresh sequence completes. The prior D10 handoff’s central generator
and App consumer evidence remains valid for the unchanged portions and was
not duplicated here.

## Commands and results

```text
git merge-base tl/integration da9a5bd860f3a16563bc2b0b0ef55ab042183091
  0b2f662e32e1a6818d58f9cf12130f0a89fb5a3b

git diff --stat 0b2f662e..da9a5bd8
  16 files changed, 380 insertions(+), 84 deletions(-)

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python \
  -m pytest -q -o addopts= -p no:cacheprovider \
  tests/packs/rendering/test_effect_registry_target.py \
  tests/packs/rendering/test_remotion_element_generation.py \
  tests/packs/test_composition_elements.py
  18 passed, 2 failed in 24.00s
  The two failures are environment absence of the installed public13 package,
  not assertion failures in the candidate logic.

git diff --check 0b2f662e..da9a5bd8
  PASS
```

Private pinned-package probe (temporary directory only; extracted local
`remotion/artifacts/banodoco-timeline-composition-0.0.13.tgz`, read-only peer
symlinks, Node `v20.19.4`):

```text
ASTRID_REMOTION_PROJECT_DIR=$TMP ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
  PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python scripts/gen_effect_registry.py
node --input-type=module -e 'import {DEFAULT_THEME} ... resolveElementRegistries(DEFAULT_THEME) ...'
  public membership: effects=1, animations=6, transitions=2 (the nine public wrappers)
  generated effects registry: no rendering or local text-card import
```

The temporary overlay and logs were removed after the probe.

No full suite, root pytest, browser, central/live socket, MP4, or shared
dependency write was run.
