# P4ccc ancestry audit — FAIL

Audit target: `f894c3c9dda25ab03527eeb7f52da5da31d627c1..ccc521b7811231984564f07ea50e9eb710466b1a`.

The target is the merge `ccc521b78` with first parent `f894c3c9` and second
parent `81aad71e`. `git diff --stat` reports exactly **29 files, 2,417
insertions, 430 deletions**. This audit is read-only: no product, test,
generated, pin, or lock file was edited.

The requested R4 control-doc path
`/home/user/peteromallet/astrid-agent/docs/projects/timeline-r4/` was absent
on this machine. I used the available copies
`/home/user/timeline-hub/hub/design/commit-v2.md` and
`/home/user/timeline-hub/hub/design/BOARD-HEADER.md`, plus PLAN §3.

## Decision

**FAIL.** Most final blobs are byte-identical to one or more donor blobs, but
byte identity alone is not sufficient here:

1. The combined-join source `5f0fb2ed` contains a broad, unproven removal of
   authored-meta validation and its tests. The available combined-join review
   (`agt-G234-current-join-review-0401`) explicitly failed the production
   `create_empty` acceptance and does not identify or approve these removed
   assertions. The target retains those exact removal hunks.
2. The target's public per-step undo files come from the `a568c4ebf`/`81aad71e`
   line, not the independently reviewed public facade donor `9fbb84ac8` /
   `246f92507`. The review of `a568c4ebf` found that `Timeline.undo` still
   inherited the numeric `Checkout.undo` signature and that its tests bypassed
   the production caller via `tl.session.undo`. Thus the target does not prove
   the required mounted production caller.
3. `design/agent-G3-R2-resume-0136.md` is an extra report in the product
   repository. The board instructions say reports belong under worker reports
   and the flat orchestrator design area; this file must not be retained as a
   product delta.
4. The dedicated inverse-076 preservation test and design report from
   `076630e4e` are absent from the target. They were already absent at `f894`
   and therefore are not among the 29 changed paths; this is an ancestry
   omission, not a reason to credit the target. `inverse.py` itself is
   unchanged across the audited range (`603ab9a6...`), so no inverse source
   edit is attributed to this range.

### Minimal correction prescriptions

These are prescriptions for new Codex revert/repair commits; no history
rewriting or silent merge resolution is authorized.

- Add one minimal revert commit that restores the removed authored-meta
  validation and original assertions, by reversing only the target hunks in:
  `astrid/core/timeline/__init__.py`,
  `astrid/core/timeline/authoring_bundle.py`,
  `astrid/core/timeline/shot_composition.py`,
  `astrid/core/timeline/shot_composition_projection.py`,
  `astrid/core/timeline/validators/registry.py`,
  `tests/sdk/test_timeline_commit_provider_document.py`,
  `tests/timeline/test_authoring_bundle.py`,
  `tests/timeline/test_meta_validator.py`, and
  `tests/timeline/test_shot_composition_projection.py`. Preserve all unrelated
  G3/G4/P4 changes in those files.
- Restore the exact reviewed public facade pair from `246f92507` (equivalently
  the reviewed `9fbb84ac8` source):
  `astrid/sdk/timeline/commit_session.py` blob
  `b139373806031d0d6e50f5eb1d27d0b3973d2255` and
  `tests/sdk/test_timeline_open_commit_v2.py` blob
  `f12ee8fc57f443f3aef43dece2627e0845d7bd04`, then rerun the public-caller
  tests. This is the smallest correction that wires the reviewed step-undo
  behavior through `Timeline.undo` rather than only `TimelineSession.undo`.
- Remove the accidental product report
  `design/agent-G3-R2-resume-0136.md` in that same new correction/revert
  series; retain its evidence only in the worker/orchestrator report stores.
