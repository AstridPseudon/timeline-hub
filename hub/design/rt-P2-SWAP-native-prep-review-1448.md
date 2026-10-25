# P2 SWAP3250 native source-result review

Verdict: **PASS for the bounded source-only review; exact replay not admitted.**

The retained 3250 facts packet is present, so the stale packet-absent wait is
cleared. The tuple/tree identities match App `fe3309db`, Agent `070dfc5e`,
Runtime `5e9ad1c6`, and Composition `635f4de0`. The registered support row is
real: `orch/tests/suites.conf:223` names `full-p2-swap-native-1055` and the
existing `test_p2_swap_native_replay_and_d112_control` selector. The frozen
Runtime harness source parses and the current Runtime base lacks its diagnostic
files, so this remains a source reference rather than current-tree execution
evidence.

App-vs-D112 differences are source-cited: App setup imports/selects old media,
places the shared occurrence, authors a `doc.patch`, then the mounted App sends
one `occurrence.fork` + `occurrence.swap-media` request with `merge: fields`;
reload and guarded Undo are separate. D112 uses a direct harness with fresh
pins, `occurrence.add-media`, then `occurrence.swap-media` against the newly
added row with `merge: atomic`, followed by direct `timeline.inverse`.
Sources: App `tests/e2e/local/three-products.p2-popup.spec.ts:254-313,365-383,423-440,523-577,854-918,949-954`; frozen harness
`diagnostics/measure_p2_swap_native.mjs:113-120,142-171` and
`diagnostics/test_p2_swap_native.py:11-24,69-120`.

Finite exact-missing inputs remain bounded as follows: (1) original request
body/commands/reads/identity missing although `original_body_count` is 1; (2)
authentic pre-SWAP base/history/closure missing; (3) exact historical media
selection and registry custody missing; (4) receiving diagnostic publication
bound to Runtime `5e9ad1c6` missing; (5) private realm/auth custody is
`UNKNOWN_CONDITIONAL`, not asserted required. No source-faithful simulation,
actual replay, or root-cause claim was made.

Full evidence: `workers/rt-P2-SWAP-native-prep-review-1448/evidence/source-result-review.md` and `.json`.

Checks: retained JSON parse, Runtime/harness AST, frozen MJS syntax, tuple/tree
identity, and `git diff --check` all PASS. No pytest/provider/native/browser/
integration/full/profile/acquisition/body command was run.
