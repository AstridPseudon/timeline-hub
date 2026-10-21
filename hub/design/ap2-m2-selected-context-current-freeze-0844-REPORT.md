# AP2 M2 selected current-context freeze

## Result

**KEEP the current selected proof source; actual qualification remains HOLD.**

The HOME correction is present at App `32b74fdea165816226b6f0727a16817a6a1a79c3`
/ tree `a3ddc2997e6460bab77d1e4ef7c1ac98ee21ad65`, integrating
`bc2ee7273b0ace87c2b2f82dd964780dffd6844b`. Its independent custody review
approved the two-file case-local eval-context change. The current harness was
not edited here and remains SHA-256
`1585677bafef583110e86a04a4490a968a8db499b0e9d566c6b890eab228ce6c`.

The only App source edit is
`tests/e2e/local/three-products.selected-param-dev.spec.ts`. It restores the
original selected proof body byte-for-byte from `ba02c8f2`:

```text
SHA-256: 10250fa44db4e2d4423f8d06258105df267e3ba4e29700d700bb1d3182a6def1
```

The pending one-file source tree, computed with a temporary private index, is
`92391f9a57dd38ce327b0a63990725053ea34601`; the eventual commit SHA is left
for the harness/manager to assign. The existing current HOME source commit
`32b74fdea` is its required ancestor. The frozen original keeper remains
clean at `ba02c8f2` / tree `7fe8c15b56da9944ae31e8273d41d3ceb21b3677`, with its
empty `KEEP` marker present.

## Composed delta and callers

The current HOME spec had removed the original 20-second same-origin mount
check, exact selected timeline URL identity, and displayed clip/P1 checks after
both reloads. Those five removed lines of behavior are restored, while the
HOME `expectConnected` replacement is not retained in this selected proof.
The original 90-second semantic ceiling, 240-second worker fixture timeout,
P1/P2 admission and source removal, P1 refusal with dirty draft, lost-ACK
exact request/key retry, restart/reload recovery, inverse/undo, and zero-legacy
POST assertions are all retained unchanged.

Changed live caller: the selected spec only. Existing harness callers remain:

- `seedSelectedParamDev` creates the P1 fixture and now uses the integrated
  case-local endpoint, selected credential FILE, harness realm, and
  `astrid-selected-param` actor through `selectedParamEvalEnv`.
- `advanceSelectedParamAndRemoveSource` admits P2 and removes authored P1/P2
  source while retaining the P1 authority.
- `startSelectedParamDevServer` uses the normal discovery proxy and the
  existing `devOrigin`/product credential FILE path.

No product source, shared helper, timeout, selector/navigation contract,
authority, schema, pin, dependency, auth/grant, or browser bearer changed.

## Cheap complete preflight

The existing 0724 `run-owned-selected-final95.sh` recipe was used once through
one disposable worker-owned copy whose source guard was adjusted only to admit
this pending one-file worktree delta. The copy and its private run root were
removed by EXIT cleanup. Exact command:

```sh
SELECTED_FINAL95_MODE=preflight \
  /tmp/ap2-m2-selected-context-current-freeze-0844-runner.sh \
  /home/user/work/wt/ap2-m2-selected-context-current-freeze-0844
```

Result: **PASS, exit 0**. All 11 preflight checks passed and aggregated no
failures:

- source ancestry/current pending tree and exact original spec bytes;
- Agent `6efc81500a0e0688c2bb41e736503f0fc3e04abb` / tree
  `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`;
