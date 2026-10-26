# D141 cut census review validation

## Results

- XML conservation: **PASS**, 7,392 unique testcase IDs; 7,300 pass, 35 failure, 18 error, 39 skipped.
- Summary reconciliation: **PASS**, XML skipped 39 = service skipped 26 + xfailed 13.
- Bad-ID conservation: **PASS**, all 53 bad IDs occur exactly once and match XML status/class/name; all 53 parameter selectors are preserved.
- Selector AST review: **PASS**, 15 exact mappings reproduce both recorded AST hashes; 38 `NEW_OURS` mappings have one bounded frozen-pristine name/body-text check with 0/0 matches.
- Source custody: **PASS** for Runtime/Agent commits, trees, clean status, and present Git blob objects.
- Cut raw/control custody: **PASS**, retained XML SHA-256 `227a6efa2e4886b0d1ae3d657e703174ef6a7ccb5f4aaa558875d3887dde31f0`; every listed cut artifact hash and `KEEP` marker match.
- Exact manifest/control custody: **FAIL**, pristine `why` actual SHA-256 `9bbf7539757ca42cce991a9ca3b16b33f5adc92cc3eb139dbb1839a8ac37d971` differs from recorded `186892ceda5ead968acf6748cc708ab4bea1cb7aa6be2770f2dcf32727da2905`; Composition and `worktree_tree` fields contain unresolved placeholders.
- Classification: **UNKNOWN**, because the pristine comparator is queued and has no test outcome. No REG, preexisting, product-fault, or zero-REG claim is made.

## Read-only commands/checks

The review used only read-only `sha256sum`, `git rev-parse`, `git status --porcelain`, `git ls-tree`, `git cat-file`/object resolution, Python standard-library XML/JSON parsing, and Python `ast` parsing/hash checks. No imports, collection, tests, providers, or failure investigation were run.

## Privacy

The published evidence was checked for the permitted safe identity, exception class, file/line, hash, and custody fields. No raw failure/error messages, runtime payload bodies, user content, credentials/keys, or URLs are present. Full test selectors remain because exact parameter names/selectors are required for conservation.
