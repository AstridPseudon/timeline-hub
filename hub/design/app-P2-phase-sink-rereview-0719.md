# P2 phase-sink rereview — FAIL

Reviewed cumulative `f09c357e2aee709b01094824c6c6bdacd9880fb9` against `f7201e02dc53ca7b1e70e38894284528fc78aa70`. Exactly four assigned files differ; no product, protected-original, generated, pin, or source changes.

Finding: D105 is not portable. Its mandatory old-red branch loads the historical harness using fixed Git commit/blob lookups at `scripts/testing/d66-plain-stack.test.mjs:14-15,264-266`. A fresh delivery without pre-squash objects cannot run the normal test successfully. Historical old-red proof may be retained as evidence, but must not gate ordinary test execution.

The phase-sink implementation otherwise passes the required controlled production-caller proof:

- Seed ordinal 1 retains the root sink and evidence.
- Two sequential ordinal-2 starts in the same private output both succeed with separate atomic `launch-*` directories, phase sinks, and `0600` runtime logs.
- Old source: both starts fail closed on sink collision.
- Current source: both starts pass; seed evidence remains preserved.
- Full P2 inventory remains three files/eight cases; each worker-scoped fixture shares `runtime-private`, while each start receives a unique child directory.
- Existing absolute-TMPDIR, symlink, collision, disabled-suite, inherited-environment, source-pin, `0700`/`0600`, `O_EXCL`/`wx`, and no-overwrite guards remain enforced.

Checks:

- Node20 D66: `27 passed, 0 failed`.
- Node20/tsx bootstrap: `1 passed, 2 failed`; both failures match the exact parent’s pre-existing Runtime-helper ABI/environment mismatch. No false all-green claim.
- App TypeScript: PASS.
- Node TypeScript: PASS.
- Scoped ESLint: PASS, 0 warnings.
- Node syntax checks: PASS.
- `git diff --check`: PASS.

No live Runtime/browser/full-suite rerun was performed. Concurrent starts were audited as atomic `mkdir` allocations but not independently executed. The eight original gesture bodies, reload, and undo remain unverified here.

No source correction was made. Recommended next step: remove D105’s runtime dependency on fixed Git history within `scripts/testing/d66-plain-stack.test.mjs`, then rerun this review.