# Gate6 farm final publication 1218

Published the complete existing `tl/vw-m3-gate6-farm-transport-1210`
packet from commit `9361d5002339adaaf2bcc80322a4695fbeaae984` into the absolute
orchestrator design directory. The fourteen committed design files were
recovered byte-for-byte under their `handoff-vw-gate6-farm-1210-*` names.

Also published bare packet aliases (`run.sh`, `preflight.sh`, the eight
supporting scripts, and `SHA256SUMS`) as byte-identical copies. This is needed
for the reviewed relative imports; it does not alter any reviewed script
bytes or hashes. No source, test, controller, node_modules, graph, media,
archive, token, marker, grant, or build output was added to this worktree or
the handoff.

Replaced the absolute 1209 request with one lean executable HOLD request. It
corrects the Agent commit to the full 40-hex
`d0a5072bbe7b7ce9489f43aa0a81027ec400343b`, keeps the historical 0d43/C13
execution tuple separate from the current integration checkpoint, uses only
absolute executable paths, records the external immutable prerequisites, and
keeps the five original cases and audio/picture negatives. The existing farm
lead ownership of environment/socket guards is explicit; no controller
expansion was made.

## Verification

- `(cd ORCH/design && sha256sum -c SHA256SUMS)` — PASS, all 10 reviewed
  scripts OK.
- `cmp` of each bare script against its committed prefixed export — PASS.
- Explicit `git cat-file` checks for every listed historical and current
  source commit/tree, plus transport commit/tree — PASS; all are real objects
  with the expected commit/tree types.
- Placeholder scan for `/path/to` in the executable request and packet — PASS.
- `git diff --check` — run after this report is written.

No local test, preflight, browser, helper, Runtime, socket, marker, grant,
physical run, or full suite was run, as required.

## HOLD / missing inputs

1. Fresh manager authorization naming the exact packet, unchanged 1054 stage,
   and fresh marker path.
2. Independent materialization of the complete 1054 sibling graph and six-file
   closure, metadata, b70 helper, pinned App graph/source/dist, public13 and
   other external media/runtime inputs, and private toolchain/temp/socket roots.
3. Central preflight and the single authorized physical five-case run remain
   unverified. No readiness, parity, qualification, or M4 claim is made.

Recommended next step: the viewing manager supplies the fresh authorization;
the farm lead then materializes the named external inputs, applies only the
permitted private path bindings and required env/socket guards, and runs the
two absolute commands in the published HOLD request once, in order.
