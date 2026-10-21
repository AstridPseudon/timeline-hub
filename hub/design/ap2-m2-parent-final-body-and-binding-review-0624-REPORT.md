# App2 M2 parent final body and binding review

## Verdict

**APPROVE** the exact final source, source/artifact custody, and literal
0617 actual-suite binding. This is an approval to execute that bound actual
lane; it is not a claim that the actual/browser lane has passed. No actual,
browser, build, full-suite, install, or source/artifact edit was performed by
this review.

The 0604 correction is a one-to-one assertion conversion from the original
`a304dce02a185a4774ff514d5aa451c9702aa46f` source: one required
`request_id` matcher field was added to the existing exact 404 body. The
status, `not_found` code, full message, and all later ADD/raw/order/reload,
lost-ACK/restart, exact-retry, undo, and zero-legacy assertions are unchanged.
The matcher is closed and exact; it uses no browser header, `objectContaining`,
field stripping, or weaker partial assertion.

## Exact final tuple

| Item | Value |
| --- | --- |
| App HEAD | `acb582c2c3b08481d43853b8526894ac60d074bc` |
| App tree | `141724b56736be40a269f60aa8bfc060914ebd29` |
| Source path | `tests/e2e/local/three-products.spec.ts` |
| Final source Git blob | `67934dbcd263d6dc52648e176c8401f94338bfc7` |
| Final source SHA-256 | `5c12370fe8a14439f6c82ddbf088bcfcc2fcdcbfb8af90cbba4ec30e72bb1603` |
| Final binary diff SHA-256 vs `a304` | `e90f1888922315c4c9a26441937b3fd1ebaf7c756465810b116d0fabc750ac77` |
| Helper | `normal014-source-common.sh` |
| Helper SHA-256 | `d9a691dcaafd7d544a467445a3a020a9ad3d02afc1d527870f00be6948fea848` |
| Final gate SHA-256 | `515931b8700aba3bf7b1a98e5013ecbe3c5769925b9ce21e44f4fb03b1a4a1e5` |
| Driver SHA-256 | `34ee03d1ea6f25ae4f68b8965f5c9b050d8892214416ec3bf551dfa81b17a2d2` |

The final95 cohort retained by the helper is Agent
`6efc81500a0e0688c2bb41e736503f0fc3e04abb` / tree
`2ed2b8a12b5b3391ca221ba6ff05390f71a73556`, Runtime and producer
`95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` / tree
`d3a290b407fa61e6ab2d476f50c068073f70df00`, 76 artifacts, manifest
`a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`, and
schema `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.

## Independent checks

- `git status --short --branch` — clean at `acb582c2…`.
- HEAD/tree, required `KEEP`, `node_modules` symlink, and ancestry checks —
  PASS. Required ancestors `5d36b0e5…`, `968bbad0…`, and original
  `a304dce0…` are reachable. The dependency link is exactly
  `/home/user/work/app/node_modules`.
- Helper profile command:

  ```sh
  env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent sh -c \
    '. "$1"; printf "APP_ROOT_SHA=%s APP_ROOT_TREE=%s\\n" "$APP_ROOT_SHA" "$APP_ROOT_TREE"' \
    sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-source-common.sh
  ```

  PASS; returned exactly `acb582c2c3b08481d43853b8526894ac60d074bc` /
  `141724b56736be40a269f60aa8bfc060914ebd29`.
- In-memory reverse of only the final parent pair, never written, hashed to
  the required old helper `af83e829f73ebcf9613e67808f81cab06c2e78f70c21bc850550cde1b5885fa4`.
  This proves the other helper bytes, roles, modes, pins, and guards are
  unchanged.
- `sh -n` on helper, final gate, and driver — PASS.
- Driver comparison against `HEAD:tests/e2e/local/support/run-parent-manual-drop-evidence.sh` — byte-identical; base-Python, ancestry, refusal, and zero-test guards retained.
- `git diff --name-only a304… HEAD`, `git diff --numstat a304… HEAD`, and
  `git diff --check a304… HEAD` — exactly one file, `1/0`, PASS.
- Compact strict-body check using the retained 6715 body
  (`request_id=85fa632fa90f48f790f0cf4f55cebb20`) — 1 valid body accepted;
  missing ID, invalid ID, wrong code, wrong message, and extra field each
  refused.
- Literal suite rows — PASS. Both
  `ap2-m2-parent-pin-final-acb-explicit-0617-preflight` and `…-actual` pin
  the recomputed gate and driver hashes; the gate pins the recomputed helper
  hash and final HEAD/tree.

## Central and retained evidence

The retained central command was:

```sh
request-test ap2-m2-parent-pin-final-acb-explicit-0617 \
  ap2-m2-parent-pin-final-acb-explicit-0617-preflight
```

Result `…-1021062025-31285`: **PASS**, exit 0 in 10 seconds. It verified the
captured service tree, protected keeper, helper/driver hashes, 76 artifacts,
manifest/schema, final95 parent source preflight, all negative custody
controls, and exactly one collected test (`three-products.spec.ts:1440`).

The exact registered actual command is:

```sh
test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-pin-final-acb-explicit-0617/final-keeper-gate.sh | cut -d' ' -f1)" = '515931b8700aba3bf7b1a98e5013ecbe3c5769925b9ce21e44f4fb03b1a4a1e5' && \
test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-current-driver-durable-promotion-0535/run-parent-manual-drop-evidence.sh | cut -d' ' -f1)" = '34ee03d1ea6f25ae4f68b8965f5c9b050d8892214416ec3bf551dfa81b17a2d2' && \
env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent NORMAL014_USE_BASE_PYTHON=1 \
sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-pin-final-acb-explicit-0617/final-keeper-gate.sh run
```

This actual row is approved as the exact bound command but was not submitted
by this review.

The retained 6715 actual on the predecessor `a304` source failed at the old
two-field body assertion before any positive downstream assertions. Its raw
body contained the exact 404 code/message plus the valid request ID, while the
browser-facing trace had no `X-Request-ID` response header. Pinned Runtime95
`common.json` requires the closed `Error` body fields `code`, `message`, and
`request_id`, with the stated `Id` pattern; pinned `door.py` intentionally
strips `X-Request-ID`. Therefore the body-only final conversion is the
correct settled contract and supersedes rejected header-based `86f`.

The live caller chain is unchanged:

`onTimelineDrop -> useExternalDrop.ts -> external-drop-utils.ts ->
useAssetManagement.placePreparedAsset -> createTimelineCommands.addClip ->
existing commit-session/outbox path`.

No concrete defect remains in the requested final source/binding review. The
downstream positive journey remains explicitly **unverified** until the
separately authorized 0617 actual lane runs. `HOME.md` was not present in the
orchestration tree; PLAN, manager STATUS, manager INBOX, and the relevant
0604/0617/retained-6715 evidence were read.
