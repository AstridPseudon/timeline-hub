PASS_SOURCE

Reviewed candidate `4dcb5a5e8a` against exact parent `7e23790248`:

- Only `astrid/sdk/timeline/_commit_patch.py` changes.
- `canonical_site()` maps `*/collection:asset` to `registry.assets`.
- `finish()` records an exact C0 field dependency using the sequential input value, with conservative ancestor fallback for missing/malformed containers.
- Existing collection checks, semantic captures, allocation/reuse/collision guards, inverse/ABA scans, sequential boundaries, aliases, and atomic fallback remain unchanged.
- Current callers traced: parent add/swap/duplicate/auto-completion; occurrence add/swap/auto-completion; shot-pool operations. Occurrence aliases resolve to their pinned internal revision.
- Rebase still scans every intervening write, so unrelated `anchor.params.later` merges while registry changes conflict, including A→B→A.
- Protected six parent-auto originals are byte-identical and remain unverified behaviorally pending MAIN proof.

Static evidence:

- Candidate Ruff via stdin: passed.
- Parent Ruff: passed.
- Parent/candidate mypy: both passed with identical diagnostics per author evidence.
- Parent/candidate in-memory compile: passed.
- Removing exactly the two asset-specific AST branches restores the parent AST.
- `git diff --check`: passed.
- No pytest, imports, helpers, fixtures, services, browsers, or functional execution run.

Limit: direct hypothetical `internal:.../collection:asset` aliases are not current production inputs; occurrence callers canonicalize through `occurrence/.../source` first. Behavioral acceptance remains the required MAIN six-original proof. Commit message and `DONE` marker created; no merge performed.