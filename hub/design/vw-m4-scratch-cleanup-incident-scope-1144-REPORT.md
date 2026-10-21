# Scratch cleanup incident disposition: worker 1134

Date: 2026-10-21

## Owner-facing disposition

Worker `vw-m4-durable-runtime-source-closure-proposal-1134` completed its unapplied proposal and then ran a broad temporary cleanup; the recorded expansion contained exactly `/tmp/vw-m4-source-main-F3vuTd` (its own completed source scratch) and the pre-existing `/tmp/vw-m4-build-projection-review-prod.KuaAYx` (owned by completed worker `vw-m4-build-projection-release-review`, a private Composition dependency-leaf/build-probe scope), and the cleanup recursively removed both roots’ regular files and empty directories; the second root’s exact historical contents, size, and per-file inventory are UNKNOWN, but retained records identify it as reproducible build scratch rather than accepted media, a Runtime graph, a lease root, or a live input, no active lease/process/test reference was found, the owner’s review was REJECT with its report/log retained, the independent targeted projection result remains retained as 2/2 passed, and all named stage/runtime/App/artifact/current packet/source controls remain present, so close locally with no restoration or historical-proof replay while preserving this incident as a recorded cleanup defect.

## Exact cleanup scope

The final cleanup block in the retained 1134 log was:

```sh
find /tmp -maxdepth 1 -type d -name 'vw-m4-*' -print
for d in $(find /tmp -maxdepth 1 -type d -name 'vw-m4-*' -print); do
  find "$d" -depth -type f -delete
  find "$d" -depth -type d -empty -delete
done
```

Its recorded expansion, in order, was:

```text
/tmp/vw-m4-source-main-F3vuTd
/tmp/vw-m4-build-projection-review-prod.KuaAYx
```

Both roots are now absent. No other top-level `/tmp/vw-m4-*` path appears in that command's recorded expansion. The first root was 1134's own temporary source layout. The second root was pre-existing and not created by 1134; its prefix matches the completed `vw-m4-build-projection-release-review` worker. That worker's brief and report describe a private leaf-linked `node_modules` overlay used for a narrow `npm run build`/packaging review of the transient Remotion animation projection. The logs do not preserve a manifest for the exact `KuaAYx` instance; deleted contents, byte count, symlinks, and any generated build files are therefore UNKNOWN.

## Dependence and remaining evidence

- No lease file, live worker status, test request, or live process referenced `KuaAYx` when checked. The 1134 log records the matching worker as already `done`; current process inspection found no matching build-projection, runtime, or make-runtime process.
- The original owner report remains at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-build-projection-release-review/REPORT.md`. It says **REJECT** for `e5565481735fa4766f6e19db0b85e2579dfff4b5`, with no source edits; its build-probe result and limitations remain in that worker's report/log. This was not an accepted release proof.
- The retained central targeted result `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/vw-m4-pure-animation-build-projection-targeted-1021012926-13618/summary` is `pass`, exit 0, 2 passed / 0 failed. Its log uses `/tmp/composition-primitives-2UZcas`, not `KuaAYx`; no accepted proof was found to depend on the deleted root.
- Retained 1134 artifacts remain: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/vw-m4-durable-runtime-source-closure-proposal.patch`, its flat REPORT/COMMANDS/FILES reports, the worker REPORT/log, and the completion marker. No product patch was applied.

There is no evidence in the retained records that `KuaAYx` held raw accepted media or active input data. That absence is not proof about unrecorded bytes: historical contents are UNKNOWN. If exact scratch bytes later become necessary, the only safe option is operator-authorized recovery from an external filesystem snapshot/undelete source; otherwise recreate a fresh worker-owned temporary root and rerun only under a new explicit brief. No recovery or proof replay is authorized by this disposition.

## Cheap post-incident controls

Named retained roots and identities:

| Item | Control | Result |
|---|---|---|
| Leased 1054 stage | `realpath -e` on `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-storage-cleared-complete-runtime-stage-1054/owned-stage`; SHA-256 of `remotion/package-lock.json` | Present; real directory; `c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24` |
| Immutable Runtime graph | `realpath -e` on `/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/node_modules`; lock hash | Present; real directory; lock hash matches retained `c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24`; retained graph identity is `4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c` |
| App graph | `realpath -e` on `/home/user/work/app/node_modules`; read-only sentinel hashes | Present; real directory; current sentinels recorded as `package.json` `7c806b078b00bba1593336c49a3d2953b3f8f7afc7fa9919f6d5d7ccc7c1aa61`, `dist/evaluation.js` `e27ed545e9e0c28cf863e7bccd4a720f61e1002e04f2946dd3afca5e5f478155`, hidden lock `4a0b613e7dc615aadd6c6fcc6152ee9113f4f2450335c8ffabc1b272ca32dcaf`; retained whole-tree identity `9686f3d7743cba4332e61e3bd4f6cecfca466c40f25dbee5f48ba8fed984cedd` |
| Immutable 0.0.14 artifact | `sha256sum -c` against its adjacent sidecar | PASS; `21fde4d2a5d62a83f97a85d4b8d9f9d3f707a6489c07eb421c6331eccf893e6e` |
| Public13 retained artifact | `sha256sum -c` against its adjacent sidecar | PASS; `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738` |
| Current packet roots | `realpath -e` on the 1054 custody report, repaired App-graph report, and 0.0.14 archive/report roots | Present; no packet root was under `/tmp/vw-m4-*` |

Current source repository controls were read-only `git rev-parse HEAD` plus `git status --short --branch`:

```text
/home/user/work/agent       1a50cf3f30398500e9f1ccf0b94d59fe7a8bdb3f  clean tl/integration
/home/user/work/runtime     b92d3e7a05eec65c142294ef4873edd059e9b31d  clean tl/integration
/home/user/work/app         92c30b570cf8105dc021a64874c258e6c950b841  clean tl/integration
/home/user/work/composition df7b86308902fae90eda1dc3080d17d8fc30ea78  clean tl/integration
```

## Future brief cleanup clause

> Cleanup is limited to the exact worker-owned temporary root recorded in this brief: `<OWN_MKDTEMP_ROOT>`. Before cleanup, require `realpath -e "$OWN_MKDTEMP_ROOT"` and refuse if it is absent, non-directory, or not under the worker's declared private scope; then remove only that exact root and verify it is absent. Never use `/tmp/vw-m4-*`, `/tmp/*`, a prefix glob, or a discovered list of other workers' roots.

## Commands and limits

- Read `PLAN.md`, 1134's `REPORT.md`/`log.txt`, the original build-projection report/brief/log, the 1054 custody report, Runtime 4913 audit report, App graph report, immutable14 review, and retained targeted-test result — PASS.
- Read-only existence/realpath/hash controls above — PASS.
- `ps -eo pid=,stat=,args= | rg -i 'build-projection|KuaAYx|vw-m4-source-main|make-runtime|request-runtime'` — no matching live worker/process (the command's own `rg` was the only transient match).
- No product test suite, cleanup replay, restoration, browser, Runtime server, helper, socket, source/graph qualification, or historical proof replay was run.
