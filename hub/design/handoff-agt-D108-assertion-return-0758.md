# F-D108 assertion-return correction (source-only)

Overall result: `NOTPROMOTED`. Authoritative D108 membership remains `EXACTMISSING`: `129` changed bodies, `113` removed assertion fingerprints, and `287` added fingerprints. The named applied rehearsal manifest/audit is absent at its recorded path; peer 0755 requests that genuine artifact. No predicate is cleared from totals.

## Corrected finite fallback

The explicit fallback direction is old captured Agent `d6294843286c18e57af3c1874cf1996be42212d2` → current upstream Agent `08e6b905114a3ee2b05c3e7980421f26b4abf15c` over `146` modified Python test paths common to both exact Git objects. It records `189` changed bodies, `310` removed assertion/raise fingerprints, and `119` added fingerprints. Residue versus the authoritative aggregate is `60 / 197 / -168` (changed / removed / added). It is retained, not reinterpreted or promoted.

Every changed function row records path, qualified name, old/current Git blob, body SHA-256, parameters, markers, and `pytest.raises` coverage-limit metadata. Every old predicate separately records `ast.Assert` and `ast.Raise`, line, exact fingerprint, body hash, and blob. Exact same-path, same-qualified-function, same-kind/fingerprint matches are `current_equivalent`; unmatched rows are `UNCLEARED`. No ordinal pairing, rename pairing, operator equivalence, or semantic inference is used.

Fallback rows are partitioned into disjoint PR-sized `NOTPROMOTED` groups. The JSON contains the complete finite rows and row-ID set arithmetic.

## Scope corrections and preservation inquiry

`d629→b943` changes six paths, including D110 `astrid/sdk/timeline/inverse.py` and `tests/sdk/test_inverse_removed_shot_owners_runtime.py`; it is not D07-only. Crosswalk JSON/Markdown hashes are recorded independently from missing-manifest expected hash `37e559…a4504`.

For preservation, the JSON explicitly compares upstream `08e6b905114a3ee2b05c3e7980421f26b4abf15c` as old against captured `d6294843286c18e57af3c1874cf1996be42212d2` and applied `c456b3281497653cecf44f61acd6fa30565d83c8` as separate new objects using the same exact Git-object/stdlib-AST algorithm. That inquiry does not replace corrected `d6294843286c18e57af3c1874cf1996be42212d2→08e6b905114a3ee2b05c3e7980421f26b4abf15c` fallback. D07, Windows0742, and D107 remain distinct scopes. No product/test/body changes were made.
