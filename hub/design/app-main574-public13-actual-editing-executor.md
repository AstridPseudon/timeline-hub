# MAIN574/public13 actual editing gate

Status: **PASS**

## Frozen qualification tuple

- App: `ea38656fe62950440b36cafee780698cff2c3f9c`, tree `8bd8f741f7c8b28b8682aa960a658417f70c8522`.
- Agent/Astrid: `8130a401bf44a518d5a40ae274d398b8c560be55`, tree `236c3e57e0265c52b81ba8085de3193026176bff`.
- Runtime: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree `7ab412cc4bcbe517efcfa806e092336390312e18`.
- App public13 archive: SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, 77 files.
- Public browser source: SHA-256 `fe380bc3280b1f5efa7ecde7cc55a5415a498f2b35af8fb693d11123aa289a28`.
- Runtime producer checks: 75 artifacts; normal locks, schema, and producer manifest verified.
- Browser: Chromium `141.0.7390.37`, executable `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`, SHA-256 `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`.

The manager-approved source keeper `/home/user/work/wt/app-m3-root8bd8-qualification-source-keeper` was used for the cold lane after `/home/user/work/app` advanced past the READY tree. Its source was verified clean at the exact App SHA/tree before the request.

## Evidence

Native3, including M2 Gate 5, passed:

- Test ID: `app-e2e-main574-public13-native3-ea38656f-agent8130-runtime2c4-e2e-integration-1020162541-30497`
- Central command: `request-test integration:app e2e-main574-public13-native3-ea38656f-agent8130-runtime2c4-e2e-integration --no-cache`, then `wait-test` on the same ID.
- Product result: 3/3 passed. Guard result: pass.
- Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-e2e-main574-public13-native3-ea38656f-agent8130-runtime2c4-e2e-integration-1020162541-30497/log.txt`

Fresh separate cold-open passed:

- Test ID: `app-m3-root8bd8-qualification-source-keeper-e2e-main574-public13-cold-open1-ea38656f-agent8130-runtime2c4-e2e-integration-1020164755-1620`
- Central command: `request-test app-m3-root8bd8-qualification-source-keeper e2e-main574-public13-cold-open1-ea38656f-agent8130-runtime2c4-e2e-integration --no-cache`, then `wait-test` on the same ID.
- Product result: 1/1 passed. Guard result: pass.
- Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m3-root8bd8-qualification-source-keeper-e2e-main574-public13-cold-open1-ea38656f-agent8130-runtime2c4-e2e-integration-1020164755-1620/log.txt`

Both lanes used the existing guarded root runner with the minimal public13 adaptation. They verified the 77-file public13 archive, all declared installed package bytes/React/Remotion peers, the Agent public12 archive, Runtime 75 artifacts, locks, tracked public-browser bundle, source hashes, browser identity, private overlay, and shared caches unchanged. The normal hosted build was allowed. No direct public dist override was used.

Local runner validation also passed:

```text
node --check current013-public13-integration.mjs
node --check run-selected.mjs
python3 -m py_compile prepare-overlay.py audit.py public-source.py
bash -n run-lane.sh
```

These checks were run from the runner notes directory and produced no errors.

## Rejected/invalid evidence

The earlier cold request against moving `integration:app` was not counted:

- Test ID: `app-e2e-main574-public13-cold-open1-ea38656f-agent8130-runtime2c4-e2e-integration-1020163517-29617`
- It snapshotted App tree `c91e3c07f293658aa0f26dd180ac464c45b71559`, not READY tree `8bd8f741...`; the source preflight rejected it before any product test ran. This is an invalid-source run, not a product failure.

The rejected `scripts/testing/main574-public13-editing.mjs` checker was not used. No new checker/framework was introduced.

## Scope and limits

- No App product or test source was modified; the assigned App worktree remains clean.
- No full suite was requested by this worker; no `tsc`, install, frame/PCM, owner-film, pixel, or physical-PCM claim was made.
- No old 7413 run was used.
- The exact central source snapshot was held clean before and after each accepted lane; synthetic snapshot HEAD was not required to equal the declared source SHA.

Runner evidence is under `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-main574-public13-actual-editing-executor/notes/main574-public13-runner/`.
