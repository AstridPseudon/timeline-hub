# Brief: Farm (area farm, prefix tf-, Timeline Child 5; runs tests only, on Claude workers)

Read `$ORCH/PLAN.md` (v2.1) and `$ORCH/MANAGER-COMMON.md` first. You never edit product code or tests; you run them and report. Results go to `$ORCH/design/farm-<run>.md`, which syncs through the hub, with: PASS/FAIL, exact commits and trees, the command, counts, and a failure classification (product / harness / environment).

## Runs
- **H0, baseline:** full suites of **upstream main** (fresh clones at origin/main) for runtime, agent and app. These are the new baselines.
- **H6 and H9:** full suites on the integrated heads (`hub/timeline/<repo>/tl/integration`); the gesture tour (P2 spec) and the gate-5 journey (P3) once they exist; a `delivery-build` dry run, if the orchestrator puts it in your INBOX.
- **On request:** runs named in your INBOX by the orchestrator, or in other lanes' Blockers lines.

Run at most 2 heavy runs at once. Preflight every run, listing everything missing in one go; zero tests executed counts as a FAIL.
