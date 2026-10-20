# Central test / destructive check-in evidence audit

**Seven physical executions were affected or conservatively uncertain: three cited PASS results and four FAIL results. After-fix evidence now reproduces the Composition and frame-readiness passes once; the cited CPU eight-test replay remains outstanding.** The fourth named failure, `1019223409-31492`, is a **cache hit**, not another physical execution. No product finding or parity failure is inferred from this incident.

This source-only audit covers the Viewing machine from **2026-10-19 19:34Z** through the announced **2026-10-20 03:12Z fix**, plus the already-running frozen successor identified in the task. It inventories **64 result directories: 53 local physical executions (all terminal at the final read), one local cache hit, ten imported MAIN assets** (the initial 63 plus one observed after-fix Composition replay; final snapshot **03:29:22.002480Z**). Every local request, snap, summary, status, exit, log and available runner metadata was read; every saved lead check-in file was read. The JSON contains full IDs, UTC file mtimes, command/tree/external tuple, count basis, actual timestamp/count/error log lines, references, affected check-in IDs, nearest unaffected bounds and required actions. See [machine JSON](central-deletion-evidence-audit.json) and the complete table below. [audit script](central-deletion-evidence-audit.py) reproduces the text audit without submitting tests.

## Time proof and all check-ins

There is **no saved deletion syscall timestamp**. The facts timestamp records an observation; the final log/meta/actions mtime bounds the saved check-in. Conservatively, this audit uses the check-in ID's minute floor through its last saved file. An intersection means **UNCERTAIN affected**, not proof that cleanup deleted that run. This deliberately includes short runs starting after the facts observation because the cleanup instant is not independently bounded. `lead-recover` was instructed to run first, and a separate record reports recovery at 22:34:43, making some later starts plausibly safe; neither record supplies deletion start/end timestamps. Do not silently promote those cases to unaffected.

| Saved check-in ID | Facts date (UTC) | Last saved file (UTC) | Physical executions intersecting conservative envelope |
|---|---|---|---|
| 20261019T2020Z | 20:20:22 | 20:20:58.472254 | Composition 22 PASS; audio-fade 32356 FAIL |
| 20261019T2042Z | 20:42:37 | 20:43:04.127200 | frame readiness 2884 PASS; clock-restart 3208 FAIL |
| 20261019T2132Z | 21:32:58 | 21:34:00.271016 | None |
| 20261019T2234Z | 22:34:45 | 22:36:42.044288 | CPU qualification 19007 PASS; cache service 31492 is separate/nonphysical |
| 20261019T2337Z | 23:37:20 | 23:37:59.668390 | None |
| 20261020T0008Z | 00:08:20 | 00:09:20.200540 | None |
| 20261020T0111Z | 01:11:49 | 01:12:28.106373 | None |
| 20261020T0204Z | 02:04:16 | 02:04:53.856394 | native frame baseline 26386 FAIL |
| 20261020T0235Z | 02:35:24 | 02:36:01.643215 | fixed-schema baseline 21023 FAIL; lead reports live deletion |

These are all nine saved directories under `lead/checkins`. Their `facts.txt:1`, log, meta, prompt, actions and report file metadata are in JSON. There is no saved earlier check-in between handover and 20:20; unsaved recovery invocations cannot be excluded from these artifacts. “Between saved check-ins” is a bounded statement about this inventory, not proof that no other cleanup ever occurred.

Run bounds use the final `snap` mtime and `status mtime − summary duration` as conservative start evidence, final status as end evidence, and actual log outcomes/observations to cross-check. A queued request is **never** an execution start. Most logs do not print wall-clock process start/end lines; this absence is explicit in JSON. Audio `epochMs` observations corroborate active playback but do not define process start. The 02:04 baseline log's first timestamp is a copied **manager grant at 02:04:22.875**, not proof that its process started before the 02:04:33 snapshot. Current running jobs have no claimed end time.

## Affected results, citations and exact next actions

