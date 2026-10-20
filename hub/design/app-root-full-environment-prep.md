# App post-root full-suite environment

Prepared, but did not register or launch, the one manager-owned App full after the cold-start fix. The historical `app-current-full-25523-classification.md` result is not reused: it qualified only the old standard8 tuple, not Root12/Runtime013 or the tracked public browser source.

## Candidate captured here

This worker started from the current cold-start-fixed App candidate:

| Input | Identity |
| --- | --- |
| App | commit `05b6b488d1834650c459c5c565f2530d9bea20e9`, tree `00e9e2a92d80ee103a94fab1d976babe3ca918e1` |
| Composition | root/lock `file:vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz`, archive SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, 77 regular files |
| Runtime lock | source commit `2c4ac180c2220bdad966bc01e95ad230e99ce26a` (Runtime013), producer SHA256 `6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`, lock SHA256 `550de9dc3269380c79f44a6db4c87a5d5459058d550ae49e635a6dda809e76a2` |
| Tracked browser source | `vendor/astrid-browser`, `ASTRID_PUBLIC_CHECKOUT` unset; provenance Agent commit `680d1aa4f1f9576d65a603472f1dd7fc0ae9ccd1`, tree `07ce61f24ec38a1a60c4a981b6bd666f4971bd67`, 155 files, source-set SHA256 `fe380bc3280b1f5efa7ecde7cc55a5415a498f2b35af8fb693d11123aa289a28` |
| Private dependency graph | read-only `/tmp/app-coherent-deps12/node_modules`; Composition 77/77 bytes and React `18.3.1`, React DOM `18.3.1`, Remotion/Player/Three/Layout Utils/Media `4.0.509` checked |

The future official Agent checkout/commit is intentionally not guessed here. The manager must bind it literally in the registration below and rerun the wrapper on the post-merge App tree. The tracked public bundle identity above is the source used when `ASTRID_PUBLIC_CHECKOUT` is absent; it is not a substitute for naming the manager’s official Agent source freeze.

## Reusable wrapper

Wrapper: [`notes/app-root-full-environment.sh`](/home/user/work/wt/app-m3-root-full-environment-prep/notes/app-root-full-environment.sh)

SHA256: `ff8f75f430ea3cba403e4634d623a5c3f4f00d30342874e1a42b6190de186af2`

The wrapper is a test-service snapshot helper, not product code and not `bin/test-run`. It:

- verifies the immutable public12 archive and all 77 installed files plus fixed peers;
- replaces only the snapshot’s ignored `node_modules` symlink (if present) with an owned root/scopes overlay whose package entries point read-only at private12; it owns `.vite`, `.vite-temp`, Vitest/npm/XDG/TMP caches and restores the original dependency symlink on exit;
- unsets `ASTRID_PUBLIC_CHECKOUT` and `ASTRID_APP_DIRECT_DIST`, uses the tracked `vendor/astrid-browser` fallback, the existing preload, `--configLoader=runner`, and `--no-cache`;
- records App HEAD/tree/status, sparse-checkout state, package/lock/artifact hashes, Runtime lock tuple, tracked public bundle identity, and any explicitly supplied Agent/Runtime checkout HEAD/tree/status before and after;
- refuses full mode unless the manager supplies literal Agent and Runtime commit/tree pins and exact checkouts, and never runs full mode without `TIMELINE_ROOT_FULL_MANAGER_APPROVED=1`.

There is no sparse checkout or source symlink mutation. The preflight used the existing worktree only to exercise the wrapper; its shared `node_modules` symlink was restored to `/home/user/work/app/node_modules` and no shared cache or dependency bytes changed.

## Bounded offline preflight

Exact command (from the candidate root):

```sh
LOG=/tmp/app-root-full-preflight4.mGxC6G
TIMELINE_ROOT_FULL_LOG_DIR="$LOG" \
TMPDIR="$LOG/tmp" \
npm_config_cache="$LOG/npm-cache" \
VITEST_CACHE_DIR="$LOG/vitest-cache" \
XDG_CACHE_HOME="$LOG/xdg-cache" \
./notes/app-root-full-environment.sh preflight
```

The wrapper’s preflight subprocesses use `env -u ASTRID_PUBLIC_CHECKOUT -u ASTRID_CHECKOUT`, the tracked browser bundle fallback, private12 overlay, the preload, `--configLoader=runner`, `--no-cache`, and maxWorkers=1. Results:

| Check | Result |
| --- | ---: |
| Package identity, public exports, shared peers (`node config/vite/timelineCompositionPackage.test.mjs`) | 9 passed |
| Actual public scene/media evaluation (`TimelineComposition.media-conformance.test.tsx`) | 19 passed |
| Native/session controls (`commitSession.test.ts` + `TrackLabel.command.test.tsx`) | 127 passed |
| Total | **155 passed, 0 failed** |

The wrapper’s before/after identity snapshots compare equal. No full suite, build, browser, socket/server, install, or project TypeScript check was run. No full request was submitted.

## Manager-only full registration template

This is a literal named registration template, intentionally not added to the central suite allow-list and not executable until the manager replaces every `<...>` with final post-merge values. The suite name is fixed and does not follow a moving checkout:

```text
# Name: full-m3-root-integration
# Bind only after the root merge and final Agent source freeze are published.
app full-m3-root-integration env \
  TIMELINE_ROOT_FULL_MANAGER_APPROVED=1 \
  TIMELINE_ROOT_FULL_APP_SHA=<FINAL_APP_COMMIT_40_HEX> \
  TIMELINE_ROOT_FULL_APP_TREE=<FINAL_APP_TREE_40_HEX> \
  TIMELINE_ROOT_FULL_AGENT_SHA=<MANAGER_NAMED_OFFICIAL_AGENT_COMMIT_40_HEX> \
  TIMELINE_ROOT_FULL_AGENT_TREE=<MANAGER_NAMED_OFFICIAL_AGENT_TREE_40_HEX> \
  TIMELINE_ROOT_FULL_RUNTIME_SHA=2c4ac180c2220bdad966bc01e95ad230e99ce26a \
  TIMELINE_ROOT_FULL_RUNTIME_TREE=<FINAL_RUNTIME013_TREE_40_HEX> \
  ASTRID_CHECKOUT=<MANAGER_NAMED_OFFICIAL_AGENT_CHECKOUT_ABSOLUTE> \
  ASTRID_RUNTIME_CHECKOUT=<FINAL_RUNTIME013_CHECKOUT_ABSOLUTE> \
  TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT=<FINAL_RUNTIME013_PRODUCER_CHECKOUT_ABSOLUTE> \
  PRIVATE12_NODE_MODULES=/tmp/app-coherent-deps12/node_modules \
  TIMELINE_SNAPSHOT_PRELOAD=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs \
  bash notes/app-root-full-environment.sh full
```

The manager must also bind the final App SHA/tree in the central snapshot’s source registration and verify that the Runtime checkout HEAD/tree, Runtime013 lock, producer manifest, public12 artifact, and official Agent checkout are the same tuple in the wrapper’s `full-before.json` and `full-after.json`. The full subprocess is the required `npm test -- --maxWorkers=2`; the wrapper adds the required Vitest hygiene flags `--configLoader=runner --no-cache` and owns the cache/preload boundary. After registration, the manager may request exactly one `full-m3-root-integration` run using the central test service, after merge; this worker did not request it.

