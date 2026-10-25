# rt-D77 whole-path guard investigation

Status: READONLY handback. No product source, tests, pins, schema, installer,
stage, npm, render, retirement, or audit action was changed or run by this
worker.

## Settled measured facts

The retained 1237 JSON is internally consistent with the requested arithmetic:

- observed allocated high-water: `1,623,728,128` bytes;
- minimum observed free: `4,393,406,464` bytes;
- shortfall below the unchanged `4,500,000,000` phase floor:
  `4,500,000,000 - 4,393,406,464 = 106,593,536` bytes;
- margin above the unchanged `4,000,000,000` overall stop:
  `4,393,406,464 - 4,000,000,000 = 393,406,464` bytes;
- observed private-phase delta after admission:
  `1,623,728,128 - 437,321,728 = 1,186,406,400` bytes.

The native-fetch interval changed free space from `4,710,780,928` to
`4,393,435,136` bytes and sampled allocation from `1,306,353,664` to
`1,623,699,456` bytes over about `2.024` seconds. The retained JSON reports
`bun install` and `gen:tool-views` exit 0. The ABI probe and Bun link rows are
`exit: 0, cancelled: true`; those are cancellation outcomes, not passing ABI
or link results. The corrected retained status is `cancelled-lower-bound` with
`phase_complete: false`.

The only truthful measurement claim is an observed lower bound for this
partial OMP/Bun phase. It is not an upper bound: native-fetch had no internal
sample, `du`/free samples are not atomic, and filesystem free space can change
concurrently outside the private root. No complete full-stage bound, Remotion
`npm ci` result, stage-fit claim, render result, reserve change, or retirement
recommendation follows.

## Boundary ownership and findings

| Boundary | Source owner / path | Existing observation | Guard finding |
| --- | --- | --- | --- |
| Installer entry and stage | Agent `astrid/installer/core.py:167-170,245-246`; `astrid/installer/backend.py:386-430` | The ordinary caller delegates to `Backend.stage`; retained normal run reached the pinned Python/Runtime/VibeComfy/tool work and stopped at the first OMP source fetch with HTTP 403. | This is the production owner. The source path has no whole-stage disk monitor around `stage`; the prior run is not an OMP/npm success proof. |
| Source/tool archive download and extraction | `astrid/installer/tools.py:101-165,464-510` | `fetch_archive` writes a `.download`, extracts, then removes the archive; `install_tools` invokes it for Bun, Node, media tools, and OMP setup. | These are mutating boundaries. In the authored 1237 wrapper, source extraction and Bun acquisition occurred before the only heavy-phase admission and outside `cmd`; they were not subject to the same bounded monitor. |
| OMP source acquisition / normalization | `astrid/installer/tools.py:334-363` | Normal OMP source path calls `fetch_archive`, then `os.replace`/tree normalization and lock/version checks. | Direct Python download/extract/rename can run without a process monitor. A whole-path guard must own this boundary, including temporary archive and extraction overlap, and must reject before starting when below admission. |
| Bun dependency install | `astrid/installer/tools.py:367-373`; production `Backend.run` `backend.py:43-60` | Retained 1237 diagnostic wrapper monitored the subprocess; `bun install --frozen-lockfile --ignore-scripts --omit optional` exited 0 and preserved the lock hash. | This is the only kind of successful monitored subprocess evidence retained. The production call is still uninstrumented. The wrapper's polling calls recursive `du` and can block the safety loop. |
| Generated tool views | `astrid/installer/tools.py:371-373` | Retained wrapper monitored `bun run gen:tool-views`, exit 0. | It writes the source tree and needs the same pre/post and cancellation ownership as install; exit 0 alone does not certify the surrounding phase. |
| OMP native download/extract | `astrid/installer/tools.py:374-386`; authored wrapper log `:6054` | Retained wrapper called `fetch_archive(NATIVE_URL, ...)` directly between `native-fetch:start` and `native-fetch:end`; no `cmd` sampler ran during the call. | This is the concrete escaped monitor. The exact 2.024-second drop crossed below the phase floor before the next sample. Download temp, extracted archive, and native-file overlap were therefore unguarded. |
| Native file placement | `astrid/installer/tools.py:376-386`; authored wrapper log `:6055-6059` | Retained wrapper used direct `Path.replace` into `packages/natives/native`, then sampled `native-linked`. | The rename/move is a mutating boundary outside the common monitor. It is not a successful ABI/link result. |
| Native ABI probe | `astrid/installer/tools.py:387-393`; authored wrapper log `:6060` | Retained JSON: `exit: 0, cancelled: true`; it started at `4,393,435,136` bytes free, already below `4.5 GB`. | Cancellation and exit 0 must be classified as incomplete. No ABI completion or native compatibility claim is supported. |
| Bun link | `astrid/installer/tools.py:394-396`; authored wrapper log `:6060` | Retained JSON: `exit: 0, cancelled: true`; it started below floor and ended at the observed lower-bound high-water. | The caller launched a post-cancel command. No link completion is supported; cancellation must terminate the phase and prevent this next command. |
| Remotion npm phase | Production `astrid/installer/backend.py:62-75,415-416`; standalone gate `scripts/reshape/remotion_gate.py:123-207` | No `npm ci` was run in 1237 because OMP did not complete and fresh admission was unavailable. | Production `Backend.run` uses uninstrumented `subprocess.run`; the later `node_modules`/marker writes need a fresh admission and the same monitor. This remains unknown, not success or failure. |
| Post-npm stage writes | `astrid/installer/backend.py:417-430` | No complete stage reached. | Service declaration, profile, version, and manifest writes are outside this partial measurement and cannot be included in a full-stage bound. |