C/P/F/S = collected/passed/failed/skipped. Pytest collected counts below are inferred from complete terminal totals; Playwright/TAP collection is printed explicitly. Full IDs and all exact-ID citations are in JSON.

| Run suffix and family | Conservative UTC execution bounds | C/P/F/S; status | Was it cited for acceptance? | Action |
|---|---|---|---|---|
| Composition `1019202023-13230` | Oct19 20:20:28.176669–20:20:32.276607 | 22/22/0/0 PASS | Yes: Composition 0.0.8 integrated baseline, [2036 escalation:7](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/escalations/closed/viewing-20261019T2036Z-theme-source-and-consumer-ready.md:7). Separate from c04 acceptance. | P1 COMPLETE: after-fix 1020032729-7262 passes63/63, all22 retained. |
| Audio fade `1019201859-32356` | Oct19 20:19:12.604255–20:20:37.604255 | 3/1/2/0 FAIL | No accepted audio gate; partial pass remains RED. | P4 once on current no-primer descendant, record original 3 versus successor 6 coverage. |
| Clock restart `1019204228-3208` | Oct19 20:42:42.563149–20:44:46.563149 | 6/0/6/0 FAIL | No: [worker report:83](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-player-clock-restart/report.md:83) calls it the corrected direct-CDP failed baseline. | Same P4, six unchanged warm/cold expectations; do not revive keepalive/primer variants. |
| Frame readiness `1019204228-2884` | Oct19 20:42:42.744864–20:43:20.744864 | 1/1/0/0 PASS | Yes, **limited readiness only**: [manager round:8767](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/viewing/rounds/20261019T2032Z.log:8767) and historical STATUS update at 8838; export parity explicitly held. | P3 COMPLETE: after-fix readiness1/1, same13 captures/markers, source postflight passed. |
| CPU qualification `1019223448-19007` | Oct19 22:35:01.311113–22:37:22.311113 | 8/8/0/0 PASS | Yes, **backend only**: [viewing-final-route:169](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/viewing-final-route.md:169), [coordination:15](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/viewing-coordination.md:15), [recovery report:30](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-cpu-evidence/REPORT.md:30). | P2 once, exactly eight tests and three retained exports. |
| Native baseline `1020020422-26386` | Oct20 02:04:33.336607–02:05:51.336607 | 4/0/4/0 FAIL | No: all four failed fixture equality before bodies; [schema report:18](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-frame-fixture-schema/REPORT.md:18). Environmental uncertainty is independent of that recorded setup mismatch. | P3 rerun COMPLETE on current reviewed descendant:4 collected/1 pass/3 fail; stays RED. |
| Fixed schema `1020021844-21023` | Oct20 02:18:50.102411–02:37:44.102411 | 4/0/4/0 FAIL | No: catalog404/ACP503 prevented qualification; postflight [actual log:274](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/vw-m3-frame-fixture-schema-e2e-viewing-native-frame-baseline-fixed-1020021844-21023/log.txt:274) shows tracked artifact ENOENT. [Lead admission:448](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/viewing/INBOX.md:448) reports live deletion. | P3 rerun COMPLETE:4 collected/1 pass/3 fail; exact source/graph postflight passed; stays RED. |

**Correction to the named incident list:** `1019223409-31492` has `cached_from=...1019223330-24853`; its summary explicitly says CACHE HIT. The physical source ran **22:33:31.302239–22:33:32.302239**, before the 22:34 check-in envelope, and logged `SyntaxError: expected 'except' or 'finally' block` before collection. The cache was served at 22:34:16; copied log mtime is not execution. Corrected 19007 later ran all eight tests but is conservatively uncertain above. P2 covers the corrected family once; rerunning the obsolete syntax error would add no evidence. This corrects incident provenance without changing any settled product decision.

## Cited passes outside saved overlap bounds

