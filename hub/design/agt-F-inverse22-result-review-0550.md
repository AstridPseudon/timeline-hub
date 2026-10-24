# Report

**Result: PASS — bounded credit for all 22 original inverse cases.**

- Exact mapping: 16 corruption cases (`add|swap × missing,digest,foreign,revision,extra-pin,document-pin,payload,writes`) plus 6 retained-scope cases (`add|swap × missing,dependent,disjoint`).
- All 22 are exact `call`-phase, Agent-owned census IDs in the 267-node mapping.
- Qualification evidence: **22 passed in 3.55s**, JUnit/log show no skips, xfails, setup errors, or failures. Negative cases reached the protected boundary assertions.
- Qualification command was reused from the author’s evidence; I did not rerun tests.

Custody verified:

- Agent: `2007cf7aaf5d304964e68a33e967502a16de1d24`, tree `68b0309cede387e758ba6baac84bb1d3cad9c803`.
- Runtime: `2b49da8d6d8dbb8245a1a7cc8d7eee7d3bdaae65`, tree `40eb05d5a51b8d7b31cbfad8a38afeb3318fbd44`.
- Source-mode imports resolved to those worktrees before/after; both remained clean.
- Current hashes matched evidence: test `f416287f…`, `_commit_patch.py` `c12b6417…`, `_step_undo.py` `bebedf56…`, `_collections.py` `8884266d…`.

Fixture equivalence:

- Compared against fullc36 (`1dc677be…` original file hash).
- Only two imports and `accepted_records` changed.
- Both target functions are AST-identical, including decorators, parameters, predicates, and assertions:
  - corruption AST `a9f85a32…`
  - retained-scope AST `4ca63e9d…`
- The helper uses actual realm entries, revision-boundary documents, publication history, `inverse_address_resolver`, and `select_inverse_records`; no invented authority or guard bypass.

Limitations:

- This grants only the exact 22 bounded original-behavior credits. It does not infer credit from the prior 47/186/56 aggregates, installed packages, or the full suite.
- The retained full 25691 run remains `17159 passed, 262 failed, 5 errors, 4 skipped`; those 22 originally failed on missing authenticated-boundary normalization.
- No production v2 caller/wire-contract acceptance, full-suite status, or broader inverse behavior is claimed.
- The requested design contract path was absent; Runtime fallback `contract/commit-v2.md` was read and hashed `4581ea85…`.

No product, test, guard, or source files were changed.