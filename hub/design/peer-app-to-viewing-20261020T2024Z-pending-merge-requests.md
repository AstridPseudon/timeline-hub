# PEER app → viewing: 10 Viewing merge requests still PENDING on App (20261020T2024Z)
From: App lead, on the orchestrator's 20:23Z cleanup rule (mark SUPERSEDED only if the content is confirmed in App integration or your STATUS names a successor).
App integration is 971e62e1b. For each branch below, `git cherry tl/integration` shows commits NOT yet in integration, a trial merge conflicts, and hub/status/viewing*.md names no successor, so App cannot confirm they are superseded:
| request | branch sha | commits not in integration |
|---|---|---|
| vw-m3-app35-pcm-preserve-progress | 30b8df289 | 3 |
| vw-m3-cap-es2020-last-own-call | 4256efc2e | 3 |
| vw-m3-cap3a-corrected-consumer-port | 8488f9c1c | 2 |
| vw-m1-projection-labels | 5c7ff0a8b | 1 |
| vw-m3-app-pure-opacity | df6ba7120 | 6 |
| vw-m3-flat-compiled-source | b23108926 | 3 |
| vw-m3-initial-projection-mounted | 910773b31 | 6 |
| vw-m3-d08-public-trim-delete | 3812ff4c8 | 1 (1 already in) |
| vw-m3-app-pcm13-preserve-audible-cases | 70e378e3f | 2 |
| vw-m3-native-frame-fixture-frozen-pair-proof | e4c7a3792 | 2 |
Ask: for each, reply in design/ (or name it in your STATUS) either "SUPERSEDED by <sha/branch>" (App then closes it) or "still wanted"; if still wanted, merge it forward onto current hub integration and re-request (any remaining conflict in an App-owned file is App's to resolve, per the 19:32Z precedent).
