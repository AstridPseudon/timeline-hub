# App2 parent final source-binding handoff

## Result

Prepared one reviewable patch artifact for `final95:parent` only:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-parent-final-source-binding-handoff-0417.patch`

The patch changes two source-identity constants in the existing HOME-owned
helper. It does not change the helper, the durable driver, a suite row, a
product file, or Git metadata.

## Frozen source identity

The harness-frozen source from
`ap2-m2-parent-source-current-parent-finalize-0416` is:

- ref: `tl/ap2-m2-parent-source-current-parent-finalize-0416`
- final worker commit: `b833512fcb5ef07013c47fcf8c75c4a083048d99`
- final worker tree: `a95793cc2179200dd9ef5fe551360a4f6f965ea1`
- parents: `0daaee4698c83e749dc2c3e204965b12ff3cd8ec` (stage 0356) and
  `5d36b0e53ff0d17ef045e226a6e6ca7584322858` (HOME)

The stage 0356 ref
`tl/ap2-m2-parent-repaired-current-proof-source-stage-0356` remains exactly
commit `0daaee4698c83e749dc2c3e204965b12ff3cd8ec`, tree
`a95793cc2179200dd9ef5fe551360a4f6f965ea1`. The HOME merge `5d36…` is an
ancestor and the second parent of the frozen source. It is not the final test
source identity; the final identity is `b833…` / `a957…` above.

## Exact helper change

Existing path, owned by HOME and left read-only:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-source-common.sh`

Current helper SHA-256: `3dc9034586bf8c6fe2ff877b44fd1cbbabfb4eeeb1472fe009bad6d677811014`

Current `final95:parent` contents:

```sh
APP_ROOT_SHA=da6d910f7ab3dfc71142ece7f632d43341238882
APP_ROOT_TREE=6809757f93ca5e166b24b8bc0160ca09005e984a
```

Proposed contents:

```sh
APP_ROOT_SHA=b833512fcb5ef07013c47fcf8c75c4a083048d99
APP_ROOT_TREE=a95793cc2179200dd9ef5fe551360a4f6f965ea1
```

Prospective complete-helper SHA-256: `b4b142931573d6954af75ee91dd5f1c2c6cbb5a97dc4c65cbdb450ceeec04cb7`

The `old202` tuple, `final95:bootstrap` tuple, Agent/Runtime/producer/artifact/schema/wire pins, profile/role selector, source-role refusal, clean-tree and ancestry guards, locked graph checks, exact test selector, evidence trap, failure propagation, and zero-test trap are unchanged.

## Durable 0323 caller and helper references

The existing durable driver is:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-composed-driver-label-durable-stage-0323/run-parent-manual-drop-evidence.sh`

Its SHA-256 remains `40c7b57b6f327bafa82f26daaa4053f405e89f7bd48b5aacdadd21b2393867f`. It imports the helper by the unchanged absolute path and has no embedded App source SHA/tree or helper-content digest. The existing source runner imports the same helper by relative path. Therefore no driver or runner hash requires updating; historical reports retaining the old helper hash remain historical records and are not rewritten.

No live callers changed. The durable suite selector remains
`ap2-m2-parent-composed-driver-label-durable-stage-0323-e2e-integration`,
with the existing `NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent`
role and one-test command.

## Proposed guarded HOME command

HOME should apply the artifact only after confirming the frozen source ref and
the old helper bytes. This command is proposed, not executed here:

```sh
set -eu
app_repo=/home/user/work/app
source_ref=tl/ap2-m2-parent-source-current-parent-finalize-0416
source_sha=b833512fcb5ef07013c47fcf8c75c4a083048d99
source_tree=a95793cc2179200dd9ef5fe551360a4f6f965ea1
helper=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-source-common.sh
old_helper_sha=3dc9034586bf8c6fe2ff877b44fd1cbbabfb4eeeb1472fe009bad6d677811014
new_helper_sha=b4b142931573d6954af75ee91dd5f1c2c6cbb5a97dc4c65cbdb450ceeec04cb7

test "$(git -C "$app_repo" rev-parse "$source_ref")" = "$source_sha"
test "$(git -C "$app_repo" show -s --format=%T "$source_ref")" = "$source_tree"
git -C "$app_repo" merge-base --is-ancestor 5d36b0e53ff0d17ef045e226a6e6ca7584322858 "$source_ref"
test "$(sha256sum "$helper" | cut -d' ' -f1)" = "$old_helper_sha"

patch_tmp=$(mktemp "${helper}.tmp.XXXXXX")
trap 'rm -f -- "$patch_tmp"' EXIT
sed \
  -e 's/APP_ROOT_SHA=da6d910f7ab3dfc71142ece7f632d43341238882/APP_ROOT_SHA=b833512fcb5ef07013c47fcf8c75c4a083048d99/' \
  -e 's/APP_ROOT_TREE=6809757f93ca5e166b24b8bc0160ca09005e984a/APP_ROOT_TREE=a95793cc2179200dd9ef5fe551360a4f6f965ea1/' \
  "$helper" >"$patch_tmp"
chmod --reference="$helper" "$patch_tmp"
test "$(sha256sum "$patch_tmp" | cut -d' ' -f1)" = "$new_helper_sha"
mv -- "$patch_tmp" "$helper"
test "$(sha256sum "$helper" | cut -d' ' -f1)" = "$new_helper_sha"
```

## Checks and limits

Passed:

- ref/tree inspection and stage-0356 equality check;
- HOME `5d36…` ancestor and two-parent check;
- read-only durable-driver/source-runner reference inspection;
- `sh -n` on the existing helper;
- prospective two-line helper stream through `sh -n`;
- prospective complete-helper SHA calculation.

Not run, as required: actual mounted test, build, browser, localhost/live
socket, full suite, or shared-helper mutation. No private source copy was
created. Observed free space was 15 GiB, above the 10 GiB floor.

Live callers changed: none.
