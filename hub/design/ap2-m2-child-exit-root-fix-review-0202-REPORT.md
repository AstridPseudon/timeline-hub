# Child-exit root-fix review

## Disposition

**HOLD.** The required real Playwright negative is now proven, and the
wrapper's immediate status capture is structurally correct. The packet is not
approved because the shared source helper was changed outside the exit fix and
the claimed failure artifacts were removed by cleanup.

## What passed

The fresh central result was:

`ap2-m2-bootstrap-current95-create-observer-cause-0115-normal014-integration-e2e-gate5-negative-single-1021021120-3198`

Its retained result files report `status=fail` and `exit=1`. The retained log
shows all of the required real-child evidence:

```text
Running 1 test using 1 worker
normal014 planted failure reached Playwright test body
1 failed
normal014 Playwright child exit: 1
```

The central summary also reports `counts: 1 failed`, so this is not a
preflight refusal or synthetic shell-only probe. The source/artifact checks and
hosted build completed before the one browser test. The structured required-case
summary guard rejected the missing real-case summary afterward, as expected
defense in depth.

The reviewed wrapper captures the `flock`/Playwright status immediately at
`normal014-app-central.sh:162`, logs it at line 163, assigns the wrapper status
at line 165, and only then runs the structured verdict check. The common EXIT
cleanup trap still receives the incoming status and returns it; it was not
changed by this worker's exit patch.

Failure cleanup was checked: `/tmp/timeline-normal014-app.lZM1VH` no longer
exists after the run. `sh -n` passed for the App and common helpers, and the
review worktree is clean.

## Blockers

1. The report says source-binding guards were unchanged, but the shared
   `normal014-source-common.sh` was changed. In particular, the final95
   `APP_BASE_RUNTIME_SHA` was changed from the existing
   `2c4ac180c2220bdad966bc01e95ad230e99ce26a` to
   `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` (line 81), and the helper now
   has the `NORMAL014_USE_BASE_PYTHON=1` bypass at line 306. The negative suite
   depends on both changes. These are separate source/setup changes, so the
   negative does not isolate the exit fix while the required source guards are
   not unchanged. The current helper also contains a separate synthetic-HEAD
   ancestry change at lines 183–188 from the concurrently reviewed source
   packet; that must remain separately owned and reviewed.

2. The central log names a Playwright trace and error-context path, but those
   files are gone because the wrapper cleanup removed the run root. The central
   log is valid failure evidence, but the requested failure artifacts are not
   retained for independent inspection. Do not claim the trace/error-context
   files as available artifacts.

The changed orchestration hashes recorded by the author were:

```text
8f70ed7adafa42d90b3053f5972bd763a653ae690c1b2dfda352e3704615686e  design/normal014-app-central.sh
c76c48fa5f73b72ada6ba8fa857f229778e2ed6948568e77000bf4c1a8490270  design/normal014-source-common.sh
2c2c9be1d0fd3bc5ad6e85fda5bc19f7be88d9c7748363274acdce0668ad24bb  tests/suites.conf
10db990835b172c58a0d3a7a43ee8c00dead5b00cb6cc198ef8984edd9221b51  normal014-negative.spec.ts
```

No `bin/test-run` edit, product-code edit, historical-result rewrite, extra
real bootstrap/neighbor run, or full suite was observed.

## Exact checks

- `sh -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-app-central.sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-source-common.sh` — PASS.
- `R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-bootstrap-current95-create-observer-cause-0115 normal014-integration-e2e-gate5-negative-single); /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test ap2-m2-bootstrap-current95-create-observer-cause-0115-normal014-integration-e2e-gate5-negative-single-1021021120-3198 100` — expected FAIL, with `status=fail`, `exit=1`, one planted Playwright failure, and child exit 1.
- Artifact check for
  `/tmp/timeline-normal014-app.lZM1VH/browser-output/three-products-normal014-planted-negative` — no files remain after cleanup.
- Review worktree `git diff --check` and `git status --short --branch` — PASS,
  clean.

## Recommended next steps

Keep the valid central negative result and its retained log. Split or revert
the source/setup changes so the exit-fix review covers only the minimal
suite/helper status-capture change, or obtain an explicit independent review
for those source/setup changes. Preserve failure artifacts in a permitted
result location if artifact-level inspection is required, while retaining the
existing cleanup/source guards. Then rerun only the authorized narrow negative
if needed; do not rerun the real bootstrap case or passed neighbor in this
review.
