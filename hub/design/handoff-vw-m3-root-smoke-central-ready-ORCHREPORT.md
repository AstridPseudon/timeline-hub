# READY — current public10 Root smoke, central one-shot

Prepared, **not browser-run and not submitted**. No product files changed. This handoff is ready for manager review; no manager grant has been created. The task's requested preparation is complete. Browser execution is deliberately pending authorization, not a claimed pass.

## Exact source and controller

- Source: `/home/user/work/wt/vw-m3-root-smoke-central-ready`.
- Committed source SHA: `5acd7233df676bf42b2086d86cb0a6358398bf5f`.
- Committed tree: `66898dd11df74e205af95903651782a29e9886b4`.
- Existing three-field smoke snapshot repair is the sole change from the earlier `384918908` qualification. PLAN and the current-root-smoke-schema/current-public10-node-qualification reports were read.
- Controller: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-root-smoke-central-ready-controller.py`.
- Controller SHA-256: `5728411e9254119723ca5af2736f0671b8c9e97b3ffeaf0679195c0eaf947acf`.
- Shell entry: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-root-smoke-central-ready-READY.sh`.
- Shell SHA-256: `1face7922354a08ef61621415412a9648a1e77870d7cc54ba9f9b23330ea15ba`.
- READY specification: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-root-smoke-central-ready-READY.json`.
- READY specification SHA-256: `d9e286ce54397020c601e7f787745aeb1a6fefb48c7a01a240e2d70f51d753a8`.
- Exact staged smoke SHA-256: `07f1ad6da95d990dcbde3c394fea84538ee0c8d557dd0232abb031a3a9fdf7f0`; its complete reviewable difference is `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-root-smoke-central-ready-invocation.patch`.

## Staging and checks

The controller repeats the previous qualified Node staging approach: current committed Remotion files, read-only symlinks to `/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules`, and an exact local copy of only `@remotion/cli`, whose real path must stay inside the staged project for the existing input binder. Other repository roots remain read-only source links. The public Composition implementation comes exclusively from the current committed tarball, never Composition source or a private evaluation import.

Public10 archive SHA-256 is `cd83b77f72ce436e25eef697b289d33adae2087d92035aa37a27a308975ddea7`; exact lock SHA-512 integrity, all **77 distinct safe regular archive members**, and every extracted file were checked. React/React DOM **18.3.1**, Remotion/media/layout-utils/renderer/bundler/CLI **4.0.509**, Node **20.19.4**, npm **10.8.2**, and all **six historical target hashes** passed. The controller contains the exact six constants from the earlier qualification.

Offline `remotion_install_problem(staged_project)` returned **None**, and the existing `_runtime_inputs` binder completed over **21,490 files**. This reuses the existing local check; it creates no launch-validation receipt, official Runtime admission, or fallback readiness grant. The binder's temporary absolute paths were cleaned after checking and must be rebound on the future run.

Pre/finally inventories matched for **2,900 tracked source files plus HEAD/tree**, **21,462 borrowed graph files plus 33 symlink records**, **466 full-browser installation files**, and the Node binary. Every one of the earlier qualification's 21,455 graph files is unchanged. The only additions since that earlier graph census are seven existing `.cache/webpack` files; those are also recorded in the borrowed-graph inventory, never modified or linked into the isolated stage.

- Node: `/tmp/vw-m3-agent-gate-node20.19.4/bin/node`, binary SHA-256 `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`.
- Full Chromium: `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`, binary SHA-256 `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`. This is a file/path/hash check, not a browser execution or version probe.

## Smoke invocation decisions

The committed smoke calls the renderer API directly. Its `selectComposition` call has no browser option and therefore cannot consume the project's CLI browser configuration. Renderer 4.0.509's installed implementation explicitly supports `browserExecutable`, `chromeMode`, and `onBrowserDownload`. Its default headless-shell mode supplies `--headless=old`, so full Chromium needs explicit `chrome-for-testing` mode.

The ORCH-staged invocation alone imports the existing `sharedBrowserExecutable` helper, forwards existing `ASTRID_REMOTION_BROWSER_EXECUTABLE` to `selectComposition`, selects full Chrome mode, and makes a browser-download request throw. The bundle uses supported `enableCaching: false` to avoid persistent cache writes. No peer is installed, patched, or copied wholesale; no network/download/install command is used.

All original closed allowed-array snapshots, golden/full fixture bytes and loading logic, positive selected-composition metadata assertions, and success/failure handling remain verbatim. The existing smoke has two named fixtures and no explicit empty selection. The ORCH invocation adds a selection using the **actual Root default props** (no synthetic fixture or replacement input), checking positive metadata and exactly one frame for its empty timeline. No media is generated, converted, relinked, or rewritten. These exact additions are visible in `invocation.patch` and are covered by the manager's controller grant.

## Execution guards and cleanup

Registered only in `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf`:

```text
agent e2e-viewing-public10-root-smoke bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-root-smoke-central-ready-READY.sh
```

The shell owns `/tmp/timeline-viewing-browser.lock` on inherited FD 9 across the entire foreground controller. Python verifies and locks that same open file description. Both the shell and controller check absolute QUIET markers; the controller repeats the check before CPU/browser steps and monitors QUIET while the smoke runs. An active marker records `PAUSED_ACK` and exits 75.

A run requires a genuine central snapshot, the exact approved source parent SHA and tree, a manager-authored `workers/vw-m3-root-smoke-central-ready/READY_GRANTED`, unchanged READY/controller hashes, and complete current source/graph/browser/Node equality with preparation. It verifies the complete restaged source/CLI/public10/peer graph against READY. Only then can it execute the smoke. An exclusive `ATTEMPT_STARTED` file permits one attempt, with a five-minute browser-phase timeout and no automatic retry. Browser subprocess groups are terminated on exit; source, staged package/graph, and borrowed graph inventories are checked again in `finally`, including failure paths. A PASS result is written only after successful final checks and cleanup.

All preparation staging has been deleted; no browser log, attempt marker, manager grant, or generated repository output exists. Future bundle/profile/temp outputs are confined to a fresh ORCH worker staging directory via TMPDIR/HOME and are removed in `finally`. Persistent run logs and source/graph manifests use flat absolute `design/handoff-vw-m3-root-smoke-central-ready-*` paths. The central service also retains its own ORCH result/log directory.

## Exact commands run and results

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-root-smoke-central-ready-controller.py prepare
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-root-smoke-central-ready-verify.py
bash -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-root-smoke-central-ready-READY.sh
git diff --check
git status --porcelain
```

