# F-D22 independent artifact review — 1525

## Final verdict

**PASS for the corrected evidence artifact, with an explicit historical-custody limitation.**
The sole full service result remains **FAIL**. The classification/inventory result remains a separate **PASS**; it is not a product or full-suite PASS.

The precise unresolved discrepancy is that the exact original 1442 JSON bytes are not recoverable. The retained 1442-path JSON is a replacement capture, not the original bytes. The new return JSON discloses this loss explicitly and has its own content hash. No existing capture was deleted or rewritten by this review.

## Static evidence checked

Sources:

- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-F-D22-custody-artifact-sol-1515.md`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-F-D22-census-return-1500-final-a6684b789b129c65f70a9e53493be1abbc9c04bbb697a03159683a9dbb50c671.json`
- Immutable raw log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D22-terminal-classify-1442/raw-terminal.log`

Verified hashes:

- New JSON: `a6684b789b129c65f70a9e53493be1abbc9c04bbb697a03159683a9dbb50c671` — matches its filename and the artifact claim.
- Raw terminal log: `e0036c850d1a7b7c78d14e3d287350795ccb8c4b03c9cd30103d9f8b9a3c60a5` — matches the artifact claim; 1,365,688 bytes and 22,747 lines.
- Retained replacement at the old 1442 JSON path: `cc8b7d96dadaa6f9022a064fcd5a5db3d72f008b1565afc1f63c72e4adbcc397`.
- Profile archive: `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.

Raw summary independently parses to exactly:

`185 failed, 16733 passed, 4 skipped, 86 warnings, 19 errors, 565 subtests passed`.

The JSON contains 204 unique entries: 185 `failed` and 19 `error`. Its canonical node set matches the 204 raw result identities after normalizing one pytest summary rendering: raw line 22640 is `tests/core/rendering/test_conformance.py::test_no_audio_wire_parity - ...`; the complete node is present in the raw traceback at lines 14436–14477. Literal raw-summary text therefore has one truncated display suffix, but no missing semantic node.

Group counts and list membership were independently recomputed:

| group | count |
|---|---:|
| child-probe | 17 |
| child-import-or-recipe | 87 |
| custody-process-assertion | 11 |
| fixture-declared-gap | 2 |
| g5-inverse | 23 |
| profile-fixture | 37 |
| child-import | 9 |
| d13-preflight | 1 |
| r1-private | 7 |
| g5-publisher | 2 |
| g5-schema | 2 |
| r3-docs | 1 |
| d09-probe | 3 |
| r5-retired-route | 2 |
| **total** | **204** |

All 11 `custody-process-assertion` entries are `UNCONFIRMED`; all 37 `profile-fixture` entries are `UNCONFIRMED`, with the stated 14/9/11/3 profile breakdown. All 23 JSON raw references are numeric, ordered, and within the 22,747-line raw log. The 11 custody windows contain their function names. The moved Remotion trace starts at 14927, its summary row is 22648, and its JSON window is corrected to `14927-14960` (no `2252x` remains).

The prior 1510 classification/inventory PASS remains distinct from the full-service FAIL and from the unresolved original-JSON custody loss. The full result is still the sole service result: 16,733 passed, 185 failed, 19 errors, 4 skipped, 565 passed subtests, exit 1.

## Scope and commands

Read-only commands run:

- `sed -n '1,240p' .../PLAN.md` and `sed` of the absolute handoff, prior 1510 report, and 1500 report.
- `sha256sum` on the raw log and new JSON; hashes above matched.
- Python 3 static JSON/raw audit: parsed the 185 `FAILED` and 19 `ERROR` summary rows; compared canonical IDs; recomputed entry, status, group, list, and trace-window counts; checked custody/profile statuses and the Remotion window.
- `find`/`sha256sum` custody search across the 1442, 1500, and 1510 worker directories; no original 1442 JSON byte copy was found. Named raw logs, reports, replacement JSON, and prior design capture are present.
- `git status --short` and `git diff --check` in this worktree: clean / no whitespace errors.

No tests, full suites, type checks, lint, provisioning, environment qualification, or live tools were run. No product repository, schema/client/pin/archive/lock/dependency, C0 request/reply shape, test expectation, route, or state was changed. No product artifact merge or merge request is requested.

Recommended next step: retain this PASS-with-limitation review beside the corrected JSON, keep the original-1442 custody loss visible, and continue the existing owner handoffs without new classification, deferred, or PASS credit.
