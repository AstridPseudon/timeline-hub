# D118a independent purpose review

Verdict: **(b)**. The four exact retained nodes expose a stale exact reason in the test, not a live product misclassification. The production refusal and no-write purpose are preserved.

## Captured path

- Reviewed unchanged Agent target SHA-256: `3138f2ac264cf3a5e52bdd44677eb6f8cf9f70d362a0630e5b16490307a6b22c`.
- The target is absent from frozen `origin/codex/handover-timeline-r4-20261019-candidate-sdk`.
- Retained D118a evidence is in the prior worker's `evidence/facts.json`, `evidence/facts.md`, `evidence/node.log`, `evidence/node.xml`, and `log.txt`. Its exact four nodes are image-at, image-hold, video-at, and video-hold; all observed `value_conflict`, while the unchanged assertion expected `dependency_changed`. Runtime was clean at `42aad0e92f6da8ea83dd0a382a87e3acd12651b0`, tree `085a5be70b56353deb41ae7d743336a4ccb7f29c`.

The caller is `completion()` → `auto_place_completion(... owner='parent', ownership='parent', track='visual', verified_media=...)` → `_parent_completion()`. It uses `Recording`, selects the parent clip collection, reads the selected anchor's `at`, `at_ms`, `track`, `hold`, `from`, `to`, and `speed`, builds one literal `clip.add-media` row, appends those reads to the command, and executes the ordinary command. `native_parent_media_commands.add_media()` independently re-reads each supplied placement field in the same birth recorder. The request therefore carries genuine field reads; it does not carry a scope read.

| node | authored input | peer change | captured dependency | attempted write |
| --- | --- | --- | --- | --- |
| image-at | verified image pin; anchor at 8, hold 2.5; visual track | anchor `at` 8 → 9 | parent/clip:anchor fields: `at`, `at_ms`, `track`, `hold`, `from`, `to`, `speed`, plus normal birth guards | one parent `clip.add-media` row, literal anchor-derived `at`, hold 5, media pin |
| image-hold | same image input | anchor `hold` 2.5 → 2 | same field set | same one-row birth |
| video-at | verified video pin; anchor at 8, hold 2.5, from 0, to 2.5, speed 1 | anchor `at` 8 → 9 | same field set | one row with literal `at`, hold 5, from 0, to 5, speed 1 |
| video-hold | same video input | anchor `hold` 2.5 → 2 | same field set | same one-row birth |

All four refuse before acceptance. The captured D118a run records no accepted persistence; the retained test also checks no mutating SQL, unchanged document/rows, empty candidates, and unchanged CAS/staging/snapshot bytes. These are the preserved refusal assertions, not the stale reason.

## Contract and comparison

C0 §3, lines 604–612, says effective `fields` conflicts when a later publication writes a guarded field/item; semantic reads use the same checks. C0 §3, lines 637–648, defines field reads as exact-value guards, collection reads as membership/order guards, and scope reads as complete-payload guards. The conflict classifier in `_commit_patch.py` maps a field guard to `value_conflict`, a collection guard to `selection_changed`, and a scope guard to `dependency_changed` (atomic uses `atomic_scope_changed`). Thus changing the anchor's captured field is correctly `value_conflict`; only widening the request to a scope dependency would make `dependency_changed`, which would change product behavior and is outside this review.

The already-approved `cb35bd4fb` / `824e03f6a` expectation correction changes the same parent path's `track-label` cases to `value_conflict` while preserving the four timing cases. That approved change is the direct passing comparison: same parent auto-completion caller, same refusal/no-write assertions, field guard, `value_conflict`. Direct recipe replay tests that expect `dependency_changed` use the lower-level native replay guard path, not this Runtime rebase classifier, so they do not override C0's Runtime rule.

## Conservation and proposal

The target's function ASTs match pre-reason-change `cf0251d0b` for every function except the already-approved reason expression in `test_relevant_stale_reads_refuse_before_accept_and_any_persistence`; the other two test bodies and all setup/helpers match. Production hashes were unchanged during this review:

- `native_auto_placement.py`: `c46e23ac43dc506ba8362abc0dbb2bf145f96ed6365b594936f83476d5490907`
- `native_parent_media_commands.py`: `673643ab9dd0f094c57da49f78c581fba5f08e7b00c7b364a41e20a0a13d5964`
- `_recording.py`: `85aefe0328a7c9787a18c2b7e19eb8b3e4220a1c53627d1e16102b42b29c8b43`
- `_commit_patch.py`: `76224a62434ade240e298bf6a1d14b64bdc2ed650923c2160cf22bdbb23a4a50`

`proposal.patch` is deliberately unapplied. It changes only the exact reason expression from “track-label only” to `value_conflict` for all three stale property variants. It conserves every original input, node selector, refusal/no-write assertion, and write operand.

## Checks

- Ruff: pass.
- Mypy `--follow-imports=skip`: pass.
- `PYTHONPYCACHEPREFIX=/tmp/app-D118a-auto-conflict-purpose-review-1141-pycache python -m py_compile ...`: pass.
- `git diff --check`: pass; worktree clean.
- No original D118a nodes were rerun; no source/test change was applied.
