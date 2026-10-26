# D141l finite read-only validation

Result: `NOT_QUALIFIED`.

## Decision

The two retained bodies are genuine same-kind App full-suite executions on the named historical sources, using the unchanged `npm test -- --maxWorkers=3` command. Their closed manager streams retain exact full `df -B1` table rows. The largest observed in-body bracket is the normal run's 5055897600 to 4839120896 bytes, a 216776704-byte drop from 00:44:22Z to 00:48:37Z. The pristine run's largest timestamped in-body bracket is 4949999616 to 4938567680 bytes, a 11431936-byte drop from 01:11:22Z to 01:15:43Z; its earlier 4951003136 row has no recoverable adjacent timestamp.

Those rows are not authenticated D89d witnesses. The installed validator's ordinary `timeline.d89d.measured-floor.v1` branch requires exactly two manager-owned witness files, each with the exact two-line bytes `Avail\n<decimal>\n`. Neither retained manager log contains those original two-line bytes: each contains a multi-line `df -B1` table. Reformatting a table row would fabricate a new witness file and is not permitted. The source-only controller admission of 5433016320 bytes is explicitly excluded because it predates the bodies and has `body_present: false`.

Therefore `X = null`; no continuous peak or bound is claimed. The selected heavy floor is the mandated fallback `5200000000` bytes, with the unchanged `4000000000`-byte stop. The source-only floor remains `4600000000` bytes. The retained current source-only admission is 4600090624 bytes at 2026-10-26T05:28:09.988639Z, so it clears the ordinary source-only floor by 90624 bytes but does not meet the selected heavy floor.

## Installed caller and schema

Read-only inspection of `/home/user/timeline-hub/hub/kit/bin/test-run` and `/home/user/timeline-hub/hub/kit/bin/d141-validate-receipt.py` found:

- Heavy suites include names beginning with `full`.
- Before admission, `test-run` looks only at the fixed path `tests/<actual-job-id>/recorded-measured-floor.json` under the manager root.
- It invokes the validator with the actual receipt path, manager root, actual job ID, repo, suite, worktree, current `HEAD`, current snapshot `TREE`, and the registered `BASE_CMD`; the validator's stdout is the measured floor used by admission.
- The validator supports both `timeline.d89d.measured-floor.v1` and `timeline.d141.measured-floor.v1`. The former has no trace/authorization extension; it still requires exact source binding and exact start/stop `Avail` witness files.
- The production receiving route remains the normal `request-test`/`test-run` path. No receipt was attached, submitted, registered, or executed here, and no job ID was invented.

## Commands and results

- `sed -n '1,260p' /tmp/.../PLAN.md` — PASS; settled plan read first.
- `sed` over installed `bin/test-run` and `bin/d141-validate-receipt.py` — PASS; no edits.
- `sha256sum` over all named JSON/run/round-log inputs — PASS; hashes are in `source-manifest.json`.
- Read-only JSON and text checks over the retained admission, result, request, snapshot, status, summary, exit, runner, and closed manager-stream records — PASS; no exact two-line `Avail` witness found.
- `git -C /home/user/work/wt/app-F-D141l-unit-measurement-0523 rev-parse HEAD HEAD^{tree}` — PASS; Composition base is 635f4de06fda22a85fc2e4cfc764d0153a4c9f40 / 5ab5191a296980a0a6bcd1178ab6902d6478a148.
- `git -C /home/user/work/wt/app-F-D141l-unit-measurement-0523 diff --check` — PASS.
- `git -C /home/user/work/wt/app-F-D141l-unit-measurement-0523 status --short --branch` — PASS; clean assigned worktree.

No tests, TypeScript, lint, browser, localhost, full suite, or test-service request was run, per the documentary-only brief.