- **f8164bef / Viewing M1 closure:** local `1019230221-8230`, 23:02:22.852538–23:02:32.852538, **4 PASS**, and final `1019230358-21654`, 23:04:08.009229–23:04:18.418939, **4 PASS**. Both fall after the 22:36:42 check-in end and before the 23:37 minute floor. [Final report:31](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m1-ssr-snapshot/REPORT.md:31) identifies the exact portable run; [orchestrator INBOX:303](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/viewing/INBOX.md:303) closes Viewing's M1 items. **No incident rerun required by the saved check-in bounds.** This does not certify global M1 or pixel/audio parity.
- **Decision 0122 / c04ada57 / Composition 0.0.10:** `composition-full-1020014116-11460`, **63 collected / 63 PASS / 0 FAIL / 0 SKIP**, 01:41:29.316645–01:41:33.316645, between 01:12:28 and 02:04. [INBOX:393](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/viewing/INBOX.md:393) approves direction; current STATUS:3 and deletion-ledger.viewing.md D12 cite the actual 63-pass run. **No direct check-in overlap.** P1 was required because the older cited 22-test baseline was uncertain; the fresh after-fix63-pass run now satisfies it, retaining all22 original names. Source package approval did not release held App/Agent consumer pins.
- **Composition 0.0.9:** `1020001557-12697`, **59 PASS**, 00:16:06.065423–00:16:09.492432, after 00:09:20 and before 01:11. No saved overlap; [coordination:5](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/viewing-coordination.md:5) limits this to source package qualification.
- **Host-live 1 PASS:** `1020012754-17587`, 01:27:54.224708–01:28:43.224708, between 01:12:28 and 02:04. Accepted lifecycle/cleanup only, [coordination:15](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/viewing-coordination.md:15). No render/browser/parity claim. Supporting wrapper unit runs **17 PASS** at 00:48 and **19 PASS** at 01:17 are also between check-ins.
- **Audio controls / U1 / T1 / phase:** monitor-control `1019225904-10161` **3 PASS** at 22:59:07–23:00:20; unchanged observed baseline `1020002626-14698` **5 PASS / 1 FAIL** at 00:26:38–00:28:36; U1 `1020011556-27355` **1 PASS** at 01:16:05–01:16:48; T1 `1020015144-17020` **1 FAIL** at 01:51:46–01:52:23; phase `1020025616-18907` **1 FAIL** at 02:56:25–02:57:13. None intersects a saved check-in. [Anchor report:32](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-player-anchor-cause/REPORT.md:32) limits U1 to one diagnostic; [same report:50](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-player-anchor-cause/REPORT.md:50) records failed/retired T1. Six passing WAV comparisons do not turn the original 5/6 RED baseline into six test passes. No incident-induced promotion or retry of retired T1 is justified.
- **Other local passes:** Agent gate **79 PASS / 4 SKIP** at 20:35:22–20:36:22; scene-host plumbing **128 PASS / 4 SKIP** at 21:26:37–21:27:30; frame preflight exits 0 at 00:35:10–00:35:13 without numeric test totals. All are between saved check-ins; skipped counts remain disclosed. Every failed predecessor and every other saved pass is included in the complete table/JSON.

**MAIN assets are not local executions.** Ten directories lack both local request and original log and match hub-exported assets. [hub-sync:94](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/hub-sync:94) exports only `status/exit/summary/ext/snap`, then imports with preserved mtimes at line109. The shared-looking `/home/user/work/...` paths alone cannot identify a host. In particular `app-e2e-m1-gesture-1019211905-11848` is explicitly **MAIN**, 2 PASS, [App coordination:138](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-m1-coordination.md:138); its 21:46 local import mtime is not a Viewing execution time. MAIN full/targeted/outbox and early Composition assets remain in JSON with missing-log uncertainty, rather than invented local bounds. Imported `composition-full-1019193251-22713` is stale queued locally while its current hub summary says cancelled on MAIN because Composition is homed on Viewing. The early Composition targeted cache traces to physical MAIN `1019185121-6767`, not a second execution. Original MAIN owners retain verification responsibility; this audit does not claim their missing logs prove unaffected execution.

## Rerun plan for the orchestrator — no submissions made here

