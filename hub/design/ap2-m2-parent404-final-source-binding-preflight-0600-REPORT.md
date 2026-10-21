# App2 M2 parent404 final source binding and preflight

## Result

Final test-only parent source binding and the source-only preflight passed.
The mounted/browser actual remains unrun and is not authorized by this worker.

The independent 0559 assertion review remains a **HOLD**: its report found
that the browser-facing Runtime door strips `X-Request-ID`, so the 0556
matcher conversion cannot be treated as mounted behavior evidence. This
worker made no source/body assertion change and preserved that hold.

## Exact source and byte deltas

- Source: App commit `86f765532d25181a1f3e953fb08f79587d328f85`, tree
  `5f1d1d06432350eacbdd3d37ae8956b9fe2f756b`.
- Parent source is a direct child of the historical `a304dce02a185a4774ff514d5aa451c9702aa46f` source and retains the required
  `5d36b0e53ff0d17ef045e226a6e6ca7584322858` skeleton and
  `968bbad09449f419ab63782fca49cad805068333` ADD-forwarding ancestry.
- Relative to a304, the source has exactly one changed file and three added
  lines in `tests/e2e/local/three-products.spec.ts`: read the correlated
  `x-request-id`, validate its shape, and include it in the exact 404 body.
- `design/normal014-source-common.sh` changed only the two
  `final95:parent` assignments:

  ```diff
  -APP_ROOT_SHA=a304dce02a185a4774ff514d5aa451c9702aa46f
  -APP_ROOT_TREE=a3c82aa91f1336b86491191acf857d88c56179b2
  +APP_ROOT_SHA=86f765532d25181a1f3e953fb08f79587d328f85
  +APP_ROOT_TREE=5f1d1d06432350eacbdd3d37ae8956b9fe2f756b
  ```

  Old helper SHA-256: `af83e829f73ebcf9613e67808f81cab06c2e78f70c21bc850550cde1b5885fa4`.
  New helper SHA-256: `3d00bda70e2371cc4af507f5916345ff02674a04cdc807af15737295dde0656f`.
  Both files are 16,643 bytes; 75 byte positions differ, exactly the two
  assignment lines (two removed and two added lines). Other roles and pins
  are unchanged.

## Final gate and registrations

Created one new gate:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent404-final-source-binding-preflight-0600/final-keeper-gate.sh`

- Gate SHA-256: `b9693fb6ccfe954ac51b3246171850009eddcde048db180d7e81ecc75aa85b2f`.
- Approved 0535 gate source SHA-256: `2aebe7cce4aab7cbf2fb4292165687385edddb0351bab12c633537bfc09c7546`.
- Gate delta is limited to final keeper root/head/tree, its matching final
  KEEP marker path, and the helper digest. Promoted driver bytes, driver SHA,
  source runner, pins, selectors, arguments, mode checks, refusal guards,
  and `NORMAL014_USE_BASE_PYTHON=1` are unchanged.
- Promoted driver SHA-256 remains
  `34ee03d1ea6f25ae4f68b8965f5c9b050d8892214416ec3bf551dfa81b17a2d2`.
- Registered exactly two literal rows in `scratchpad/orch/tests/suites.conf`:
  `ap2-m2-parent404-final-source-binding-preflight-0600-preflight` and
  `ap2-m2-parent404-final-source-binding-preflight-0600-actual`.
  The actual row was not requested or run.

## Final cohort and literal preflight

The source helper closed the following final95 cohort:

```text
Agent       6efc81500a0e0688c2bb41e736503f0fc3e04abb / 2ed2b8a12b5b3391ca221ba6ff05390f71a73556
Runtime     95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c / d3a290b407fa61e6ab2d476f50c068073f70df00
Producer    95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c / d3a290b407fa61e6ab2d476f50c068073f70df00
Artifacts   sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac
Manifest    a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d, count 76
Schema      6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d
Wire        sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816
```

Literal registered preflight command:

```sh
test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent404-final-source-binding-preflight-0600/final-keeper-gate.sh | cut -d' ' -f1)" = 'b9693fb6ccfe954ac51b3246171850009eddcde048db180d7e81ecc75aa85b2f' && test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-current-driver-durable-promotion-0535/run-parent-manual-drop-evidence.sh | cut -d' ' -f1)" = '34ee03d1ea6f25ae4f68b8965f5c9b050d8892214416ec3bf551dfa81b17a2d2' && env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent NORMAL014_USE_BASE_PYTHON=1 sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent404-final-source-binding-preflight-0600/final-keeper-gate.sh preflight
```

Central request and result:

```text
request-test ap2-m2-parent404-final-source-binding-preflight-0600 ap2-m2-parent404-final-source-binding-preflight-0600-preflight
result: ...-1021060330-8353, PASS, exit 0, 8s
```

The central log verified the final service tree and keeper, helper/driver
hashes, 76 artifacts, manifest/schema pins, the parent-media source
preflight, and exact collection:
`three-products.spec.ts:1440`, total 1 test in 1 file.

## Controls and exclusions

Offline controls all refused as required: wrong tree, wrong keeper, wrong
helper digest, wrong driver digest, and wrong argv. Shell syntax for the
helper and gate and `git diff --check` passed. No product edit, build,
browser, mounted actual, full suite, dependency install, or actual-suite
request was performed. Temporary control files were cleaned up.
