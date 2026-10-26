# D141 cut census correction validation

## Result

The two 0137 custody findings are corrected in an immutable derivative record. This is a finite evidence correction, not a behavioral or comparator result.

- The original 0132 `cut-failures.json` and `selector-map.json` are referenced byte-exact by SHA-256; neither was copied, refreshed, or reclassified.
- The original 0132 source manifest hash and the complete 0137 review/findings hashes are retained as history.
- The pristine `why` file is explicitly treated as mutable queue-admission diagnostic text. The original 0132 claimed hash, the 0137 observed hash, and the 0143 current observed hash are all retained; the current observation is timestamped and is not test proof.
- Every unresolved tree token from the 0137 finding is replaced by a real tree resolved from its named immutable commit with `git rev-parse <commit>^{tree}`. No source was edited.
- Runtime, Agent, and Composition commit/tree/origin bindings and clean-state observations are frozen in `source-manifest.json`.
- The pristine request remains `queued`; XML, summary, runner exit, comparator body, and any REG/preexisting/zero-REG verdict remain missing or unknown.

## Acceptance checks

| Check | Result |
| --- | --- |
| Parse `correction.json` and `source-manifest.json` as JSON | PASS |
| Original 0132 cut/selector/source hashes present and unchanged by reference | PASS |
| Two findings represented exactly once | PASS |
| Current `why` observation includes hash, size, time, mutable-diagnostic label, and no behavioral-proof claim | PASS |
| Original, 0137, and current `why` observations preserved without false equality | PASS |
| No unresolved tree token in derivative JSON/Markdown | PASS |
| All resolved commit/tree pairs match exact Git objects | PASS |
| Pristine queue missingness and no-regression verdict remain explicit | PASS |

No imports, collection, tests, lint, typechecks, providers, full suites, or product execution were run, as required for this evidence-only correction.
