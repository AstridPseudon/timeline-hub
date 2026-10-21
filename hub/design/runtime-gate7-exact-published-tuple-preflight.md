# Gate 7 exact published014 tuple preflight

Date: 2026-10-21 UTC

## Verdict

The owner-requested source tuple is known and present as Git objects, but it is
not aligned with the four canonical delivery inputs. No delivery rerun is
authorized from the current mirrors, and the existing proper dry run `10810`
must not be relabeled.

Owner's requested tuple:

| repository | requested commit | requested tree |
| --- | --- | --- |
| Agent | `091aa23ec83ea05ffd3b0115a640230d51c8c429` | `e3ae90fe482ba6cad6c3f94069127faf76ebceb6` |
| Runtime | `b92d3e7a05eec65c142294ef4873edd059e9b31d` | `6abc2f117391de8e7e35c0283f575a002199894d` |
| App | `3be3c116610c4ffdf019cba447464280fd7b8e06` | `d030e4b8b41a1d5ec46de1c0c245111cafa7e98a` |
| Composition | `7bb54bbd64107e5090643ecca1e4d33164173e85` | `20467712e66dbadff4d562c0d5baae22b8c077a7` |

The owner/manager status at 03:51 requests exactly this published014 tuple.
The Agent and App adoption declarations identify `091…` and `3be…` as the
current source choices; they do not make those commits the canonical delivery
branch tips.

## Exact local and hub state

Read-only probes of `/home/user/work/{agent,runtime,app,composition}` found:

| repository | local `tl/integration` commit/tree | hub integration commit/tree | owner tuple relation |
| --- | --- | --- | --- |
| Agent | `7ab6cbae273f133b3adf2a7bae9f2439f02ce71e` / `075339b2c6d5e57c1b0e76754457d053b51edf2c` | same `7ab…` / `075339…` | requested `091…` is an ancestor of `7ab…` |
| Runtime | `b92d3e7a05eec65c142294ef4873edd059e9b31d` / `6abc2f117391de8e7e35c0283f575a002199894d` | same `b92…` / `6abc2f…` | exact |
| App | `976e08c6c8fffd4ebb4e61e8fc1523685a330f87` / `196cb0c8c630bd21b851ce8a9d1d0e056edd9a2f` | same `976…` / `196cb0…` | requested `3be…` is an ancestor of `976…` |
| Composition | `7bb54bbd64107e5090643ecca1e4d33164173e85` / `20467712e66dbadff4d562c0d5baae22b8c077a7` | same `7bb…` / `204677…` | exact |

The exact Agent commit is available on the hub-published worker refs
`timeline/agent/tl/agt-m2-gate13-published014-current-proof`,
`timeline/agent/tl/agt-m4-published014-full-env-preflight`, and
`timeline/agent/tl/agt-review-d13-installed-authority-security`; the exact App
commit is available on the hub-published App worker refs including
`timeline/app/tl/app-m4-post-pin014-current-full-execute-r8`. Neither is the
repo's `tl/integration` ref.

This is not a missing-object problem. It is a source-selection problem: the
canonical mirrors contain later descendants, and a normal fast-forward mirror
sync cannot move either integration ref backward to the owner's selected
ancestor. The Agent mirror is therefore stale for the requested exact source
selection even though its tree contains that source in its ancestry.

## What the reviewed delivery carrier can select

The installed, reviewed carrier is
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build`,
SHA-256
`3dfd5c28a9be9ab809e6c1fe1e9a83fbf8417ea888afc1b10eec5f751023e990`.
Its source selection is fixed in the reviewed code:

```text
WORK = /home/user/work
BRANCH = tl/integration
BASE = origin/main
```

Its only CLI selectors are `--dry-run`, `--repos`, and repeated `--extra`.
The App `private_source_view` is only a private shallow-history view of the
fixed `/home/user/work/app` source; it is not an arbitrary source-root or tip
selector. There is no existing delivery-build source-root/ref option.

The normal immutable carrier helper can create exact checkouts:

```bash
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-checkout \
  agent 091aa23ec83ea05ffd3b0115a640230d51c8c429 \
  "Gate7 owner published014 exact source carrier"
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-checkout \
  app 3be3c116610c4ffdf019cba447464280fd7b8e06 \
  "Gate7 owner published014 exact source carrier"
