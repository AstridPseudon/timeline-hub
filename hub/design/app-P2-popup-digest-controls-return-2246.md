## Report

PASS. No source changes made; branch is clean and ready for normal merge.

D83 behavior ledger: On `tl/app-P2-popup-digest-controls-return-2246` (`a1af384bbfd435eee78dc3a4802048150138b331`, tree `992c2b4560f1eab3baa4880b493bff0f16ccf7ef`), the applied popup digest source remains blob `e8eef3daefd841017a81e1eb3cad37fda357183f`; source SHA is `4292d0b5928e1390c48d0e33876621a2e9b6c7e0616607a72f1b3fa3873d1de9` before and `f7dedc84f2a5ddfe855b8ce0fda2edc6b3d4bb71e3bbef030266596855f237b6` after, with proposal SHA `fa30b382ce155015bd330301574297a9e2bcd152a47a362246ce3cd363de52f6`. The retained response independently passed pinned Runtime-Python hashing (`dd264762…`) versus old JS hashing (`446afd12…`); canonical and opaque-field mutations changed the computed digest, left the wire digest unchanged, and failed the strict equality assertion. Eight actual opaque/unknown-field candidates were present. ADD and SWAP list-only selectors each collected exactly one test. No browser, native, service, endpoint, body replay, or source edit was performed; result is PASS and ready for normal merge.

Tests/controls:

- Retained-response old JS digest: PASS, `sha256:446afd120855f6b8df8a67304d6b0d107f6e604c6bbcf5fee91e9345b3f15707`.
- Pinned Runtime helper: PASS, `sha256:dd264762d1813774416abcb3fbd7016de660aba94468278c039fffbe51a8b2c8`.
- Canonical mutation: PASS refusal; mutated digest `sha256:50040a81076fc7bfa44d5f423044720c077a684a70a22e85fa06d3de8df16323`.
- Opaque mutation: PASS refusal; mutated digest `sha256:e0045310ef900894e68c70c5e0938da90b3116029b562d8ab513d8bdca4bdaaf`.
- Playwright `--list`: ADD 1 test; SWAP 1 test.
- `git diff --check`: PASS.
- Pinned Runtime/Agent checkouts: clean and unchanged.
- Prior accepted typecheck/lint evidence was not repeated per brief.

The custom D66 collection wrapper hit sandbox-only `EPERM` during child-process spawn; direct existing Playwright list-only collection passed. DONE marker and conventional commit message were created.