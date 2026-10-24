# D79 hung-request stack kit

This is a private, non-gating handoff. It does not change Runtime product code, schemas, generated clients, protected tests, or the live test service.

## Files and hashes

- `hung-request-stack.ts` — bounded observer/capture helper. SHA-256 `8fe2114105d7e96d60b5dde40de0d7adb0349a66ffd26438211379f138e45e16`.
- `hung-request-stack.test.ts` — author acceptance controls. SHA-256 `a1ab481f9d06d641f61e56ad8db38438f10a0c245e5bb1ea99391d83a9c761a3`.
- `app-harness.patch` — App `harness.ts`/`app.ts` integration. SHA-256 `979d78418bc607b89d25c6db8b9eeb9bfb3413baccb655c2919d978952bcc87f`.
- `test-run.patch` — optional test-service output routing. SHA-256 `740d2a9e7f7c9e53658c3c74378288e49f2ec2a6f88b8fc135d59d9a7cc9d6d8`.

Install the helper as `tests/e2e/local/support/hung-request-stack.ts` in the normal App checkout, then apply `app-harness.patch`. Apply `test-run.patch` only through the normal test-service publication route; it places `D66_OUTPUT_DIR` under the per-run result directory so the D66 helper evidence is durable.

## Runtime behavior

- A capture starts only from Playwright `request` events that the App harness classifies as its Runtime door path. `response`, `requestfailed`, and `requestfinished` are terminal events; suite elapsed time and output silence are never used.
- The threshold is fixed at 20 seconds. There is no request timeout change, retry, signal, exception masking, or product behavior alteration.
- The harness registers only its supervised Runtime daemon child PID and its `/proc/<pid>/stat` start-time incarnation. The provider is represented by that same daemon PID; no separate provider process is invented.
- At the threshold, availability is inspected once: installed `py-spy` first, then installed `gdb` only when `py-spy` is unavailable. A failed/refused `py-spy` attach never retries with `gdb`.
- Each pending request gets at most one capture. Completion/abort removes the timer; harness teardown aborts remaining observations.
- Raw debugger output is private evidence (`0600`). JSON evidence contains only a safe run/source/ordinal, tool, supervised PID/incarnation, status/reason, and basename/file/line frame summary. Request URLs, bodies, headers, credentials, locals, and debugger errors are not exported.
- Unknown PID, unowned/unsupervised target, incarnation change, missing tool, permission refusal, timeout, debugger failure, and evidence-write failure are recorded or ignored without changing the observed request's semantics.

## Integration modes

The App patch installs an auto Playwright fixture in `support/app.ts`, so normal App journeys get the observer without test-body changes. D66 sets `D79_HUNG_STACK_EVIDENCE_DIR` only for the normal suite stage and uses `D79_HUNG_STACK_RUN_ID` for source/run association. The optional test-run hunk routes D66 output under `$D/d66`.

The Runtime target is available only while the owned daemon child is live. If it exits or its incarnation changes before attach, the helper emits an unavailable marker and does not search `/proc` for replacement processes.

## Verification

See `../evidence/commands.txt`, `kit-test.log`, `kit-tsc.log`, `kit-eslint.log`, and the patch dry-run logs. The author suite is six tests, including fake-clock begin/response/abort/multiple-pending controls, fake debugger subprocess, unknown/unowned/incarnation/missing-tool/dump-failure/permission-failure controls, and an owned Python-child smoke. In this environment `py-spy` is absent and `/usr/bin/gdb` is installed; the smoke therefore exercises the gdb path and records any ptrace refusal truthfully.
