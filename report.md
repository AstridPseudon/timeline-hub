# P4 ten-note seed review

## Result

**PASS** — reviewed candidate `0afe4e082fd01fc7ffbff469b842538dc21fa50b`,
tree `41b002d59bcbcca0840a774b2bb8b7620e4c92f4`.

The staged base is exactly reviewed `9b658b28c3a7bc3ebda3ad5a7b5b417d78553720`,
tree `84bd8ef3429c06ced18c0639388be8b2c8ecd030`. The candidate diff from that
base is limited to `report.md` and
`tests/editing_conformance/test_p4_ten_note_v2_runtime.py`. The test change is
limited to importing the normal authoring compiler, updating `_seed_original`,
and its docstring. `tests/sdk/fixtures/p4_commit_cases/cases.json` and the
ten-note test body/assertions are unchanged.

## Seed review against PLAN §3 P4 and C0 §§1–5, 7

`_seed_original` now follows the reviewed single-HTTP correction: it starts
from the existing `document_fixture(shared=True)`, adds only the empty
`p4_note` namespace required by the patch parent path, converts the complete
document to the authoring bundle, compiles it with
`compile_authoring_candidate`, and seeds the compiler's complete parent/shot/
internal closure. `parent.setdefault("registry", {})` retains the fixture's
registry and supplies the normal Runtime envelope if absent.

The offline boundary check confirms:

- authored parent fields are byte/value-equal apart from the compiler-owned
  `occurrences` projection; timing (`at`, `hold`, placement timing), opaque
  values, explicit `null`, absent-vs-present note state, and list order are
  preserved;
- authored placement fields and occurrence order are preserved; only the
  compiler-owned `shot_revision_id` is added to each occurrence;
- authored internal timeline payloads are preserved exactly;
- shot payload authored fields are preserved, while the compiler-owned
  internal revision link and per-placement item identity are allowed to be
  materialized by the normal compiler;
- compiler-owned revision IDs, content digests, occurrence pins, and the
  dependency manifest are seeded from the actual compiler output, not copied
  from or substituted for fixture expectations; the resulting closure reopens
  successfully.

The original assertions remain in place for one ten-command/ten-step commit,
per-step inverse and redo, show/history readback, restart, and unchanged
non-note closure. No timing, opaque/null/absence/order/binding assertion,
fixture, expected pin, helper, schema, product, generated, lock, launcher, or
suite file was changed by this review.

## Evidence

Commands run from the candidate worktree:

```text
PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-app2-native/bin/python -m pytest -q -o addopts= -p no:cacheprovider --collect-only tests/editing_conformance/test_p4_ten_note_v2_runtime.py::test_http_ten_note_commit_per_step_inverse_and_redo
PASS — 1 test collected; only the existing unknown pytest `timeout` config warning.

ruff check --config pyproject.toml tests/editing_conformance/test_p4_ten_note_v2_runtime.py
PASS — All checks passed.

mypy --config-file pyproject.toml --no-incremental astrid/sdk/timeline/commit.py astrid/sdk/timeline/commit_session.py astrid/sdk/timeline/emitter.py astrid/sdk/timeline/sync.py
PASS — Success: no issues found in 4 source files.

git diff --check 9b658b28c..HEAD
PASS.

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-app2-native/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P4-ten-seed-review-0511/seed_witness.py
PASS — authored parent/internal/placement closure preserved; compiler-derived occurrences, IDs, pins, digests and manifest reopen.
```

## Exclusions and handoff

The test body was not run. No HTTP request, socket, browser, build, full suite,
or service execution was performed. Therefore Runtime acceptance, inverse/redo
execution, CLI show/history readback, restart behavior, and the full unchanged-
closure assertions remain unverified here. The manager should run the exact
one-test selector against the existing `p4-v2-http-nodes` service next.
