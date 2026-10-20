# AP2 M2 public13 effective build attachment fix

## Result

The App product tree is unchanged at committed `01230a5657853be85745566542af6546d254c28c` (central snapshot tree `c4965a7f5fe818a1cf2f6cb091ec4ff93fcde64a`). The fix is an external central runner artifact only:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-public13-effective-build-attachment-fix/public13-integration-runner.sh`

Runner SHA-256: `40c25724b502ce5582caf04c6ebf44ab89a509b5f3d629876d599f57c3e5fa7a`.

The runner now:

- verifies frozen Agent `8130a401bf44a518d5a40ae274d398b8c560be55` / tree `236c3e57e0265c52b81ba8085de3193026176bff` and Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a` / tree `7ab412cc4bcbe517efcfa806e092336390312e18`;
- builds one private per-run package graph, copies only `@banodoco/timeline-composition` into it, and leaves the locked graph and shared installs read-only;
- attaches that graph to the App root, Agent root, and Agent `remotion` root;
- asserts App and SDK `createRequire` plus Vite resolution, package version `0.0.13`, package/evaluation hashes, and the real `clipOpacity` export before `npm run build:hosted`;
- uses the validated read-only `venv-app2-native` interpreter for both Agent and Runtime;
- restores the original App `node_modules` symlink and removes every private run path via `trap` cleanup.

## Evidence

Static checks passed:

```text
sh -n .../public13-integration-runner.sh
git status --short --untracked-files=all       # clean; no product changes
```

Central build-only preflight passed:

```text
public13-effective-build-preflight-1020185825-29195
exit 0, 80s
```

It logged both App and SDK resolution to the private package path, version `0.0.13`, tarball SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, and a successful hosted Vite build.

The first ordinary replacement (`...1020185958-25195`) was setup-aborted before browser launch because the initial runner revision named nonexistent `venv-agent`/`venv-runtime` paths. It was not treated as product evidence. After correcting those external paths to the validated `venv-app2-native`, the one justified replacement run was:

```text
public13-effective-ordinary-integration-1020190207-4949
exit 1, 79s
```

Its hosted build passed and the source tuple was correct, including Agent `8130...`, Runtime `2c4...`, and all three contract digests. The journey then failed before any product interaction at Chromium launch: `browserType.launch: Target page, context or browser has been closed`, with Chromium exiting `SIGTRAP`. No additional browser rerun was made.

## Disposition

Composition resolution/build failure is fixed and centrally verified. The ordinary browser journey remains unverified because of the central Chromium launch failure. The original App symlink was restored after both runs; no shared node_modules, venv, or product dependency was modified. Follow-up: repair the central Chromium launch environment, then rerun the already-passed build/resolution guard and the ordinary journey under the orchestrator’s retry policy.
