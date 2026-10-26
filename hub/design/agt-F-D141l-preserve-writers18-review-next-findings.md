# D141ee/D141l independent writers18 review

Verdict: `REG_REQUIRED_FOR_15_ROWS`; `3 RENAME_MOVE_ONLY`; `0 OWNER-APPROVED_RETIREMENT`; `15 DROPPED_BY_OUR_PATCHES_REG`.

I applied the controlling MAIN D141ee ruling from the task brief. A generic G5/D52 scope, source commit, migration label, current PASS, or approximate purpose is not owner approval and cannot establish preservation. A row is RENAME/MOVE-only only when the current function has the same body and assertions under a new ID. I compared frozen Git source and AST inputs/assertions/body hashes directly.

Rows 1–3 satisfy the exact AST identity test and their current `[commit]` counterparts are `PASS` in the supplied cut XML. Rows 4–18 have changed function bodies and/or assertion ASTs. The two rows previously labelled `PARTIAL_UNPROVEN` (12–13) are therefore REG rows, not a permitted partial migration. Their one generic current counterpart does not preserve the two actor-specific inputs, writer identity, or discard-first narration assertions.

## Coverage and status

All 18 assigned pristine IDs are present exactly once in `map.json`; there are no omissions or group overlaps. Current counterpart selectors have 17 unique IDs because rows 12–13 intentionally collide on one generic current test. All 18 pristine XML selectors and all 18 current XML selectors are `PASS` in the supplied XML files. That is current/pristine test-result evidence only, not product acceptance.

| rows | disposition | reason |
|---|---|---|
| 1–3 | `RENAME_MOVE_ONLY` | Function-body and assertion AST hashes are identical; only the front-door selector is `[publish]` → `[commit]`. |
| 4–11 | `DROPPED_BY_OUR_PATCHES_REG` | Current commit-path tests have changed inputs, fixtures, bodies and/or assertions; generic G5 migration citations do not waive same-body/assertion identity. |
| 12–13 | `DROPPED_BY_OUR_PATCHES_REG` | Two pristine actor-specific parameter cases were replaced by one generic conflict test; identity and discard-first predicates are absent. |
| 14–18 | `DROPPED_BY_OUR_PATCHES_REG` | Current D66/D39/G234/native-commit tests are materially different bodies/assertions; generic migration records are not exact owner decisions. |

## Adjudication of the author packet

The author packet's `16 PROVEN_MIGRATION / 2 PARTIAL_UNPROVEN` result is not accepted under D141ee. Its cited `agent-G5-publish-final-review-1617.md`, `agent-G5-cli-native-ports-1515.md`, `agent-G5-current-final-review-1638.md`, `agt-D86-publication-0127.md`, D39/D72 material, and `agent-G234-current-qualified-join-0524.md` establish migration scope or bounded current behavior, but none is an exact owner decision authorizing retirement of these pristine assertions. They cannot convert rows 4–18 into migration evidence. No owner-approved retirement is claimed; any proposed retirement remains pending.

## Required next action

Use the exact originals in `restoration-manifest.json` from immutable Agent ref `64197afa297f86f1e738238d5e80aff6d33e303a`. One manager-owned restoration author should restore all 15 listed original IDs/bodies/assertions (or obtain an exact owner retirement decision for each) and then run one targeted same-kind test run. Do not adapt the assertions to the current generic counterparts and do not execute the retired publish route.

The supplied full-pair context remains non-ship: cut `397` bad outcomes (`201 FAIL`, `196 ERROR`) and `19 FAILS_BOTH` remain visible. No REG0, D141v, or product acceptance conclusion is made.