**P1 — COMPLETE once, no further request.** The manager submitted `composition-full-1020032729-7262` with `nocache=1`; this is physical execution, not a cache hit. Actual command `npm test`, c04 tree `9c9a7d3fb03fdffc50741eb2eba64f4cff47cddb`, bounds **2026-10-20T03:27:38.792776+00:00–2026-10-20T03:27:42.792776+00:00**, exit0, **63 collected / 63 PASS / 0 FAIL / 0 SKIP**. All original22 TAP names are present and pass, so old22/22 maps explicitly to new63/63 with **22/22 retained**, zero lost tests. Original and previous63 logs predated the fix; this new run is the valid after-fix replacement. No submission was made by this worker.

**P2 — one corrected CPU eight-test run, currently blocked on safe runner binding.** The old suite hard-codes `/home/user/work/wt/vw-m3-cpu-profile-proof/remotion`, whose worktree is now absent; do **not** blindly request that stale setup. Manager must bind the existing qualified runtime to a reviewed source descendant retaining test blob `70f6dc9c021f0b2888e9281f83bdc7b4ab35c576`, then centrally run:

```sh
/home/user/work/venv-agent/bin/python -m pytest -q -m integration   -o tmp_path_retention_policy=all --basetemp=<new-retained-evidence-dir>   tests/packs/rendering/test_viewing_cpu_export.py
```

Require **8 collected / 8 PASS / 0 SKIP**: absent-install, valid-install, three broken-install cases, and **media-only / text-card / transition-windows** real exports. Retain all MP4/provenance/probe data, original environment/refusal assertions, source equality, Node20.19.4/npm10.8.2/1194 shell, Composition8/93bc and all77 package files and six package/runtime identities before/after. No installs or graph copies are authorized/performed by this audit. Current four-case App run cannot substitute for these eight backend tests. A lower count or a missing export does not reproduce the cited PASS.

**P3 — COMPLETE once; limited readiness reproduced, render/parity remains RED.** Existing `vw-m3-render-route-qualified-prep2-e2e-viewing-render-route-qualified-1020031108-18739` terminated at **03:26:35.320186Z**, exit1: **4 collected / 1 PASS / 3 FAIL / 0 SKIP**. Do not duplicate the incident replay. Its overall run began03:11 before the announced fix; the actual **readiness test started03:16:52.307Z**, duration9317ms, after the fix. The exact test-results JSON and `render-door-route-source-result.json` are retained under that worker; JSON mappings cite both. Source postflight says **passed**, `before == after` including snapshot identity/content and selected source/graph guards; no ENOENT or silent loss of source is accepted.

The passing readiness subcase retains **1 collected / 1 PASS**, **13 native captures** at `[0,37,44,45,52,89,90,120,121,135,143,164,135]`, marker pairs `120→0,121→1,135→15,143→23,164→44,135→15`, five unique video-frame hashes and managed fetch checks. Actual retained evidence is `/tmp/viewing-render-door-route-gYm3M3/player-export-frame-parity-14991-ative-frames-without-export/viewing-parity/fixture-readiness.json`. This reproduces old2884's limited readiness proof afterfix on the reviewed muted/routes descendant, with unchanged selected cases/counts and exact source postflight. It does not require overall four-case success to recognize the separately completed readiness test.

The other three cases (normal Render MP4, positive frame comparison, picture mismatch control) failed because the mounted render action did not finish. Both old four-failure families have therefore been **rerun once** on the current frozen fix descendant: old4/0/4 versus new4/1/3; allfour collected, no skips. Their failed gates remain RED and require separate reviewed diagnosis, not another blind incident retry or old bad-fixture replay. Frozen Agentb70/Runtime9f9 lease2/Compositionc04/installed8/f816 donor and 77-file/six-hash guards are preserved.

