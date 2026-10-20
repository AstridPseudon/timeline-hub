# App M2 final-root parent-split browser source

## Result

Staged the approved current-root parent clip-split consumer and one deferred current013 browser qualification lane on base `b1ef4b9b910ba72375c34cf319692f90d22edc25`.

The final uncommitted source tree is `bcb885e3ae9dc54a6eaa69e5ee95b354bf05b894`. The 16 product/test/fixture paths in the approved split delta are byte-identical to `tl/app-m2-main17-parent-split013-source-port` at `30b63a28a8ef339becae27549191755192f3106a`. The b1 live label-policy files were left unchanged. No older split pins, root-cohort changes, writer deletion, deletion ledger, or fallback-after-capture path was imported.

## Source and browser lane

Product source ports the approved single raw-parent `clip.split` cohort:

- raw parent/config mirror validation and literal `parent/clip:<id>` binding;
- one reserved right ID carried through capture, finish, retry and recovery;
- exact opaque row values, registry reads, rational frame/source-window behavior, closure/selection guards and atomic preview;
- current hook/SDK/session routing, persisted outbox retry, Runtime undo path;
- unsupported shapes remain on the established pre-capture route; native capture errors do not fall back to snapshot writing.

Added source-only current013 controls:

- `playwright.clip-split.config.ts`;
- `scripts/testing/current013-parent-split.mjs` and its no-browser launcher-control test;
- `tests/e2e/local/clip-split-command.spec.ts` (477 lines, under the 500-line limit).

The staged browser case uses current 0.2.13/S2, Agent `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`, Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, public Composition 0.0.12, current013 source preflight, the existing three-products harness, tracked public bundle and manager-owned overlay/short temp inputs. It drives real UI split into two raw halves, checks exact opaque/registry/parent-config/shot/internal closure, reloads, restarts Runtime, retries the exact persisted request/key, performs Runtime inverse undo, asserts renderer-off and zero legacy publisher traffic, and includes one direct-neighbor write producing a real 409 with the captured draft retained across reload. No exhaustive matrix is added.

Cache identity for the eventual central run is:

`parent-split-treebcb885e3ae9dc54a6eaa69e5ee95b354bf05b894-agentd8749a9ce12a699672faf3ad96b4e4cbea9245c2-runtime2c4ac180c2220bdad966bc01e95ad230e99ce26a-client13-public12-0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3-runner041583a150d0e883ff2ecbb03582a9aef4d116c50cdc134c111d95c389e567c4-helper82ff12281994e3bce006d643fc2b090ef356784c6854b959e82c87caf3347901`

## Targeted evidence

- `node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-main17-parent-split013-source-port/notes/runner.cjs node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-main17-parent-split013-source-port/notes/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism [13 split/session/neighbor files]` — PASS, 13 files / 712 tests.
- `node --experimental-vm-modules scripts/testing/current013-parent-split.test.mjs` — PASS, 5/5 launcher-control tests.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-main17-parent-split013-source-port/agent-d874 /home/user/work/venv-agent/bin/python src/tools/video-editor/commands/fixtures/clip_split_parity.py` — PASS, 1/1 native command/record/output/inverse/redo.
- Scoped ESLint over the 16 split product paths, browser spec and launcher test — PASS, zero diagnostics.
- `git diff --check` — PASS.
- Source audit — PASS: all 16 approved split paths byte-equal to the reviewed source candidate; b1 label-policy files unchanged.

Not run by instruction: browser, localhost/socket, Runtime live acceptance, full suite, build, tsc/typecheck, install, or central test-service request. Therefore actual UI acceptance, process restart in a browser, real 409 preservation, exact retry over the live Runtime and zero legacy traffic remain unverified.

## Decisions and future central command

I retained the current b1 root and only applied the approved split delta; the source review explicitly approved this delta after independent review, while qualifying it only at a later current-root gate. I did not retire `splitClipAtPlayhead` because its unsupported-shape branch is still required before native capture. No merge or deletion claim is made.

After the manager confirms the current root is green, run centrally with manager-supplied SHORTTMP, tracked public bundle and own overlay paths:

`env -u ASTRID_PUBLIC_CHECKOUT -u ASTRID_APP_DIRECT_DIST NODE_PATH=<manager-overlay> TIMELINE_CURRENT013_SHORT_TMPDIR=<manager-shorttmp> TIMELINE_CURRENT013_RUN=1 TIMELINE_CURRENT013_APP_TREE=bcb885e3ae9dc54a6eaa69e5ee95b354bf05b894 TIMELINE_CURRENT013_AGENT_SHA=d8749a9ce12a699672faf3ad96b4e4cbea9245c2 TIMELINE_CURRENT013_RUNTIME_SHA=2c4ac180c2220bdad966bc01e95ad230e99ce26a TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT=<runtime-producer> ASTRID_CHECKOUT=<agent-d874> ASTRID_RUNTIME_CHECKOUT=<runtime-013> ASTRID_PYTHON=/home/user/work/venv-agent/bin/python ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python TIMELINE_BUNDLE_AGENT_HEAD=d8749a9ce12a699672faf3ad96b4e4cbea9245c2 TIMELINE_BUNDLE_RUNTIME_HEAD=2c4ac180c2220bdad966bc01e95ad230e99ce26a TIMELINE_CURRENT013_CACHE_ID=<cache-identity> node scripts/testing/current013-parent-split.mjs`

Do not schedule this browser command before manager-root qualification. Do not claim consumer deletion until this real gate proves the listed acceptance and the required zero-legacy boundary.

