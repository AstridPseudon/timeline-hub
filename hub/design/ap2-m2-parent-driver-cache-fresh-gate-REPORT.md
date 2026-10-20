# AP2 M2 parent driver cache-fresh gate

## Result

The single authorized fresh central gate executed the corrected App snapshot
driver, private source preparation, hosted build, and real browser test. It
did not qualify: the real mounted manual-drop journey failed at the first
opaque-media response assertion because the import response omitted `digest`.
This is a genuine product/test failure after browser execution, not a cache,
driver, build, or early-run failure.

No App source, local driver, browser, socket, or full-suite changes were made.
The assigned worktree remains clean.

## Source and pin validation

The unchanged committed donor was verified before submission:

- donor commit: `74643bed98fc9bf3102f544bc189e6464510f58b`
- donor full tree: `a75e27930df49a0c4ee9005806d59b14f16d2361`
- donor status: clean
- corrected retained driver: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-retained-evidence-real-gate/run-parent-manual-drop-evidence.sh`

The driver accepted only the exact App tree and clean status. The central
service's synthetic App commit was retained as observed evidence:

```text
observed App HEAD: 014fc615c7ab8e0bb2d1078b7d713d144ccc0e0e
observed App tree: a75e27930df49a0c4ee9005806d59b14f16d2361
observed App status: clean
expected original App HEAD: 74643bed98fc9bf3102f544bc189e6464510f58b
expected App tree: a75e27930df49a0c4ee9005806d59b14f16d2361
```

Strict external pins passed before the gate and again in the central runner:

- Agent `3c4f6de4fa777323b3386c01c7266b619b86af6d`, tree `aaf49eca6c2b119b21df1d89b0e56df5d1c60f9c`
- Runtime `202074110717146fc7f08af2306a8dd7f695b0b1`, tree `ee39286bd0eb27d4075074cc4785d6d15e33f243`
- Runtime producer `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`, tree `4b7dd0fe44be973c344bab3de568eaf0bdd28476`
- producer is an ancestor of Runtime: passed
- artifact `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0`
- schema `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`
- locked Composition `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`

Resource preflight passed: zero private014 worker directories, 17 GiB
available, and the retention probe passed. The normal `--no-cache` request
was the authorized cache bypass; no cache deletion or owner decision was
needed.

The independently approved correction report also records the focused guard
suite as 16 passed, plus JavaScript syntax, shell syntax, and diff checks. I
did not rerun that source suite because this worker made no driver or source
edit.

## Central gate

Exactly one request was submitted, with `--no-cache`:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-parent-snapshot-tree-guard-source ap2-m2-parent-retained-evidence-real-gate --no-cache) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Run ID: `ap2-m2-parent-snapshot-tree-guard-source-ap2-m2-parent-retained-evidence-real-gate-1020225033-23319`

Result: **FAIL, exit 1, 129 seconds**. The central runner reached the
pre-browser collection, private graph preparation, hosted build, and one
Playwright worker. The hosted build passed in 1m21s; only ordinary Vite
chunk-size and dependency warnings were emitted.

Pre-browser evidence included:

- one collected test: `tests/e2e/local/three-products.spec.ts:1208:1`
- `private node graph: packages=532 bins=34`
- `normal014 App PRE-browser: private npm/Vite caches and hosted build output verified`
- artifact and schema verification passed

## Real browser evidence

The seeded real media was `video/webm`, decodable, 160935 bytes, with object
ID/digest `sha256:263405664d5947bdd88509f47b3dbdadf1eb1826d4bf36da096630ad100bf41d`.
The retained bounded summary records six Runtime requests and these statuses:

- POST `/media-imports`: `201`
- ordinary selection GET: `200`
- deliberately wrong verified selection GET: `404`, `not_found` (native refusal)
- positive import POST: `201`
- positive selection GET: `200`
- positive verified selection GET: `200`

The browser reported zero console entries and zero captured errors. The test
then failed at `tests/e2e/local/three-products.spec.ts:1303`, where the
positive import entry was expected to contain:

```text
digest: sha256:263405664d5947bdd88509f47b3dbdadf1eb1826d4bf36da096630ad100bf41d
```

The received entry contained `object_id`, `size`, and `media_type`, but no
`digest`. Because this assertion is before the subsequent lost-ack/reload,
retry, undo, opaque-preservation, and zero-legacy assertions, those milestones
are **not proven by this run**. The browser did execute the real media and
refusal/positive request paths; this was not an early test-service failure.

## Retained evidence

The wrapper copied evidence before disposable-root cleanup to:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-retained-evidence-real-gate/recorded-evidence/`

Retained files:

- `playwright-trace.zip` (2924249 bytes)
- `error-context.md` (15168 bytes)
- `bounded-browser-evidence.json` (7111 bytes)
- `runner-tail.log` (21186 bytes)
- `source-tree.txt` (345 bytes)
- `result.txt` and `retention.log`

The source tree report and bounded summary preserve the observed synthetic
App identity, strict external revisions, request/response facts, and first
browser failure. The disposable run root was removed only after those copies.

## Tests and checks run

- donor full-tree/clean checks using `git rev-parse` and `git status`: passed
- strict Agent/Runtime/producer pin and producer-ancestry checks: passed
- `sh -n .../run-parent-manual-drop-evidence.sh`: passed
- `sh .../run-parent-manual-drop-evidence.sh probe`: passed
- central retained-evidence gate above: failed at the real opaque-media
  `digest` assertion after build/browser execution
- App worktree `git status --short --branch`: clean; no local full suite,
  browser, or socket run was performed; the only local driver action was the
  read-only shell syntax/retention probe above

## Blocker and recommended next step

Qualification is blocked by the positive `/media-imports` response omitting
the required `digest` field despite returning the matching `object_id`. The
App/Runtime owner should repair or reconcile that response contract while
preserving the existing refusal and opaque-field expectations, then obtain a
newly authorized gate. Do not count this run as proof of reload/retry/undo or
zero legacy traffic, and do not resubmit this worker's one-request gate.
