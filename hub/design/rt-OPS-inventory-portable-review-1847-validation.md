# OPS portable whole-maker fixture review

Verdict: **FAIL**.

The reviewed final source is branch `tl/rt-OPS-inventory-portable-review-1847`,
commit `674d13e26ce40ce9a158a7e50b226c247fbc9588`, tree
`f2abd214b4b45fa4a6b6de0932ad5371e4f3fc4b`. The `f6b9` label in the authored
fixture manifest is the parent input/source baseline (`f6b9d4d...`, tree
`a4fe6f...`), not the final source SHA.

## Findings

1. Required `git diff --check f6b9d4d52..HEAD` fails:

   ```text
   ops-child-custody/e2e-fixtures/tiny/makers/candidate-c3226b/make-child-venv:1224: new blank line at EOF.
   ops-child-custody/e2e-fixtures/tiny/makers/parent-0857/make-child-venv:1201: new blank line at EOF.
   ```

   These are the exact packaged maker bytes, so removing the blank lines would
   require a new source review and new manifest hashes.

2. `--check-only` does not compare committed receiving-carrier bytes with the
   accepted fixture bytes. At `e2e_inventory.py:255-269` it checks Git
   readability, clean status, exact path set, and 100644 modes, but does not
   hash `git show HEAD:<path>` against `fixture_sources()`. The later
   `committed_fixture()` check at lines 325-334 does compare bytes, but that is
   after the check-only admission point. A clean checkout with altered
   committed content can therefore pass the required census and fail only
   during venue preparation.

3. The check-only census is not total for fixture-source failures. The initial
   manifest walk records missing/mismatched fixture files, but the later source
   carrier loop calls `fixture_sources()` directly. Its `require()` can raise
   before the promised complete JSON `missing` list is emitted.

The 1829 diagnosis is confirmed: the original 1747 runner omitted private
`tests/suites.conf`, so unchanged `Store.ensure`/`_verify_projection` failed
before any stage. The finalized source creates an empty private baseline at
`e2e_inventory.py:415-422` before the unchanged `Store.initialize` calls. The
original result remains parent exit 2 with zero stages; no parent RED or
candidate GREEN is inferred.

## Source/provenance checks

- Packaged parent maker SHA-256: `0857a5e0...e57b6d39`, mode 0755.
- Packaged candidate maker SHA-256: `c3226b93...72e7142e`, mode 0755.
- Protected Store helper: `123bb93c...b7adfe2`.
- Protected dependency helper: `116b4e6b...d7bfe2`.
- Parent/candidate/production Store-Python block: `0889b240...8ca50c`.
- Parent/candidate/production verifier block: `f7c7ebcc...5eda209`.
- Bootstrap archive: `443977b0...cb548`; its three required wheel hashes
  match the source pins.
- Tiny source/maker manifest hash and mode audit: PASS.
- Source scope from `f6b9`: exactly seven paths, all under the fixture/docs/
  test-support scope; no normal-source pin/client or production files changed.

The real Agent venv reports Python 3.13.16, build 1.4.0, setuptools 80.9.0,
and wheel 0.46.3. `/usr/bin/python3.13` reports Python 3.13.16 and imports
the required stdlib modules. Current free space was below the unchanged normal
child reserve, so no body was authorized.

## Targeted commands

| Command | Result |
| --- | --- |
| `bash -n` on both packaged makers | PASS, exit 0 |
| in-memory compile of seven embedded Python blocks in each maker | PASS |
| `PYTHONDONTWRITEBYTECODE=1 python3 -B -m py_compile ops-child-custody/tests/e2e_inventory.py ops-child-custody/tests/support.py` | PASS, exit 0 |
| `/home/user/work/venv-agent/bin/ruff check --no-cache ops-child-custody/tests` | PASS |
| `git diff --check f6b9d4d52..HEAD` | FAIL, exit 2; two blank-at-EOF findings above |
| check-only with all external prerequisites omitted | PASS as a negative control: exit 2, JSON emitted, `mutating_setup_started`, `maker_started`, `store_initialized`, and `git_mutated` all false; all supplied external omissions were listed |
| whole-maker E2E | NOT RUN by this review |

No full suite, live Runtime, production Store, Git history creation, install,
network, credential, permission, browser, or whole-maker body was run.
