# Validation — F D141z native whole-path investigation

- Read settled `PLAN.md` first; no plan decision was changed.
- `git rev-parse HEAD` — PASS: `8e42d6f663d506be02f5f63b9e56596884648b50`.
- `git diff --quiet HEAD --` — PASS before evidence-only outputs; repository
  source remained unchanged.
- `git diff --name-status 32bc... 8e42...` — PASS: exactly four modified
  source/control files plus two authorized tracked `.pyc` deletions.
- SHA-256 of candidate, original SAFE0812, qualified56f2 donor, and F1 paths
  — PASS; all values are in `source-map.json`.
- `python3 -B` AST parse of both candidate Python files plus JSON parse of
  `install-map.json` — PASS.
- `bash -n ops-d141z-build-stop/check.sh` — PASS.
- `git diff --check 32bc... 8e42...` — PASS.
- Candidate/qualified `rg` line-map controls for cancellation, control-pipe,
  parent-death, heavy ownership, process groups, wait/reap, and builder route
  — PASS; the exact map is in `source-map.json` and `findings.md`.
- Exact F1 `test -e` checks — PASS for the finding: all three canonical
  Runtime coordinates were absent at this App venue.
- Own PTY disk sampler used actual `df`/`du`, 5-second cadence and
  `ulimit -v 4194304`; it was explicitly stopped, waited, and reaped. Its
  continuity limitation is recorded in `sampler-lifecycle.json`.

Not run by instruction: real delivery build, dry-run/rehearsal, install,
service/queue/registry request, normal `test-run` dispatch, body, full suite,
ZIP, package install, or historical 0741 replay. No product/test/generated/
wire/schema changes were made.
