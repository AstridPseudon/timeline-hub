# M4 Viewing size census report

## Done

- Refreshed the existing Viewing-owned census and cut-plan docs using the
  settled PLAN section 3 boundary and the existing flat manifest.
- Pinned current heads: Composition `5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8`,
  Agent `d0a5072bbe7b7ce9489f43aa0a81027ec400343b`, App
  `20ea14c26526fe4924354f10a177aebbaf6002bc`; baselines are unchanged and
  recorded in the docs.
- Recorded physical and nonblank counts consistently, with bytes and file
  deltas.
- Listed actual merged deletions separately from held D08, D09, and D10 work.
  The dead inspector, App audio-fade helper, App fallback/vendor reductions,
  and App trim subcut are not misreported as new canonical reductions.
- Accounted delivery-note infrastructure outside the census: process-custody /
  PID-reuse guards, short-lived Remotion attempt-temp accounting and owner-root
  cleanup, and retained source-carry/source-identity/verified-source guards.

## Checks

- `node --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-size-census-gate-review-script.mjs` — PASS.
- Read-only manifest recount against the pinned SHAs, using `splitlines()` for
  physical and `strip()` filtering for nonblank — PASS; totals are recorded in
  both docs.
- `git diff --no-index --check /dev/null <updated census doc>` and the same for
  the cut plan — PASS.
- Product tests, builds, installs, browser/socket captures, and full suites —
  NOT RUN (explicitly forbidden by the task).

## Decisions and limits

The prior frozen JSON/script were preserved as historical raw evidence rather
than overwritten. Q1 remains present and uncredited. D08 host/audio parity,
D09 private evaluator/mouth/crop/parity work, and the remaining Agent D10
source-adapter copies remain held. No architecture or feature decision was
changed.

No blocker.
