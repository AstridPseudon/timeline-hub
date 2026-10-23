# P3 corrected environment review handoff

## Verdict

**Operational PASS; Gate-5 execution remains BLOCKED.**

The 0419 flat handoff is independently confirmed. The existing
`ap2-P3-gate5-h6-0348` row changed only the two Agent path values from the
0414 env-final row: `ASTRID_CHECKOUT` and the Agent entry in `PYTHONPATH` now
point at `/home/user/work/wt/agt-pin-f894c3c9`. The exact row hash is
`9cdbe46e5862b4a9cd42222e1030d44e5af57b633ecb24ca05b477d91d634c25`.

The isolated Agent is clean at `f894c3c9…`, tree `d24f25a…`; Runtime is clean
at `34eac004…`, tree `98535748…`; full bundle SHA environment values match.
Supported Python imports resolve to those trees. The durable 0407 graph retains
80 official Composition files, the manifest's 73,451-byte archive proof and
SHA-256 `819acf6b…`; no synthetic package roots exist and official Node exports
resolve to `dist/*`. The archive source is absent, so the retained manifest and
unchanged 0414 graph evidence are reused without duplicate archive proof.

The original exact title selector lists exactly one test. No browser, service,
socket, build, body, launcher, or full suite ran; no journey or production-
caller acceptance credit is claimed. Shared dependencies were not installed,
extracted, replaced, or written.

## Remaining blocker

App's 0406 Vite public-export resolver correction is still **BLOCKED**: the
package-root alias intercepts the legitimate generated subpath imports even
though the exact archive exports them from `dist/*.js`. The 0409 assertion
correction and setup failures `19140`/`29980` remain non-body evidence. The
contract §§1/4/7 request/reply/history shape remains unchanged, including full
scope/base, commands, label, step patches/reads, merge and optional reads,
`dry_run`, key, canonical accepted/merged receipts, history/dependencies, and
conflict/invalid/preview forms. The production caller must still be exercised
by the eventual central Gate-5 body run.

Next: App owner fixes and reviews the resolver without shims/fallbacks, then
the orchestrator runs the single exact Gate-5 case against this pinned cohort.