- Separately restore the missing inverse-076 evidence files from the reviewed
  source as a new Codex commit, subject to manager confirmation:
  `tests/sdk/test_timeline_inverse_binding.py` and
  `design/agent-G4-inverse-binding-sol-0336.md`. Do not replace the current
  `inverse.py` from this audit; it is outside the audited delta.

The target also retains the combined-join review's known G4 limitation:
`RemoteTimelines.create_empty` remains on the legacy direct
`create_timeline`/`publish_parent_composition` route in the unchanged
`astrid/sdk/remote.py` baseline. That is outside the 29-path delta but means
the production-caller acceptance remains unqualified; passing local tests do
not override this finding.

## File-by-file identity map

`before` is the blob at `f894c3c9`; `after` is the blob at `ccc521b78`.
“Exact common donor” means the after blob is byte-identical to the named
reviewed source blob; it does not waive the explicit review gaps above.

| Path | Before blob | After blob | Source identity / finding |
|---|---|---|---|
| `astrid/core/timeline/__init__.py` | `92a26c467c4c9975d8a969f6b037b0cae37353c7` | `542ee5a9ade775ee035ab55d44dda2528f2fddfb` | Exact common G2 `43d24dd52` / combined `5f0fb2ed` / G3 `44ea02571`; meta API export removal is unreviewed. |
| `astrid/core/timeline/authoring_bundle.py` | `d0d7dbd0aa961f1b2bd1442f2d4daa2ad7b53193` | `169b21c27a79b21eccec51d305abdbd6934e0fc5` | Exact common donor blob; 5f removes meta validation, opaque-meta filtering, and associated media-discovery guards without explicit approval. |
| `astrid/core/timeline/shot_composition.py` | `23105de991d1bde32b4ed8c98e0c036f560e0629` | `895ecd7afd92669b8127e48e3faae7389b91e2b3` | Exact common donor blob; removes canonical shot/occurrence/timeline meta validation. |
| `astrid/core/timeline/shot_composition_projection.py` | `04493587ea7de6b933774914df9ed4d4706ef860` | `5f4dafe30349247efe63a2dc82f89fdca8e9825f` | Exact common donor blob; removes projection meta validation and its test. |
| `astrid/core/timeline/validators/registry.py` | `c9ba3bcf86902ffa518f2a5e96881ff29d2d6168` | `25d18a67e63dcd946bb201f655ba214a3a4bf0a0` | Exact common donor blob; removes registry asset-meta validation. |
| `astrid/packs/rendering/docs/scripts/timeline_document.py` | `9228238f27cccc61b23ffe7021e8e7fd0cb57fb2` | `39f9795913e8eb690af87f7410f519fdded357d5` | Exact combined/G3 donor blob; no target-only hunk found. |
| `astrid/packs/timeline/cli_native.py` | `2346240753e8caaa9d3b9501cae4a3a97d511437` | `03130f003097ba3168c61ae11f9ad48b153cdb6c` | Exact combined/G3 donor blob; no target-only hunk found. |
| `astrid/sdk/_remote_timeline.py` | `f21f57708d12e848b27216c3b076f0989df9c307` | `92ddf74bd2f816dfd121caa41a7c9e42a28ad781` | Exact combined/G3 donor blob; no target-only hunk found. |
| `astrid/sdk/timeline/__init__.py` | `fe1efa51f8abbe9f3d2e1e288e5805545dbcd897` | `614c6305b4fb45d61ca318348cacf5c0ba871453` | Exact common donor blob; no target-only hunk found. |
| `astrid/sdk/timeline/api.py` | `b5703ad5497ab0a63068ba25229885dec798510f` | `223690a560878806423adb08047079fba8d7425a` | Exact common donor blob; no target-only hunk found. |
| `astrid/sdk/timeline/commit.py` | `9cbe823d1db166e3701d9d6bc372a7266417d6f1` | `67f8d59089e6b378a697e29f7285bb75f403743b` | Exact combined/G3 donor blob; no target-only hunk found. |
| `astrid/sdk/timeline/commit_session.py` | `ABSENT` | `fbc08d58adfbc0728e0ee08d35409e09f6ec15da` | Exact combined `5f0fb2ed` blob, but **not** exact reviewed public-facade `246f92507` blob; production caller gap. |
| `astrid/sdk/timeline/emitter.py` | `ABSENT` | `23b7618c64daf34a0d34238d8ab02669a2bfab4d` | Exact combined/G3 donor blob; no target-only hunk found. |
| `astrid/sdk/timeline/store.py` | `0da563af5f911f94b4432395f2d072a83ed11916` | `be8ee13319814c5449f30886dcbfea57195e66a0` | Exact combined/G3 donor blob; no target-only hunk found. |
| `astrid/sdk/timeline/sync.py` | `2c000a86fd8170991e084b7f39f98e4f1b045d47` | `5e7dfeec3b2a7f03849b58e5d09a5456b81a0a7b` | Exact reviewed `a568c4ebf` / P4-step `81aad71e`; source review found public facade was bypassed, so not production-qualified alone. |
| `astrid/sdk/timeline_sheet.py` | `6ae8d494d6684a9706ef533f825d419f34bf8d42` | `a1ab81277dbf2f31be7f82989058ea458d88c5d9` | Exact combined/G3 donor blob; no target-only hunk found. |
| `design/agent-G3-R2-resume-0136.md` | `ABSENT` | `b4382eb32029936de1e4c98d83617325e8ae7fc8` | Exact G3-approved report blob, but prohibited extra product-repo report; prescribe removal. |
| `scripts/reshape/baselines/ruff_astrid.json` | `2f9625301bc126b4fa8e49dbaad5efa5c9b3e9ec` | `956ab7e1aa2f6a009cffa6f339e7dd7e284ec11f` | Exact G2/G3 donor blob; ratchet remains 2150/2150. |
| `tests/editing_conformance/test_document_patch_emitter_engine.py` | `ABSENT` | `15ff6bd512a196a6e9ca3340418235ea4c6566e2` | Exact combined/G3 donor blob; no target-only hunk found. |
| `tests/editing_conformance/test_document_patch_emitter_v2.py` | `ABSENT` | `34570f1918b998b0a430e22b07451fa3daaf77fc` | Exact combined/G3 donor blob; no target-only hunk found. |
| `tests/editing_conformance/test_p4_ten_note_v2_runtime.py` | `ABSENT` | `5ee8dd5b863c164e0ea5f03257ac61849a425061` | Exact reviewed P4 source blob; HTTP body was not executed here. |
| `tests/sdk/test_timeline_commit_provider_document.py` | `1b1d0378e52e10e84549e6f651914dbba0a972eb` | `a2a123d0e25d3e6dd3d113b2e340d00dd784301c` | Exact common donor blob, but removes the authored-meta/component-media roundtrip test; unreviewed assertion removal. |
| `tests/sdk/test_timeline_open_commit.py` | `ABSENT` | `5df49be1dbd064ae5379b0f27e1319174da0cf0c` | Exact common G2/combined/G3 donor blob; no target-only hunk found. |
| `tests/sdk/test_timeline_open_commit_v2.py` | `ABSENT` | `77f1bf77dbc6b1fed74aac0ceb0e6a7a18076792` | Exact `a568c4ebf` / `81aad71e` blob, **not** reviewed P4 facade `246f92507` blob; its public-caller proof is insufficient. |
| `tests/sdk/test_timeline_sync.py` | `f59189d429fb96ed285c1fdd33d427b1d0d1f885` | `0fb59fc3f34d786a90ecc15496013ef24b8a7c05` | Exact `a568c4ebf` / `81aad71e` blob; tied to the unmounted public-facade gap. |
| `tests/timeline/test_authoring_bundle.py` | `b0f56b3844056197637831e375588d95ea4b3ded` | `2e8a4563cb76b85c8b54d1dfdfbedc3dc8ef8c61` | Exact common donor blob, but deletes three authored-meta/media/validation tests; unreviewed assertion removal. |
| `tests/timeline/test_authoring_media.py` | `67a40c7d3073805e0ee42ead869f21f8751a55c1` | `399029e2978ac15e47db33fc15794f4bc977a2ca` | Exact G3 `44ea02571` donor blob; no target-only hunk found. |
| `tests/timeline/test_meta_validator.py` | `e311a61ecdb6fa7291760d4d7de88e3f8c577445` | `7a87918d83564d7b4c8027c57401458e50c08c7d` | Exact combined/G3 donor blob, but removes size/depth/boundary assertions; unreviewed weakening. |
| `tests/timeline/test_shot_composition_projection.py` | `2cbe0a660c3bf8f36443a348758a4bf6bcc325a1` | `bf761d9aa5f9526670fe803e75e8d82ae0d3e5e2` | Exact common donor blob, but removes the projection/canonical meta-validation test; unreviewed assertion removal. |

