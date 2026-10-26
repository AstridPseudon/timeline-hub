# D141 protected review findings

## PASS

- Runtime’s authenticated `0849` publication and both exact source preimages match the declared byte counts and SHA-256 values.
- The README candidate preserves all 35,560 source bytes and adds only the bounded disclosure suffix.
- The gate candidate preserves all 25,966 source bytes and adds only the bounded disclosure plus complete table.
- The disclosure occurs once in each candidate; fences are balanced.
- The numbered candidate table matches the controlling `id-join.json` exactly: 32 IDs, five absent files followed by 27 absent exact titles/predicates. All are final `OWN/N/A`; no `OWN/UNKNOWN` final classification is used.
- Exact `delivery-build.render_readme` was imported and called as a function only with controlled four-repository dictionaries. All placeholders resolve; disclosure and table counts are 2 and 1 respectively.
- The missing-gate fallback retains `_Not recorded yet.` and removes the gate placeholder.

## Boundaries retained

The underlying App full and Node suites remain failed as documented, with the separate collection error, exact Node `ssh-keygen ENOENT` non-regression pair, pristine failures, 82e9 applicability boundary, and three inherited lint diagnostics. This review makes no global REG0, gate, ZIP, product, or final-delivery claim. It does not claim an App inventory is Main inventory, and it does not claim canonical CAS ownership.

## Gap

The author’s monitor retained one final durable sample and disclosed a persistence gap for live samples. This reviewer retained the required monitor session but cannot observe a worker PID from the PTY wrapper; the session ID is recorded in `sampler-lifecycle.json`. No continuous disk-coverage claim is made.
