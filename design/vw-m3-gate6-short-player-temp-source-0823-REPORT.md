# Gate 6 short Player temp source packet — 0823

## Result

Published the smallest coordination-only handoff for the proven Chrome
`SingletonSocket` path failure. No Composition product source, graph, fixture,
codec, threshold, controller, Runtime DTO, API, store, dependency, or shared
worktree was changed. No central request, helper, Runtime, browser, renderer,
export, localhost, live-socket, or full-suite run was made.

The unapplied patch is
`design/vw-m3-gate6-short-player-temp-source-0823-PATCH.patch`. It updates the
retained 0803 runner source as follows:

1. The future physical namespace is fresh
   `gate6-20261021T0823`; historical `gate6-20261021T0803` and spent physical
   `29863` evidence are not reused or deleted.
2. Before `issue.mjs` allocates the future physical attempt, the packet proves
   the recorded 29863 socket shape is still too long and allocates a fresh
   direct `/tmp/vw-<id>` root with exact-run ownership, mode `0700`, and a
   positive `<108`-byte SingletonSocket witness.
3. The long packet `TMPDIR/TMP/TEMP` stays on the Playwright test process and
   all controller, helper, Runtime, and normal export descendants. The new
   root is passed as `VIEWING_PLAYER_TMPDIR` only to that final Playwright
   invocation; the App test harness validates it and supplies it only in the
   actual launch call:

   `chromium.launch({ args: harness.chromiumArgs, executablePath,
   env: { ...process.env, TMPDIR, TMP, TEMP } })`.

   Thus the normal export continues to reach Agent d0a5072b's internal
   invocation path and accounted `.r-*` attempt scratch. The external Player
   root is not a renderer quota exemption and is never selected by Runtime or
   Agent Root preparation.
4. Postflight evidence remains in the run-owned `PLAYWRIGHT_OUTPUT_DIR`; only
   after the test process returns does ownership-safe cleanup inspect the exact
   `/tmp/vw-<id>` root and remove it. Foreign owners, symlink roots, symlink
   children, wrong mode, wrong basename, and overlong socket witnesses refuse
   cleanup or launch.

The exact fresh packet materialization path for the remaining authorized run
is:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-short-player-temp-source-0823/gate6-20261021T0823`

That path is intentionally unallocated by this task. It must be created only
by the authorized future runner after independent process-custody review.

## Source reasoning and custody handoff

The retained 29863 traces show the actual Chrome launch reached
`harness.ts:292` with the real options `args: harness.chromiumArgs` and the
reviewed Player executable. Chrome constructed a 188-byte path ending in
`com.google.Chrome.tFXWh4/SingletonSocket`, before any case body, media, or
comparison artifact. The patch uses that exact launch seam instead of merely
changing the parent shell's `TMPDIR`.

The Playwright process itself keeps the old long temp root, so Runtime/helper/
export descendants cannot inherit the short directory through ambient process
environment. Agent d0a5072b's existing internal-invocation proof selects the
accounted attempt root and `.r-*` child for normal export scratch. The only
process receiving the short values is Chrome and its browser children from the
launch `env` option.

The pure control source proves:

- a direct `/tmp/vw-<id>`, owner-only `0700` root and positive socket budget;
- the retained long-path shape as a negative witness;
- planted foreign-owner and symlink-root launch refusal;
- planted symlink-child cleanup refusal, followed by successful owned cleanup;
- no cleanup of a root that changes ownership or identity after validation.

No exhaustive matrix or new test framework was introduced. The patch retains
fd9 lock lifetime, diagnostic/physical namespace separation, all 0803 child
markers/env/result/source/graph guards, exclusive issuance, parentfd9 through
cleanup, and the existing preflight/authority boundaries.

## Verification

Passed locally:

```text
python3 -m py_compile design/...-short-player-temp-controls.py — PASS
python3 design/...-short-player-temp-controls.py — PASS
  short-player-temp-controls=PASS
recorded 29863 socket witness — PASS, 188 bytes
positive short witness — PASS, 69 bytes
ownership-safe cleanup — PASS
private packet `patch --dry-run` against retained 0803 runner/frozen harness — PASS
private patched `bash -n` for runner/preflight — PASS
git diff --check — PASS
```

The py_compile bytecode was removed after the check. No build output remains
in the worktree. The future packet's Bash/Node checks, source graph hashes,
foreign-cwd checks, and full old source pins remain to be run by the central
runner from the fresh packet; this worker did not claim them.

## Remaining prerequisite

Independent process-custody review must approve the exact fresh packet and the
App harness launch-env handoff. After that review, the manager may authorize at
most the one remaining physical request using `gate6-20261021T0823`. That run
must preserve the current 0803 evidence and use the same preflight, exclusive
issue, fd9, source/graph, helper, Runtime, export, and postflight controls.
Only that authorized run can establish Player/export frame and PCM parity;
this source packet does not claim those results.
