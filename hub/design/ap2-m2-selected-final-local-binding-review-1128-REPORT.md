# AP2 M2 selected final local-binding review 1128

## Result

**HOLD — the exact LOCAL current-binding launch is not approved.** MAIN also
remains HOLD as already recorded in the 1120 packet; this review gives no MAIN
approval.

The 1120 exported packet has a closed current App binding (`0cc2583a…`, tree
`320e74a…`) and no stale `a50ca4a…`/`92391f9…` role in the four exported
scripts. The independent static custody check nevertheless found three
runner guard/hash mismatches. They are on both the cheap-preflight path and
the actual path, so the runner would refuse before the selected child launch.

## Complete mismatch list

`ap2-m2-selected-clean-keeper-main-port-1120-runner.sh` line 438–440 checks
the old approved helper/driver hashes, while its bound paths point to the new
1120 exports:

| guard | runner expects | bound 1120 file actually hashes to |
|---|---|---|
| `OLD_DRIVER` | `a959de6e0041f0d8ee28b949a19f5add97d7fb5de27714da6beaad15abd6ce4f` | `cf4ddff51c86e2be5a1d7bdae705aa3390eaf4c931e6cea7b2369311dadecea7` |
| `SOURCE_COMMON` | `96969ce9ff43b676abb4616009fd1112e93020065483b2a8ae0afac7245ba109` | `647ea22abf9cf452ca9cb1a8a21633dcd33dc201ac0cc8bbc4f65b6f07929b2b` |
| `PARENT_MEDIA` | `1d2ebce742bab9a20a911baedab8e7e318e82d6f1043f7f554949855acf646fd` | `ce9e86fab603bd654e572bba67bfca0f9214722f4036cce19840960d9ff6b702` |

These are real 1120 binding deltas: the source helper accepts explicit graph
and archive paths; the parent helper uses the exported source helper and
explicit graph/archive variables; and the P1 driver has explicit graph/archive
and trace-destination bindings. The packet manifest correctly records the
new hashes, but the runner's internal guards were not rebound to them.

The guard is called by `run_cheap_preflight` at line 519 and by `run_actual`
at line 671. Therefore the smallest HOLD is this custody-guard closure, not a
product/spec/pin/source-logic issue. Do not authorize the local launch until
the runner's three expected hashes and its reverse-diff/hash inventory are
repaired and independently rechecked. Do not weaken or remove the guard.

## What remained closed

- Current App source/keeper binding is `0cc2583aaf07e89190b9344b5ac82849d6279586` /
  `320e74a93676c781e83885b86ec237b4a1465d80`, with keeper
  `/home/user/work/wt/app-pin-0cc2583a`.
- The static runner delta from approved `96629aa9…` is limited to the intended
  path/keeper/current-source binding changes; no stale `a50ca4a…` role appears
  in the exported scripts or selected run body.
- The retained final95 identities remain Agent `6efc8150…`, Runtime/producer
  `95bd3c5f…`, manifest count 76, Composition `0.0.13`, embedded package
  `9412ae25…`, and graph archive `895c628a…`.
- Static comparison found the selected spec/title/P1/P2/body/budget bindings,
  credential FILE/origin scope, zero-test guard, child return propagation,
  partial trace/context retention, optional DOM handling, and no-shared-write
  controls unchanged from the approved runner. These are static continuity
  findings only, not execution evidence.

The prior 1120 report's local preflight/list1 PASS is retained as existing
evidence and was not rerun. It cannot override the current, directly
reproducible hash contradiction above; the recorded PASS is not treated as
launch approval.

## Exact checks

Read-only/static checks performed for this review:

```text
sha256sum of all four exported scripts and empty KEEP; packet hash table comparison  PASS
diff -u approved966 runner and baseline helper/driver diffs                  PASS: binding-only deltas identified
runner expected-vs-exported OLD_DRIVER/SOURCE_COMMON/PARENT_MEDIA audit       HOLD: all three mismatched as listed above
stale a50ca4a/92391f9 App-role scan of exported scripts                      PASS: none found
assigned App worktree git status                                              PASS: clean
```

Existing 1120 evidence (not rerun): all four `sh -n` checks, clean keeper
identity, and the single offline preflight with 12 aggregate checks plus
Playwright `1 test in 1 file` list1 were reported PASS.

No browser, build, Runtime, service, socket, actual run, install, full suite,
or repeated unchanged control was run for this review. No product/source/spec/
pin/repo documentation or `.gitignore` file was changed.
