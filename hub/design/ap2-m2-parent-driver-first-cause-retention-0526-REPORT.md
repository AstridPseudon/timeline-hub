# M2 parent driver first-cause and retention diagnosis

## Result

The authorized actual `26621` failed before the browser and before any
request. The exact first failing condition was the durable driver's stale App
ancestry guard:

```text
git -C "$app_root" merge-base --is-ancestor "$app_ancestry_anchor" "$observed_app_head"
```

The consumed durable driver set `app_ancestry_anchor=7e85d89120227f336a2e8dbf8e0ea44d98311da0`; the observed approved parent was HEAD `a304dce02a185a4774ff514d5aa451c9702aa46f`, tree `a3c82aa91f1336b86491191acf857d88c56179b2`. The ancestry command returns exit 1. The current source driver already carries the reachable anchor `84ec385a463fd4907628e68e87aabbe717202a96`, for which the check returns 0.

The durable driver has `set -eu` and installs its EXIT trap before the guard.
It exits at line 168, before `run_root` or `runner.log` is created. The trap
records `runner_status=1` and the fallback `runner.log was not retained by the
runner`; this is not cleanup loss. There is no child command, browser, HTTP
request, ADD body, or product assertion.

## Historical evidence

- Central test: `ap2-m2-parent-complete-current-proof-source-0455-ap2-m2-parent-finalhash-actual-0517-1021052152-26621`.
- The central log reaches, in order: captured service-tree guard, protected
  keeper guard, helper hash guard, driver hash guard; then exits 1.
- Retained evidence has `runner_status=1`, empty `requests`, `responses`, and
  `console`, and no trace, error context, or request/response summary.
- Helper SHA: `af83e829f73ebcf9613e67808f81cab06c2e78f70c21bc850550cde1b5885fa4`.
- Consumed durable driver SHA: `40c7b57b6f327bafa82f26daaa4053f405e89f7bd48b5aacdadd21b2393867f0`.
- The four outer hash guards passed; the stale ancestry guard was inside the
  durable driver and was not covered by them.

## Cause classification

| Candidate cause | Finding |
| --- | --- |
| `set -e` early exit | **Yes.** The stale `merge-base` condition returns 1. |
| Wrong mode/root | **No.** Invocation was `run "$KEEPER"`; keeper HEAD/tree, clean status, `KEEP`, and node-module provenance passed. |
| Cleanup deleted evidence | **No.** `run_root` was never created. |
| Wrong `TMPDIR` marker | **No** for the first cause; `merge-base` does not use it. |
| Runner path | **No** for the first cause; helper/driver paths existed and hash guards passed. |
| Nested environment mismatch | **Not the first cause.** After ancestry was corrected, the next observed boundary was offline private-venv pip setup because the actual driver omitted `NORMAL014_USE_BASE_PYTHON=1`. |

## Harness-only candidate

Changed file only:

`tests/e2e/local/support/run-parent-manual-drop-evidence.sh`

Candidate identity:

```text
sha256: 362f9ae837a2a7a9fbd5ddda21a51821b7b59476f5252d3b1758907538c2b9af
git blob: 6973b135c901b21ede85830a1cee5eb258e5a465
```

The candidate:

- retains sanitized driver context (`failure_stage`, static command label,
  child exit, mode/root identifiers, and presence-only env identifiers) outside
  the disposable run root before cleanup;
- preserves the existing source identity, evidence-presence, selector,
  timeout, browser-lock, graph, pin, and clean-tree controls;
- passes `NORMAL014_USE_BASE_PYTHON=1` to the existing child runner, using the
  already-provisioned read-only venv and avoiding the observed offline pip
  install; and
- retains and propagates nonzero child status while keeping the existing live
  callers and product path unchanged.

No product source, public API, DTO, store, selector, timeout, or shared
dependency changed.

## Safe real-branch diagnostic

I ran the unchanged real source runner and corrected App driver with only two
ephemeral PATH stubs: `npm run build:hosted` and the final Playwright child.
No browser, build, socket, install, central actual, or full suite ran. The
real setup traversed through:

