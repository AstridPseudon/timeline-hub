# Parent central-command custody review 0508

Decision: HOLD approval of both registered suite commands on one remaining literal-command defect. The source tuple and central source-only evidence are approved; the preflight and actual rows must pin the final SHA-256 of their external executable guard in the literal command.

## Approved source tuple and evidence

- Captured service tree: `a3c82aa91f1336b86491191acf857d88c56179b2`.
- Original keeper: HEAD `a304dce02a185a4774ff514d5aa451c9702aa46f`, tree `a3c82aa91f1336b864911acf857d88c56179b2`, clean, with its `KEEP` marker and existing `/home/user/work/app/node_modules` link.
- Helper: `af83e829f73ebcf9613e67808f81cab06c2e78f70c21bc850550cde1b5885fa4`.
- Durable driver: `40c7b57b6f327bafa82f26daaa4053f405e89f7bd48b5aacdadd21b2393867f0`.
- Source preflight reported 76 verified artifacts, manifest `a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`, schema `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.
- Own evidence directory: `.../scratchpad/orch/workers/ap2-m2-parent-central-keeper-command-preflight-0508/evidence-final95-parent-a304-central/preflight`.

The central source-only preflight passed at result `.../tests/ap2-m2-parent-central-keeper-command-preflight-0508-ap2-m2-parent-central-keeper-command-preflight-0508-preflight-1021051417-15272/` (exit 0). Wrong captured tree, wrong keeper, wrong helper hash, and wrong argv all refused. Exact collection passed with one test: `three-products.spec.ts:1440`.

## Smallest defect

The registered rows currently invoke this external guard without pinning its own final digest:

    app ap2-m2-parent-central-keeper-command-preflight-0508-preflight /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-central-keeper-command-preflight-0508/final-keeper-gate.sh preflight
    app ap2-m2-parent-central-keeper-command-preflight-0508-actual /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-central-keeper-command-preflight-0508/final-keeper-gate.sh run

The guard’s current SHA-256 is `2fe1bf06d796d1342870a02a06a0d0f10057ba20bc2a29e0cad8a43deaaf16e1`. Add an inline literal check before each invocation: compute the guard SHA-256 and require equality to that exact value, then invoke the same `preflight` or `run` command. This satisfies the rule that an executable wrapper outside the captured source must be final-hash-pinned in the literal command.

After that literal pin is added, rerun only the source preflight command; no actual/browser/build/full run is authorized by this review. The actual command remains unrun.

## Review scope and tests

Prior 0501 source/helper/body approval was reused as directed; it was not replayed. No source edits, build, browser/actual, hosted, or full suite run was performed. The only central run requested for this review was the source-only preflight above.

Two transient command defects were caught and corrected before the passing result: the driver digest initially omitted its final `0`, and the wrong-helper negative initially did not refuse. The final retained evidence shows the corrected 64-character digest and all four refusals.