- Runtime and producer `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` / tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`;
- 76 artifacts, manifest
  `a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`,
  artifact `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`,
  schema `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`;
- locked Composition `0.0.13`, outer graph archive
  `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`,
  embedded package `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`,
  77 embedded members;
- exact owned graph: Node `v22.22.0`, Vite `5.4.21`, Vitest `4.1.5`,
  Playwright `1.60.0`;
- exact CLI/list command: `node node_modules/playwright/cli.js test
  --config playwright.three-products.config.ts --grep "$TEST_TITLE" --list`;
  one test in one file, title `local DEV selected PARAM uses admitted P1
  through P2 removal, refusal, retry, reload and undo`;
- case-local child context: endpoint is the Runtime `discovery.endpoint`,
  realm is `this.realmId`, actor is `astrid-selected-param`, and both
  `ASTRID_TIMELINE_EVAL_CREDENTIAL` and `ASTRID_RUNTIME_CREDENTIAL` point to
  the 0600 `selected-agent-credential.json` FILE under the harness tmp root;
  normal discovery uses `ASTRID_WORKSPACE_DISCOVERY` and the existing proxy,
  while `ASTRID_RUNTIME_OPERATION_ORIGIN` is the same-origin `devOrigin` and
  the browser receives only `WORKSPACE_RUNTIME_TOKEN_FILE`;
- physical child paths are short, absolute, and non-symlinked for this
  worktree, the shared App install, and the locked graph node_modules;
- wrong role/tree/pin/path/argv/zero-test and wrong artifact-version refusal
  controls;
- nonblocking browser lock available; `/tmp` and `/home/user/work` each had
  `14019144` KiB free (above 10 GiB); one App overlay copy only.

The following were deliberately not run: browser, build, daemon, localhost or
live socket, actual selected case, full suite, install, or central test
service. The prior 0730 central result remains a first-hand **HOLD** at the
Runtime handshake (`unauthorized: invalid bearer credential`) before any
selected behavior assertion; it is not relabeled by this source freeze.

Additional checks:

```text
./node_modules/.bin/eslint --no-cache --max-warnings 0 \
  tests/e2e/local/three-products.selected-param-dev.spec.ts       PASS
git diff --check                                                   PASS
node --check scripts/runtime-discovery-proxy.mjs                  PASS
```

## Closed selected-role binding proposal (not applied)

The shared helper remains byte-identical and read-only. Its current whole-file
SHA is:

```text
/tmp/.../design/normal014-source-common.sh
before: a0ed2bd7d6688799f22bc8f17f89631c603e4e692a8d5e71f3ee3b26437b27b3
```

After the manager has the final harness commit, propose adding one new closed
role, `final95:selected`, preserving `final95:parent`, `final95:bootstrap`, all
profile pins, and every guard:

```diff
   final95:parent)
     APP_ROOT_SHA=af1605a28f31a53b5a3472251493d44941b618fe
     APP_ROOT_TREE=b0cb1f973c0e1b465241ebef38bd267fd39f0434
     ;;
+  final95:selected)
+    APP_ROOT_SHA=32b74fdea165816226b6f0727a16817a6a1a79c3
+    APP_ROOT_TREE=92391f9a57dd38ce327b0a63990725053ea34601
+    ;;
   final95:bootstrap)
```

The unsupported-role text would change only from `parent or bootstrap` to
`parent, bootstrap or selected`. The proposed whole-helper SHA is
`83a597c7bec81ff438640e69a2a612e243ca43f262cd75ac8931dd603db1fcef`; the
proposal was generated in memory and passed `sh -n`. It was not written to the
shared helper.

Application is closed by these refusal rules: require the current helper whole
hash `a0ed2bd7…` before applying; require zero existing
`final95:selected)` role occurrences and exactly one each of the existing
parent/bootstrap roles; refuse any unknown role; and rederive the final
App tree/commit after harness exit before replacing the proposed pending
source tuple. The current helper’s `NORMAL014_APP_SOURCE=selected` probe
refused with status 2, proving collision/unknown-role refusal before proposal.
The existing parent role is not replaced or relabeled.

This is a proposal only. The manager may reconcile the final App commit SHA
and tree against the keeper after harness exit, then apply the role only after
the whole-helper hash and source collision checks pass.

## Next step

Keep this one selected source and the existing frozen keeper lease. The manager
should reconcile the final harness-produced App commit/tree, then independently
review the closed-role helper proposal before any one authorized actual run.
