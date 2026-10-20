# App public12 private dependency graph — READY

Status: **READY** for the static capability consumers named by the orchestrator.

The graph is a genuinely fresh private install rooted at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/clean-project`

It was installed from frozen App root `0ea988bdd2907c876b82fd2620820e3fb6d6ea84` with exact frozen inputs:

- `package.json` SHA256 `0c77703dab8eeb46e05fa7555bbaf5e9ea4fbef077b4759610049fe110894090`
- `package-lock.json` SHA256 `310d447508a2f0c023176a3283724455cd5823b6ffe116177f8e30d541de82a0`
- `vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz`: 58,444 bytes, SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, 77 regular tar members

The graph has 35,641 physical entries, 32,417 regular files, and 624 package manifests. Its only 36 symlinks are relative internal `.bin` links; all package/local links are materialized as private real directories. No external links, directory links/cycles, self-links, foreign-device files, or hardlinks escaping the graph were found. Four hardlinked files are internal to this graph and are fully accounted for by the physical manifest.

The three small frozen local file dependencies were included as private source inputs because npm’s exact lock resolves them (`vendor/timeline-ops`, `vendor/timeline-schema`, and `vendor/fake-indexeddb`); their graph copies total 548,864 allocated bytes. This is not a borrowed or polluted App graph and does not broaden the prior six-exclusion policy. No full App source duplicate was made.

## Evidence

- `npm ci --no-audit --no-fund` under Node 20.19.4/npm 10.8.2: **exit 0**, 569 packages added.
- npm validated 671 registry lock nodes with integrity fields; none were missing. Install log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/npm-ci.log`.
- Normal postinstall `remotion-4.0.509-audio-resume.mjs --apply`: **exit 0**; read-only `--check`: **exit 0**, both target files patched to exact known hashes.
- Pure import probe for React, ReactDOM, Remotion, Remotion media/player/layout-utils, and Composition: **exit 0** (`pure-imports-ok`).
- TypeScript declaration probe over the same packages with `tsc --noEmit --strict --skipLibCheck`: **exit 0**.
- Peer versions and six tree hashes match the frozen values: React/ReactDOM `18.3.1`; Remotion, media, player, and layout-utils `4.0.509`.
- Resource watchdog: npm phase ended with 11,385,954,304 bytes free and 756,113,408 bytes private allocation; final audit measured 11,677,130,752 bytes free and 752,308,224 bytes for project/cache/temp, within the 10 GiB floor and 1.4 GB budget.

Exact physical manifest and machine-readable evidence:

- [READY marker](handoff-vw-m3-app-private12-clean-install-READY)
- [full physical manifest](handoff-vw-m3-app-private12-clean-install-manifest.json), SHA256 `d20a148e05c14ba3e0cbb31ba3accf3b349fd95c21529e6a7df38633e8a02a46`
- [JSON report](handoff-vw-m3-app-private12-clean-install-REPORT.json)
- [metadata](handoff-vw-m3-app-private12-clean-install-metadata.json)
- [commands](handoff-vw-m3-app-private12-clean-install-COMMAND.md)

## Scope and non-claims

This is only a static minimal-capability environment. No product files, package pins, repository refs, shared dependencies, shared caches, browser, socket/listener, render, current API, Root activation, M2, parity, Vitest cache, or full suite was run or changed. Consumer workers must keep their own caches outside this graph and treat the graph as read-only after READY.
