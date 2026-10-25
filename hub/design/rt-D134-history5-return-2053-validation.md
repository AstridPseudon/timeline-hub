# D134 first return validation

## Result

Applied the two finite source/setup corrections supported by the protected
review: Gate1 now uses the qualified current schema/Runtime tuple, and the
prepared-video guard now names the same qualified Runtime commit/tree. The M1
archive link is repaired in evidence only. The authentic archive is present,
but the retained current source still reaches the `on` assertion at line 133;
that behavior remains UNKNOWN. No live qualification or product-fault claim is
made.

## Exact source tuple

- Agent parent: `a30e74e901a28b39c28facba3deb00d76f186e23`, tree `ece8e0887e48e45cb1fce85b1256c49a0f6126c0`.
- Qualified Runtime: `ab1e4f6141987706132916e2da16477f5a019464`, tree `7d8e77b2f5a4af79305c9212ce5174d3ea9fd657`.
- Current edit schema SHA-256: `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`.
- Current `runtime.lock.json` SHA-256: `ad818e99cb0759d1742d9f67b5bb3367b03fd3e88d8f65846253169272b8b6ce`.
- M1 archive SHA-256: `2915bd4ac0d46954d19c30f87a517b82074218699978e650fab03fcba81b72d3`; authenticated members include `backup/manifest.json`, `backup/cas-manifest.json`, and `backup/realm.sqlite3`.

## Meaningful source delta

- `test_gate1_fresh_word_transcript_frontends.py`: replaced stale schema and Runtime identity literals; bound `fresh_realm` to `use_runtime(commit=NORMAL_RUNTIME)` and used that exact extracted root for Runtime test imports. Removed the now-unused `runtime_checkout` import.
- `test_prepared_video_birth.py`: replaced only the stale expected Runtime source/tree literals.
- `test_m1_legacy_archive_read.py`: unchanged. Archive presence does not repair the retained `on` behavior boundary, so no normalization/removal/retirement was attempted.

The exact five assigned node IDs, all three Gate1 parameter values, assertion
records, raises, authored inputs, media inputs, and purposes are mapped in
`predicate-map.json`.

## Static checks

All commands used the three assigned files and worker-owned caches under
`/tmp/w-ab02322cac`:

```text
RUFF_CACHE_DIR=/tmp/w-ab02322cac/d134-ruff-cache /home/user/work/venv-agent/bin/ruff check tests/editing_conformance/test_gate1_fresh_word_transcript_frontends.py tests/editing_conformance/test_prepared_video_birth.py tests/editing_conformance/test_m1_legacy_archive_read.py
PASS — All checks passed!

PYTHONPYCACHEPREFIX=/tmp/w-ab02322cac/d134-pycache /home/user/work/venv-agent/bin/python -m py_compile tests/editing_conformance/test_gate1_fresh_word_transcript_frontends.py tests/editing_conformance/test_prepared_video_birth.py tests/editing_conformance/test_m1_legacy_archive_read.py
PASS — exit 0

git diff --check
PASS — exit 0

MYPY_CACHE_DIR=/tmp/w-ab02322cac/d134-mypy-cache /home/user/work/venv-agent/bin/python -m mypy --cache-dir=/tmp/w-ab02322cac/d134-mypy-cache --config-file pyproject.toml tests/editing_conformance/test_gate1_fresh_word_transcript_frontends.py tests/editing_conformance/test_prepared_video_birth.py tests/editing_conformance/test_m1_legacy_archive_read.py
PASS — Success: no issues found in 3 source files
```

## Functional status

Functional pytest was NOTRUN. Observed free space was `4,486,144,000` bytes,
below the mandated `5,000,000,000`-byte admission floor and above the
`4,000,000,000`-byte source-only stop line. No provider, body, socket,
collection, browser, full, or central test-service run was requested. No
`originals.xml` was generated.

The exact M1 retained failure boundary is `test_m1_legacy_archive_read.py:133`.
The archive is authentic and available; the remaining on/opaque/anchor
behavior is UNKNOWN pending a separately authorized qualified source/behavior
run.
