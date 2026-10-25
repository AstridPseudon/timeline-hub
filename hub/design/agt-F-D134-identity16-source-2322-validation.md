# D134 identity16 validation

## Read-only evidence checks

- Root-cluster JSON enumeration: 16 member IDs; unique count 16.
- Root-review2029 and retained partition read; root-004 classifications
  conserve 11 setup/expectation-proved and 5 UNKNOWN.
- Current Agent head verified as
  `41ad656529fa8489829de9078b1b6e157c7433c8`; pre-edit tree
  `d29e47fe7be6e55940b42fa1477a23e7925f62fa`.
- Current lock source verified as Runtime
  `f103bb46866999c961a8865636f2e66d544e0c9b`; producer tree
  `5d0cedf2e5134acf895e8d43191cc5fdc09f9883`.
- D139 provenance review read-only evidence confirms the 15 canonical consumer
  bytes are equal between f103 and ab1e.
- Current source blobs, source SHA-256 values, caller boundaries, and receipts
  are recorded in `source-manifest.json` and `member-map.json`.
- No source/test body or assertion diff beyond the three current-runtime setup
  literals.

## Governing static checks

```text
RUFF_CACHE_DIR=/tmp/w-d6d6d6bf03/d134-identity16-ruff \
  /home/user/work/venv-agent/bin/ruff check \
  tests/editing_conformance/test_gate1_fresh_word_transcript_frontends.py \
  tests/editing_conformance/test_inverse_stage_runtime_regressions.py \
  tests/editing_conformance/test_native_word_anchor_vectors.py \
  tests/editing_conformance/test_next_command_cohort_runtime.py \
  tests/editing_conformance/test_prepared_video_birth.py \
  tests/editing_conformance/test_word_binding_recipe.py \
  tests/sdk/test_timeline_commit_provider.py
PASS - All checks passed!

PYTHONPYCACHEPREFIX=/tmp/w-d6d6d6bf03/d134-identity16-pycache \
  /usr/bin/python3.11 -m py_compile \
  tests/editing_conformance/test_gate1_fresh_word_transcript_frontends.py \
  tests/editing_conformance/test_inverse_stage_runtime_regressions.py \
  tests/editing_conformance/test_native_word_anchor_vectors.py \
  tests/editing_conformance/test_next_command_cohort_runtime.py \
  tests/editing_conformance/test_prepared_video_birth.py \
  tests/editing_conformance/test_word_binding_recipe.py \
  tests/sdk/test_timeline_commit_provider.py
PASS - exit 0

git diff --check
PASS - exit 0
```

Functional tests, provider preflight/launcher, central service, mirrored tests,
and full suites were not run by task scope. The five UNKNOWN cases therefore
remain unqualified.
