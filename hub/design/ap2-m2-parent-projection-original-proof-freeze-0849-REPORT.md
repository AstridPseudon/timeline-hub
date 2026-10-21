# AP2-M2 parent projection/original proof freeze 0849

## Result

**CLOSED — final95:parent source freeze proposal only.** The worker preserved
the current HOME source and composed the one missing original mounted-ADD proof
body from the frozen `af1605a28` / `b0cb1f973` packet. No shared helper was
modified, and no browser, build, daemon, socket, install, full suite, actual,
or test-service submission was run.

The worktree is based on reviewed delivery `b1e3547e4` (tree
`aa659245db3e58c2cf592e4437316aeb1454f38f`). The only uncommitted path is the
intended proof-source edit:

```text
tests/e2e/local/three-products.spec.ts
```

The two approved projection blobs already present in `b1e3547e4` remain exact:

```text
src/tools/video-editor/lib/drop-position.ts       git blob c634ede997c8ca9c197fcf17d84fcf2630c69889
src/tools/video-editor/lib/drop-position.test.ts   git blob 4ed1d4cde67f32f1b573baafea400ae58bc4dd22
```

Their file SHA-256 values in this worktree are
`d15c0a5de1e6f1758e01ba592e2fad9f71ae6f270c2bc669c24ae2441a11429d` and
`15527e983f17052d60885932f4cb2aec5d22b0cc6e9ab43d277c0f3fbc91b0e4`.

## Original/new spec identity and exact delta

```text
HOME/original spec SHA-256: 56560d53aecf1d1ad2fce737e3955b20d35792bde3115da6f0df51913bc87bb5
frozen/new spec SHA-256:    5c12370fe8a14439f6c82ddbf088bcfcc2fcdcbfb8af90cbba4ec30e72bb1603
HOME/base spec git blob:    2873ae7db3944ef4ed58fed9ab5d6d73390bb0f3
frozen/new spec git blob:   67934dbcd263d6dc52648e176c8401f94338bfc7
frozen source:              af1605a28f31a53b5a3472251493d44941b618fe
frozen source tree:         b0cb1f973c0e1b465241ebef38bd267fd39f0434
```

The exact seven-line source delta is the reviewed strict refusal contract:

```diff
-expect([404, 409]).toContain(wrongVerified.status());
+expect(wrongVerified.status()).toBe(404);
+await expect(wrongVerified.json()).resolves.toEqual({
+  code: 'not_found',
+  message: 'selected media is not a managed project generation/variant/object',
+  request_id: expect.stringMatching(/^[A-Za-z0-9][A-Za-z0-9._~-]{0,127}$/),
+});
```

The full original packet remains unchanged: File/import/selection/verified
reads; strict 404 body/code/message/request_id; no Door header; `V1`/`at`
placement; genuine raw/opaque/order checks; explicit newborn hold expectations;
native `clip.add-media`; no `afterClipId`, `removeClipId`, or `replaceClipId`;
lost ACK; exact original retry body/key/response; reload; Runtime restart;
undo; and zero legacy traffic. SWAP, after-anchor, selector, timeout, guard,
pin, fixture-normalization, and afterClip activation remain untouched.

The reviewed projection correction remains the exact two-file HOME delta from
`32b74fdea` to `b1e3547e4` (39 focused tests and lint were previously reported
green). Its live consumers are unchanged: `useDragCoordinator.ts` consumes
`computeDropPosition`; `useExternalDrop.ts` finalizes external drops;
`external-drop-utils.ts` carries the selected target; and
`useAssetManagement.ts` performs native prepared placement. No proof runner,
session, provider, door, retry, writer, or pin source was changed.

## Cheap complete preflight

The corrected aggregate preflight passed. It checked the following exact
commands/conditions; all were read-only apart from temporary files created and
removed by the existing `probe` guard and Playwright list discovery:

```sh
git status --short
git diff --check
git diff --name-only
git merge-base --is-ancestor 5d36b0e53ff0d17ef045e226a6e6ca7584322858 HEAD
git merge-base --is-ancestor 968bbad09449f419ab63782fca49cad805068333 HEAD
git merge-base --is-ancestor 6bdb7dfadb5218d00cb04db45f67468609b0a1c6 HEAD
git merge-base --is-ancestor b1e3547e46d5436e509b36a9ad535565d0238e0f HEAD
```

Results: exact base HEAD/tree, exactly one intended dirty source path, no
untracked files, whitespace clean, and all four ancestry checks passed.

Pinned identity checks passed:

