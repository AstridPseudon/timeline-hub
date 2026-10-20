Completed the current-base presenter prerequisite on Agent `ef6eec5572c5c0def7ca8a22c14caa12f24f0b82`. This is a reviewable product branch, not an old-ancestor handoff. The actual tracked component already exists on CURRENT and origin/main; the earlier “no astrid_motion motion.ts” finding is stale on this base. No R4 pack, external pack, new plugin, host adapter, provider, timing compiler or command is needed.

Read PLAN first, available Viewing STATUS, Agent's flat `design/handoff-agent-review-viewing-20261020b.md` approval, current-Agent public10 audit, the approved full-mouth product handoff, retained physical MANAGER-PASS and selected-cut aggregate ORCHREPORT. A current Agent manager STATUS file is absent from the available scratchpad/status roots and from `hub/timeline/agent/tl/integration`; current source and the Agent review/audit were used instead. This missing status document did not block source verification.

Source ownership and minimality:

- `astrid/packs/astrid_motion/pack.yaml:280` already registers `effects/am-presenter`, pack version `0.1.0`. Python discovery supplies `pack:astrid_motion`; `scripts/gen_effect_registry.py:350` generates the actual effects map, whose owner selection forwards both drawing and `prepareSceneCapability` (`:388`). `remotion/webpack-alias.mjs` resolves that existing manifest entry. `remotion/src/host-registries.ts:9` combines ordinary generated maps, and actual Root uses those maps at `remotion/src/Root.tsx:85`. Explicit owner is `{kind: "effect", id: "am-presenter", packId: "astrid_motion"}`. This is in-tree source owned by Agent, with its Git revision and normal generated source fingerprint; there is no external pin to invent.
- Pre-change component, motion, presenter-core and both shared helpers are byte-identical between this HEAD, origin/main `a411628f8fd6129f9c58c332019b56769d997384`, and donor `8c46d913^`. The original component SHA256 is `3943547265a7e169a7f59c94d7f1a079c7581c51a8daf448a8337c858f386168`. Exact per-file SHA evidence is in the flat evidence JSON.
- Ported only donor `8c46d913`'s presenter-local sharing/capability, then the approved preserve-known padding. Final component bytes equal donor8c; final motion/scene bytes equal qualified source54b9c1fe. Shared helpers and presenter-core stay unchanged. New `scene.ts` is declared as an implementation resource in the existing presenter entry. No synthetic component or registry is used in the added tests.
- Five product files: **+93/-28 lines**, net65. Five test/baseline files: **+975 lines**, including the unchanged332-line/286-hash historic JSON. Overall10 files, +1068/-28. No broad prerequisite closure was necessary.

| File | Changed lines |
| --- | --- |
| `astrid/packs/astrid_motion/pack.yaml` | +4/-0 |
| `astrid/packs/astrid_motion/rendering/elements/effects/am-presenter/component.tsx` | +11/-27 |
| `astrid/packs/astrid_motion/rendering/elements/effects/am-presenter/element.yaml` | +8/-0 |
| `astrid/packs/astrid_motion/rendering/elements/effects/am-presenter/motion.ts` | +38/-1 |
| `astrid/packs/astrid_motion/rendering/elements/effects/am-presenter/scene.ts` | +32/-0 |
| `tests/packs/rendering/presenter_crop_geometry.mjs` | +56/-0 |
| `tests/packs/rendering/presenter_scene_capability.mjs` | +286/-0 |
| `tests/packs/rendering/presenter_ssr_before.json` | +332/-0 |
| `tests/packs/rendering/test_presenter_crop_equivalence.py` | +160/-0 |
| `tests/packs/rendering/test_presenter_scene_capability.py` | +141/-0 |

