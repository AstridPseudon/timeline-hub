# D134 identity16 protected review validation

All checks were read-only. No product, test, pin, source, Git ref, hub, or
credential was written.

## Enumeration, hashes, and ancestry

PASS: root-004 JSON and original partition contain 16 IDs; source map contains
16 IDs in the same order and set; unique count is 16.

PASS: original partition classifications conserve 11 setup/expectation-proved
and 5 UNKNOWN. Current map conserves the same split, with all 16 functional
statuses `NOTRUN`.

PASS: candidate `1ae468a0ba47dd43ac0a1dc81b9fb4884ad4ea52` has parent
`41ad656529fa8489829de9078b1b6e157c7433c8`, candidate tree
`2e44289552b3cd52152e80f22f21d5e12d1bf52c`, and parent tree
`d29e47fe7be6e55940b42fa1477a23e7925f62fa`. `git rev-list --count
41ad6565..1ae468a0` returned `1`; merge-base ancestry passed.

PASS: `git diff --name-status 41ad6565..1ae468a0` returned exactly:

```text
M tests/editing_conformance/test_gate1_fresh_word_transcript_frontends.py
M tests/editing_conformance/test_prepared_video_birth.py
```

PASS: all seven current source file Git blobs and SHA-256 values match the
candidate source manifest; five scope files are unchanged from the parent.

PASS: inverse7 Runtime tuple is retained exactly as Runtime
`6634a17f3ffd885567ba3c91b6c7a560df7375a4`, tree
`47b376717ce7a919a697c62133de3e74dc9f6d3a`.

## AST and source checks

PASS: a Python AST comparison over all seven files, normalizing only the four
old/new Runtime identity strings, found normalized AST equality. Aggregate
assert, raise, call, assignment, control-flow, and function counts are equal.

PASS: the textual candidate diff contains exactly three literal replacements:
Gate1 `NORMAL_RUNTIME`, prepared-video `expected_runtime_source`, and prepared-
video `expected_runtime_tree`.

PASS: direct Git-object/hash verification of the D139 canonical15 receipt
reproduced 15/15 equalities across current Agent files, Agent parent files,
Runtime `f103` objects, and recorded SHA-256 values.

PASS: Runtime `f103bb46866999c961a8865636f2e66d544e0c9b` exists with tree
`5d0cedf2e5134acf895e8d43191cc5fdc09f9883`; provider, validation, and Runtime
fixture blobs used by the setup boundary are equal to `ab1e`.

PASS: `git diff --check 41ad6565..1ae468a0`.

## Governing static checks

```text
RUFF_CACHE_DIR=/tmp/w-50ee72cadd/d134-identity16-protected-review-2327/ruff-cache \
  /home/user/work/venv-agent/bin/ruff check \
  tests/editing_conformance/test_gate1_fresh_word_transcript_frontends.py \
  tests/editing_conformance/test_inverse_stage_runtime_regressions.py \
  tests/editing_conformance/test_native_word_anchor_vectors.py \
  tests/editing_conformance/test_next_command_cohort_runtime.py \
  tests/editing_conformance/test_prepared_video_birth.py \
  tests/editing_conformance/test_word_binding_recipe.py \
  tests/sdk/test_timeline_commit_provider.py
PASS: All checks passed!

PYTHONPYCACHEPREFIX=/tmp/w-50ee72cadd/d134-identity16-protected-review-2327/pycache \
  /usr/bin/python3.11 -m py_compile <same seven files>
PASS: exit 0

git diff --check 41ad656529fa8489829de9078b1b6e157c7433c8..1ae468a0ba47dd43ac0a1dc81b9fb4884ad4ea52
PASS: exit 0
```

## Environmental check and non-runs

`/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check
runtime.lock.json --producer /home/user/work/runtime` returned exit 1 because
the shared Runtime worktree HEAD is `0ca306d...`, not the lock’s `f103...`.
This was recorded, not repaired, and is not used as a candidate source delta.

Pytest, collection, imports/provider execution, launcher, preflight, body,
service, child, core, Store, retirement, acquisition, and central/farm suites
were not run, per task scope. No functional result is claimed.