**P4 — one current six-case audio baseline run for both affected audio antecedents.** The four-case frozen run has released resources; manager reviews unchanged no-primer `vw-m3-observed-player-baseline`, grants fresh quiet/peer ACKs, and requests centrally once: `$ORCH/bin/request-test vw-m3-observed-player-baseline e2e-viewing-audio-observed-baseline --no-cache`. Its existing setup selects:

```sh
npm exec -- playwright test --config tests/e2e/timeline/player-audio.config.ts   --grep 'amplified fade timing' --repeat-each=3 --workers=1
```

Require **6 collected = 3 warm + 3 first-cold**, disclose pass/fail/skip counts and raw WAVs; preserve unchanged clock/WAV limits, BEFORE-gesture monitor and six-hash/77-byte pre/post guards. Compare original 32356 **3/1/2**, original 3208 **6/0/6**, and later unchanged baseline14698 **6/5/1**. The six-case run expands the earlier three-case attempt; count differences are explicit, not evidence of lost collection. The saved later baseline predates the fix and is not accepted as the after-fix rerun. No obsolete primer/keepalive, T1 worklet, clock patch or threshold changes. A failing repeat stays RED and is not automatically a product finding from the invalid predecessor.

## Validation, limits and handoff

Executed here: `python docs/video-editor/central-deletion-evidence-audit.py` (read-only input audit, writes only this report and JSON); an inline `python -` AST/JSON assertion check (PASS: nine check-ins, 64 records, 53 physical/one cache/ten imports, seven affected with three PASS/four FAIL, all 22 original Composition names retained, correct cache source, completed four-case result and new after-fix mappings); and `git diff --check` (exit 0). **No product tests, full suites, central requests, browser/socket work, installs, copies, service changes or git mutations were performed.** The task's absolute `QUIET.md` path was checked first: it is currently a dangling symlink to missing `managers/viewing/QUIET.md`; GlobalQUIET.md contains a historical 23:59 App install completion. No capture was attempted regardless.

Decisions: keep every ambiguous check-in boundary affected; distinguish cited supporting approval from a held RED gate; distinguish cached/imported assets from physical execution; consolidate reruns only where exact test identities and counts can be compared. Two valid **after-fix** mappings arrived during finalization and are documented above: Composition63 retains original22; readiness1/1 retains all13 captures. Both reproduce once. The cited CPU8 replay and one current six-case audio rerun remain outstanding. No cited pass is yet shown to fail reproduction; the three remaining frame/render failures were previously RED. Escalate a cited PASS only if its valid rerun does not reproduce, per INBOX:458–463.

Blocked: P2 safe runner/source binding; exact historical cleanup instants and original MAIN logs are unavailable. Recommended next step: orchestrator updates manager STATUS with seven affected/uncertain physical runs, cached31492 correction, P1/P3 completed mappings (render/parity still RED), and schedules P2 plus P4 once under reviewed source/quiet controls. No further P1/P3 incident rerun is needed. No settled plan decision was changed.

<!-- BEGIN INVENTORY TABLE -->

The table includes **every one of the 64 saved result directories**, including observed after-fix replacements. Times are UTC conservative execution bounds, not request times. `C/P/F/S` means collected/passed/failed/skipped; `?` is unavailable. Pytest C is inferred from terminal totals unless explicitly logged. Every nonoverlap row also has its nearest preceding/following check-in bounds in `central-deletion-evidence-audit.json`. Imported rows have no defensible local execution window.

