# Agent video unplace review — APPROVE

Reviewed `tl/agt-m2-video-unplace-widen` at `85d357748132461157f0d6f6146f179dd4fcb20a`, parent/merge base `25eb4e261e5fc2efdab72db6ebcbeca4fbdf7db3`, against Agent integration `a2ba1bca3cb68a15abb62a1260162c4cb73903af`, with final conflict/schema refresh at `78d548cf059a5875f5333590e6ae84051504f809`, on 2026-10-20. All eight changed paths inspected. No blocking findings or requested product changes. Approval covers this bounded Agent patch only.

The handler requires an explicit occurrence/raw child, guards exclusive shot ownership, reads the entire removed video row and registry binding, and uses the existing exact guarded inverse. Source `0..4` and trimmed `2..6` / hold `4` / speed `2`, rational fps, raw order, opaque values and sibling isolation pass. Replay rejects changed owner identity (including a different exclusive shot with identical payload), raw window/binding/order, and newly declared dependencies. Undo rejects intervening row/binding/order/owner writes, including ABA. Ordinary replay retains the settled equal-state ABA policy. Cross-scope dependency checks run before writes; conservative refusal of declared transitions/relations/sequences/formulas/slots is the existing bounded policy, not general reference analysis.

Keep-as-pooled remains an atomic unplace + canonical `shot.pool` add batch. Exact Runtime verification and retained binding checks refuse mismatched object/generation/variant, including when the mismatched selection itself has matching verified metadata. Existing aliases and opaque registry metadata survive; surviving placements and changed pool membership/order refuse; absent/empty pool state and raw position restore exactly. Existing registry codec limitations remain; no codec migration is approved.

The large fixture diff is mostly regeneration/reordering plus enlarged capture, not lost image behavior: fixture bytes increase only `124951 -> 126229`. Entire loaded image create case is identical; both image inputs/outputs and verified inputs are identical; image-unplace writes/derived writes/created/dependencies are identical. All old 122 unplace reads remain among the new 313. Keep the compact known-path loader and factored record-command/input references. Four extra create/unplace input/output opaque nested `records`/`command`/`reads` probes preserve bytes and independent copies. Do not replace this with recursive JSON rewriting or restore avoidable duplication.

Fresh evidence, all from private copies outside the repo:

- Candidate core/neighbors: **352 passed in 113.61s**.
- Private S2 RuntimeService/RequestCommitPort: **4 passed in 36.57s** (image/video × plain/pool; capture, no-write preview, commit, restart/reload, exact retry without re-execution, changed-payload refusal, exact undo/redo).
- Private integration overlay (current integration + exactly the eight candidate paths): **39 passed in 36.95s**.
- Independent review script: **28 adversarial/vector/opaque checks passed**, including all six complete exported vectors with exact records/output/inverse/redo.
- Six changed Python files: Ruff passes. Schema/fixture/three-way audit passes. Review worktree stays clean.

Prior worker evidence was inspected in its report and log: **352 passed in 43.73s**, **4 passed in 22.66s**, with the disclosed fixture setup corrections. These are supported by the fresh reproduction above.

Actual Agent schema bytes are identical at parent, candidate and integration: SHA256 `83a476f894f31dc359514e9c081bf28da2b1f8cd515bb30cce14292823753224` (43 definitions). Retained private S2 schema bytes match Runtime commit `f7081c14efd9a5b834987e7a1e2abf597b66313b` exactly: SHA256 `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef` (48 definitions). `PlacementUnplaceArgs` remains the identical closed empty object. No schema or dependency pin changed.

No current integration conflict: every changed path is byte-identical between the candidate parent and final integration `78d548cf`; read-only three-way file merges produce exactly the candidate files, exit 0 for all eight. The private integration overlay tests passed at `a2ba1bca`; the later native-frontends merge at `78d548cf` received a fresh conflict/schema check, not another test run. Recheck if integration advances before merge.

Qualification limits: Runtime evidence uses the private unpublished S2 candidate and its validated source-fixture helper for the already-placed seed. It proves neither normal API birth-to-unplace history nor owner-film compatibility, installed/public client qualification, HTTP/browser behavior, App producer parity or App cutover. The enlarged native image/video capture must be ported and qualified by the App owner before activation. No public qualification or cutover is approved. No full suite requested/run, no sockets/browser suite, product fixes, dependency mutation, git mutation, integration changes or ledger edits.

Recommended next step: orchestrator may merge this bounded Agent patch through the normal queue; retain the six capture vectors and coordinate subsequent full release-tuple/App qualification with their owners.

Exact commands, logs, decisions and limitations: [detailed review report](../workers/agt-review-video-unplace-current/notes/report.md).
