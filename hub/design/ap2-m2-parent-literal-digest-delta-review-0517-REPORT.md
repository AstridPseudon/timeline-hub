# App2 M2 parent literal digest delta review 0517

## Verdict

**APPROVE** the exact finalhash preflight and actual command registrations. The 0508 HOLD is closed by the one required literal prefix: the external gate SHA-256 predicate is first and uses the exact 64-hex digest `2fe1bf06d796d1342870a02a06a0d0f10057ba20bc2a29e0cad8a43deaaf16e1`.

No App product source, proof source, helper, driver, keeper, tree, live caller, or registration was modified by this review. The two registrations were manager-owned inputs reviewed in place.

## Exact commands

```sh
app ap2-m2-parent-finalhash-preflight-0517 test "$(sha256sum -- '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-central-keeper-command-preflight-0508/final-keeper-gate.sh' | cut -d' ' -f1)" = '2fe1bf06d796d1342870a02a06a0d0f10057ba20bc2a29e0cad8a43deaaf16e1' && '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-central-keeper-command-preflight-0508/final-keeper-gate.sh' preflight
app ap2-m2-parent-finalhash-actual-0517 test "$(sha256sum -- '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-central-keeper-command-preflight-0508/final-keeper-gate.sh' | cut -d' ' -f1)" = '2fe1bf06d796d1342870a02a06a0d0f10057ba20bc2a29e0cad8a43deaaf16e1' && '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-central-keeper-command-preflight-0508/final-keeper-gate.sh' run
```

The existing gate invocations and arguments are unchanged; only the final digest test was prefixed. Shell quoting around the absolute path changes no argv.

## Custody tuple

- Captured service tree: `a3c82aa91f1336b86491191acf857d88c56179b2`.
- Original keeper HEAD: `a304dce02a185a4774ff514d5aa451c9702aa46f`.
- Original keeper tree: `a3c82aa91f1336b86491191acf857d88c56179b2`.
- Helper SHA-256: `af83e829f73ebcf9613e67808f81cab06c2e78f70c21bc850550cde1b5885fa4`.
- Correct full driver SHA-256: `40c7b57b6f327bafa82f26daaa4053f405e89f7bd48b5aacdadd21b2393867f0`.
- External gate SHA-256: `2fe1bf06d796d1342870a02a06a0d0f10057ba20bc2a29e0cad8a43deaaf16e1`.

The keeper was clean, its `KEEP` marker remained present, and its existing `node_modules` link remained unchanged. No stale truncated driver digest was used.

## Evidence

Offline controls passed: the correct digest prefix passed in the same shell form; a wrong digest and a privately modified gate copy both refused before a post-`&&` child sentinel. Both registration lines matched the exact predicate and preserved the approved preflight/run argv.

The one allowed central source-only suite passed:

```text
test ap2-m2-parent-literal-digest-delta-review-0517-ap2-m2-parent-finalhash-preflight-0517-1021051812-12544: pass exit=0
```

It verified 76 artifacts, manifest `a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`, schema `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`, captured tree/keeper identity, and helper/driver hashes. All four negatives refused: wrong captured tree, wrong keeper, wrong helper hash, and wrong argv. Exact collection passed with one test: `three-products.spec.ts:1440`.

The exact actual command above is approved for a later authorized run. This review did not run it, and did not run a browser, hosted build, product edit, full suite, or install.
