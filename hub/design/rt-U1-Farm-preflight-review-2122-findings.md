# D135 independent review

Verdict: **FAIL**.

The candidate’s seven-module source-only import census is structurally sound
for the checked frozen objects, but it does not satisfy the executable Farm
gate as written.

1. **Required Runtime/Agent commit and tree are not enforced.**
   `source-manifest.json` records the required `0bb3bc45/tree73d92563` and
   `32dde0c/tree81ad4d`, and the 21 listed blobs match those objects. However,
   `preflight.py` never reads `source_tuple`, invokes Git, or checks a checkout
   commit/tree. `_source_checks` only hashes the listed files. A different
   checkout can therefore pass the listed-file checks without being either
   required frozen source tuple.

2. **The interpreter requirement is only path equality.**
   The preflight records `platform.python_version()` and
   `platform.python_implementation()` but readiness only tests
   `matches_expected` (lines 357–364 and 405–414). It does not require CPython
   3.13, and `--expected-interpreter` is overrideable. The recipe’s `test -x`
   checks existence, not implementation/version.

3. **Distribution minimums are metadata only.**
   `_package_check` records each manifest `minimum` but never parses or compares
   it; any installed version with an importable module is marked `installed`
   (lines 217–230). This does not enforce the declared pytest, timeout, PyYAML,
   jsonschema, or referencing prerequisites.

4. **`all-missing.json` does not list every missing input.**
   Import failures are appended to `all_missing` (lines 381–391), but
   `package_missing`, failed source hashes, failed AST manifests, origin
   failures, interpreter failures, and path failures are kept separate and are
   not written to `all-missing.json` (lines 393–440). In particular, a missing
   distribution is absent from the required “exact missing distribution/module
   names” refusal record.

5. **Local-helper origin/manifest coverage is incomplete.**
   `_origin_guards` checks only the seven `actual_modules` (lines 300–328).
   The manifest’s helper source files are hash-checked as paths, but the
   origins of helper modules loaded transitively by the real imports are not
   required to match those source files, and helper ASTs are not included in
   the manifest side-effect/import coverage. The exact Python path makes the
   intended order clear but does not itself prove every loaded local helper’s
   origin.

6. **The durable collection counter can report a false zero.**
   The recipe parser takes counts only from root attributes (lines 62–65). A
   normal pytest `<testsuites>` root may omit aggregate `tests`, `failures`,
   `errors`, and `skipped` while child `<testsuite>` elements contain them. The
   prescribed parser then records zero instead of aggregating children. A safe
   synthetic probe with one child suite (`tests=2`, `failures=1`, `skipped=1`)
   produced `tests=0`, `failures=0`, `skipped=0`.

The six-file argv, addopts clearing, cache disabling, timeout 45, durable XML,
log, exit and collection paths are otherwise present and unchanged. The
actual Farm preflight and six-file body remain **NOTRUN**; no provider, socket,
Store initialization, pytest collection, test body, acquisition, or broad
suite was run for this review.