- Final offline preparation: **exit 0**; pins/all77/input binding/Node staged-smoke syntax/pre-finally immutability passed. Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-root-smoke-central-ready-prepare.log`; binder output: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-root-smoke-central-ready-prepare-readiness.json`; full inventories: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-root-smoke-central-ready-prepare-pre.json` and `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-root-smoke-central-ready-prepare-finally.json`.
- Offline verifier: **exit 0**, all checks passed. It proves the original assertion/fixture sections and success/failure tail are unchanged, the extra empty check uses Root defaults, READY/controller binding is current, inventories match, and staging/repository are clean. It also runs two negative local wrapper checks: a noncentral cwd is refused, and a central-shaped temporary cwd with no manager grant is refused before source/browser work. Both intentionally return **exit 1**, consume no attempt, and launch no browser. Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-root-smoke-central-ready-verify.log`.
- `bash -n` and staged Node `--check`: **passed**. `git diff --check`: **passed**. `git status --porcelain`: **empty**.
- No repository suite was rerun because no product files changed. The preceding schema repair's **31 passed / 2 subtests** and actual generated Root bundle + 15-field check remain that earlier worker's evidence, not a new test claim here.

## Manager's next commands — only after explicit review/approval

The template below is approval for this one central smoke, not a product readiness grant. The worker has **not** copied it into the active grant path.

```sh
root_smoke_orch=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
root_smoke_prefix="$root_smoke_orch/design/handoff-vw-m3-root-smoke-central-ready"
# Manager only, after approving the exact source/controller/READY tuple above:
cp "$root_smoke_prefix-grant-template.json" "$root_smoke_orch/workers/vw-m3-root-smoke-central-ready/READY_GRANTED"
root_smoke_request=$("$root_smoke_orch/bin/request-test" vw-m3-root-smoke-central-ready e2e-viewing-public10-root-smoke)
"$root_smoke_orch/bin/wait-test" "$root_smoke_request"
```

If wait-test exits 124, wait on the same request again; do not resubmit. No browser/socket/service request was made during this task. No full suite is requested or needed for this handoff. If the source, graph, browser, or controller changes, the manager must review a refreshed preparation rather than editing a pin or bypassing the guard. Once an actual attempt starts, preserve its result and stop; a second attempt needs a new explicit task/grant, not deletion of the one-shot marker.

This is package-consumer Root bundling/selection/metadata smoke only. Browser selection remains **unverified** until that central run. It proves neither frames, audio, codecs, parity, owner-film behavior, live admission, nor M3 completion. Nothing is blocked for the preparation task; the later run is awaiting the intentionally required manager grant.
