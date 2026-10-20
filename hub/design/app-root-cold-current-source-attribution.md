# App root cold/current Agent source attribution

## Freeze/check proposal

Use `8130a401bf44a518d5a40ae274d398b8c560be55` (tree
`236c3e57e0265c52b81ba8085de3193026176bff`) as the **source-only current
candidate** for post-cold qualification. It contains the merged strict
same-batch inverse guard (F1), WC4 native element/PARAM authority, and the
Scene/save extraction. It is compatible with the already qualified normal
tuple below; no new client, schema, Runtime pin, artifact, or private S3
input is needed.

This is not an App adoption/release decision. The Agent owner’s explicit
confirmation of `8130a401` as the consumer source cohort is not present in the
reviewed status/release docs; keep the App marker/root merge held until that
confirmation and the cold browser pass exist.

| frozen input | exact value | comparison to d874 evidence |
|---|---|---|
| Agent | `8130a401…` / tree `236c3e57…` | new source candidate; do not relabel d874 |
| Runtime | `2c4ac180c2220bdad966bc01e95ad230e99ce26a` / tree `7ab412cc…` | unchanged |
| normal client/schema/artifact | `0.2.13` / `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4` / `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56` | unchanged |
| normal lock | `runtime.lock.json` SHA256 `c2ed617f38bc53e4f90dc082f082d38828d8f68a93e61776300ec7082ef23311` | byte-identical |
| Agent command schema consumed by App | `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef` (48 definitions / 22 ops) | byte-identical |

The App-consumed `EditCommand`/commit envelope remains the existing
`src/integrations/runtime/timeline-commit-types.ts` shape (`op`, `version`,
`select`, `args`, recorded guards; `timeline.commit` accepted canonical
document/commands/id-map/provider/compiler fields). No protected schema,
generated-client, artifact, or lock path differs between d874 and 8130.

The changed source bytes are limited in meaning to: WC4’s native
`timeline_elements` path plus `_selected_param_authority`, recording/command
and inverse plumbing; F1’s staged-record check in `commands.py`/`inverse.py`;
and Agent Scene/save/source-window extraction. The d874 browser journeys use
move/track-label capture and standalone move inverse, not WC4 element/PARAM
authority or a same-batch element-selection inverse. Scene extraction is a
Viewing/render concern, not an App commit DTO change.

Exact source delta accounting is `git diff --stat d8749a9c..8130a401`: 57
paths, `+4600/-661`. The semantic product paths are
`astrid/sdk/timeline_elements.py`,
`astrid/sdk/timeline/_selected_param_authority.py` (new),
`astrid/sdk/timeline/{commands,inverse,commit,_clip_scalar_commands,_recording}.py`,
`astrid/sdk/{remote,workspace_client}.py`, plus the Scene/save extraction in
`astrid/core/{execution/generic_host.py,rendering/{service.py,verified_source.py,window_inputs.py}}`
and `astrid/packs/rendering/{rendering/renderers/remotion/{run.py,root_preparation.py},actions/timeline_visualize/composed_frame.py}`.
The remaining delta paths are their tests, fixtures, and review/docs; no
App-consumed schema/client/lock/artifact bytes changed.

## Required checks after owner confirmation

| proof | classification |
|---|---|
| Cold first-label browser lane | **must rerun** on 8130 + the App cold fix; this is the known initial-basis defect and is not covered by d874. |
| Native3 (M1/Gate5/conflict) and regular-labels3 | **source-cohort rerun required** for any current-root claim, but not a direct WC4/F1 semantic regression: their exercised commands are move/track-label, with a standalone inverse. Preserve d874 results as historical only. |
| App targeted generic commit/outbox/inverse envelope tests | Existing d874-compatible DTO behavior; rerun only as the normal current-tree targeted smoke, not as WC4 proof. |
| App element/PARAM/undo consumer proof | **not supplied by d874 browser evidence**; run an existing focused/native consumer lane if App exposes one before claiming WC4 adoption. Do not invent a fixture or pin. |
| Scene/render/PCM/browser full suites | out of this source-attribution task; no result claimed. |

Offline controls on private archives of Agent 8130 and Runtime 2c4: 9 native
F1/WC4 cases passed; 38 WC4 unit cases passed; 9 scalar/conformance cases
passed. No browser/build/socket/install/full run was performed here.

Exact checks used:

```text
git diff --name-status d8749a9c..8130a401 -- runtime.lock.json astrid/core/timeline/schema astrid_runtime_client artifacts.json
# empty (no protected bytes changed)
sha256sum astrid/core/timeline/schema/edit-command.schema.json runtime.lock.json
# a6f1aaa9…  c2ed617f…
```
