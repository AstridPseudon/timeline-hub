## H32 mapping report — READY, census unchanged

Read-only mapping against `agent-D32-current-node-reconciliation-H30-corrected.json` (`267 = 202 closed + 65 open`).

### Exact candidate delta: 25 nodes

| Family | Exact open selectors | Proof / fidelity |
|---|---:|---|
| D09 | 3: `test_public_checkout_check_uses_retained_managed_scene_result`; `test_saved_and_frozen_candidate_scene_only_use_real_managed_bundle[candidate]`; `[saved]` | [runtime-D09-review-0601.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/runtime-D09-review-0601.md), receipt `agent-F-D09-invocation-return-2255.md`, 3 passed. Bodies AST-identical; predicates and parameterization retained; production managed-scene caller traced. Retained Runtime `8ea0766f` execution is not current `1d9ddba` execution; current Runtime was only import-probed. No HTTP/C0 claim. |
| Restructure | 7: all selectors in `test_timeline_restructure.py` plus historical guarded selector | [runtime-restructure-review-0602.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/runtime-restructure-review-0602.md), `originals.xml`, 7 passed/54.26s. Bodies AST-identical; guarded file byte-identical; production funnel and request construction traced, including base pair, commands, label, steps, merge, reads, source, dry-run, idempotency. `rationale`/`group_id` optional and omitted. No installed HTTP/full-suite claim. |
| Normal publication | 7: `test_nudge_disjoint_clips_merge_onto_peer_head`; changed-key payload; retry `[1]`, `[2]`; narration recovery; publish-with-client; publish-without-client | [runtime-normal-publish-review-0601.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/runtime-normal-publish-review-0601.md), `originals.xml`, 7 passed/1 failed. Original bodies AST-identical. `test_ordinary_publish_preserves_complete_closure_and_followups` remains OPEN; failure occurs before Runtime submission. |
| CLI | 5: asset replacement/swap; nudge/set/close-gap; voice-line swap; repeated gaps; replace/insert/script forwarding | [runtime-CLI-whole-path-review-0601.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/runtime-CLI-whole-path-review-0601.md), `cli-five-baseline.xml`, 5 passed/6.30s. Exact arguments/order/output predicates preserved; source/body identity retained. This is five unit/staging scenarios plus a source-final-writer trace, not mounted HTTP/C0 behavior. |
| Track labels | 3 exact maps: `dispatch[args0-画面 🎬]` → `apply[...]`; `dispatch[args1-]` → `apply[...]`; `dispatch[args2-None]` → `apply[...]` | [viewing-F-track-label-review-0547.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/viewing-F-track-label-review-0547.md), [label report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-label-credit-map-0622/report.md), retained CLI0404: 11 passed/1.63s. Unicode, empty, and clear/remove predicates, command golden, `pub1`, and final state retained. Intentional migrated `apply` path uses `source.via=sheet`; retired dispatch is not claimed. |

All five groups are pairwise disjoint, all 25 selectors are currently `active_owner`, and none overlaps SDK9.

Candidate arithmetic only: `202 + 25 = 227`, `65 - 25 = 40`. No census status, mapping CSV, or count artifact was changed.

### Reserved SDK9 nodes — excluded

The concurrent SDK9 worker owns these nine nodes:

- `test_sdk_capture_reference_admission... [False]`, `[True]`
- `test_contiguous_helpers_keep_sequential_steps[False]`, `[True]`
- the five persistence nodes: discard working copy, truncated temp, lock-holder death, restart merge, and both-sides-changed refusal.

### Other unresolved nodes

The remaining 31 non-SDK9 nodes are the open three.js rejection; commit graph/scalar/schema/helper nodes; occurrence-delete `[3-0]`, `[3-1]`; restart/history persistence; Runtime generic-host pack cleanup; and stale-head authoring publication. The failed normal-publication closure node remains explicitly open.

### Validation

Exact stdlib validation command: `python3` heredoc over the frozen census, asserting node uniqueness, `202/65` status counts, 3/7/7/5/3 membership, disjointness, SDK9 non-overlap, failed-node exclusion, and remaining arithmetic.

Result: `PASS stdlib census validation`; `total=267 closed=202 open=65 candidate_delta=25 remaining=40 sdk9_reserved=9`.

No pytest, original body rerun, full/browser/HTTP/gate run, product edit, schema/client/pin change, or current-head chase was performed. Worktree is clean. Commit message and empty `DONE` marker were created.