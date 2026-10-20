# MAIN17 / current013: single-parent split source port

Completed source-only on branch `tl/app-m2-main17-parent-split013-source-port`. **Current-tuple qualification remains first; no writer retirement, integration/release approval or Gate 5/6 closure.**

## Exact source

- Assigned base: `cee68b807017efc8669c7d75318cf51aa70ec855`, tree `b2c510ca8893c4d3c238fb042f9ec7e7252edbc0` (MAIN17/root13/public12/cold4).
- Approved source: `tl/app-m2-refreshed-split-source-port`, `f665d5308cc018bc89eff73a5cff21dc8a3bf1b3`, tree `058af3c7a4ebd09ef1c8e18ed13baa8990ae7a5e`, delta against `85efd0ffa5cefc4ba38c63e0fb75e50258c5c28c`.
- Final candidate tree: **`070cd9e6f7d09dec6b8e6d988ba7d3a93b9ea6c9`**. Calculated from base tree entries plus final file bytes using Git's blob/tree hash format, without index/object/ref writes. Harness supplies the final commit.
- Applied only the approved 16 split paths. All 16 are byte-identical to f665; both approved CORS paths already matched and remain unchanged. No old root or source-pin differences imported. Size: **+4,438/-33**, net +4,405; product 10 paths **+626/-33**, net +593; remaining six paths are tests/verifier/golden. `notes/source-audit.json` records complete path hashes.
- All original tracked tests and every path outside this delta remain unchanged. The four fixed-label paths (`trackLabelGesture`, `TrackLabel.command.test`, `TrackLabel`, `useTimelineTrackManagement`), cold-label config/spec/helper, MAIN17 lifecycle/touch, 7M1/server/proxy, render/admission/download and generated surfaces are preserved. No parallel live-local label policy changes were imported or overwritten.

## Behavior and native limits

The approved single raw-parent media cohort uses the existing split ID seam once, before capture/preview. The exact right ID, literal source seconds/window/speed, rational-fps geometry, original reads/selections/bindings/created claims persist through capture/finish/submit, unknown ACK, dependent split/move suffixes and recovery. ACK handling re-executes the original guarded capture, without recapture or ID allocation. Full-row local preview comes from that native execution.

Native eligibility and capture share `parentClipSplitRows`: mismatched/null/invalid/ambiguous mirrors cannot enter native capture. An unsupported input may use its established writer **before** capture; once capture starts, any failure stays visible and cannot fall back to a snapshot. Existing multi/group/occurrence/new-track and unsupported positive paths/writers remain. No DTO ownership field or inferred occurrence ownership was introduced; raw `parent/clip:<id>` binding is required and opaque `app.canonical` is not authority.

Exact Agent **`d8749a9ce12a699672faf3ad96b4e4cbea9245c2`** was archived privately and used via PYTHONPATH, with bytecode/cache writes disabled and shared venv untouched. Native v1 accepts literal registry-backed media with supported windows/hold and exact half-open frame geometry. Mapped, animated, dependent and transition-bearing shapes remain outside this native cut. The fixed Runtime source is **`2c4ac180c2220bdad966bc01e95ad230e99ce26a`**, client **0.2.13 / S2**, unchanged `runtime.lock.json`; all **13 locked files** match that exact producer and manifest. S2 edit-command schema SHA-256 `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef` (22 variants). Public12 tar SHA-256 remains `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`; all **77 private installed files** equal the artifact. Package/lock unchanged.

**Incoming-transition check:** d874 refuses a non-null target transition and any non-null parent-neighbour transition before creating the right row. Differential probes matched those atomic refusals; explicit null was preserved on both halves. No accepted native right-segment incoming-transition counterexample was found in the exercised cohort. No App transition-clearing or reassignment policy was invented; the existing successful transition split writer remains. This does not qualify broader transition support.

## Exact commands and results

CWD for App commands: `/home/user/work/wt/app-m2-main17-parent-split013-source-port`. Define:

```sh
W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-main17-parent-split013-source-port
N="$W/notes"
```

Tests used Node 22.22.0, Vitest 4.1.5, private public Composition 0.0.12, React 18.3.1 and Remotion 4.0.509. Only this worktree's own node_modules link temporarily pointed at `$W/private12/node_modules`. Its scope links borrow read-only dependencies; Composition was extracted privately from the unchanged public12 tar. The original `/home/user/work/app/node_modules` link was restored. Private config imports this worktree's normal test config and puts cacheDir under `$N`; preload only supplies its existing `__dirname` requirement. No shared files/links/caches changed; before/after package/peer/cache audits compare equal.

```sh
node --require "$N/runner.cjs" node_modules/vitest/vitest.mjs run --config "$N/vitest.config.ts" --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism $(cat "$N/targeted-files.txt")
```

**PASS, exit 0: 27 files / 1,295 tests**, 113.57 seconds (`notes/targeted.log`). Exact selection:

