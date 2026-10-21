# Parent selector/argv custody review 0252

## Verdict

**APPROVE the bounded selector fix for manager consideration of one justified
rerun.** This is not approval of the mounted ADD journey, a browser run, a
central run, or any writer deletion. The manager decides whether to submit the
existing named suite once.

## Cause and fixed argv

The author proved the first mismatch in the 0236 run:

- PRELIST used the injected supported selector `--grep 'M2 real mounted
  manual video drop'` and collected exactly the intended case.
- ACTUAL used the copied runner's unchanged dynamic value, the anchored
  bootstrap selector `--grep "^M2 real gate 5 bootstrap actual consumer:
  production initializer uses native create/init, exact retry, restart and
  guarded undo$"`, with no file operand. It therefore returned `No tests
  found` before any case assertion or browser request.

The committed fix is `fb07523d5d5c3f268c205b3f50a337b686357ea4`, parent
`743d3464d1ed548986f29249bd9b4215baccf9bb`, with exactly one changed file:
`tests/e2e/local/support/run-parent-manual-drop-evidence.sh`.
The wrapper now rewrites the copied runner's required-case value to the full
manual ADD title (preserving the structured exact-name summary guard) and
rewrites only the run-stage selector to the supported substring. The final
wrapper SHA-256 is:

```text
9c3bd0c88df9290d78a3ba5838bb177f90d31494f5a235b9f7ea4682f05b8775
```

The resulting ACTUAL collection command is run from the copied runner's
overlay cwd with the existing config and private cache/output variables:

```text
node node_modules/playwright/cli.js test \
  --config playwright.three-products.config.ts \
  --grep 'M2 real mounted manual video drop' --list
```

The author froze the external driver identities at:

```text
normal014-app-central.sh  8f70ed7adafa42d90b3053f5972bd763a653ae690c1b2dfda352e3704615686e
normal014-source-common.sh 3dc9034586bf8c6fe2ff877b44fd1cbbabfb4eeeb1472fe009bad6d677811014
```

## Offline checks

Run directly in this review worktree, with private `/tmp` cache/output paths:

- Correct selector `--list`: **PASS**, exactly one test:
  `three-products.spec.ts:1440:1 › M2 real mounted manual video drop:
  Runtime selection refusal is closed, native ADD recovers exactly, and undo
  preserves opaque data`.
- Wrong/old bootstrap selector `--list`: **PASS refusal**, exit status 1,
  `Error: No tests found`, zero tests. No fallback to another case.
- `sh -n` on the committed fixed wrapper: **PASS**.
- `git diff --check tl/integration..tl/ap2-m2-parent-actual-argv-collection-cause-0250`:
  **PASS**.

The fix diff does not touch `three-products.spec.ts`, its config, product code,
pins, artifacts, imports, or any timeout/retry/framework. Bootstrap suites
still invoke the unchanged source runner directly. The source runner's
private-spec mixed-selector override remains unchanged, and its exact
`normal014_required_case` summary guard remains in place. The original manual
ADD body/assertions are not changed by this fix; the frozen source packet
remains the authority for the exact-404 negative and all positive/recovery,
reload, retry, undo, opaque-data, and zero-legacy assertions.

## Custody identities checked

The strict source controls remain present in the unchanged external helpers.
Read-only object and cleanliness checks confirmed:

```text
App frozen source: da6d910f7ab3dfc71142ece7f632d43341238882
App tree:          6809757f93ca5e166b24b8bc0160ca09005e984a
Agent:             6efc81500a0e0688c2bb41e736503f0fc3e04abb
Agent tree:        2ed2b8a12b5b3391ca221ba6ff05390f71a73556
Runtime:           95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c
Runtime tree:      d3a290b407fa61e6ab2d476f50c068073f70df00
Producer:          95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c
Producer tree:     d3a290b407fa61e6ab2d476f50c068073f70df00
Artifact:          sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac
Manifest:          a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d
Manifest entries:  76
Schema:            6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d
Private App dependency-graph source archive: 895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30
Official immutable Composition 0.0.13 archive: 9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738
```

Agent and Runtime source worktrees were clean when checked. The unchanged
runner still requires exact trees, clean App state, pin bytes, artifact
manifest/schema equality, import collection, and producer HEAD. Those guards
were not rerun as a full source preflight here.

## Live callers and suite

The live mounted path remains:

`onTimelineDrop` → `useExternalDrop.ts:dispatchTimelineDrop` →
`external-drop-utils.ts:handleFileDrop` → `useTimelineState` parent-media
commands → `useAssetManagement.placePreparedAsset` → native
`createTimelineCommands.addClip` → existing `commitSession` /
`useTimelineCommandSession` outbox and commit path.

The wrapper is called by the retained 0236 suite at `suites.conf:34` and the
new explicit source-bound final95 suite at `suites.conf:105`. The exact command
to use, if the manager authorizes one rerun, is:

```text
sh tests/e2e/local/support/run-parent-manual-drop-evidence.sh run "$PWD"
```

No rerun was submitted by this review. No browser, localhost/live socket,
central service, full suite, install, or product edit was performed.
