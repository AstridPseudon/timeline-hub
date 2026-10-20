# MAIN17 / normal Runtime013 composed App source typecheck

PASS. Ran the requested actual App source typecheck **once**, exit **0**, with **zero diagnostics**. No product, test, configuration, generated-client or lockfile edits were made. No baseline/new-failure classification or product follow-up is needed for this run.

## Exact source and pins

| Source | Commit | Tree |
| --- | --- | --- |
| App, this worktree | `927545cf52fdfbb273afbe7f190e00e11e5e2d70` | `96605f2a46c49fcf96cd12ca3679014f00ae28de` |
| Agent keeper `/home/user/work/wt/app-m3-agent013-current-pair-source` | `d8749a9ce12a699672faf3ad96b4e4cbea9245c2` | `75354d38c898729bac09619679f5421faba319ed` |
| Runtime producer keeper `/home/user/work/wt/app-m3-runtime013-producer-source` | `2c4ac180c2220bdad966bc01e95ad230e99ce26a` | `7ab412cc4bcbe517efcfa806e092336390312e18` |

Both App and Agent **normal** `runtime.lock.json` pins identify that exact Runtime producer and artifact:

- Contract/client: `workspace.v1` / `0.2.13`.
- Schema: `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`.
- Artifact: `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`.
- Component manifest: `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5`.

Before tsc, the existing wrapper's exported `readCurrent013Inputs` and `checkCurrent013Sources` were called directly with the exact paths/SHAs above, both existing venv Python entry points, and `TIMELINE_CURRENT013_APP_TREE=96605f2a46c49fcf96cd12ca3679014f00ae28de`. Its browser launcher was never called. Source/cleanliness, both normal pins, generated metadata, both public12 archives and Runtime's 75-artifact manifest checks passed. Its producer-aware vendor checks passed for all **13 App** and **15 Agent** locked destinations. Full output: [pair-preflight.log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-main17-root013-composed-typecheck/notes/pair-preflight.log).

The source report was read at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-main17-root013-label-port.md`. Its source audit was adapted only to this assigned root and retained at [source-audit.py](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-main17-root013-composed-typecheck/notes/source-audit.py). Before and after tsc it reproduced the exact App tree and passed the entire source allowlist: approved public12/normal013 Root+wrapper bytes, five reconciled MAIN17 files plus the production rename test, all unrelated base paths, six protected server paths including the clean shared Vite reconciliation, seven unchanged three-products journey bodies/helpers, provider parity, and the original three `useClipDrag` expected failures. MAIN17 `17e46de99b7cef52fe494de1703a9865a8d4be24` is an ancestor (exit 0). No behavior expectation was changed.

## Dependency identity

Only this worktree's ignored `node_modules` symlink was redirected from the shared default to **`/tmp/app-coherent-deps12/node_modules`**. The shared default10 dependency tree was not used for tsc. Dependencies were read without installs, patches or cache writes into shared directories.

- Node `v22.22.0`, npm `10.9.4`, TypeScript **`5.9.3`** (the existing private12 compiler).
- `.bin/tsc` resolves to `/tmp/app-coherent-deps12/node_modules/typescript/bin/tsc`; SHA-256 `8d5fa5bd883fec0979fc2004f1fe1d99aef40570155d550eadc0b03b55513bf0`.
- Root `package.json` and `package-lock.json` retain `file:vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz`, version `0.0.12`; lock SHA-512 integrity matches the archive.
- Public12 archive: **58,444 bytes**, SHA-256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`. Exactly **77** unique regular safe archive members; the installed package contains exactly those 77 files, byte-equal to the archive.
- React/React DOM **18.3.1**; Remotion/Player/Media/Layout Utils/Three **4.0.509**; `three` **0.185.1**. All required peers resolve to the same physical entries from App and Composition.
- Ambient packages: `@types/react` 18.3.28, `@types/react-dom` 18.3.7, `@types/node` 22.19.17, `@types/three` 0.185.4; `@react-three/fiber` 8.18.0.

