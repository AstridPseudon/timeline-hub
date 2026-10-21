# AP2 M2 parent snapshot source identity fix

## Result

Updated the existing final95 App consumer source guard in
`design/normal014-source-common.sh`. It no longer requires the consumer
snapshot `HEAD` to equal the declared parent source commit when the central
service has wrapped the exact tree in a synthetic commit. The guard now:

- accepts the exact declared source `HEAD`;
- otherwise requires the declared source commit to be an ancestor of the
  observed `HEAD` with `git merge-base --is-ancestor`;
- still requires the exact frozen source tree, clean tracked/untracked state,
  and all four approved 10fa pin hashes.

The producer/Agent/Runtime checkout path remains exact-`HEAD` through
`prepare_checkout`; no producer guard was broadened. The App runner, parent
runner, public13 locked graph, artifact/schema, Python import, and marker
guards were not otherwise changed.

## Snapshot evidence

The retained 0138 metadata records the exact parent source snapshot:

```text
tree=972d2ed2e4f85f334eb9f2e6ca40d9bfbce9eac7
worktree=/home/user/work/wt/ap2-m2-parent-frozen-source-single-gate-0138
```

The central `test-run` implementation creates its snapshot with
`git commit-tree $tree -p HEAD`; therefore the synthetic snapshot has the
declared source commit in ancestry while its `HEAD` differs. The exact parent
source is `25155ccb22728780a3ecd6379a929cad75cc1400` and its tree is the
frozen `972d2ed2e4f85f334eb9f2e6ca40d9bfbce9eac7`.

## Verification

Passed:

```text
sh -n design/normal014-source-common.sh design/normal014-app-central.sh design/normal014-parent-media-central.sh
git diff --check
```

Focused temporary Git fixtures, using the same `commit-tree ... -p source`
shape as the service, passed a synthetic snapshot and refused all requested
negatives: changed tree, dirty file, foreign pin, and missing provenance.
The positive fixture reported tree `972d2ed2e4f85f334eb9f2e6ca40d9bfbce9eac7`
and a synthetic `HEAD` whose parent was the declared source commit.

The central source-only preflight was requested exactly once:

```text
R=$(.../bin/request-test ap2-m2-parent-frozen-source-single-gate-0138 normal014-parent-source-identity-preflight --no-cache)
.../bin/wait-test "$(basename "$R")"
```

Result `...-1021020355-15103`: **pass, exit 0, 19s**. It used the exact
parent tree and reached `normal014 parent-media preflight: source tuple, d05e
marker, locked graph, and shell guards verified`, including
`verified artifacts=76` and the frozen schema digest. No parent case, browser,
socket, package install, full suite, or actual gate ran.

An initial source-only preflight on this worker’s integration tree was refused
before output because that tree was `e615c0a3...`, not the final95 parent tree;
it was not used as evidence. The temporary suite entry was removed afterward.

The assigned App worktree remains clean. No product files or shared
dependencies were modified.

## Next step

The orchestrator may rerun the existing final95 parent gate from the exact
parent source worker. This worker did not claim that actual gate’s behavior.