## Independent evidence used

- G2 reviewed source: `43d24dd52e7351bcca17fcaa13987b76856dc763`, report
  `workers/agt-G2-forward-review-0056/report.md`.
- Combined G2/G3/G4 source: `5f0fb2edb72aae37ba86e3ffe28f5e79b63aa026`, report
  `workers/agt-G234-current-join-review-0401/report.md` and flat design
  review. That review is **FAIL** for the live `create_empty` caller; it is
  not blanket approval of every inherited deletion.
- G3 approved schema donor: `44ea025712c53339d78c05919d7de6996efcb1be`, report
  `workers/agt-G3-schema-fixtures-review-0327/report.md`.
- G3/R2 current-source report: `workers/agt-G3-R2-resume-sol-0136/report.md`
  and `design/agent-G3-R2-resume-0136.md`.
- Public facade donor: `246f92507f15ac16c3bb559b7ce1576a608c86d8` /
  `9fbb84ac89c3bd5e6c7ef5e38dc3f0fed243226f`; report
  `workers/agt-P4-facade-final-port-0416/report.md`.
- P4 ten-note source: `9b658b28c3a7bc3ebda3ad5a7b5b417d78553720`; report
  `workers/agt-P4-six-final-review-0449/report.md`.
- Inverse preservation source: `076630e4e450602dfa78ae1df359b42ba3d8f8d9`,
  whose dedicated test/design files are absent from the target.

