# AP2-M2 parent projection final owned binding 0855

## Result

Bound the existing `final95:parent` execution chain to the harness-committed
0849 App source. This was preflight-only; no actual was submitted or run.

The source is this clean worktree:

```text
path=/home/user/work/wt/ap2-m2-parent-projection-final-owned-binding-0855
HEAD=8eb4d08e60f434b938ea885c8cadca4bd87151b3
TREE=ea317333400d1a342f2520556eef8ce9399666c1
spec=tests/e2e/local/three-products.spec.ts
spec_sha256=5c12370fe8a14439f6c82ddbf088bcfcc2fcdcbfb8af90cbba4ec30e72bb1603
```

The source contains the approved projection blobs exactly:

```text
src/tools/video-editor/lib/drop-position.ts      c634ede997c8ca9c197fcf17d84fcf2630c69889
src/tools/video-editor/lib/drop-position.test.ts  4ed1d4cde67f32f1b573baafea400ae58bc4dd22
```

The original parent proof body remains intact: strict verified-selection 404
body/code/request_id, explicit newborn hold, raw/opaque/order checks, native
`clip.add-media` parent placement at `V1`/`20`, no `afterClipId`,
`removeClipId`, or `replaceClipId`, lost-ACK exact retry body/key/response,
reload, Runtime restart, guarded undo, and zero legacy traffic. No App/spec,
session, harness, pin, assertion, or product caller was edited.

## Exact minimal delta

The shared helper was changed only under the delegated collision guard. Before
mutation its whole-file SHA was
`a0ed2bd7d6688799f22bc8f17f89631c603e4e692a8d5e71f3ee3b26437b27b3`; the
`final95:parent` old pair occurred once each in the role. The only helper
delta was:

```diff
-APP_ROOT_SHA=af1605a28f31a53b5a3472251493d44941b618fe
-APP_ROOT_TREE=b0cb1f973c0e1b465241ebef38bd267fd39f0434
+APP_ROOT_SHA=8eb4d08e60f434b938ea885c8cadca4bd87151b3
+APP_ROOT_TREE=ea317333400d1a342f2520556eef8ce9399666c1
```

The final helper SHA is
`96969ce9ff43b676abb4616009fd1112e93020065483b2a8ae0afac7245ba109`.
The old pair now occurs zero times and the new pair once each. Programmatic
reverse substitution of only these two lines reproduces the exact old helper
SHA, proving all other roles, profiles, guards, pins, and bytes are unchanged.

## Owned immutable artifacts

Copied from the approved 0756/0801/0806 parent chain into the worker-owned
durable directory:

```text
gate=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-projection-final-owned-binding-0855/final-keeper-gate.sh
gate_sha256=45b10f9bbae7d33030ecbe1166d7447090d6a9fc98e9b08c041d13b69a022bd1
driver=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-projection-final-owned-binding-0855/run-parent-manual-drop-evidence.sh
driver_sha256=34ee03d1ea6f25ae4f68b8965f5c9b050d8892214416ec3bf551dfa81b17a2d2
```

The gate changes only its keeper path, final HEAD/tree, helper hash, and
worker-owned driver path; the driver copy is byte-identical to the approved
source driver. Existing registered evidence/custody paths, source runner,
child-RC/retention/cleanup behavior, credentials/auth/guard semantics, and
the immutable old tools remain retained.

## Commands and results

Passed:

```text
sh -n normal014-source-common.sh normal014-parent-media-central.sh final-keeper-gate.sh run-parent-manual-drop-evidence.sh
sh run-parent-manual-drop-evidence.sh probe
git diff --check
source/blob/body identity checks
helper old/new collision counts and reverse hash proof
aggregate gate preflight (once)
```

Aggregate preflight command:

```sh
env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent NORMAL014_USE_BASE_PYTHON=1 sh '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-projection-final-owned-binding-0855/final-keeper-gate.sh' preflight
```

Result: PASS. It verified captured/keeper `HEAD=8eb4d08e…`, `TREE=ea317333…`,
clean status and KEEP, helper/driver hashes, 76 artifacts, manifest
`a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`, schema
`6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`, and
the parent-media source preflight. Existing bounded negatives refused wrong
captured tree, wrong keeper, wrong helper hash, and wrong argv. Exact list
collection passed with one test at `three-products.spec.ts:1440`.

The driver launch-only guard probe passed, including zero-test refusal and
evidence copied before disposable-root cleanup. The bounded wrong-source,
wrong-hash, and correct-one-test controls therefore passed without a browser,
build, daemon, socket, install, service submission, full suite, or actual.
The unchanged driver's prior bounded launch-only dispatch evidence was reused
per the no-repeat instruction: the real setup reached its child seam with
stubs, a planted child failure propagated `1`, and the clean child path reached
the required one-test control. No unchanged broad control was rerun.

The one permitted HOME remote check was attempted once with `git ls-remote`;
the configured GitHub proxy was unavailable (`connect to 127.0.0.1:37123`), so
no remote merge state is claimed and no polling was performed.

## Literal syntax-checked central proposals

These are proposals only; neither was registered or submitted here. Both
were passed through `sh -n` after deriving the hashes from the files.

```text
app ap2-m2-parent-projection-final-owned-binding-0855-preflight test "$(sha256sum -- '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-projection-final-owned-binding-0855/final-keeper-gate.sh' | cut -d' ' -f1)" = '45b10f9bbae7d33030ecbe1166d7447090d6a9fc98e9b08c041d13b69a022bd1' && test "$(sha256sum -- '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-projection-final-owned-binding-0855/run-parent-manual-drop-evidence.sh' | cut -d' ' -f1)" = '34ee03d1ea6f25ae4f68b8965f5c9b050d8892214416ec3bf551dfa81b17a2d2' && env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent NORMAL014_USE_BASE_PYTHON=1 sh '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-projection-final-owned-binding-0855/final-keeper-gate.sh' preflight
app ap2-m2-parent-projection-final-owned-binding-0855-actual test "$(sha256sum -- '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-projection-final-owned-binding-0855/final-keeper-gate.sh' | cut -d' ' -f1)" = '45b10f9bbae7d33030ecbe1166d7447090d6a9fc98e9b08c041d13b69a022bd1' && test "$(sha256sum -- '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-projection-final-owned-binding-0855/run-parent-manual-drop-evidence.sh' | cut -d' ' -f1)" = '34ee03d1ea6f25ae4f68b8965f5c9b050d8892214416ec3bf551dfa81b17a2d2' && env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent NORMAL014_USE_BASE_PYTHON=1 sh '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-projection-final-owned-binding-0855/final-keeper-gate.sh' run
```

## Remaining checks and custody

Final custody review should recheck the exact source/tree/helper/gate/driver
tuple and then manager-authorize exactly one actual, if desired. The mounted
parent behavior remains unqualified by this worker. No actual, browser, build,
daemon, socket, install, full suite, or service submission was run.
