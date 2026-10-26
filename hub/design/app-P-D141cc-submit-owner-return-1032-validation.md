# D141cc validation

## Verdict

The private submit-owner continuation is **READY_FOR_INDEPENDENT_REVIEW**. It is
source-only and does not change product code, tests, the production builder,
registry, queue, wire contract, or any service state.

The control model is deliberately a harmless in-memory service stub. It proves
the old overlap shape (two worker invocations each making one normal call) is a
failure and proves the corrected route adopts an existing exact request before
considering any new request. It covers all requested custody, status, source,
selector-isolation, disk-stop, and duplicate-call controls.

## Exact checks

- `evidence/candidate/check.sh` — **PASS**.
  - Controller self-test: 12 scenarios PASS.
  - Python AST guard and private-cache compile: PASS.
  - `bash -n`: PASS.
  - `ruff check --select F evidence/candidate/controller.py`: PASS.
  - Genuine-builder binding/conservation and all seven dispatch rows: PASS.
- `python3 -m json.tool evidence/candidate/cases.json` — PASS.
- `python3 -m json.tool evidence/adoption.json` — PASS.
- `python3 -m json.tool evidence/source-manifest.json` — PASS.
- `python3 -m json.tool evidence/dispatch-recipes.json` — PASS.
- `python3 -m json.tool evidence/sampler-lifecycle.json` — PASS.
- `sha256sum` source publication and reviewed source-map/binding inputs — PASS;
  hashes are recorded in `source-manifest.json`.

## Control coverage

The self-test covers initial single ownership; live preflight-only ownership;
normal-created-before-artifact-durable recovery; same tool-session resume vs a
new invocation; adoption of queued/running/completed/cancelled requests;
multiple-candidate and mismatched-source rejection; honest cancelled old
attempt handling; independent selector failure isolation; exact-ID 4-GB stop;
and no duplicate submit/body calls. `scenario_original_overlap_is_failure`
retains the proved failure shape rather than rewriting it as a pass.

## Disk trace

The first tool made a fresh five-second read-only `df` trace before private
inputs were created. It observed 5,961,859,072 bytes at both samples, remained
above the 4,000,000,000 stop, then sent TERM, waited, and reaped the sampler.
This trace is present-time evidence only and does not backfill any service
trace or qualify an actual body.

## Not run

No actual `--submit`, request/wait/stop operation, body, browser, localhost,
full suite, delivery build, dry run, rehearsal, registration, product test,
typecheck, lint, or queue/registry operation was run. Product types/lint and
product tests are N/A for this private operational artifact.
