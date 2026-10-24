## Report

Implemented harness-only qualification:

- Added [`tools/run-env-misc-0020.sh`](/home/user/work/wt/agt-F-env-misc-qualified-0020/tools/run-env-misc-0020.sh).
- Added one targeted service row: `env-misc-qualified-0020`.
- No product, test-body, profile, guard, pin, registry, dependency, or source edits.

Qualification result:

- Central run `agt-F-env-misc-qualified-0020-env-misc-qualified-0020-1024002045-5955`: **PASS**
- `3 passed in 38.98s`
- Passed:
  - installer `[False-0]`
  - installer `[True-1]`
  - bootstrap environment test
- D13 was not run: c886 lacks the required c36 Agent wheel at `/home/user/work/bench-store/entries/child-c886.../wheelhouse/astrid-0.1.0-py3-none-any.whl`. The old ef851 carrier was not reused.

Verified c886 `python -I` origins, RECORD/direct URLs, provision receipt, Node 20, 819acf profile lock/archive/tool hashes, and unchanged before/after profile resource hashes.

Additional checks:

- `bash -n tools/run-env-misc-0020.sh` — passed
- `git diff --check` — passed
- Original test body hashes match the c36 source tuple.

Commit message and `DONE` marker were written.