# agent-F-writer-review-0858

Independent Luna review of `tl/agt-F-writer-0847`.

Verdict: **FAIL**. Source SHA `c2584a01439bf6136f87c8c6e83b33c6d37cd139`; tree SHA `b133b6ee46efde4e9157cb40ab392a60e62b4d9d`.

The exact 13-node author group reproduced `12 passed, 1 failed in 5.14s`.
The sole failure is `test_duplicate_preflights_and_publication_are_core_only`,
which reaches the existing D17/G5 duplicate owner through the deliberately
minimal fixture client's missing authenticated handshake and then its
intentional archive-failure assertion. It is outside the three-file review
scope and is not counted as a repair regression.

Blocking review finding: `timeline_document.py:275` calls
`TimelineSession._bundle(session_state)` with no pending command. The current
`TimelineSession._bundle` implementation only passes `publication_id` to
`fetch_bundle` when a pending/extra `doc.patch` exists. A direct capture with
base `{revision_id: r1, publication_id: pub1}` and `pending=[]` observed
`fetch_bundle(..., revision_id='r1', client=...)` with no publication pin. The
detached preflight/emitter base therefore does not authenticate the same exact
revision/publication pair, even though the later commit staging does. This
violates the requested C0/G3 exact-pair/full-closure check.

Verified: `_check_core` replaces renderer diagnostics only; all core-invalidity
guards refuse before writing; private `_check_core` overrides remain honored;
narration binding is gated by actual `narration_changes()` rather than number
of placements; and the feedback oracle's `clip.move` to `doc.patch` update
preserves the original durable feedback predicates.

Quality: Ruff `2149/2149`, mypy baseline `1912/1912`, vendor lock PASS,
artifact manifest PASS, and `git diff --check` PASS.

Next owner: repair the detached-document pair-pinned `_bundle` preflight and
rerun the exact 13 nodes. Keep the duplicate failure with the existing D17/G5
owner; no duplicate source work was performed here.
