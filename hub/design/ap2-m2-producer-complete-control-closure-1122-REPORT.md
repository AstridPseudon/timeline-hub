# AP2 M2 producer complete control closure — 1122

## Result

The product worktree is unchanged and clean. I restored the omitted existing
control dependency, validated the exact 1113 artifact closure, recovered the
1113 report and handoff outside the App repository, and exported the command
closure for MAIN:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-producer-complete-control-closure-1122-command.tar.gz`

SHA-256:

`6983e1f08fe9207faacefe79494300a6ded3c55272a36f85363deeb95c6645d5`

The task is blocked at the single authorized preflight. The first mismatch is
the existing custody gate's line 66: the MAIN keeper has no
`node_modules` symlink. Per the run rule, I did not run the five controls or
retry the preflight.

## Bound source

- App source: `5863411a8c2400db719b5385002b05af0a2b3891`
- Source tree: `31b0f77c6ef4e9fdbeff3e4f88cc4705f0891e89`
- Source parent: `b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7`
- Strict baseline: `17d2518c341c47a2d8634047b400399886da3a2a`
- Ancestry check: `5863411a → b8cc7e1c → 17d2518c` (PASS)

The retained binding readback remains `51` hash guards, `20` path guards,
`1` version guard, and reverse binding `PASS`. The exact existing
`launch-tool-stub.py` was copied from 0945; its SHA-256 is
`4299795135db4be3b83b41d9034cb1519b529925865222f9af866029df9264b7`, matching
both 0935 and 0945. All eight rebound artifacts were copied byte-for-byte
from the 1113 packet and retained mode `0755`.

## Harness dependency inventory

The durable archive contains `outer-controls-run.py`, the exact
`launch-tool-stub.py`, and these eight existing chain artifacts:

1. `producer-startup-custody-gate-0717-owned.sh`
2. `producer-physical-keeper-gate-0717-owned.sh`
3. `producer-runner-0717-owned.sh`
4. `producer-public13-runner-0717-owned.sh`
5. `producer-startup-only-gate-0717-owned.sh`
6. `producer-startup-only-probe-0717-owned.mts`
7. `producer-startup-module-format-probe-0717-owned.mts`
8. `producer-retain-failure-artifacts-0753.sh`

The full harness closure also includes these existing external inputs and
invoked files, which were checked by inventory but not copied into the App
tree:

- `tests/suites.conf`, the original integration registration line;
- MAIN keeper `/home/user/work/wt/app-pin-5863411a`, its `KEEP` marker, and
  the three guarded source files plus `package.json` and Playwright config;
- `tests/e2e/local/support/harness.ts`, imported by both startup probes, and
  its direct project import `config/vite/projectElementSelection.ts`;
- the producer test's direct imports: `tests/e2e/local/support/app.ts`,
  `tests/e2e/local/support/producer-ownership-current-pin.ts`,
  `src/tools/video-editor/dev/scene-phase-markers/extension.ts`,
  `src/tools/video-editor/dev/transcript-lane/extension.ts`, and
  `src/sdk/video/timeline/sourceMap.ts`;
- Playwright config dependency `playwright.direct.config.ts`;
- the locked graph directory and its archive, frozen Agent and Runtime
  repositories, and the existing shared App install;
- the existing `venv-app2-native`, `/opt/pw-browsers`, private temp/cache
  roots, and the fixed browser lock path used by the retained runner.

The stub provides the control-only launch boundary for `git`, `node`, `npm`,
`flock`, `sh`, `mktemp`, `cp`, and the Playwright child. It is not new logic.

## Validation and run evidence

Passed before the authorized run:

```text
inventory: exactly 8 chain files; all 8 match 1113 originals
stub: exact match to 0935 and 0945; mode 0755
binding readback: 51 hash / 20 path / 1 version; reverse PASS
python -m py_compile outer-controls-run.py launch-tool-stub.py: PASS
sh -n artifacts/*.sh: PASS (6 files)
node --check both .mts probes: PASS
```

Authorized preflight, invoked once:

```sh
cd /home/user/work/wt/app-pin-5863411a && \
  sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-complete-control-closure-1122/artifacts/producer-startup-custody-gate-0717-owned.sh preflight
```

Result: exit `1`, empty preflight log. Read-only replay of the ordered gate
checks identifies the first mismatch as:

```text
producer-startup-custody-gate-0717-owned.sh:66
test "$(readlink "$KEEPER/node_modules")" = /home/user/work/app/node_modules
actual: /home/user/work/wt/app-pin-5863411a/node_modules does not exist
```

The keeper identity, tree, clean status, source hashes, artifact hashes, and
KEEP marker were otherwise present. The current shell reports Node `v22.22.0`;
MAIN's Node `20.19.4` compatibility is not proven. No browser, build, install,
full suite, socket, daemon, service, actual producer registration, or five
controls ran. Five-control result is `0/5` (not reached), not a pass claim.

Original 19080/failure packets and prior worker records were not modified.

## Next step

MAIN must provide or restore the already-approved keeper `node_modules`
symlink to `/home/user/work/app/node_modules` without installing or mutating
the shared dependency. Then a fresh worker may perform the one remaining
authorized preflight/control attempt; this worker must not retry it.
