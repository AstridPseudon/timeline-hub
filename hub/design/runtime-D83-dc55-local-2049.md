# D83 dc55 report

- Added only `d83-native-dc55-2049` to `suites.conf`; prior D83 rows preserved.
- Copied evidence byte-exactly: SHA-256 `caafc14…0eb6ce`.
- Source pinned at `dc55b8bc6e638acd9e5031ff6b51b50cd2e2b63c`, tree `0f941b27…`.
- Central run: `8 passed, 1 deselected`, exit 0, 84.30s.
- JUnit: `evidence/native-dc55.xml`; raw stacks/profiles verified mode `0600`.
- Baseline failure preserved: e745 had 7 passed/1 failed due to N4 observer-on final history GET timeout. No baseline 8-pass claim.

Validation: private Ruff, compile, `git diff --check`, hash/copy checks all passed. No product changes, full-media/doc-patch rerun, full suite, lock-wait inference, or causal/gate claim made.

Commit message and `DONE` marker written.