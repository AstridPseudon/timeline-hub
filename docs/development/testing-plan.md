# TESTS: tests that tell us the truth (Astrid · Runtime · App)

> The cross-repo testing plan for Astrid, the workspace Runtime and the App (astrid-app). It lives here because Astrid hosts the journeys (`astrid dev journey`, see `journeys.md`).

A standalone plan in Megado format: cards with size, route, inputs, outputs and "Done when". It is not run inside Otto.

**Revision 4, 16 Oct 2026.** Revision 3 (15 Oct) set the shape: three layers, producer-owned manifests, and real journeys. Revision 4 keeps that shape and changes what didn't hold up:
- **The Checkpoint B criterion "the owner watches the film" is now an automated check.** Playback is proved by preview parity and a revision marker (F2.4).
- **The quarantine cap now applies to the end state, not day one.** `known_failures` only shrinks, and the cap of 10 applies once each burn-down card is done.
- **The smoke can build a generated mini-realm** (`--reference generated`), so it needs no copy of the real film. It still runs only on macOS until the Runtime launcher has a Linux custody provider (Owned debt); the real film stays the release gate.
- **Old checks are deleted only after their replacement exists.** Runtime's i06 and activation join moved from U4 to TIDY.
- **The plan's end state no longer depends on Otto tooling.** "`otto-heavy` flags leftovers" is out.
- **Thirteen cards became nine**, each with explicit inputs, so the waves can be scheduled mechanically.
- **The "where we are" numbers were re-measured** on 16 Oct in a clean Linux container.
- **New: how the plan is executed** (waves and model tiers).

**The owner's yardstick (15 Oct):**
- No arbitrary time constraints. Durations are recorded and never judged. Only a genuine hang fails.
- What counts: tests that are robust and thorough, assert meaningful behaviour, and do it as elegantly as possible.
- Not excessive: a test earns its place by catching a failure nothing else catches. Fewer, truer tests beat more tests.

## Status (16 Oct 2026, end of the first execution run)

| Card | State | Evidence |
|---|---|---|
| LEAK | **Done** | Both suites reap their process groups and fail a session that leaks file descriptors (`tests/lanes.py`). |
| UA (Astrid) | **Open: green apart from owned known failures** | <!-- ASTRID-FINAL --> |
| UR (Runtime) | **Done** | Default run 1,928 passed, 4 known failures, 0 red (was 88 failed, 2 collection errors). |
| UP (App) | **Done** | Default run 19,050+ passed, 7 known-failure entries (was 264 failed). <!-- APP-FINAL --> |
| C1 | **Done except C1.3** | `artifacts.json` in Runtime and Astrid; vendor locks in the App (4) and Astrid (3), checked locally per push and against the producer's main in a boundary job. C1.3 (timeline packages) is owned debt. |
| C2 | **Done** | Nine responses recorded from a real daemon; the App's and Astrid's parsers, conflict classifiers and fakes are held to them; the paired relay is checked against every call the App makes. |
| F1 | **Built, not run end to end** | Generated reference, `--backend`, env scrubbing, disk preflight, revision set, killed-task read-back, `runtime_restart`; 82 plumbing tests. The run needs macOS (Owned debt). |
| F2 | **Thin slice built on the direct path**; passed 3 of 3 consecutive local runs on this container (Linux, one worker, about 51 s each) | Cases 1-3 in `astrid-app/tests/e2e/local/three-products.spec.ts` (agent → open App; concurrent edit; Runtime restart), Astrid side `astrid/core/dev/cross_client.py`, nightly job `three-products` in `astrid-app/.github/workflows/direct-journey.yml`. Steps 3, 4 and 6 blocked (Owned debt: Remotion gate and Linux custody); relay variant after Plan B M0. |
| TIDY | **Done where R-1 allows** | Homes written, then deleted: Astrid's m4/m7/m8 gates and artifacts, the CI mirror (`run_ci_checks.sh`, its 25-minute self-test, the sandbox test), the stage-1 cross-repo acceptance and cold-launch matrix (real-daemon homes in `test_runtime_client_cutover.py`), the VLM gate and dead files; Runtime's i06 proof; the App's real-bridge harness (new tests for recovery retry, promote and duplicate failure toasts, the watchdog banner; the network audit in every timeline spec) and the bridge-latency gate. Kept with their unblock tests: see Owned debt. |

