# F-D22 audio fixture review

Verdict: **PASS**, bounded to candidate `8d5a368f7530b58494830165e2744f7c56a08395`.

The exact two-file diff preserves all 15 audio vectors and their predicates,
removes only the two non-pytest `xfail` metadata fields, and routes the two
original fade positives through projection followed by the existing trusted
normal-audio preparation boundary. The fixture proves real staged WAV bytes,
registry digest identity, loopback attempt URL serving, attempt containment,
and authored-input immutability. Existing wrong-digest, forged-render-source,
and Composition forged-input controls passed in the same central targeted run.

Evidence:

- Central targeted: **58 passed, 1 deselected, 6 warnings in 30.49s**.
- Ruff touched-file check: PASS; repository baseline **2149/2149**.
- Python compilation and `git diff --check`: PASS.
- Runtime: `9ce4242bc01f100bab9efc51032a73985cefb2b2`.
- Node: `v20.19.4`.
- Source Composition archive: `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.
- Candidate tree: `d5bb88f708738efcf0ad28c13cbfb99d8e50d32f`.

Limits: Mypy could not run in the shared venv because dependency/stub state
fails before analysis; no shared install was changed. The central generic
targeted environment used its Composition 0.0.14 profile, not the separate
819acf profile. No full suite was requested. The audio contract document still
contains stale old strict-xfail/no-producer wording and needs owner
reconciliation separately; it was not part of this candidate diff.
