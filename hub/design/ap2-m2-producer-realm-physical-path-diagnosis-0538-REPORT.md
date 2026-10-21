# App producer realm-root physical-path diagnosis — 0538

## Result

Diagnosed `23729` as a real launch-environment failure before producer traffic.
The existing Runtime symlink guard is correct. I prepared one minimal wrapper-only
candidate in `scripts/testing/run-producer-public13-list.sh`; no Runtime, Agent,
Provider, harness body, test, helper, config, selector, timeout, executable,
schema, pin, graph, or source checkout was changed.

The original producer case was **not rerun**. No producer body, browser, build, or
local socket was run by this worker. The next execution remains blocked until an
independent custody review, candidate source preflight, and one central
startup-only smoke are complete.

## Exact first cause and path chain

Retained central result:

- Test `ap2-m2-producer-final-reviewed-run-one-case-0532-ap2-m2-producer-run-mode-closed-repair-0524-actual-1021053231-23729`
- one test collected, zero passed, one failed; exit 1
- first failure: `DirectHarness.startRuntime` at `python -m runtime_protocol.cli start`
- Runtime response: `startup_error: realm root must not traverse a symlink`
- producer body count: 0

The launch chain is deterministic from the existing runner and harness:

1. `run-producer-public13-list.sh` creates a physical short `/tmp/tla-XXXXXX`
   and passes its `a` child as `APP_ROOT`; `a` is a symlink to the App checkout.
2. The existing public13 runner creates
   `$APP_ROOT/.public13-effective-ordinary/{agent,runtime,node-modules,tmp,npm-cache,pw-cache,browser-output,vite-cache}`.
3. It exports `TMPDIR=$APP_ROOT/.public13-effective-ordinary/tmp`.
4. The existing harness executes
   `this.tmp = mkdtempSync(path.join(tmpdir(), 'astrid-direct-'))`.
5. Therefore the original realm and support paths were lexically under
   `/tmp/tla-XXXXXX/a/.public13-effective-ordinary/tmp/astrid-direct-<suffix>`;
   the `a` component traversed the deliberate App symlink.
6. The harness then derived `realmDir`, `supportDir`, `credentialPath`, and
   `auditPath` from that same `this.tmp`.

The exact non-secret Runtime argv from `DirectHarness.startRuntime` is:

```text
/home/user/work/venv-app2-native/bin/python -m runtime_protocol.cli start \
  --root <TMPDIR>/astrid-direct-<suffix>/realm \
  --support-root <TMPDIR>/astrid-direct-<suffix>/support \
  --port 0 --display-name Direct Journey \
  --door-origin <origin> --door-port <door-port> \
  --door-credential-file <TMPDIR>/astrid-direct-<suffix>/product-credential.json \
  --door-audit-log <TMPDIR>/astrid-direct-<suffix>/door-audit.jsonl
```

The source-main path is the existing App module
`tests/e2e/local/support/harness.ts`, whose `REPO_ROOT` is derived from that
module and whose `startRuntime` implementation is unchanged. Runtime’s exact
source pin `2c4ac180c2220bdad966bc01e95ad230e99ce26a` contains the same
`LocalRuntimeBoundary._validate_path` symlink fence; no guard was removed or
weakened.

## Candidate correction

The wrapper now uses its already-created private physical `$SHORT_ENV_ROOT` as a
dedicated child `TMPDIR` only when the existing forwarder launches the Playwright
list/run command. It verifies that the directory is physical with `realpath`.
The public13 runner’s short App path, `PWTEST_CACHE_DIR`, `npm_config_cache`,
`VITE_CACHE_DIR`, `PLAYWRIGHT_OUTPUT_DIR`, browser executable, Chromium args,
test argv, and timeout remain unchanged. The existing harness still owns and
cleans the same per-run realm/artifact scope and bytes; only the parent path for
that ephemeral carrier is physical.

Candidate identity:

- App HEAD: `17d2518c341c47a2d8634047b400399886da3a2a`
- App tree: `d63fe4f1e1f32a01acfc9d11cda6c29066fce162`
- approved source ancestry: `00bbc22d63b4abe7275cfe9ad5f3762157d7394f` → current HEAD
- candidate wrapper SHA-256: `329cfca7ff6fcc6764e5eaa6cb53ba77a40e6aa842361d0ed6795ca5b4398352`
- candidate binary diff SHA-256: `5ad2df372cb058dd96a69541cc9343488fcc0630c3645fbc14b8758de37f2ce1`
- immutable original wrapper SHA-256: `87194093b49f09a627074ae6545944f870284e43e5c29f5a6310d9cf00dca4f0`
- existing public13 runner SHA-256: `be59b3da5c01e0df22ec556cc84cd25a2a1a4304cf4542035829003eecb2e75b`
- changed paths versus approved source: only `scripts/testing/run-producer-public13-list.sh`

