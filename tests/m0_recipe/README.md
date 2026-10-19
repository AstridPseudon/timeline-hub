# M0 recipe experiments

These are isolated design spikes, not the M1 product port. Run explicitly:

```bash
PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q tests/m0_recipe
```

`test_recipe_main.py` exercises main's actual authoring bundle, chapter storage
and transcript APIs, reusing fixture constructors from main's suites.
`test_recipe_spikes.py` runs the real frozen R4 recorder, compiler, inverse,
rebase and immutable-media capture APIs in separate interpreters. It extracts
the frozen Agent ref into pytest's temporary directory; no refs are changed and
no dependencies are installed. `ASTRID_RECIPE_R4_ROOT` can name an existing
read-only R4/port-spike tree containing its fixture tests and generated client.
Imports in each child select that tree explicitly; main's imports stay separate.

The frozen source is
`origin/codex/handover-timeline-r4-20261019-candidate-sdk`
(`11caf1d9de291d76f491cf69f7942606b7471d7a`). Tests assert **observed** behaviour,
including gaps. A green run does not mean the proposed recipe is implemented.

| Case | Real API / observation |
| --- | --- |
| Ripple/insert | `_apply`, `rebase`, inverse: deterministic replay; concurrent new clip silently joins ripple, requiring a membership policy/guard. |
| Transition | Composite predecessor validator: exact endpoint, adjacency, gap/overlap and inserted predecessor; audio crossfade guards both endpoints; visual admission requires renderer today. |
| Shared/occurrence | Main immutable closure adapter creates independent authored owners for a shared source, preserves sibling and opaque values; shared edits must explicitly target all intended owners. |
| Chapters | Main split/flatten/Checkout retains chapter shots and parent-owned crossing visuals/music. |
| Music | Actual managed-bed source/ripple basis, deterministic compiled outputs and guarded insertion/gain inverse. R4 leaves the representation upgraded to v2. |
| Transcript | Main source-scoped document identity and timing-derived word IDs; R4 exact snapshot/source/word pins and refusal to rebind shifted legacy ordinal. |
| Tracks | Real create/remove and inverse: later population blocks removal, empty deletion restores complete row. |
| IDs | Real add/rebase retains created IDs; collision refuses; explicit map works only if other authored uniqueness constraints also hold. |
| Clears/no-ops | Explicit clear differs from null and omission; inverse restores presence. Same-value intent is guarded in R4 calls but absent from its direct-write output. |
| ABA/history | Local value-only inverse permits ABA; real provider history guard rejects it. Publication ancestry distinguishes repeated content revisions and fails on missing edges. |
| Media | Real provider capture/add/swap: immutable metadata replay, foreign/stale/forged selections refused; undo retains a registry entry used by later clips. Runtime acceptance authority is outside this unit spike. |

No renderer responses are fabricated and no product code is patched. The media
read and publication-history ports supply explicit detached fixture data; they
do not prove a live Runtime transaction or filesystem/credential authority.
Linux only; no native macOS, App browser, live Runtime, pixel or PCM claim.
Full contract and source-level requirements are in orchestration
`design/edit-recipe.md`. During the product port, translate these observations
into native editing-conformance tests and remove the frozen-ref dependency.
