# P4 D141l CLI continuation validation

Verdict: `PASS` for the one selected CLI body, with an explicit dispatcher disk-trace custody gap.

## Actual run

- Fresh sustained sampler: six samples from `2026-10-26T10:39:01.935Z` through `10:39:06.992Z`; minimum available bytes `7,539,040,256`, above the native `5,000,000,000` admission and `4,000,000,000` stop thresholds. The retained trace is `disk-trace.txt`.
- CAS installer: `python -P /home/user/work/agent/tools/install_p4_launcher.py /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-P4-D141l-owning-receiving-0907/evidence/candidate-row.txt /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-P4-D141l-cli-body-continuation-next/private/registration f6996b4f1b5c697762bcad3f7cc725c555cf227460240dd0c48e105ac0a0a027 p4-current-becfe-http-3legs` — exit `0`; candidate row installed exactly; outside rows byte-identical.
- Exact dispatcher submission: `bin/request-test integration:agent p4-current-becfe-http-3legs --no-cache` — one submission, service `agent-p4-current-becfe-http-3legs-1026103939-14092`.
- Exact wait: `bin/wait-test agent-p4-current-becfe-http-3legs-1026103939-14092 1` — terminal `pass`, exit `0`; dispatcher summary reports `1 passed in 4.66s` and service elapsed `7s`.

The JUnit reports one test, zero failures/errors/skips, suite time `4.643s`, testcase time `3.436s`, for `tests.editing_conformance.test_p4_cli_sheet_v2_runtime::test_cli_sheet_v2_runtime_preserves_document_and_reads_back`. The command retained `-m pytest`, `-m integration`, `--timeout=45`, `-o addopts=`, and `-p no:cacheprovider`.

## Custody and source checks

- Actual request, row, snapshot, launcher, manifest, runmanifest, JUnit, status, exit, service log, and launcher raw artifacts remain in their original absolute paths. Their measured hashes are in `result.json`; private full custody is retained at `private/terminal/custody.json`.
- Agent, Runtime, App, and Composition were re-read after terminal completion. All are clean at `ecdc242/95d98/82e9/635f`, with trees `d362fe/78df31/6a6e49/5ab519` and the reviewed origins. No Composition repository file was edited.
- `bash -n` on the production launcher, AST parsing of the installer and selected test, registry target/outside-row checks, and the independent terminal custody check all passed.
- Product lint/types are N/A: this task made no product, test, generated-file, pin, or repository change.

## Explicit limitation

The central dispatcher result has no `disk-trace.tsv`; the named service remained on the native LIGHT path. No body-wide disk trace is claimed, and no `request-stop-test` was applicable because the retained sampler never crossed `4,000,000,000` bytes. This is a custody limitation, not a fabricated pass or a reason to rerun through another route.