```text
Agent  6efc81500a0e0688c2bb41e736503f0fc3e04abb / tree 2ed2b8a12b5b3391ca221ba6ff05390f71a73556
Runtime/producer 95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c / tree d3a290b407fa61e6ab2d476f50c068073f70df00
Runtime lock SHA-256 770352eaf1d015e90fca0ed2f1893749b73b69356ca82a7223b2573276fe485e
generated metadata 4cd934d868eafd5ab82578da2232f1ee13f04d83c9314b3473b75bd951570044
generated client c575f183b6486dd07e8ec798f5a46bff4c9ffc0918892b189c1a433b9f80762d
timeline types f8cbbbbc48713a308c2ac2e2e977d08525c4280ef4dc93cd3e8d842245394564
artifact archive 895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30
Composition 0.0.13 member archive 9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738
Composition member count 77
artifact manifest count 76 (locked profile)
```

Owned graph and environment checks passed: `node v22.22.0`, Vite `5.4.21`
resolved from `/home/user/work/app/node_modules`, locked graph node_modules
resolved to its physical owned directory, and no group-writable locked-graph
files were found. The inherited normal discovery/credential paths and static
guards remain present (`WORKSPACE_RUNTIME_TOKEN_FILE`, discovery
`worker_credential_file`, and the runtime discovery proxy); live discovery and
credential provisioning are intentionally unverified because that requires a
daemon/socket run.

Syntax and runner guards passed:

```sh
sh -n tests/e2e/local/support/run-parent-manual-drop-evidence.sh
sh -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-parent-media-central.sh
sh -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-source-common.sh
sh tests/e2e/local/support/run-parent-manual-drop-evidence.sh probe
sh tests/e2e/local/support/run-parent-manual-drop-evidence.sh unsupported
PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers TMPDIR=/tmp node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --grep 'M2 real mounted manual video drop' --list
```

The unsupported-argv command refused as required; `probe` passed; list
discovery collected exactly `three-products.spec.ts:1440:1`, one test in one
file. No literal `ORCH/` path exists under App. The local browser lock was
available nonblocking, `/tmp` had `14,626,508 KiB` free (over 10 GiB), physical
short children were `0`, and private graph copies were `0`.

## final95:parent helper custody proposal

The shared helper was read-only and remains byte-identical at:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-source-common.sh
current whole-helper SHA-256: a0ed2bd7d6688799f22bc8f17f89631c603e4e692a8d5e71f3ee3b26437b27b3
```

The closed binding recipe from 0756/0801 is an exact role-local replacement:

```diff
-APP_ROOT_SHA=acb582c2c3b08481d43853b8526894ac60d074bc
-APP_ROOT_TREE=141724b56736be40a269f60aa8bfc060914ebd29
+APP_ROOT_SHA=af1605a28f31a53b5a3472251493d44941b618fe
+APP_ROOT_TREE=b0cb1f973c0e1b465241ebef38bd267fd39f0434
```

Exact whole-helper identities for that proposal are:

```text
before: d9a691dcaafd7d544a467445a3a020a9ad3d02afc1d527870f00be6948fea848
after:  a0ed2bd7d6688799f22bc8f17f89631c603e4e692a8d5e71f3ee3b26437b27b3
```

The current helper has the new SHA/tree pair exactly once and the old pair
zero times. Reverse substitution reproduces the before hash without writing
the helper. A future mutator must refuse unless the whole helper is exactly
the stated `before` hash and the old role pair has exactly one collision-free
occurrence; this worker did not mutate it. All other profiles, roles, pins,
guards, and live callers are byte-identical by that reverse proof.

The post-harness source identity is intentionally not invented here: the
harness must commit this worker's one-file source delta, then report the final
commit SHA/tree and source blobs. Only after that identity is known may final
custody replace the role's `af1605a28`/`b0cb1f973` pair with the harness commit
SHA/tree and recompute the helper hash. The manager/final-custody owner must
retain the minimal source lease/KEEP and refuse any collision or unaccounted
path.

## HOME merge dependency and boundary

The HOME merge must retain `b1e3547e4`'s exact two projection blobs and add
the frozen strict parent proof source above. After harness commit, final
custody must resolve identity through the source blobs/tree report, update only
`final95:parent`, and leave all other roles/profiles/pins byte-identical.
Final role switch and any later actual journey require manager/final custody;
they are not authorized by this worker.

No targeted browser test was run. The prior projection delivery report is the
evidence for its 39 focused tests/lint; this worker's evidence is source
identity, offline guards, syntax, and list discovery only.