[dependencies.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-main17-root013-composed-typecheck/notes/dependencies.json) records exact physical paths, including the read-only private timeline-ops/schema links. The before/after dependency-resolution records compare equal; the source audit rechecks all public12 bytes after tsc. This is scoped verification, not a claimed hash census of every dependency file.

## Exact command and diagnostics

Working directory: `/home/user/work/wt/app-m3-main17-root013-composed-typecheck`.

```sh
W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-main17-root013-composed-typecheck
env npm_config_cache="$W/notes/npm-cache" npm_config_offline=true \
  flock -w600 /home/user/work/.app-tsc.lock \
  env NODE_OPTIONS=--max-old-space-size=4096 \
  npm exec tsc -- --noEmit -p tsconfig.app.json \
  > "$W/notes/tsc-diagnostics.txt" 2>&1
```

Executed once through [run-tsc.sh](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-main17-root013-composed-typecheck/notes/run-tsc.sh). Start **2026-10-20T12:35:30Z**, end **2026-10-20T12:36:26Z** (56 seconds including npm overhead). [tsc-exit.txt](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-main17-root013-composed-typecheck/notes/tsc-exit.txt): **0**. Full combined stdout/stderr [tsc-diagnostics.txt](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-main17-root013-composed-typecheck/notes/tsc-diagnostics.txt): **0 bytes / 0 lines**. [npm-debug.log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-main17-root013-composed-typecheck/notes/npm-debug.log) confirms exact argv and exit 0; its unsuccessful npm notifier lookups did not install packages. The private npm cache was removed after retaining that debug log.

`tsconfig.app.json` checks `src` under the existing strict ES2020/bundler configuration, with the existing test exclusions and `skipLibCheck`. Root `tsconfig.json` has `files: []`; root-only tsc was **not** used as coverage. No compiler configuration was widened, no casts/suppressions were added, and no compiler output was emitted.

Other exact verification commands (all exit 0):

```sh
python3 -B "$W/notes/source-audit.py" > "$W/notes/source-audit.json"
node --experimental-import-meta-resolve "$W/notes/dependencies.mjs" > "$W/notes/dependencies.json"
git merge-base --is-ancestor 17e46de99b7cef52fe494de1703a9865a8d4be24 HEAD
git diff --exit-code HEAD
git diff --check
```

The source/dependency commands were repeated after tsc into `source-audit-after.json` / `dependencies-after.json`; both `cmp` comparisons exited 0. Wrapper preflight internally ran these successful producer-aware commands with `PYTHONDONTWRITEBYTECODE=1`:

```sh
node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/app-m3-runtime013-producer-source
/home/user/work/venv-agent/bin/python /home/user/work/wt/app-m3-agent013-current-pair-source/scripts/vendor_lock.py check /home/user/work/wt/app-m3-agent013-current-pair-source/runtime.lock.json --producer /home/user/work/wt/app-m3-runtime013-producer-source
```

A preliminary dependency probe used CJS resolution and rejected ESM-only `@remotion/media`; the corrected read-only ESM resolution probe passed. This changed only the external probe, with no compiler rerun or package modification.

## Handoff and limits

No blocker or settled-design deviation. No unit/full suite, build, browser, localhost/live-socket run, actual Agent/Runtime acceptance, restart/retry/reload/undo journey, rendered frame/audio parity, owner-film or macOS gate was run. The successful typecheck establishes App source compatibility with these installed declarations; **it does not establish actual Agent acceptance**.

Manager next: review this exact source/result and launch the planned actual matching pair qualification. Keep the source report's separate cap-policy escalation outside this typecheck result. No duplicate typecheck is requested here.

Source remains clean at the exact commit/tree above. No build output or temporary files remain in this worktree. The local `design` report is ignored by existing policy; identical copies are saved in ORCH/design and worker/report.md. A conventional commit message and DONE are supplied; no KEEP is created. No integration edits, commits, merges, checkouts, pushes or test-service requests were made.
