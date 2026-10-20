# Exact successful verification commands

Cwd: `/home/user/work/wt/vw-m3-pcm-admission-public-export-proposal`.
Node `v22.22.0`; clean graph TypeScript `5.9.3`, tsx `4.21.0`, esbuild `0.27.7`.
The local overlay contains real scope directories and leaf symlinks only. It was removed after verification. No dependency installation or shared writes.

```sh
cd /home/user/work/wt/vw-m3-pcm-admission-public-export-proposal
W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-pcm-admission-public-export-proposal
P=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-pcm-admission-public-export-proposal
export TMPDIR="$W/tmp"
export TSX_DISABLE_CACHE=1
python3 "$P-setup-overlay.py"
node "$P-prerequisite.mjs"
node node_modules/typescript/bin/tsc -p typescript/tsconfig.test.json
node --experimental-test-isolation=none --import ./typescript/tests/register-extensionless.mjs --test typescript/test-dist/tests/audio-envelope-admission.test.js typescript/test-dist/tests/evaluation.test.js
# 16 pass (7 new + 9 existing); targeted-final.log
node --experimental-test-isolation=none --import "$P-file-stdio.mjs" --import ./typescript/tests/register-extensionless.mjs --test typescript/test-dist/tests/animations.test.js typescript/test-dist/tests/clip-opacity.test.js typescript/test-dist/tests/evaluation.test.js typescript/test-dist/tests/registries.test.js typescript/test-dist/tests/scene-diagnostics.test.js typescript/test-dist/tests/scene-evaluation.test.js typescript/test-dist/tests/theme.test.js typescript/test-dist/tests/transition-policy.test.js typescript/test-dist/tests/transition-spans.test.js scripts/gen-registry.test.mjs
# 69 pass; existing69-file-stdio.log
node --import tsx scripts/gen-registry.ts --check
node scripts/build.mjs
node node_modules/typescript/bin/tsc -p "$W/public-types.tsconfig.json"
node "$P-public-probe.mjs"
python3 "$P-graph-check.py"
git diff --check
git apply --reverse --check "$P.patch"
```

All commands above exit 0. The two build commands are the exact registry-check and build-script steps of `npm run build`. No pack, archive or install was run. The private NodeNext type probe uses `$W/node_modules/@banodoco/timeline-composition` pointing to this worktree; its complete source is the adjacent `-public-types.mts`.

The flat patch also passed `git apply --check "$P.patch"` from `$W/patch-check`, a minimal private baseline containing the original `typescript/src/evaluation.ts` from `git show HEAD:typescript/src/evaluation.ts` and an empty `typescript/tests/` directory.

The initial default-isolation Node 22 and Node 20 attempts are retained as `-targeted.log`, `-targeted-node20.log`, `-existing69.log`, and `-existing69-node20.log`. They are **not qualification**: isolation reported only per-file passes and the existing registry test failed because captured child pipes returned `EPERM`/empty stderr. The final runner uses `--experimental-test-isolation=none`; the private `-file-stdio.mjs` adapter substitutes private regular-file descriptors for captured subprocess output, preserving real exit codes and exact stdout/stderr bytes. It changes no test assertions or source under test. New purity tests use inherited stdio and explicitly assert no spawn error.
