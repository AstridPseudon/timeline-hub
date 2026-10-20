# Executed from /home/user/work/wt/vw-m3-app-pcm13-implementation-brief
O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
W="$O/workers/vw-m3-app-pcm13-implementation-brief"
P=proposals/app-continuous-pcm13
N="$W/fixture/node_modules"
python "$P/stage.py"
# PASS: archive SHA256 verified, all 77 public13 members extracted, 8 App files read.
PCM_BASELINE=1 node "$P/stage.mjs"
node "$N/vitest/vitest.mjs" run --no-cache --configLoader=runner --maxWorkers=1 --config "$W/fixture/vitest.config.mjs" continuousPCM.contract.test.tsx compiledAudioSourceClock.test.ts > "$W/red.log" 2>&1
# exit 1: 19 passed / 5 failed (required positive and four forgeries).
node "$P/stage.mjs"
node "$N/vitest/vitest.mjs" run --no-cache --configLoader=runner --maxWorkers=1 --config "$W/fixture/vitest.config.mjs" > "$W/green-final-public13.log" 2>&1
# exit 0: 3 files / 41 passed, 5.39s, verified public13 export-map resolution.
node "$N/eslint/bin/eslint.js" --no-cache --no-config-lookup --config "$P/eslint.config.mjs" "$P/AudioTrack.tsx" "$P/"*.test.tsx "$P/"compiledAudioSourceClock*.ts
# exit 0: scoped TypeScript/browser/hooks rules, not the complete App lint configuration.
# From the tiny exact-base port-check directory:
# cwd=$W/port-check
git apply --check /home/user/work/wt/vw-m3-app-pcm13-implementation-brief/proposals/app-continuous-pcm13/consumer.patch
# exit 0; no patch applied to App.
