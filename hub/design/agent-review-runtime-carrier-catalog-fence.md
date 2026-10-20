# Agent counterpart review: Runtime catalog-head carrier fence

**APPROVE — bounded private source review only.** Runtime
`7b8d6d9afe963e2b7a6c6b32fd4e3797451090da` / tree
`d20b745c26a33c2ea4e20863f846335c8cf33e1e` is approved as the narrow
catalog-head-fence counterpart for Agent
`3730d0bd51686a1692450359482205df64dcc839` / tree
`3892a10bcffa9bf520b4c79591637cf3259d6724`, private schema
`f80215f272bc2cf302d772d619cb8248108eb597a654e01ab89c3a332204d94f`.

The source boundary is clean: 16 paths differ from Runtime `81f8c7e`; with
the documented 17-path audit boundary (including the unchanged door-audit
test), exactly 415 candidate paths are outside the allowlist and all 415 blobs
match `81f8c7e` (0 mismatches, 0 missing). The public floor remains
`a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`.

The new guard requires the project-scoped `shot_revision_heads.revision_id`
to equal the authenticated accepted image revision on current, inverse-source,
and accepted-historical-slot authorization. Thus a newer catalog head cannot
be repointed through any of those proofs. The typed/private controls,
public-floor refusal, legacy-v1 and accepted-ledger-first retry behavior remain
preserved. The focused regression passed: **1 passed in 1.88s**.

This is not approval to pin, release, activate, integrate, or claim native
qualification. The successor must include Runtime current integration
`a51af885ea631c695a857985239c7fe7bf2e871f` / tree
`7c6ab6700307309a7942e64eb4d0c6c7cc42b681`, retain CAS commit
`3021a5b79102e9c0873f70df46f5a686bd1276ff` / tree
`521fb1dc9aa9e4094e0f901aa3961a1f9db0d471` and its clip-replacement tests,
and preserve/re-review the catalog-text replay fix if merged (local ref
`63e761e29e7e51fc5fa71cc01cd1fe0cf5952125`; the handoff text has a final-`f`
typo). Then run one coordinated `3730` native pair; no such pair was run here.
