# app lead — 2026-10-19T20:18:53Z
- Handover received 2026-10-19T20:12:58Z. App manager started 20:15Z on the app machine: Codex gpt-6.1-sol high (no fallback). Dispatcher + hub-syncd running; Codex signed in.
- Integration: main's last local merge 0f16295c1 (Merge tl/app-m1-wiring-fix) never reached hub/tl/integration before handover; the app manager re-merged the same branch as 430546e42 — identical tree, no work lost. The 0f16295c1 sha in STATUS refers to main's copy.
- Adopted in-flight worker branches from hub: app-m1-{editor-wiring,projection-fact,recovery-basis,recovery-compose,recovery-ui,wiring-fix}. Viewing branches (vw-*) left for the merge-request path.
- Machine notes: Playwright 1.60 runs on the preinstalled Chromium via a local browsers shim (headless); ImageMagick 7 CLI shim; venv-agent/runtime ready. Baseline full-e2e-timeline on pre-handover tree 76f1e5b: 10 passed/28 failed (mostly "unexpected 404 request(s)" + layout snapshots) — first recorded run of this suite, for the App manager to triage.
- Hourly lead check-ins publish here.
- 2026-10-19T20:22:18Z: hub-syncd + dispatcher restarted by area lead (manager escalation app-20261019T2020Z-sync-daemon-restart handled locally).

## 2026-10-19T20:46:34Z — lead actions
- DONE: tool update (kit bin copied 20:20 by manager), hub-syncd restarted 20:21Z on the new hub-sync, dispatcher restarted 20:22Z. Top of STATUS shows "tool update done".
- Sync gap 20:26–20:45Z: cause was the hub clone left mid-rebase by a content conflict in hub/design/app-m1-coordination.md (main's 20:26Z section vs App manager's 20:25Z section, both appended at the end). Resolved by keeping both sections; pushed 20:45:24Z; hub-syncd restarted; syncing normally.
- Kit bug (for main): hub-sync's 'git pull -q --rebase' leaves the clone stuck mid-rebase on any design-doc conflict, and later cycles keep writing the heartbeat while every push is rejected. Suggest: on pull failure run 'git rebase --abort', then re-pull resolving hub/design with -X theirs or a union merge, and only write the heartbeat after a successful push.
- Adopted branches app-m1-recovery-basis/compose fast-forwarded locally to main's dc519fb7f / 436410bcd (the hub already had these). The new hub-sync does not republish imported branches.
