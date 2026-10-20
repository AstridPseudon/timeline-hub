# Current-default smoke review

## Verdict

**APPROVE** — `tl/vw-m4-smoke-current-default` is correct and minimal for the requested fix.

The only product delta versus `46bd700b2` is `scripts/smoke-package.mjs`: it reads the version from the `package.json` located relative to the script URL and uses that version for the default tarball name. The explicit positional tarball argument remains unchanged. No other source or product files changed.

Review source: Git `7301badb7a38520d29202bde349b09c3364bc176` (`fix(composition): resolve smoke tarball from package version`). Central snapshot tree: `99148b72ed957e79753c263120f7d4cc5e284fba`.

## Checks

- `node --check scripts/smoke-package.mjs` — PASS.
- `git diff --check 46bd700b2` — PASS.
- Default missing-path check, from `/tmp` with no argument — exit 1 as expected; tar attempted `/tmp/banodoco-timeline-composition-0.0.12.tgz`, proving the version is `0.0.12` from the script-relative package metadata rather than a cwd package.
- Explicit `0.0.10` override — the real tar command received the supplied absolute `banodoco-timeline-composition-0.0.10.tgz` path and listed the valid archive. The local sandbox then returned `EPERM` from Node `spawnSync` before the temporary npm stop-hook could run; this is a local process-execution limitation, not a product failure. The central package smoke below exercised the complete path.
- Invalid-path comparison against the baseline script from `46bd700b2` — both exit 1 with the same tar diagnostics (`Cannot open: No such file or directory`, child status 2, unrecoverable). Only expected Node source-location/PID metadata differs.
- `git status --short --branch` after cleanup — clean; no build output or private dependency link remains in the worktree.

## Central evidence

Before requesting the suite, `node_modules` in this private worktree was a symlink to the clean shared `/home/user/work/composition/node_modules`; the shared dependency tree was only read. It was removed after the request. No App or scenegraph tree was touched.

Command requested exactly once:

```text
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test vw-m4-current-default-final-review viewing-current-default-smoke) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Result: **PASS**, exit 0 in 7 seconds. Suite command:

```text
env PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH npm_config_cache="$PWD/.npm-cache-viewing-current-default" sh -c 'npm run build && npm pack --ignore-scripts && npm run test:package'
```

The isolated consumer smoke passed, including plain Node ESM, bundled render, scoped host capability/override, shared theme/peer identity, TypeScript declarations, dependency identity, and installed-package immutability. The central log reports package version `0.0.12`, filename `banodoco-timeline-composition-0.0.12.tgz`, 77 files, 58.4 kB package size, and successful `test:package`.

## Artifact

The retained/generated public-12 tarball is exactly 77 members and 58,444 bytes:

```text
sha256 0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3
```

All available `banodoco-timeline-composition-0.0.12.tgz` copies checked in the orchestration scratch space have that same SHA-256. The central pack used the same filename, version, 77-file count, and package size; no npm pack format change was observed, so the immutable artifact was not rewritten.

## Isolation and follow-up

No local install, network access, browser, socket, render, git mutation, push, or product edit was performed. The central suite’s consumer install ran in its own temporary consumer with its private npm cache, as specified by the suite. Recommended next step: merge the approved minimal script delta.