**Product bugs the tests found and fixed on the way (R-13):**
- the training pack's schema root;
- the hype arrangement rules lost in 71d43e00 (editorial arrange and refine, video_editing cut failed at import);
- `understanding.understand` lost its mode choices and per-mode required inputs in the same port;
- the generation-publication CLI still looked for `executor_root`, which schema-v3 capabilities no longer carry;
- h3_av verified protected pixels through a different RGB conversion than it composed them with, so any yuv420p source failed verification;
- Ctrl+C cleanup had a 1 s floor that a busy host's census overran (now 5 s, a cap, not a wait);
- the first-party pack list; `pixel.strip` had no capability-matrix row; three bare env-var strings;
- the stale Runtime TypeScript conformance client;
- the App reading only the old nested Runtime error body and misreading a 422 as an unavailable capability;
- four doc commands that did not exist;
- the CI rewrite had dropped Astrid's release-wheel job (restored).

**Test-system fixes on the way:** a vendor-lock boundary check now fails only when a vendored file changed (a version-only producer change was failing every consumer); running one test from a file with a known failure no longer trips the stale-entry check; the App's theme test pins the clock (the theme follows the time of day).

## End state (what "done" means)

When this plan is finished, these statements are true. Each one is checkable.

1. **One honest answer per repo.**
   - A plain default run is green in CI, on every push.
   - Red means something is broken; there is no "normal red".
   - At most 10 quarantines per repo, each owned and expiring.
   - Every test runs in a lane with a recorded result. The union of the lanes equals the collected suite.
2. **No copy between the products can drift unnoticed.** Each copy is checked by **artifact digest** against a producer-owned manifest, so a one-byte change fails the consumer. There are three producers:
   - **Runtime**: clients, schemas, fixtures, and real-daemon response fixtures.
   - **Astrid**: its CLI command surface, its elements catalog, and the `astrid-browser` source the App vendors.
   - **The timeline packages**: schema and composition, including transitive copies.

   Every journey records the exact revision set it tested:
   - the Astrid, Runtime and App heads;
   - the manifest versions;
   - the vendored commits.
3. **The human-and-agent workflow is proven for real.**
   - **`smoke`** (Astrid + Runtime) runs on any Linux or macOS machine against a generated mini-realm, and against a clone of the real film on the reference machine. It proves:
     - host start;
     - a render admitted the way the App admits it;
     - host replacement after a code change;
     - a crash mid-render, with orphans reaped and the killed task ending in a defined state;
     - a Runtime restart under a live host.
   - **`full`** (all three, through the topology beta users run: the App on its Workspace v1 provider → paired relay → connector → Runtime) proves:
     - an agent publish shows up in the open App;
     - a concurrent human/agent edit loses nothing;
     - the App's own render action renders exactly the accepted revision;
     - the rendered film plays through the relay, matches the preview, and has sound;
     - the App survives a Runtime restart without losing its draft.
4. **Every red names its cause:**
   - the layer and the phase;
   - a hang is stopped and named as a hang;
   - a provider failure (Codex or the image model) is kept apart from a product failure.
5. **Each check runs where it belongs, once:**
   - hosted CI runs the local and boundary layers per push;
   - the smoke runs before merges that touch R-11's paths, and at each release;
   - `full` runs at each integration point and release;
   - no render or journey runs in hosted CI per push.
