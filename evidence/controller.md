# D141p freeze-2 execution controller handoff

Status: `NOT_READY`; no service submission, registration, checkout, preflight, browser, provider import, collection, or body occurred.

## Admission and source order

1. Agent performs its freeze-2 merge-forward first and returns the qualified full head/tree, clean source receipt, and producer provenance.
2. App finishes the authorized merge-forward onto the verified `d822d2f5d2bd05187b4ff5b6071c3e13945d4747` tip, receives independent review, and has the source worker—not this packet—run `scripts/installer/update-manifest.mjs`. The candidate `8f278b91…` stays unmerged.
3. Receive the genuine four-way tuple and exact detached checkouts. Validate every full 40-character commit/tree, clean status, parent/origin identity, source receipt, and no mutable-home substitution.
4. Receive the installed Runtime paired-kit receipt, its source/review/CAS hashes, and the supported API for the paired admission/continuous trace. If the installed API is missing, use the ordinary 5 GB rule and `WAIT`; invent no flags and do not edit `--run` or queue routes.
5. Take one paired admission at `>= 4,600,000,000` available bytes. Require a continuous 5-second `KEEP` trace through preflight/body, stop at `4,000,000,000` before/during/after, and run one heavy unit at a time. There is no second floor gate between preflight and body. The source-only packet itself has no proof-body admission.

The final source tuple, paired kit receipt, fresh admission, exact builder output, and recorded final authorization are immutable prerequisites. Until then, this controller is `NOT_READY` and emits no final binding.

## D66-only route

The later production caller uses the existing D66 `--submit` path from the genuine final App source, followed only by the central service:

```text
cd /home/user/work/app
env -u NODE_PATH -u ASTRID_PUBLIC_CHECKOUT -u ASTRID_APP_DIRECT_DIST -u APP_DIRECT_DIST \
  D66_SUBMIT_TARGET=app-pin-${APP_HEAD8} \
  D66_SUBMIT_PLAN_PATH=<unique-existing-controller-evidence>/<selector>/submit-plan.json \
  D66_OUTPUT_DIR=<unique-existing-controller-evidence>/<selector>/d66 \
  D66_SUBMIT_SUITE=d141g-${selector}-${APP_HEAD8}-submit \
  /home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node \
  --max-old-space-size=6144 --import tsx scripts/testing/d66-plain-stack.mjs ${selector} --submit
```

The D66 caller must use the real `buildSubmitPlan`/`serviceRecipe` output and its normal receipt-backed checkout path. `--submit` atomically registers the paired rows; then use only:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test app-pin-${APP_HEAD8} d141g-${selector}-${APP_HEAD8}-submit-preflight --no-cache
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test <preflight-result-id>
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test app-pin-${APP_HEAD8} d141g-${selector}-${APP_HEAD8}-submit --no-cache
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test <normal-result-id>
```

Run preflight first and queue normal only after preflight PASS. Compare the actual registered bytes to the production-builder bytes before either paired part. Do not use direct `--run`, hand-written rows, a broad P2 row, or an old row. Preserve old `18617` and `19479` unchanged; do not retarget or cancel them.

## Selector order and disposition

Run the eight paired selectors in this order, one heavy at a time:

1. `p2-automatic-child-placement`
2. `p2-popup-add`
3. `p2-parent-move`
4. `p2-transition-none-single`
5. `p2-transition-none-bulk`
6. `p2-register-asset`
7. `p1`
8. `p3`

The six P2 rows are the named six only. `SWAP`, `Element`, broad P2, D136, B022, Gate3, D77, profile work, own investigations, and refused routes remain out of scope; no duplicate P4/P5 body is added.

The existing HARD Sol0149 lineage is reserved only for a newly proved `REG` result; it is not a source or admission shortcut.

D141j popup ADD remains unchanged. If it passes, report `NOT REPRODUCED` and `cause undetermined`; do not call it fixed. If it fails, preserve the failure and stop popup ADD. Any later diagnostic body requires exactly these four structural fields to be proven visible in a retained pre-body artifact first: read-head continuity; occurrence presence in that read; `activeCanonicalOccurrences` before `useShotGroups`; shot-group output before `ShotGroupOverlay`. No collector is introduced now.

Before claiming P4 carryover, check the actual freeze-2 source against `app-P4-D141-path-independent-0226-source-map.json`. If the path changed, use the existing owner decision; do not create a duplicate P4/P5 body.
