# App2 M2 parent 404 final binding and source preflight

## Result

The final BODY-only source is bound in the external preflight artifacts, but
the required central source preflight is blocked by an identity contradiction
in the settled instructions. No actual/browser run was requested or run.

The final source keeper is clean and was independently checked:

- HEAD: `acb582c2c3b08481d43853b8526894ac60d074bc`
- tree: `141724b56736be40a269f60aa8bfc060914ebd29`
- required ancestry: `5d36b0e53ff0d17ef045e226a6e6ca7584322858`,
  `968bbad09449f419ab63782fca49cad805068333`, and original `a304dce02…`
- `KEEP` is present, the keeper is clean, and
  `node_modules -> /home/user/work/app/node_modules` is unchanged.

## Exact binding deltas

The previous 0600 binding was inactive and pinned the held intermediate
source `86f765532d25181a1f3e953fb08f79587d328f85` /
`5f1d1d06432350eacbdd3d37ae8956b9fe2f756b`. The final 0604 source is the
body-only correction above. Relative to original `a304dce02…`, its only
source change is the one exact body field:

```diff
 request_id: expect.stringMatching(/^[A-Za-z0-9][A-Za-z0-9._~-]{0,127}$/),
```

The source file SHA-256 is
`5c12370fe8a14439f6c82ddbf088bcfcc2fcdcbfb8af90cbba4ec30e72bb1603`.
All downstream no-mutation, ADD, raw/order, reload, lost-ACK/restart,
exact-retry, undo, and zero-legacy assertions remain unchanged.

`normal014-source-common.sh` was guarded at its prior 0600 whole-file SHA
`3d00bda70e2371cc4af507f5916345ff02674a04cdc807af15737295dde0656f` and
contained only the accepted old pair `86f765/5f1d`. Per the task, only that
pair was reversed to `a304dce02a185a4774ff514d5aa451c9702aa46f` /
`a3c82aa91f1336b86491191acf857d88c56179b2`. The reconstructed helper SHA is
exactly the required
`af83e829f73ebcf9613e67808f81cab06c2e78f70c21bc850550cde1b5885fa4`.

The new gate was copied from approved 0535 gate SHA
`2aebe7cce4aab7cbf2fb4292165687385edddb0351bab12c633537bfc09c7546` and
changes only keeper path, final HEAD, and final tree. Its SHA is
`893272e40b692c9a35e153bbb4abbddec9a1e907430f11225b832034ae773398`.
The promoted driver remains byte/hash-identical at
`34ee03d1ea6f25ae4f68b8965f5c9b050d8892214416ec3bf551dfa81b17a2d2`.
Both new suite rows literally pin these final gate and driver hashes; the
actual row remains unrun.

## Verification

- `sh -n final-keeper-gate.sh` — PASS.
- Final keeper HEAD/tree, clean status, `KEEP`, node_modules link, and the
  three required ancestry checks — PASS.
- `git diff --check a304dce02… acb582c2c` — PASS.
- Local binding/hash checks for helper, gate, driver, and final keeper — PASS.
- Central request after registration correction:
  `ap2-m2-parent-body404-final-binding-preflight-0609-preflight-1021061403-2279`
  — gate guards PASS, then source preflight exit `1` before artifact
  collection.

The first central submission (`…1021061308-5917`) did not execute the gate:
the suite registration had one missing closing quote around the immutable
driver path and failed shell parsing with exit `2`. That registration was
corrected before the gate-reaching submission.

## Blocker

The mandated helper pair is now `a304/a3c82`, with the mandated helper SHA
`af83e829…`. The mandated final keeper is `acb582c2c3…/141724b5…`.
`normal014-source-common.sh:verify_app_source` requires the supplied keeper
tree to equal its pinned `APP_ROOT_TREE`, so the exact source preflight
refuses before the 76-artifact checks: `a3c82… != 141724…`. This is a direct
incompatibility between the instruction to reverse the helper pair and the
instruction to preflight the acb582c2c final keeper. I did not silently pin
acb or alter the source runner.

## Live callers

No live caller or App product path changed. The existing chain remains:
`onTimelineDrop -> useExternalDrop.ts -> external-drop-utils.ts ->
useAssetManagement.placePreparedAsset -> createTimelineCommands.addClip ->
commit-session/outbox`.