6. **Less than today:**
   - the ~10 proof and gate mechanisms (including the App's retired `astrid serve` harness) reduce to the journeys;
   - each of their useful assertions has a named new home;
   - fakes are trusted only for what real-daemon fixtures verify;
   - no new framework.
7. **Test runs don't harm the machine.** Every suite reaps the daemons and hosts it started. It fails if it leaves processes or file descriptors behind.

## Layers

1. **Local behaviour** (per repo, every push). Everything deterministic that needs no second repo, real host, renderer or network, including filesystem, database and component tests.
2. **Boundary compatibility** (every push to a consumer, and whenever a producer's manifest changes):
   - digests against producer manifests;
   - consumers' parsers and fakes run against **real-daemon response fixtures**;
   - the paired relay's route table is checked against every call the App actually makes.

   This proves fidelity to a pinned producer version, not compatibility with every future push.
3. **Real journeys** (`astrid dev journey --tier smoke|full`). `full` includes `smoke`.

When all three layers are green, the main things work together. When one is red, it says which thing is broken.

## Where we are (evidence)

Re-measured 16 Oct 2026 in a clean Linux container (4 cores, Python 3.11, Node 22), at Astrid `54095b4`, Runtime `9780b59` and App `c986308`.

| | Astrid | Runtime | App |
|---|---|---|---|
| Collected | 11,887 tests | 1,944 tests | 19,081 tests (4,532 suites) |
| Collection errors | 29 files | 1 file (i06), plus 4 more from undeclared test deps (`jsonschema`, `PyYAML`) | — |
| Red in a full run | ~850 (one full pass, 16 Oct; ~600 triaged so far) | **88 failed / 1,853 passed** | **264 failed / 18,815 passed** (95 files) |
| Main cause of the reds | Tests not updated for 71d43e00 (packs moved `executors/` → `actions/`, schema v3 `pack.yaml`) | Tests not updated for 9ba7b1c (task-spec dedup) and 9d2b5df (remote activation order) | Mocks and fixtures drifted from the product's current exports |
| Real product bugs found | training schemas root missing; editorial `arrange` imports a removed function; first-party pack list stale; custody race on Linux | remote-worker drain broken by merge 5053297; TS conformance client stale against the contract | pack commands use the retired task envelope; seam admission refuses popup edits; recovery draft dropped by the poll gate; 22 ungoverned SDK exports |
| Tests that rewrite tracked files | `remotion/src/types.generated.ts` | `egg-info/SOURCES.txt`, the generator test | — |

**Progress (16 Oct):** Runtime's default run is green (1,914 passed, 3 known failures). The App's default run is green apart from tests that were timing out under load, which are now fixed (19,050 passed, 7 known-failure entries). Astrid is in progress.

**Copies between the products (15 Oct, checked):**
- Astrid's Python client exactly matches Runtime's, but by hand-copied hashes.
- **The App's `generated.ts` has drifted.**
  - `publishParentComposition` accepts `[200, 201]`; the server always returns 200.
  - The App's guard checks only `SCHEMA_DIGEST` and runs in no CI.
- Runtime's `contract/manifest.json`:
  - lists paths, with no digests and no version;
  - omits the visual fixture and the conformance YAML.
- `component-manifest.json`'s fixture digests are placeholders (`aaaa…`).
- Runtime has two differing TS clients: `packages/typescript` and `clients/typescript`.
- The TS "generator" patches its own committed output.
- The conformance YAML says PATCH 1→2, while the actor publishes a composition revision.
- Timeline-schema exists in three versions:
  - Astrid's Python pin (ArtAgents `242f9c43`, which is Astrid's own history under its old name);
  - **0.0.1**, transitively, in Astrid's Remotion lock;
  - the App's vendored 0.0.2.

  Composition is 0.0.6 versus 0.0.2, and Remotion 4.0.509 versus 4.0.503.
- The App vendors `astrid-browser` from Astrid `06dee36` (25 Sep), and nothing checks it.
- **The App's agent prompt tells the agent to use `timelines retime-clip`, which Astrid removed** (0bd37792).
- Five Astrid test files pin Runtime `afccb430` in a sibling checkout that doesn't exist.

**Live interaction bugs found by the reviews.** These were fixed *before* this plan started, each with a red→green test, and merged to main on 15 Oct 2026 (Astrid 42eca1d7, Runtime ec18217, App 295670ca4). This plan is testing only. Its cards keep those behaviours covered.

| ID | Bug | Where | Kept fixed by |
|---|---|---|---|
| B1 | The paired relay's allowlist rejects `…/timelines/{id}/composition-revisions` and `…/inspect` (and `/v1/capabilities` on the Runtime side). Paired-mode saves likely fail. | `astrid-app/config/vite/pairedRoutePolicy.ts` | C2.3, F2 |
| B2 | The ACP prompt names the removed `retime-clip` command. | `astridAcpLauncher.ts` | C1.2 |
| B3 | The App classifies conflicts by regex on the message. The App's fakes send codes the Runtime never sends. | `client.ts:146`, `fakeBridgeRouter.ts:684` | C2 fixtures |
| B4 | An expired lease is reaped only inside a claim. A crashed render stays `running`, and the App's render poll spins forever. | Runtime `store.py:3368`; App `useRenderState.ts:776` | UR.6, F1.2 |
| B5 | After a Runtime restart, the pack host keeps a sticky fence and refuses to re-register until an Astrid client opens. App-started renders then never run. | `generic_host.py:6015` | F1.3 |
| B6 | The App's `generated.ts` accepts `[200, 201]` for `publishParentComposition`; the server only returns 200. | App `generated.ts` | C1.4 (regenerated, then digest-pinned) |

**Duplication:**
- Fakes: ~20 Runtime fakes in Astrid, and ~9 in the App. The App's main fake imitates the retired Astrid bridge.
- ≥6 host-launch fixture families.
- ≥5 ways to locate the other repo.
- Proof and gate mechanisms:
  - in Astrid: the dev journey; s1/m4/m7/m8; stage1 acceptance; iteration e2e; tests/proofs; evals/timeline; the VLM gate; smoke_*.sh;
  - in Runtime: i06 and the activation join;
  - in the App: `verify-paired-release-e2e` and `REAL_BRIDGE`.

## Rulings

| # | Ruling |
|---|---|
| **R-1** | Three layers only. Nothing else gates a merge or a release. Other harnesses are folded in or deleted, and only after each useful assertion has a named new home. |
| **R-2** | The default run leaves out tests that need a pack host or other long-lived subprocess, Node, ffmpeg or Remotion, native macOS, the network, or a second checkout. They are marked `integration`, `darwin_native` or `live`, and run in a recorded nightly lane. **The nightly lane obeys R-6 like any other lane**: its reds are owned and expiring, never ambient. |
| **R-3** | Each producer (Runtime, Astrid, the timeline packages) owns a versioned manifest of artifact **digests**. Consumers vendor by script and check digests, never hand-copied hashes or version strings. |
| **R-4** | A fake is trusted only for operations whose real-daemon responses (including errors) it reproduces from recorded fixtures. Anything else fails loudly. No universal fake. |
| **R-5** | Runtime never imports Astrid or the App. Cross-product tests live in the consumer and record the producer versions. |
| **R-6** | Red is never normal, and never accepted: a failing test is fixed (or, if it measures the wrong thing, corrected), never listed, xfailed or skipped. There is no known-failures list (removed 18 Oct 2026). An import or collection error fails the run. |
| **R-7** | Delete before adding. A test pinned to a removed design is deleted, with a `removed.yaml` line, not fixed. No new framework. A test of a deliberately *changed* design is updated to assert the new behaviour. |
| **R-13** | **Small product fixes ride with the test that exposes them.** The plan is testing-only, but a test that exposes a small, unambiguous product defect (a wrong path, a stale generated file, a broken import) gets the fix in the same commit. Anything larger becomes a known failure with an owner and a reason naming file:line. |
| **R-8** | Tests assert behaviour and identity, not private attributes or proxies. Examples: "the output is revision R", not "a render finished"; "the killed task ended in state X", not "the next render works". |
| **R-9** | Every suite reaps what it starts and fails on leftovers. Required lanes fail when prerequisites are missing. Heavy local runs go through `otto-heavy` when it is present; nothing requires it. |
| **R-10** | Every journey phase reports success, failure or hung, with its duration and the machine load. Durations never fail a run. Hang ceilings are many times the usual duration. Provider failures are reported separately and never replaced by a fixture. |
| **R-11** | **When journeys run.** Every merge runs the affected local and boundary checks. The smoke also runs before a merge that touches any of:<ul><li>Astrid `astrid/core/execution/{process_group,custody_broker,task_scope,generic_host*}.py`, `astrid/sdk/{autobootstrap,host_bootstrap,workspace_client}.py`, `astrid/packs/rendering/**` or `remotion/**`;</li><li>Runtime `runtime_protocol/**` or `astrid_runtime/**`.</li></ul>The thin `full` runs before a merge that touches the App's `src/integrations/runtime/**`, `renderRouter.ts`, `useTimelineSave.ts`, `usePollSync.ts`, `config/vite/paired*` or the connector. Both run at each integration point and release. |
| **R-12** | **One pre-push command per repo** (`scripts/check-before-push`, a small script, not a framework). It runs the default run and, when R-11's paths changed, the smoke, **locally**. That local smoke is the "before merge" check of R-11; hosted CI never runs it. A push to main without it is not done. |

## Cards

Sizes are rough focused days, for ordering only. **In** names the cards whose outputs a card needs; a card with no inputs can start at once. Route is normal or xhard.

### LEAK: test runs clean up after themselves
`1 d · normal · in: — · out: U#no-leaks` · **partly done 15 Oct**
**Done when:**
1. ✅ Astrid and Runtime suites own and reap every daemon and host process group, and fail on leftovers (Astrid 390e6679 + a6e7bd40; Runtime 66751d7 + dd57fe2).
2. A session-end check compares open file descriptors and rooted processes with the start, in both suites, and fails on growth.

### UA: Astrid honest and green (with its CI)
`4 d · normal · in: — · out: U#green-astrid, CI#astrid`
**Done when:**
1. **CI that can pass.** The frozen m4/m7/m8 jobs, the Runtime pin `a278cd46` and the duplicate suite run are gone. One unit job runs the default run, with the cheap static gates (`make structure ruff mypy cycles`) as steps. (r4 GREEN's `make doc-refs` does not exist; its documentation checks join those gates when written.) `scripts/check-before-push` exists.
2. **Dependencies resolve.** `pip install -e '.[dev]'` works in a clean environment. The timeline-schema pin points at a reachable source (today it names `banodoco/ArtAgents@242f9c43`, which `uv` cannot fetch).
3. **Collection is honest.** Collection-time side effects move into fixtures. One `runtime_checkout` fixture replaces the five locators and the `afccb430` / `70e269bc` pins. Collection has zero errors: each erroring file is deleted (with a `removed.yaml` line) or repaired. No test listed by r4 GREEN item 6 as "never obsolete" is deleted.
4. **Lanes are complete.** The union of the default, nightly and journey lanes equals the collected suite, checked by a test.
5. **Green.** Every failure is fixed, moved to the right lane, or put in `known_failures`, with at most 10 at close. `xfail_strict` is on, and no test is weakened without a reason in its commit.

### UR: Runtime honest and green
`2 d · normal · in: — · out: U#green-runtime, CI#runtime`
**Done when:**
1. Test dependencies are declared (`jsonschema` and `PyYAML` are imported by tests but not declared), so a clean `pip install -e '.[test]'` collects the whole suite.
2. Every current red is dispositioned.
3. Tests stop rewriting committed files: `test_generated_client.py:707`, and whatever regenerates `astrid_runtime.egg-info/SOURCES.txt` (better: stop committing `egg-info`).
4. A generous per-test hang guard is set (hangs only).
5. Runtime's first workflow runs the default run, plus `test_second_client_e2e.py` as a boundary job with an npm cache. `scripts/check-before-push` exists.
6. A test keeps B4 fixed: an expired lease with no new claim ends in its defined state.

### UP: App honest and green
`2 d · normal · in: — · out: U#green-app, CI#app`
**Done when:**
1. vitest is measured and gets a per-push workflow. `scripts/check-before-push` exists.
2. The default run needs no Astrid checkout. Today the vitest config fails to load without `ASTRID_CHECKOUT`, because the vendored `astrid-browser` lacks `tools/catalog.json` and the `video_editing` pack.
3. Tests that reach into another repo (`astridSceneAuthoring`, `localExtensions.catalog`, `portableVisualSeamIntent`) move to the checkout lane, or the producer runs them itself (R-5).
4. Every red is fixed or put in `known_failures`. Known today: the load-dependent flakes in `astridAcpBridge.test.ts`, `PublicAstridSite.lifecycle` and `AgentChat.projectContract`, and `shotCompositionRuntime.test.ts`, whose handshake fixture no longer matches the product connector role.
5. Stub-bridge and real-bridge tests are separated. `bridge-latency.yml`'s expected red is gone.

### C1: three producers, checked by digest
`2.5 d · normal · in: UA, UR, UP · out: C#manifest`
**Done when:**
1. **Runtime** `contract/manifest.json` has a version and digests for the openapi, the schemas, **the one named canonical TS client**, the Python client, the visual fixture and the conformance YAML. The placeholder digests in `component-manifest.json` are real. The conformance YAML's PATCH step matches what the actor does. Runtime CI runs `generate.py --check`.
2. **Astrid** publishes a manifest by script (with `--check`) of its CLI command and flag surface, the editor/elements catalog, and the `astrid-browser` sources the App vendors. An App test asserts every `astrid-tools …` command in the ACP prompt exists in it. That keeps B2 fixed.
3. **Timeline packages:** Astrid and the App check the effective schema and composition artifacts by digest, including the transitive 0.0.1 in Astrid's Remotion lock.
4. Astrid and the App vendor by one script each and record the manifest versions. The hand-copied hashes are deleted. The App's `generated.ts` is regenerated (B6).
5. A planted one-byte change fails each consumer.

### C2: fakes verified by real-daemon fixtures, and the relay route table
`2 d · xhard: every unit test that uses a fake trusts it · in: C1 · out: C#fake`
**Done when:**
1. The existing real-daemon actor records response fixtures, digested in Runtime's manifest: the publish 409 body; task admission; task read; managed outputs; an events page that crosses a page boundary.
2. The App's zod parsers (`src/integrations/astrid/*Routes.ts`), the App's `isRuntimeConflict` and the Python fake each accept exactly those fixtures. Unsupported operations fail loudly.
3. **The paired relay's route table** is checked against every method, path and header the App's providers call (positive), and the forbidden routes are kept (negative). That keeps B1 fixed.
4. Other fakes move over when their file is next touched.

### F1: smoke, the real Astrid + Runtime contract
`2.5 d · normal · in: UA, UR · out: F#smoke`
**Already in `astrid dev journey`:** host start, renders, outdated-host replacement, survives a heavy job, PATH reuse, `kill -9` idle and mid-render with orphan reap, a Node preflight, recorded durations, generous hang ceilings, failures that show stdout and stderr.

**Done when:**
1. **Portable.** `--reference generated` builds a mini-realm (a few seconds of ffmpeg test media, one timeline) so the smoke runs on any Linux or macOS machine, including a cloud container. The real-film reference stays the release run. It runs from a disposable worktree of HEAD, never editing the shared checkout.
2. **The killed task is read back from the Runtime:** it carries `task.lease_expired`, it ends in one defined state, and a stale attempt's publication is rejected.
3. **New phase `runtime_restart`:** restart the Runtime under an idle host, then admit an excerpt render **through `POST /v1/tasks` in the App's request shape**, with no Astrid client open. It completes. That keeps B5 fixed.
4. The summary records the revision set: the Astrid HEAD, the imported `runtime_protocol` checkout and its HEAD, the App HEAD, and the manifest versions.
5. Preflight checks free disk against the Runtime's free-space floor (4 GiB) plus the expected render scratch, and refuses to start without that headroom.
6. Unit fixtures prove each outcome kind (success, failure, hung). The journey takes GATE item 5's scenario registry, so r4 cards can add scenarios.

### F2: full, all three products through the shipping topology (thin first)
**Related:** the App's same-machine direct path (hosted page → loopback gateway → local Runtime) has its own journey, `astrid-app/tests/e2e/local/direct-journey.spec.ts`, run by Plan A (`astrid-app/tasks/2026-10-16-plan-a-same-machine-direct.md`). F2's thin slice runs on that direct path; the cross-device relay variant (card F2-L1) comes after Plan B M0.

`4 d · xhard: the only test across all three · in: F1, C1, C2 · out: F#full`
**Built, thin slice on the direct path.** The I09 handoff case it started from (`astrid-app/tests/e2e/release/paired-repository.spec.ts`) is deleted: its assertions now live in cases 1-3 of `astrid-app/tests/e2e/local/three-products.spec.ts`. The Astrid side is `astrid/core/dev/cross_client.py` (`identity`, `host`), and the shared helpers are in `astrid-app/tests/e2e/local/support/`. **Not** the paired-release phases or `REAL_BRIDGE`: they drive the retired `astrid serve`.

**Topology:** the hosted App build on its RuntimeDataProvider, through the loopback gateway, to a real Runtime on SQLite in a throwaway realm; the Astrid CLI is a second client of that Runtime (Plan A direct path). Each case first asserts that the App, Astrid and the Runtime share one realm, one instance and one contract. The relay variant (the paired relay and connector, `transport: relay`) runs the same cases after Plan B M0 (card F2-L1).

**Done when**, in order. *Status: 1, 2 and 5 built (cases 1-3); 3 and 4 blocked and 6 full tier only (Owned debt: Remotion gate and Linux custody).*
1. **Agent → open App.** Astrid publishes a revision while the App is open, and the App shows it without a reload. One real task-activity event for that work is visible in the App.
2. **Concurrent edit.** Start an App edit and hold its save acknowledgement; publish an agent edit from the CLI; make another App edit, then release and retry. Both edits survive, or a named conflict keeps the draft intact. The retried save produces exactly one publication. Opaque fields and explicit clears are preserved. Both clients agree after a reload. This carries r4 IP3/IP4.
3. **Render that revision, adversarially.** Render accepted revision R through the App's render action (`renderRouter.enqueueAstridRuntimeRenderTimeline`). Publish R+1 before it executes. The task's `timeline_authority.parent_revision_id` equals R, and a frame or audio marker that distinguishes R from R+1 is R's.
4. **The render plays, and it is the film the App showed.** Through the relay, a seek returns 206 with `Content-Range`. Frames decode near the start, middle and end, and **match the App's preview of R at those times** within a perceptual threshold (r4 IP5). The decoded audio isn't silent. Playwright's Chromium must decode H.264/AAC; that is checked in preflight. If the App later gets an in-app player for renders, this step drives it; until then it reads the output through the relay.
5. **Runtime restart with the App open:** the App shows its relaunch notice, the draft survives, and it saves after the relaunch.
6. **Full tier only:** the Codex image → sprite step comes before step 1, as a separately reported product check. The thin slice uses existing film media.

Phase outcomes follow R-10.

### TIDY: fold or delete the other mechanisms, assertion by assertion
`1.5 d · normal · in: F1, F2 · out: T#one-gate`
**Done when:** each item below has every useful assertion mapped to its new home (a line per assertion, reviewed), and is then deleted:
- Astrid: stage1 cross-repo acceptance and `stage1_acceptance.py`; `iteration_video_runtime_e2e`; `evals/timeline`; `smoke_*.sh`; `tests/proofs`; the VLM gate; the s1/m4/m7/m8 scripts, Makefile targets and `artifacts/`; `run_ci_checks.sh`; the cold-launch matrix;
- Runtime: `test_i06_composed_proof.py` and `test_astrid_activation_join.py` (F1 covers them);
- the App: `real-bridge-serve.mjs`, the `astrid serve` path in `verify-paired-release-e2e.mjs`, and the unpinned `bridge-latency.yml`.

**Deferred, not in this plan:** custody behaviour tests become PROCLIFE's acceptance tests when PROCLIFE lands (a reused pid is never signalled, no process is signalled twice, busy means a task in flight, the crash journal is reaped on start), and the custody broker's ~23k lines of tests go with it.

## Owned debt (outside the cards, recorded so it is never ambient)

- **Astrid structure: 23 distinct violations, now a shrink-only gate** (`scripts/reshape/baselines/structure_astrid.json`, checked in the default lane). A new violation fails; a fixed one must leave the baseline. Removing the rest needs design decisions, not test fixes:
  - 9 top-level `astrid/` modules and dirs outside the canonical packages;
  - `packs/vibecomfy/direct_image` and `media` not converted to executor folders;
  - `core/execution/generic_host.py` importing pack internals (6 sites);
  - 3 `sys.modules` registrations that `importlib` legitimately needs, where the rule allows no exemption.
- **Astrid ruff/mypy baselines were reset on 16 Oct** (ruff 1,469 → 2,294; mypy 956 → 2,152). The old CI never reached them, so they had drifted. They now only shrink. The import-cycle baseline was regenerated from 14 stale pairs to the 6 real ones.
- **The smoke cannot run off macOS: three product blockers (found 16 Oct while building F1).**
  1. The Runtime launcher (`astrid_runtime up/down/restart`) needs Darwin audit-token custody (`astrid_runtime/custody_broker.py:899`). On Linux its process identity is also `ps-lstart:` while the daemon records `proc-start-ticks:`. A Linux custody provider is a security design decision.
  2. `rendering.render` readiness and claim require a provisioned Remotion even for media-only timelines (`rendering/pack.yaml:1015`, `generic_host.py:5945-5979`), though the task adapter already renders those with ffmpeg.
  3. Linux process census misses an exited-but-unreaped leader (`process_group.py:190-193`, `:426`), so any fast-exiting child (`node --version`) raises "owned leader exited before ancestry capture". This is also behind several known failures.

  Until these are decided, F1 runs on the reference Mac and F2 cannot start. Remotion provisioning in a cloud container also needs Node exactly 20.19.4 and GitHub archive tarballs for the @banodoco packages.
- **F2 steps 3, 4 and 6 are not built (thin slice, direct path).** Step 3 (render R, publish R+1 before it runs) and step 4 (the render plays and matches the App's preview) need `rendering.render` to run a media-only timeline without a provisioned Remotion (`astrid/packs/rendering/pack.yaml:1015` sets `requires_remotion: true`; `astrid/core/execution/generic_host.py:5945-5979` enforces it), or Remotion provisioned in the container (Node exactly 20.19.4 and the @banodoco tarballs). They also need the Linux custody gaps closed: a short-lived descendant that is absent between the census and registration raises `UnadmittedCandidateAbsent` (`astrid/core/execution/custody_broker.py:2913`), and a fast-exiting leader is missed by the census (`astrid/core/execution/process_group.py:48-49`, raised at `:470`). Step 6 (Codex image → sprite) is full tier only and needs the network (R-2 `live`). None of these is a `test.fail` or `test.fixme` stub. Released by: a case `render R, publish R+1 before it runs` in `astrid-app/tests/e2e/local/three-products.spec.ts`, driving `renderRouter.enqueueAstridRuntimeRenderTimeline` (`astrid-app/src/tools/video-editor/lib/renderRouter.ts:947`); the `f2.marker` colour already gives step 3 a frame marker that tells R from R+1. Step 6 is released by the full-tier journey (F2-L2) on a machine with network access.
- **C1.3, the timeline packages:** schema and composition are produced outside these three repos (banodoco/timeline-composition and friends), so digest checks need a manifest there. Versions still differ (Astrid's Python pin, 0.0.1 transitively in Astrid's Remotion lock, the App's vendored 0.0.2; composition 0.0.6 vs 0.0.2). Alignment stays with r4 PINS.
- **TIDY items kept by R-1, with the tests that would release them:**
  - Astrid smoke scripts: `smoke_wheel_install.sh` is the home for installed resources, the vendored client, wheel identity, both adversaries and workspace cleanup. It reads its expected values from the checkout and the installed registry, `make wheel` runs it, and CI's `release` job runs it (`--wheel/--venv`) against the wheel it built and installed.
  - Astrid `evals/timeline` and `tests/proofs`: none of their useful checks have homes; they need local run artifacts (integration lane).
  - Runtime `test_astrid_activation_join.py`: five cross-process activation checks with no other home. Their right home is an Astrid test that drives a real Runtime relay (R-5).
  - App `scripts/release/verify-paired-release-e2e.mjs`: the whole script is the paired `astrid serve` release gate, wired into `verify-extension-ship`. Its useful checks (serve-owned render evidence, provenance) belong to F2; retiring it is the release owner's call. The real-bridge specs it stood beside are gone, with homes for their App assertions.
- **App `config/contracts/astrid-plan-a-c2.json`** still carries stale hand-pinned client digests (`generatedClientCompatibility`). Removing them changes a frozen contract digest, so it needs a coordinated bump. The vendor locks are now the real check.
- **Linux custody gaps behind Astrid known failures (product, PROCLIFE):**
  - a short-lived SDK-render descendant reaped between the census and `register()` raises at `custody_broker.py:3051`; Linux has no unadmitted-absent handling like Darwin's (`:2909`). All six render-parity tests in `test_conformance.py` are `flaky:` entries for it;
  - `host_bootstrap.py:561` retires a host registered by another process with a numeric `os.killpg`, because no custody handle exists across processes.
- **The capability parity gate's proof run** is an integration-lane test. Its cpu and render proofs are now real-daemon tests in `test_runtime_client_cutover.py`; its local_generation and provider proofs need an OS network sandbox for the provider broker and a Runtime checkout on the path, so they do not pass in a plain Linux container.
- **Astrid's capability catalog** (`astrid/packs/_core/skill/references/capabilities.md`) is generated from whatever packs are installed, so it lists the external hivemind pack where that is installed and the doc-refs check depends on the machine. It is also stale for in-repo packs (`chiptune.midi` missing, the removed `h3_av.transform` listed). The owner decides whether it covers installed external packs; then it is regenerated.
- **The App's typecheck and lint are not in CI:** `tsc -p tsconfig.app.json` reports 36 errors and a repo-wide ESLint run reports 29 errors (measured on this branch; the count moves, so re-measure before baselining), none in files the F2 card touched. Each needs a shrink-only baseline or a burn-down before it can gate.
- **Astrid's recoverability gate** (`test_recoverability_conformance_zero_mode`) is red on upstream main: the 71d43e00 port to pack actions brought 230 bare raises and direct stderr writes. Converting them to the recoverable-error contract is product work, owned by the pack-actions port.
- **Six TCP provider actions declare no host-managed broker** (`test_every_tcp_provider_manifest_declares_an_enforceable_host_broker`). Adding a broker to `network_policy` is a security change, so the test stays a known failure until the provider owner adds them; tests do not write security policy.
- **Astrid's stage-1 evidence chain** (`stage1_acceptance.py`, `stage1_evidence_capture.py`, `s1_gate.py`, their tests and the evidence contract) asserts no product behaviour, but deleting it retires the App doc's `acceptance.json` deliverable (`astrid-app/docs/local-runtime/01-astrid-beta.md:407`). That is the owner's call.
- **Known failures** (each in `tests/known_failures.txt` or as an `it.fails` entry, owned and expiring 30 Oct): see each repo. Astrid's list is longer than 10, so UA stays open (R-6).


## Relation to r4

- **Replaced:** GREEN's suite-greening (by UA, UR, UP) and GATE's single-film gate (by F1 and F2).
- **Kept:** IP1 (preservation); IP3 and IP4, carried into F2.2; IP5 (preview = render parity), now F2.4's check; IP6 (SEC-1…5, reconnect, Range seek); REPLAYS.
- **Owned here:** the journey takes GATE item 5's scenario registry. UA owns GREEN's doc and manifest checks.
- **Pins:** PINS-ASTRID and PINS-APP still align the renderer closure; C1.3 proves it by digest.
- **To amend in r4's text:** `testing.md:25,29,32` and GATE items 1–3 (no journey per merge, "≤5 min", "not observed (deadline)").

## Order and checkpoints

```
wave 1:  LEAK   UA   UR   UP          (independent, in parallel)
wave 2:  C1 → C2      F1              (C1 needs the three greens; F1 needs UA, UR)
wave 3:  F2 → TIDY
```

**Checkpoint A** (end of wave 2):
- the three default runs are green in CI;
- a planted one-byte drift fails in each consumer;
- the portable smoke, with `runtime_restart` and the read-back of the killed task, passes in a clean container and is the R-11 merge check.

**Checkpoint B** (end of wave 3): `journey --tier full` passes on main against the real film, including F2.4's preview-parity check after a concurrent edit.

## How it is executed

The plan is executed in waves of agents. The shape matters more than the headcount.

**The referee is the test run, not a model.** A card's "Done when" is checked by running something: the suite, the planted drift, the journey. That is what lets cheap models do most of the work.

| Tier | Does |
|---|---|
| **Haiku** (most calls) | Run suites and group failures by signature; add markers and lanes; delete tests for removed designs with their `removed.yaml` line; write CI workflows and `check-before-push`; manifest and vendor scripts to a written spec; relay route-table entries; map old assertions to new homes. |
| **Sonnet** | Review every Haiku diff for weakened tests (a removed assertion, a widened tolerance, a new skip); fix genuinely red tests; implement C1, C2 and F1; take over any task Haiku fails twice. |
| **Opus** | Decisions made once and reused: the manifest format, the mini-realm, F2's topology; settle disputed "real bug or stale test?" calls; approve every deletion batch (UA.3, TIDY); the xhard cards. |

**Guard rails:**
- Each change lands as a small commit on a branch per repo, with the referee's result in the message.
- A change that makes a red test green by weakening it is rejected, whatever the tier.
- Every disposition (fixed, moved, deleted, known failure) is one line in the card's PR, with its reason.