Frozen body identities remained:

- spec: `d91d0c1cce22f68119cd30fcb0a288346474b0ad4b64c84dcee3b730fa468d89`
- helper: `50cbe5341f24c9a1ecc999018e2c6d975380a3440570abce151f9173c9752016`
- config: `5b880ceff883abce2575a3a85aaa4eda69d3bcb848768ff0e91f337d50cca4c0`
- Agent/Runtime cohort: `8130a401bf44a518d5a40ae274d398b8c560be55` /
  `2c4ac180c2220bdad966bc01e95ad230e99ce26a`
- private graph and Composition identities remain the reviewed
  `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30` /
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.

The immutable original gate/registration was not edited. Any next candidate gate
must bind the new wrapper hash explicitly and retain the existing source/body/
cohort checks; no ancestry was manufactured.

## Evidence run by this worker

Passed:

- `sh -n scripts/testing/run-producer-public13-list.sh`
- `git diff --check`
- source identity, body/tree identity, ancestry, and wrapper-only approved-delta checks
- path audit: old realm chain crossed only the deliberate App alias; fixed realm
  carrier was physical and symlink-free
- Runtime source-seam probe using `LocalRuntimeBoundary._validate_path` and
  `RealmStore.initialize`: planted symlink negative refused; real physical private
  root positive accepted
- nonblocking browser lock inspection: available (`flock` exit 0)
- disk floor: approximately 14.3 GiB available at final inspection

The path audit measured a representative old lexical `TMPDIR` length of 60 bytes
versus 25 bytes for the physical short carrier. The short browser cache/output
paths remain bound to the public13 run root; the browser’s OS temp/profile carrier
is now the equally short physical temp root.

Nested-path audit result:

| Consumer | Existing path after candidate | Result |
| --- | --- | --- |
| Runtime realm, support, credential, audit, harness source/artifact roots | `<physical-short-TMPDIR>/astrid-direct-<suffix>/...` | physical, private, same harness scope |
| Runtime/Agent checkout and private node-modules | `<short-App-alias>/.public13-effective-ordinary/{runtime,agent,node-modules}` | unchanged short import paths; not passed as realm/support roots |
| Playwright output and PWTEST/npm/Vite caches | `<short-App-alias>/.public13-effective-ordinary/{browser-output,pw-cache,npm-cache,vite-cache}` | unchanged, runner-owned and cleaned |
| XDG cache/config | `<physical-short-root>/{xdg-cache,xdg-config}` | unchanged, physical |
| Chromium executable/options | `/opt/pw-browsers/chromium-1194/chrome-linux/chrome` plus existing `chromiumArgs` | unchanged |

Thus the candidate changes only the existing harness temp carrier. It does not
canonicalize, copy, or substitute the Agent/Runtime source graph, browser
executable, Composition package, provider, or evidence output path.

The central startup-only smoke was **not run**: the test service has no registered
startup-only command for this existing DirectHarness, and a local daemon/socket
run is explicitly out of scope. Source-only checks are not claimed as startup
proof. No actual producer execution is authorized from this report alone.

## Remaining prerequisites and unchanged callers

Before any producer actual:

1. Independent custody review must approve the exact candidate wrapper diff/hash
   and verify all frozen source/body/cohort/graph identities.
2. Run the candidate wrapper’s complete source preflight from a clean central
   snapshot; the current worker is intentionally dirty only because it contains
   this candidate.
3. Run one central startup-only smoke through the existing DirectHarness with the
   physical child `TMPDIR`, real daemon health, and teardown, with no producer
   action/body and no browser/build if the existing smoke seam permits it.
4. Recheck the browser lock, disk floor, two-copy limit, read-only shared graph,
   exact argv, and test count immediately before any separately authorized actual.

Existing callers and their frozen assertions are unchanged. The registered
producer entries still point at their prior immutable keeper/wrapper hashes; the
candidate requires a new explicit registration/gate binding. No shared harness
edit or HOME-owner seam is required by the diagnosis; no concurrent shared edit
was made.

## Commands not run

No original producer actual, no producer body, no build, no browser, no full suite,
no local socket/daemon startup, no install, and no shared dependency/cache/venv
mutation were performed.