```text
src/tools/video-editor/commands/clipSplitCapture.test.ts
src/tools/video-editor/commands/clipSplitGesture.test.ts
src/tools/video-editor/commands/commitSession.split.test.ts
src/tools/video-editor/hooks/useTimelineCommandSession.split.test.tsx
src/tools/video-editor/commands/clipMoveCapture.test.ts
src/tools/video-editor/commands/trackLabelCapture.test.ts
src/tools/video-editor/commands/trackLabelGesture.test.ts
src/tools/video-editor/commands/commitSession.test.ts
src/tools/video-editor/commands/commitOutbox.test.ts
src/tools/video-editor/commands/authoringBundle.test.ts
src/tools/video-editor/commands/authoringBundle.moveOpaque.test.ts
src/tools/video-editor/commands/authoringBundle.sharedOpaqueRemap.test.ts
src/tools/video-editor/commands/semanticGestures.test.ts
src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx
src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx
src/tools/video-editor/hooks/useClipEditing.test.ts
src/tools/video-editor/hooks/useTimelineOps.test.ts
src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts
src/tools/video-editor/hooks/useTimelineState.history-authority.test.tsx
src/tools/video-editor/hooks/useTimelineSave.test.tsx
src/tools/video-editor/hooks/useTimelineTrackManagement.test.ts
src/tools/video-editor/lib/timeline-patch.test.ts
src/tools/video-editor/components/TimelineEditor/TrackLabel.command.test.tsx
src/tools/video-editor/components/TimelineEditor/TrackListRenderer.test.tsx
src/tools/video-editor/components/TimelineEditor/TimelineCanvas.test.tsx
src/tools/video-editor/components/TimelineEditorShellCore.test.tsx
src/tools/video-editor/lib/mobile-interaction-conformance.test.tsx
```

The selection covers native ingress/SDK/session/capture, reserved-ID retry/recovery and after-ACK guards, dependent split/move suffixes, ordinary suffix draft preservation, collection preflight, original group/multi/new-track operations, fixed label remount behavior and MAIN17 shell/touch controls. These are in-process tests; mocked provider calls do not prove HTTP traffic or Runtime acceptance.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$W/agent-d874" /home/user/work/venv-agent/bin/python src/tools/video-editor/commands/fixtures/clip_split_parity.py
```

**PASS, exit 0: 1/1 reviewed native fixture**, complete command/record/authored output/inverse/redo (`notes/native-parity.log`).

```sh
cd "$W/agent-d874"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$W/agent-d874" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_m2_clip_split.py
```

**PASS, exit 0: 80 tests**, 3.79 seconds (`notes/native-tests.log`). This is one targeted native file, not a full suite.

Additional differential probe, from App CWD with the private dependency link in place:

```sh
node --import tsx "$N/native-export.ts"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$W/agent-d874" /home/user/work/venv-agent/bin/python "$N/compare-native.py"
```

**PASS, exit 0: 7/7 cases** (`notes/app-export.log`, `notes/differential-parity.log`). Five accepted cases: reviewed golden, fractional literal source window/speed, null speed/hold, image hold, explicit-null transition. Actual App captures and replay records equal native capture/execution; entire before/after bundles agree; executing the actual App command produces the same complete native immutable document; recorded inverse restores the entire input bundle and redo the entire output. Two non-null transition cases match atomic native refusal. Input documents are retained in `notes/case-documents.json`, sealed/validated by d874, with no manually authored command claims.

Probe development corrected two harness assumptions: mutated fixture documents require new native content digests, and JS JSON serialization erases Python integer/float representation. Re-materializing immutable IDs directly from a serialized preview bundle can therefore produce different digests; production submits commands and native execution owns immutable identities. Final proof compares actual submitted commands through native execution and whole predicted authored bundle values, without claiming App-generated immutable identity equivalence or changing product code.

```sh
node node_modules/eslint/bin/eslint.js $(cat "$N/lint-files.txt") --max-warnings 0
node "$N/test-preservation.cjs"
node scripts/quality/check-known-failures.mjs
python "$N/audit-source.py"
python "$N/audit-deps.py" > "$N/deps-after.json"
cmp "$N/deps-before.json" "$N/deps-after.json"
git diff --check
```

All **PASS, exit 0**. Lint: 14 changed TS/TSX files, zero diagnostics. Preservation: four imported test files byte-identical, **50 callbacks preserved**, all pre-existing tracked tests unchanged. Failure guard: only three existing authorized drag markers; zero forbidden/new markers. Source/pin audit: exact candidate tree/allowlist/public12/013/S2 and protected root paths. Dependency/cache audit equal; whitespace clean. Logs and supporting scripts are retained under this worker's `notes/`.

## Decisions, limits, next real gate

No design deviation or task blocker. No new API/ownership policy, test failure marker, writer deletion or integration mutation. One extra bounded differential probe supplements the approved fixture; no product/test adjustment was needed. An initial Node AST audit subprocess hit sandbox EPERM; the successful audit reads Python-exported `git show` bytes instead. No behavior test failed or was weakened.

**Not run or claimed:** full suite, build, browser, live socket/localhost, tsc/typecheck, install, actual current Runtime acceptance, real reload/process restart, publication-history guarded undo/redo, audiovisual parity or zero legacy HTTP traffic. No full-suite/central browser request made. Shared dependencies/venv and other worktrees untouched; no commit/merge/rebase/checkout/push/ref deletion.

Next: finish current-root/current-tuple qualification first. Then compose the retained split browser source onto the current wrapper/seed and explicit d874/2c4ac/013/public12 tuple (its old config pins 027/4c), register the exact central lane and prove renderer-off gesture acceptance, full immutable parent/config/shot/internal reload, guarded Runtime undo/redo, lost ACK/newer edit/process restart/exact body+key retry without recapture/reallocation, disjoint success/conflict/ABA with draft kept, and zero legacy saves/parent or shot snapshot POSTs throughout. Only the separately qualified supported cohort can justify a later writer cut. Broader writers stay open.

Handoff: `report.md`, `commit-msg`, `DONE`, `KEEP`. KEEP retains this source candidate only; it does not assert runtime/release qualification. No build output or temporary files remain in the worktree.