## Verification

All commands were run from this worktree with private caches under the
worker's resolved tmpdir. No full, browser, live HTTP, P5, or native-14 suite
was run.

Passed targeted behavior:

```text
303 passed, 3 deselected in 38.44s
424 passed in 97.43s
```

The first attempt failed before collection because the orchestration `tmpdir`
is a pointer file, not a directory: 303 setup errors (`NotADirectoryError`).
The second command used its resolved pointer `/tmp/w-47e848dc90` and passed.

Quality results:

```text
normal Ruff ratchet: current=2150 baseline=2150 — PASS
normal mypy ratchet: current=1915 baseline=1915 — PASS
artifact_manifest.py --check — PASS
vendor_lock.py check ... --producer /home/user/work/wt/rt-pin-34eac004 — PASS
```

The broad scoped Ruff command reports 30 existing/donor findings, including
`store.py:227`, several `timeline_sheet.py` findings, 23 `F811` findings in
`test_timeline_open_commit_v2.py`, and one import-order finding in
`test_shot_composition_projection.py`. The broad private mypy command reports
20 findings in five files; a focused seven-file SDK/rendering check reports one
`store.py:563` type error. No budgets or baselines were raised.

`git diff --check` on the worktree is clean. `git diff --check
f894c3c9 ccc521b78` reports the donor-inherent blank line at EOF in
`tests/editing_conformance/test_p4_ten_note_v2_runtime.py`.

No product changes were made by this audit. The next step is the named
minimal correction/review sequence above; do not mark P4 ancestry PASS from
the targeted test counts alone.