| Full run ID | UTC bounds | Status; C/P/F/S | Check-in / disposition |
|---|---|---|---|
| `app-e2e-m1-gesture-1019211905-11848` | —–— | pass; 2/2/0/0 | MAIN import |
| `app-full-1019192621-29082` | —–— | queued; ?/?/?/? | MAIN import |
| `app-m1-client-021-targeted-1019194959-25695` | —–— | pass; 13/13/0/0 | MAIN import |
| `app-m1-client-pin-targeted-1019193214-11027` | —–— | pass; 52/52/0/0 | MAIN import |
| `app-m1-client-review-targeted-1019192223-2934` | —–— | pass; 202/202/0/0 | MAIN import |
| `app-m1-client-review-targeted-1019192312-21089` | —–— | pass; 203/203/0/0 | MAIN import |
| `app-m1-outbox-browser-full-e2e-timeline-1019191816-103` | —–— | pass; 1/1/0/0 | MAIN import |
| `composition-full-1019193251-22713` | —–— | queued; ?/?/?/? | MAIN import |
| `composition-full-1019201848-24783` | 10-19 20:18:57–10-19 20:18:59 | fail; ?/?/?/? | between saved check-ins |
| `composition-full-1019202023-13230` | 10-19 20:20:28–10-19 20:20:32 | pass; 22/22/0/0 | 20261019T2020Z; P1 |
| `composition-full-1020001557-12697` | 10-20 00:16:06–10-20 00:16:09 | pass; 59/59/0/0 | between saved check-ins |
| `composition-full-1020014116-11460` | 10-20 01:41:29–10-20 01:41:33 | pass; 63/63/0/0 | between saved check-ins |
| `composition-full-1020032729-7262` | 10-20 03:27:38–10-20 03:27:42 | pass; 63/63/0/0 | between saved check-ins; P1 |
| `composition-targeted-1019185121-6767` | —–— | pass; 2/2/0/0 | MAIN import |
| `composition-targeted-1019185217-17416` | —–— | pass; 2/2/0/0 | MAIN import |
| `vw-m1-audio-quiet-full-e2e-viewing-audio-quiet-1019200121-24009` | 10-19 20:01:23–10-19 20:11:11 | fail; 6/0/6/0 | between saved check-ins |
| `vw-m1-ssr-snapshot-consumer-integration-ssr-snapshot-1019230221-8230` | 10-19 23:02:22–10-19 23:02:32 | pass; 4/4/0/0 | between saved check-ins |
| `vw-m1-ssr-snapshot-consumer-integration-ssr-snapshot-1019230358-21654` | 10-19 23:04:08–10-19 23:04:18 | pass; 4/4/0/0 | between saved check-ins |
| `vw-m3-agent-gate-targeted-1019203517-26651` | 10-19 20:35:22–10-19 20:36:22 | pass; 83/79/0/4 | between saved check-ins |
| `vw-m3-audio-drain-lifetime-e2e-viewing-audio-drain-lifetime-1019232034-13253` | 10-19 23:20:39–10-19 23:21:35 | fail; 3/0/3/0 | between saved check-ins |
| `vw-m3-audio-fade-e2e-viewing-audio-fade-1019201859-32356` | 10-19 20:19:12–10-19 20:20:37 | fail; 3/1/2/0 | 20261019T2020Z; P4 |
| `vw-m3-audio-monitor-control-e2e-viewing-audio-monitor-control-1019225904-10161` | 10-19 22:59:07–10-19 23:00:20 | pass; 3/3/0/0 | between saved check-ins |
| `vw-m3-audio-phase-physical-prep-e2e-viewing-audio-phase-amplified-1020025616-18907` | 10-20 02:56:25–10-20 02:57:13 | fail; 1/0/1/0 | between saved check-ins |
| `vw-m3-cpu-export-qualified-e2e-viewing-cpu-qualified-1019221442-26979` | 10-19 22:14:43–10-19 22:15:27 | fail; 6/5/1/0 | between saved check-ins |
| `vw-m3-cpu-export-smoke-e2e-viewing-cpu-export-1019214636-5951` | 10-19 21:46:40–10-19 21:47:08 | fail; 6/5/1/0 | between saved check-ins |
| `vw-m3-cpu-export-smoke-e2e-viewing-cpu-export-1019214803-26154` | 10-19 21:48:10–10-19 21:48:48 | fail; 6/5/1/0 | between saved check-ins |
| `vw-m3-cpu-profile-proof-e2e-viewing-cpu-profile-1019223330-24853` | 10-19 22:33:31–10-19 22:33:32 | fail; 0/0/0/0 | between saved check-ins |
| `vw-m3-cpu-profile-proof-e2e-viewing-cpu-profile-1019223409-31492` | —–— | fail; 0/0/0/0 | cache; trace vw-m3-cpu-profile-proof-e2e-viewing-cpu-profile-1019223330-24853; P2 |
| `vw-m3-cpu-profile-proof-e2e-viewing-cpu-profile-1019223448-19007` | 10-19 22:35:01–10-19 22:37:22 | pass; 8/8/0/0 | 20261019T2234Z; P2 |
| `vw-m3-cpu-shell-export-e2e-viewing-cpu-shell-1019222045-2446` | 10-19 22:20:59–10-19 22:21:52 | fail; 6/5/1/0 | between saved check-ins |
| `vw-m3-frame-fixture-restart-e2e-viewing-frame-fixture-1019203528-8996` | 10-19 20:36:27–10-19 20:37:10 | fail; 1/0/1/0 | between saved check-ins |
| `vw-m3-frame-fixture-restart-e2e-viewing-frame-fixture-1019203755-20151` | 10-19 20:37:57–10-19 20:39:19 | fail; 1/0/1/0 | between saved check-ins |
| `vw-m3-frame-fixture-restart-e2e-viewing-frame-fixture-1019204037-5691` | 10-19 20:40:42–10-19 20:41:37 | fail; 1/0/1/0 | between saved check-ins |
| `vw-m3-frame-fixture-restart-e2e-viewing-frame-fixture-1019204228-2884` | 10-19 20:42:42–10-19 20:43:20 | pass; 1/1/0/0 | 20261019T2042Z; P3 |
| `vw-m3-frame-fixture-schema-e2e-viewing-native-frame-baseline-fixed-1020021844-21023` | 10-20 02:18:50–10-20 02:37:44 | fail; 4/0/4/0 | 20261020T0235Z; P3 |
| `vw-m3-frame-harness-fix-e2e-viewing-frame-fixture-1019202445-32716` | 10-19 20:24:46–10-19 20:25:28 | fail; 1/0/1/0 | between saved check-ins |
| `vw-m3-frame-harness-fix-e2e-viewing-frame-fixture-1019202551-26076` | 10-19 20:26:02–10-19 20:26:55 | fail; 1/0/1/0 | between saved check-ins |
| `vw-m3-frame-harness-fix-e2e-viewing-frame-fixture-1019202733-16727` | 10-19 20:27:47–10-19 20:28:31 | fail; 1/0/1/0 | between saved check-ins |
| `vw-m3-frame-harness-fix-e2e-viewing-frame-fixture-1019202835-26360` | 10-19 20:28:47–10-19 20:29:31 | fail; 1/0/1/0 | between saved check-ins |
| `vw-m3-frame-parity-e2e-viewing-frame-parity-1019195636-17453` | 10-19 19:56:43–10-19 19:56:53 | fail; 0/0/0/0 | between saved check-ins |
| `vw-m3-frame-parity-e2e-viewing-frame-parity-1019195720-3494` | 10-19 19:57:28–10-19 19:57:41 | fail; 0/0/0/0 | between saved check-ins |
| `vw-m3-frame-parity-e2e-viewing-frame-parity-1019195801-8323` | 10-19 19:58:04–10-19 20:05:20 | fail; 2/0/2/0 | between saved check-ins |
| `vw-m3-frame-parity-e2e-viewing-frame-parity-1019200601-16506` | 10-19 20:06:08–10-19 20:18:07 | fail; 2/0/2/0 | between saved check-ins |
| `vw-m3-frame-preflight-proof-integration-viewing-frame-preflight-1020003507-5330` | 10-20 00:35:10–10-20 00:35:13 | pass; ?/?/?/? | between saved check-ins |
| `vw-m3-frame-render-baseline-e2e-viewing-native-frame-baseline-1020020422-26386` | 10-20 02:04:33–10-20 02:05:51 | fail; 4/0/4/0 | 20261020T0204Z; P3 |
| `vw-m3-observed-player-baseline-e2e-viewing-audio-observed-baseline-1020002626-14698` | 10-20 00:26:38–10-20 00:28:36 | fail; 6/5/1/0 | between saved check-ins |
| `vw-m3-player-anchor-cause-e2e-viewing-audio-anchor-scout-1020011556-27355` | 10-20 01:16:05–10-20 01:16:48 | pass; 1/1/0/0 | between saved check-ins |
| `vw-m3-player-anchor-cause-e2e-viewing-audio-anchor-tap-qualification-1020015144-17020` | 10-20 01:51:46–10-20 01:52:23 | fail; 1/0/1/0 | between saved check-ins |
| `vw-m3-player-clock-restart-e2e-viewing-audio-fade-1019203451-25358` | 10-19 20:34:52–10-19 20:36:38 | fail; 6/0/6/0 | between saved check-ins |
| `vw-m3-player-clock-restart-e2e-viewing-audio-fade-1019203658-10813` | 10-19 20:37:12–10-19 20:38:38 | fail; 6/3/3/0 | between saved check-ins |
| `vw-m3-player-clock-restart-e2e-viewing-audio-fade-1019203925-31166` | 10-19 20:39:27–10-19 20:40:59 | fail; 6/0/6/0 | between saved check-ins |
| `vw-m3-player-clock-restart-e2e-viewing-audio-fade-1019204228-3208` | 10-19 20:42:42–10-19 20:44:46 | fail; 6/0/6/0 | 20261019T2042Z; P4 |
| `vw-m3-player-clock-restart-e2e-viewing-audio-fade-1019204459-26192` | 10-19 20:45:14–10-19 20:46:51 | fail; 6/5/1/0 | between saved check-ins |
| `vw-m3-player-startup-e2e-viewing-audio-fade-1019220813-26490` | 10-19 22:08:27–10-19 22:09:37 | fail; 6/0/6/0 | between saved check-ins |
| `vw-m3-player-startup-e2e-viewing-audio-fade-1019220955-25613` | 10-19 22:09:57–10-19 22:11:27 | fail; 6/2/4/0 | between saved check-ins |
| `vw-m3-player-startup-e2e-viewing-audio-fade-1019222718-26671` | 10-19 22:27:30–10-19 22:29:03 | fail; 6/4/2/0 | between saved check-ins |
| `vw-m3-player-startup-resume-e2e-viewing-audio-fade-1019224648-8456` | 10-19 22:46:50–10-19 22:48:23 | fail; 6/4/2/0 | between saved check-ins |
| `vw-m3-raw-audio-device-e2e-viewing-audio-platform-1020000534-28429` | 10-20 00:05:47–10-20 00:05:56 | fail; 6/0/6/0 | between saved check-ins |
| `vw-m3-raw-audio-device-e2e-viewing-audio-platform-1020001144-24475` | 10-20 00:11:48–10-20 00:12:26 | fail; 6/3/3/0 | between saved check-ins |
| `vw-m3-real-host-wrapper-integration-viewing-pack-wrapper-unit-1020004822-694` | 10-20 00:48:29–10-20 00:48:31 | pass; 17/17/0/0 | between saved check-ins |
| `vw-m3-render-route-qualified-prep2-e2e-viewing-render-route-qualified-1020031108-18739` | 10-20 03:11:17–10-20 03:26:35 | fail; 4/1/3/0 | between saved check-ins; P3 |
| `vw-m3-scene-host-plumbing-targeted-1019212623-11531` | 10-19 21:26:37–10-19 21:27:30 | pass; 132/128/0/4 | between saved check-ins |
| `vw-m3-viewer-host-live-proof-integration-viewing-host-live-1020012754-17587` | 10-20 01:27:54–10-20 01:28:43 | pass; 1/1/0/0 | between saved check-ins |
| `vw-m3-wrapper-lifecycle-join-integration-viewing-pack-wrapper-unit-1020011737-17212` | 10-20 01:17:50–10-20 01:17:52 | pass; 19/19/0/0 | between saved check-ins |
