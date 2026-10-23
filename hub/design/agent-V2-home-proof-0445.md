# PASS — V2 home proof

Integrated `9729c07b764ba6cce1bb31686cb93d29fc72b14d`, tree
`81233b797eee27dedb8a39a3c2528fb5dff0765e`. The V2 validator and direct P1
regression blobs exactly match reviewed `89c700aded947a4c498043e0f1a46b4ab3e0a873`.
The mounted caller is `commit.py:1114` → `validation.py:441` → timing
validator. Review0414 targeted command passes **144 tests** on this tree; the
three-test reduction from the earlier 147 is inherited `838431382` meta-test
rewriting, not a V2 blob change. Ruff `2150/2150`, mypy `1915/1915`, scoped
Ruff/private mypy/diff, vendor-lock, and artifact-manifest checks pass. The
first-parent `ccc521b78` P4 ancestry remains separately unqualified; no G234,
whole-P4, or overall-home claim is made.