1. App package/source/ancestry/clean/head guards;
2. Agent/Runtime/producer checkout and exact 76-artifact/schema verification;
3. locked graph and Composition 0.0.13 checks;
4. base-Python imports and collection marker;
5. private App overlay and private node graph (`packages=532`, `bins=34`);
6. runtime-lock update and both lock checks; and
7. the existing hosted-build seam, then the existing Playwright seam.

A planted final-child failure returned 97, was retained as `runner_status=97`
with its runner tail, and the driver returned 97. A separate clean stub emitted
the exact required case summary and returned 0; the driver returned 0 with
`runner_status=0`, `request_response_console_summary=true`, and
`source_identity=true`.

The corrected branch's next prerequisite was independently observed before the
base-Python candidate: default private venv setup attempted
`pip install jsonschema>=4.18 referencing>=0.30 PyYAML>=6.0 pytest>=8 pytest-timeout>=2.4`
and failed with DNS/no matching distribution. The base-Python setting is thus
evidence-backed, not a guess.

## Complete prerequisite list

1. Central snapshot tree must equal `a3c82aa9…` and be clean; passed
   historically.
2. Protected keeper must equal HEAD `a304dce0…` / tree `a3c82aa9…`, contain
   `KEEP`, and resolve `node_modules` to `/home/user/work/app/node_modules`;
   passed historically.
3. Exact helper and durable-driver hashes must match; passed historically,
   although the matched driver contained the stale anchor.
4. Driver package/source files must exist; App HEAD must be a descendant of
   the ancestry anchor, clean, and 40 lowercase hex characters. The historical
   run failed exactly at the ancestry item.
5. Driver must create a private run root and runner copy, transform the
   existing source runner, and apply executable permissions; reached by the
   corrected stub run.
6. Child environment must select `final95:parent`, use the existing base
   Python, and pass the private run root; passed in the corrected stub run.
7. Source helper must verify exact Agent/Runtime/producer commits and trees,
   76 artifacts, manifest/schema digests, producer ancestry, and the generated
   import/collection marker; passed in the corrected stub run.
8. Locked graph must be present and immutable/read-only, archive digest
   `895c628a…`, and Composition 0.0.13 bytes `9412ae25…`; passed in the
   corrected stub run.
9. Private App overlay and private node graph must be created without writing
   shared `node_modules`; passed in the corrected stub run.
10. Runtime lock update/check and all pinned generated-file digests must pass;
    passed in the corrected stub run.
11. Existing hosted build must create `dist/index.html`; not executed here,
    replaced at its existing command seam.
12. Existing Playwright command must run with the exact manual-drop selector,
    browser lock, output directory, and timeout; not executed here, replaced at
    its existing child seam.
13. Evidence must be copied outside the disposable root before EXIT cleanup,
    and exact child exit must propagate; candidate failure and clean probes
    passed.

## Callers, scope, and verification

Live suite callers remain unchanged: the existing relative parent rows, the
retained-evidence row, and the two durable driver rows in `suites.conf` (the
historical report identifies lines 34, 42, 105, 106, and 107). The product path
is unchanged:

`TimelineEditorCore.tsx:onDrop` → `useExternalDrop.ts` →
`external-drop-utils.ts:handleFileDrop` → `useAssetManagement.ts:placePreparedAsset`
→ `useTimelineCommandsService.ts:commands.addClip` →
`useTimelineCommandSession.ts` durable parent-media session/outbox.

No actual was retried or requested. Mounted parent behavior remains
unqualified because `26621` never reached it. A future actual needs the
corrected durable wrapper/source candidate, a fresh single authorization, and
the same frozen keeper/source guards.

Exact checks:

- `sh -n tests/e2e/local/support/run-parent-manual-drop-evidence.sh` — PASS.
- `NORMAL014_RECORD_DIR=<private> sh tests/e2e/local/support/run-parent-manual-drop-evidence.sh probe` — PASS; planted exit-73 child stderr/command/exit/provenance retained.
- `git diff --check` — PASS.
- Corrected real-branch diagnostic with build/browser stubs — PASS for setup
  traversal, nonzero propagation, and clean success/provenance; no
  browser/build/socket/install/central actual.
- No full suite was run.
