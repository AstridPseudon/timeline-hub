## Verdict: FAIL overall

- Exact SDK9 delta: PASS — 9 closures (2 capture, 2 helpers, 5 persistence), changing `202/65` to `211/56`.
- Cumulative preservation: PASS — 258 node records, 27 prior proof records, prior 60 mapping rows, inverse22/D40 sections unchanged.
- Counts: PASS — 267 total, 211 closed, 56 open; all tagged `ours`; family sum 56; owner sum Agent 51 + Runtime 1 + Viewing 4.
- Mapping: PASS — 69 unique JSON/CSV-identical members; external SHA `6422ec5cd2f310a118b8d9e88f6ac3fe3cbb55d916655c7921e933c91235d07c`.
- Scope: PASS — exactly five evidence files changed; zero product changes. Schema pair and 24 unqualified SDK selectors remain excluded. Helper temporary packet remains unavailable. No full AST hashes were invented.
- Full suite honesty: PASS — retained result is `FAIL 17159 passed, 262 failed, 5 errors, 4 skipped`.

Metadata: FAIL. The caller inventory does not explicitly preserve `rationale`, `group_id`, `merge fields|atomic`, or stable idempotency semantics. Reply inventory omits explicit head, revision, digests, attribution, conflict reason, and current head. Per the brief, these cannot be inferred from “full receipt” or narrower source evidence.

Commands run: stdlib Python JSON/CSV/hash/membership/diff audit; `git diff --name-only HEAD^ HEAD`; parent-vs-candidate JSON comparisons; SHA verification. No tests, lint, mypy, body reruns, full/browser/gate runs, installs, or product edits.

Recommended next step: correct only the evidence metadata to enumerate the complete v2 request/reply fields, then re-review without changing the 9-node count.