Behavior: one shared anchor normalizer, erase rectangle, pixel transform and mosaic predicate serve drawing and capability. Existing `motionAt` and `presenterAt` remain the timing/view authority. The public mouth inspection ROI pads actual erase geometry by one logical pixel horizontally and two vertically. Default/partial/fractional/raw-invalid normalized anchors remain KNOWN; mosaic and unsupported outer geometry remain unknown. Presence is unknown; opaque support is none. Explicit normalized151/104/19 at640x360 yields the approved `(298,202,345,219)`/799 crop; distinct erase control is `(300,206,343,215)`/387. Raw legacy-input equivalence remains unqualified. Private crop, statistics, callers and thresholds are unchanged.

Current callback/consumer trace, inspected without edits:

- `rendering/renderers/remotion/run.py:1013` stages the actual render; `:1104` constructs merged Root props, `:1167` writes them, and `:1369` batches exact sorted/deduplicated requested frames into a returned frame-to-PNG map. Current signatures expose no `on_scene_props` callback, and current source has no donor `remotion/native-scene.mjs` or `src/host-scene.ts`.
- `timeline_visualize/composed_frame.py:348` calls that real batch capture through the persistent renderer; `:516` handles PNG cache/fresh capture. The cache holds PNGs, not prepared-scene/owner/ROI facts. `layers/base.py:350` carries frames and selected cut context but no retained public ROI. `layers/builtin.py:369,427,429` retains the selected-key lip-sync path and private component-zero `model.mouth_box`; `motion/model.py:541` remains its private geometry. Luminance18 and strict2% comparison stay untouched.
- Therefore the selected-cut report's `on_scene_props` trace is accurate for its source54b9, but does not describe CURRENTef6e. That callback is a separate owner task; this port does not silently import it. Direct tests prepare public Composition using actual current generated maps, matching the current host convention in `remotion/tests/composition-package.mjs`, without adding production scene infrastructure. A trusted exact Root/owner/component-zero ROI retained with the PNG series is still required before replacing the private consumer.

Verification: **23 passed, no skips/xfails**. Exact commands, exit codes and outputs are retained at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-presenter-current-port-verification.txt`: direct presenter/crop files17passed/9.38s; neighboring registry generation and private presenter expectations6passed/2.99s; Ruff, both Node syntax checks, whitespace and reverse patch checks exit0. The17 include actual public10 Node execution, all286 unchanged registered SSR hashes, strict TypeScript declarations, seed/word boundaries and three states, rational fps, half-open/preroll/speed clocks, owner dispatch, normalization, moving view geometry, mosaic/outer unknowns and799/387 geometry. Fixture validates all77 extracted immutable public10 package files and coherent resolved React18.3.1/Remotion4.0.509 peer locations/versions. Node20.19.4 and the existing read-only host peer graph were reused; no dependencies were installed or modified.

Historical physical PASS1020061231-9845 and selected-cut25PASS were read, not rerun or represented as new-current pixel evidence. No browser, renderStill/export, socket, full suite, make check, network, installation, push or git commit/ref mutation ran. No new pixels or owner-film parity is claimed. Gate6/D09 and the production source join remain open; this does not block landing the bounded capability prerequisite.

Flat handoff files, all absolute:

- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-presenter-current-port-patch` — complete10-file current-base patch, SHA256 `af4641755679de175752c69f2300ba69b82adc3b15176d1d576d39369acf7567`.
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-presenter-current-port-product.patch` — five product files only, SHA256 `2b6540b11e84b8275e8a3eb5abc548838163b7a2823ba65e2ff0a2dbe2881d88`.
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-presenter-current-port-evidence.json` — exact file/line counts, source lineage and hashes.
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-presenter-current-port-apply-check.txt` — full patch dry-check and actual application to exact-current-base file copies, resulting10files byte-identical to worker. Temporary copies removed.
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-presenter-current-port-verification.txt` — exact commands and results.

No implementation blocker. Recommend landing this branch through the normal harness/merge queue, then let the Agent/core capture owner implement the separately reviewed trusted source join before any private crop/statistic migration. Commit message and DONE are written in the assigned worker directory. No reports, archives, generated maps or build output were added to the repository.