## Wrapper-specific failure sequence

The authored wrapper in the retained 1237 log has these control defects:

1. `sample()` performs recursive `du -B1 -s` over the phase root and archive,
   then `cmd()` calls `free()` again. The critical poll therefore blocks on
   recursive traversal and duplicates work; `du` cannot be the safety decision
   path. It also does not give an atomic pair with whole-filesystem free space.
2. `fetch_archive` for native materialization is called inline, not through
   `cmd()`. The monitor is absent for the entire native download/extract
   interval, which is where the measured floor crossing occurred.
3. `cmd()` accepts any nonzero cancellation outcome and returns a row even when
   cancellation happened. The caller does not inspect the returned
   `cancelled` flag, so it invokes ABI probe and then Bun link after cancellation.
4. If a child exits before the loop's first poll, only the post-exit sample is
   available. A fast mutator can cross the floor without a live cancellation;
   the post-sample must still classify the boundary unsafe/incomplete.
5. Admission is checked only after source extraction and Bun setup, rather than
   before every mutating boundary. A pre-existing low-space case can therefore
   mutate before being classified as blocked.
6. `status = 'complete'` is assigned unconditionally after the ABI and link
   calls. Since both returned `exit: 0, cancelled: true`, the authored result
   falsely claimed completion. The retained correction to
   `cancelled-lower-bound`/`phase_complete: false` is the only honest status.

## Minimal finite guard requirements

These are bounded controls for the source repair owner, not a product/API
change:

- One guard must own every mutating boundary in the path, including direct
  archive download, extraction, rename/move, Bun commands, native materialization
  and Remotion `npm ci`. No inline `fetch_archive` or post-command write may
  escape it.
- Before each boundary, perform a cheap, nonrecursive free-space admission
  check. Keep recursive `du`/allocation accounting out of the critical poll;
  collect it separately and bounded, or after the boundary. Do not treat a
  delayed `du` result as live safety state.
- Preserve the existing decimal thresholds: fresh heavy admission strictly
  above `5,200,000,000`; phase cancellation before the `4,500,000,000` floor;
  overall stop at `4,000,000,000`. A finite poll interval alone cannot prove an
  upper bound unless the unobserved write/download chunk is itself bounded or
  checked at a controlled write seam.
- For subprocess work, use the existing normal owned-process-group cancellation
  seam, with bounded wait/cleanup. On cancellation, mark the current phase
  terminal, prevent all subsequent commands, and retain the trigger and final
  free/allocated samples. Do not use a global kill or invent a new service.
- For direct Python mutators, either move the operation behind the same bounded
  callback seam or return a supported cancellation point before it starts. A
  monitor around only `Popen` cannot guard a synchronous download/extract.
- Treat a child exit before the first poll as a completed observation requiring
  a post-boundary check, not as proof that the boundary was safe. Any post-check
  below floor is incomplete/unsafe even with exit 0.
- Define completion as all expected boundaries observed and successful, no
  cancellation, no floor violation, integrity checks passed, and final phase
  admission still valid. `exit == 0` is never sufficient by itself.
- Finite stub controls must cover: fast download-like growth, a slow/blocking
  allocation measurement, pre-existing low space, child exit before polling,
  child cleanup and cancellation propagation, and an all-steps success path.
  These controls can use stubs; no real disk-filling or heavy phase is needed.

## Scope and handback

The parallel Sol guard-repair worker had no finished source/evidence artifact at
the time of this review, so there is no candidate hash or control result to
consume and no source PASS is asserted. The 12:25 targets remain held. The
ordinary installer, C0 request/reply shape, product scope, and contract remain
unchanged. No audit, retirement, retry, source reacquisition, npm, stage, or
render action is recommended from this partial scope.

