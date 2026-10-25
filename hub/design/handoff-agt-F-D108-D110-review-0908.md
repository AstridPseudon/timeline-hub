# F-D108/D110 independent protected review

Verdict: **PASS**.

Reviewed author commit `ae2704cb305dc20e972d1a94eea7eac71ee2d2f8` against parent
`d0ecf1d69a7b37f86034bc52004f73f6c6231603`. The exact diff is one insertion and
one deletion in `tests/sdk/test_inverse_removed_shot_owners_runtime.py`: the
module-level pytest plugin tuple is replaced by `editing = runtime_case.editing`.
No other path changed. Target/helper ASTs, bodies, predicates, source graph,
inputs, opaque values, identities and assertions are conserved. The imported
fixture is the genuine `params=['add', 'swap']` fixture, so the corrected test
uses the intended shared seeds and caller containment.

The original `actual2016` FixtureLookupError was a setup/registration failure;
this review does not rerun that baseline. The corrected independent run is
`actual2PASS`: both real-provider ADD and SWAP cases passed on Runtime
`1daca2a33f6d7b10053e07c539a54843e3984e19`, with authentic XML at
`workers/agt-F-D108-D110-review-0908/evidence/review.xml`.

Candidate file SHA-256 is
`d4309b77ab5c4593928ecee738ca426a064ed821191d2d6ad5a9800f86d56a30`;
parent is `a325f2706e3d5c8c8b5b34e4fec6975206d7217a55e04dd4454a8cd39166ecdb`;
diff is `7994a99c4c66279cbb22645b3aaea47d69c41f680e7ab128139b7fa25607ca85`.
Ruff, mypy, py_compile and diff-check all pass. Proposed existing D72
disposition: keep WC3 **OPEN — explicit branch lifecycle and caller cuts
pending**; this focused D110 review does not change the ledger or claim
full-suite/release-wide qualification.
