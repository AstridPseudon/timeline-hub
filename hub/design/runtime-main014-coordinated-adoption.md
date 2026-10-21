# Main014 coordinated adoption recommendation

**HOLD — Runtime qualified; coordinated adoption is not READY.**

Exact Runtime producer: commit `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`,
tree `d3a290b407fa61e6ab2d476f50c068073f70df00`, immutable checkout
`/home/user/work/wt/rt-pin-95bd3c5f`. Main-merged base is `8bd92de` with Main
parents `7a956c0` and `b535646`; the candidate also carries true merge parent
`d1bde2c` and current-integration parent `9d1c43c`. Contract/client are
`0.2.14`/`0.2.14`; Runtime schema is `7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816`;
raw Agent schema is `6ba7b51e…` (55 definitions/29 operations); the 76-artifact
version is `54205b3e…`.

Runtime evidence already passing: central `full31902` on this exact tree —
`5988 passed, 26 skipped, 15 xfailed, 12 warnings`, exit 0, 353.01s; exact
scoped `5889` — `6 passed` in 2.75s; normal generator/artifact checks; local
contract cohort `1581 passed`; commit integration `11 passed`; door `1293
passed`; Gate 4 `29 Python + 61 TypeScript passed`. Runtime integration remains
public `0.2.13` until the synchronized step.

The required current Agent report is absent. Existing Agent pin evidence is a
different producer: Runtime `a0dca169…`, tree `4b7dd0fe…`, schema `ce3781…`,
artifact `f021…`; it must not be treated as equivalent. Agent owns the fresh
normal lock/client generation, current-source SHA/tree and Main ancestry, paired
suite, and the assigned two-node hold-clear proof
(`test_ordinary_http_empty_bootstrap_must_be_reachable` and
`test_ordinary_http_authored_source_window_hold_clear_preserves_timing`).

App now has a reviewed bounded private-staging pin candidate: commit
`10fa2ff9a8216604aa39e3584f89dc9e7a09080a`, tree
`01fd2a04ff0c383ec5281043c7e5a4c843d1d835`, parent/current integration
`f54cd98ed91de213763b196e4ed770b557897a8b`; owner STATUS records Main860
ancestry only as the short form `08dd…`, not a full reviewed ancestry. Its normal
`node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/rt-pin-95bd3c5f`
passed; schema guard passed 1 test, four client files passed 44 tests, and the
central vendor-lock target passed 13 tests. The review correctly HOLDs matched
Agent/App/Runtime qualification: the exact Agent `95bd` consumer SHA/tree and
paired current-source lane are still absent. Historical App/App2 evidence is
public Runtime `2c4ac180`/0.2.13 or `58973`, not a substitute. App owns the
remaining matched qualification, preserving draft/retry/undo assertions. No
Runtime merge/publication or consumer activation is recommended until the
Agent pin and paired App result exist.
