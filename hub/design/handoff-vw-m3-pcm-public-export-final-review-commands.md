# Exact review commands and results

```sh
# Reviewed tree: af98594dce80c0350a1fc21dfc44839b2279edf1; parent e80c46baf.
# cwd: /home/user/work/wt/vw-m3-pcm-public-export-final-review
# Node v22.22.0; TypeScript 5.9.3; dependencies read only.
P=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-pcm-public-export-final-review
W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-pcm-public-export-final-review
export TMPDIR="$W/tmp"
export TSX_DISABLE_CACHE=1
python3 "$P-audit.py" before
# exit 0: private physical graph matches provisioning manifest (35,545 entries),
# snapshots 26 loose 0.0.11/12 archives, 3 sidecars, 11 repository pin/manifest files.
# The audit creates only our real node_modules scopes and read-only leaf links.
node node_modules/typescript/bin/tsc -p typescript/tsconfig.test.json
# exit 0; -check1.log
node --experimental-test-isolation=none --import ./typescript/tests/register-extensionless.mjs --test typescript/test-dist/tests/audio-envelope-admission.test.js typescript/test-dist/tests/evaluation.test.js
# exit 0: 16 passed, 0 failed, 0 skipped; -check2.log
node --import tsx scripts/gen-registry.ts --check
# exit 0; -check3.log
node scripts/build.mjs
# exit 0; -check4.log
# Copy flat -public-types.mts and -public-types.tsconfig.json to $W/public-types.*.
# $W/node_modules/@banodoco/timeline-composition points to reviewer worktree.
node node_modules/typescript/bin/tsc -p "$W/public-types.tsconfig.json"
# With skipLibCheck:true, exit 0; -check5-scoped.log. Existing proposal setting.
# Initial stronger skipLibCheck:false run exits 2 (-check5.log):
# dist/lib/audio-envelope.d.ts(1,35): TS2307 './audio-curves.generated'.
node "$P-public-probe.mjs"
# exit 0; -check6.log; advertised export-map resolution, peer-denying loader,
# browser/timer traps, valid record and four forgeries.
# Baseline diagnosis: read/extract the EXISTING public12 tar into
# $W/baseline-types/node_modules/@banodoco/timeline-composition, link read-only
# dependency leaves with real scope parents; no pack/install. Use flat
# -existing-types.mts and a strict NodeNext/noEmit/skipLibCheck:false config.
node node_modules/typescript/bin/tsc -p "$W/baseline-types/existing-types.tsconfig.json"
node node_modules/typescript/bin/tsc -p "$W/existing-types.tsconfig.json"
# Both exit 2, identical sole TS2307 for './audio-curves.generated'.
# -strict-baseline-final.json and -strict-*-final.log retain commands/output.
# Initial immutable12 diagnostic lacked peer links as well (-strict-immutable12.log);
# corrected private baseline peer overlay removes those setup errors.
python3 "$P-audit.py" after
# exit 0: graph, all discovered archives/sidecars and all 11 files identical.
git diff HEAD^ HEAD --name-only
git diff HEAD^ HEAD -- typescript/src/lib/audio-envelope.ts typescript/src/lib/use-audio-envelope.ts typescript/src/types.ts package.json package-lock.json
git show HEAD^:typescript/src/lib/audio-envelope.ts | sha256sum
sha256sum typescript/src/lib/audio-envelope.ts
# Both edbf7f270a6291459a7951f0ffafe38d2e2757197ba900edf3be42b3af51fddc.
git apply --reverse --check "$P.patch"
git diff --check
git status --short
# All exit 0; final status empty after private node_modules/dist/test-dist removal.
# Exact proposal patch and flat source copies verified byte-identical to producer.
```