```

Those would yield immutable detached carriers under
`/home/user/work/wt/agt-pin-091aa23e` and `/home/user/work/wt/app-pin-3be3c116`.
They are safe exact-source carriers for inspection or a test that explicitly
accepts a checkout path. They cannot select delivery inputs: `delivery-build`
does not read those paths, and `ASTRID_CHECKOUT`, `PYTHONPATH`, symlinks,
copied source, or an import overlay do not change packaging authority. No such
source-import workaround is valid here.

## Owner-only alignment blocker and normal resolution

The owner/area managers must first establish the requested commits as the
canonical `tl/integration` inputs (or explicitly decide that the canonical
integration descendants, `7ab…` and `976…`, supersede the request). The normal
mirror path after that owner decision is the existing hub publication and
`hub-sync` fetch/fast-forward path; verify the four exact `tl/integration`
commit/tree pairs in the table above before packaging.

No worker should force, reset, or rewrite either integration ref. In
particular, a detached `request-checkout` result does not remove this blocker,
and fetching the already-published Agent/App worker refs does not update
`hub/timeline/{agent,app}/tl/integration`. Until the owner-only mirror decision
is complete, there is no safe command using the unchanged reviewed carrier
that packages the requested tuple.

## Ready command after alignment

Once the owner confirms the canonical mirrors expose exactly the requested
tuple, run this one fresh dry run. The preflight is read-only; the carrier
itself re-pins and rechecks `origin/main` and `tl/integration`, verifies each
fresh-main patch application, verifies each bundle, and requires applied-tree,
bundle-tree, and source-tree equality.

```bash
set -eu
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
for spec in \
  "agent 091aa23ec83ea05ffd3b0115a640230d51c8c429 e3ae90fe482ba6cad6c3f94069127faf76ebceb6" \
  "runtime b92d3e7a05eec65c142294ef4873edd059e9b31d 6abc2f117391de8e7e35c0283f575a002199894d" \
  "app 3be3c116610c4ffdf019cba447464280fd7b8e06 d030e4b8b41a1d5ec46de1c0c245111cafa7e98a" \
  "composition 7bb54bbd64107e5090643ecca1e4d33164173e85 20467712e66dbadff4d562c0d5baae22b8c077a7"; do
  set -- $spec
  test "$(git -C "/home/user/work/$1" rev-parse tl/integration^{commit})" = "$2"
  test "$(git -C "/home/user/work/$1" rev-parse tl/integration^{tree})" = "$3"
  test -z "$(git -C "/home/user/work/$1" status --porcelain)"
done
test "$(sha256sum "$ORCH/bin/delivery-build" | awk '{print $1}')" = \
  3dfd5c28a9be9ab809e6c1fe1e9a83fbf8417ea888afc1b10eec5f751023e990
test -z "$(find "$ORCH/delivery" -maxdepth 1 -type f -name 'timeline-delivery-*.zip' -print -quit)"
GIT_CONFIG_GLOBAL=/dev/null PYTHONDONTWRITEBYTECODE=1 \
TIMELINE_DELIVERY_SCRIPT_SHA=3dfd5c28a9be9ab809e6c1fe1e9a83fbf8417ea888afc1b10eec5f751023e990 \
python3 "$ORCH/bin/delivery-build" \
  --dry-run --repos "agent runtime app composition" \
  --extra "extras/owner_film_cliplook_scan-v1.0.8.zip=$ORCH/design/handoff-vw-m4-owner-scanner-delivery-payload-scanner-v1.0.8.zip" \
  --extra "extras/owner-film-differences.md=$ORCH/design/handoff-vw-m4-owner-scanner-delivery-payload-owner-film-differences.md"
```

The two frozen extras remain scanner
`204a7aac78177824219954574f67fcaf4c56ac81620d533ecb376030340c93ee` and
owner instructions
`969fe3034ca1e7b7aab061ff16575fe7f7d973d9c9ec1f81c347464c4d9da220`; the
existing regular-file/non-symlink, traversal, collision, checksum, and
no-ZIP guards remain in force. This command is not to be submitted before the
tuple checks pass. It is not a repeat of `10810`, and no checksum/scanner,
full, render, browser, or final-ZIP run was performed for this preflight.

## Existing evidence preserved

`10810` remains valid only for Agent `7ab6cbae` / tree `075339…`, Runtime
`30413e3c` / tree `2c5a508…`, App `3be3c116` / tree `d030e4…`, and Composition
`7bb54bb` / tree `204677…`. Its extras and 12-file retained stage are not
reused as evidence for Agent `091…` or Runtime `b92…`; only the reviewed
carrier and guard requirements are reused above.
