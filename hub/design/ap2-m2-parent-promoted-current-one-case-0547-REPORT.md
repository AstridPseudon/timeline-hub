# AP2 M2 parent promoted current one-case 0547

## Result

The one approved central actual was submitted exactly once and failed in the mounted browser case. No App source, assertion, caller, helper, selector, timeout, pin, or option was changed. No retry was submitted.

- Test ID: ap2-m2-parent-promoted-current-one-case-0547-ap2-m2-parent-current-driver-durable-promotion-0535-actual-1021054752-6715
- Status: FAIL, exit 1, 78s
- Count: 1 collected, 1 executed, 1 failed, 0 passed
- Exact suite: ap2-m2-parent-current-driver-durable-promotion-0535-actual
- Tree: a3c82aa91f1336b86491191acf857d88c56179b2
- Frozen keeper: HEAD a304dce02a185a4774ff514d5aa451c9702aa46f, clean, KEEP present
- Driver SHA-256: 34ee03d1ea6f25ae4f68b8965f5c9b050d8892214416ec3bf551dfa81b17a2d2
- Gate SHA-256: 2aebe7cce4aab7cbf2fb4292165687385edddb0351bab12c633537bfc09c7546
- Helper SHA-256: af83e829f73ebcf9613e67808f81cab06c2e78f70c21bc850550cde1b5885fa4
- Driver is byte-identical to HEAD:tests/e2e/local/support/run-parent-manual-drop-evidence.sh.
- 5d36b0e53ff0d17ef045e226a6e6ca7584322858 and 968bbad09449f419ab63782fca49cad805068333 are keeper ancestors.
- Keeper node_modules resolves to /home/user/work/app/node_modules; local browser flock was nonblocking/idle; free space was 14 GiB; no new App/source copy was made.

## Exact command

    test "$(sha256sum -- '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-current-driver-durable-promotion-0535/final-keeper-gate.sh' | cut -d' ' -f1)" = '2aebe7cce4aab7cbf2fb4292165687385edddb0351bab12c633537bfc09c7546' && test "$(sha256sum -- '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-current-driver-durable-promotion-0535/run-parent-manual-drop-evidence.sh' | cut -d' ' -f1)" = '34ee03d1ea6f25ae4f68b8965f5c9b050d8892214416ec3bf551dfa81b17a2d2' && env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent NORMAL014_USE_BASE_PYTHON=1 sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-current-driver-durable-promotion-0535/final-keeper-gate.sh run

Central source preflight ...-1021054051-11866 passed with the same tree, 76 artifacts, and exact listing three-products.spec.ts:1440:1 / Total: 1 test in 1 file.

## First failure packet and boundary

Build and all pre-browser custody checks passed. The first browser assertion failed at tests/e2e/local/three-products.spec.ts:1505. The real wrong-verified-selection request returned:

    GET /api/runtime/v1/projects/edb1507099a64ed7af9cd84eff22306b/media-selection/verified
      object_id=sha256:1d9fd75956a1fc3a7e57b0e26f0d2ea521b0f4e66286068025a077e9290b2350
    HTTP 404

Expected body:

    {"code":"not_found","message":"selected media is not a managed project generation/variant/object"}

Raw Playwright body included the same fields plus "request_id":"85fa632fa90f48f790f0cf4f55cebb20", causing deep-equality failure. The retained bounded sanitizer records the 404 body without request_id. Trace, error context, runner tail, sanitized request/response summary, source identity, and runner_status=1 are retained.

The failure is before page.unroute, positive ADD, command body/key checks, lost-ACK/reload/restart recovery, exact retry, undo, opaque/order, and zero-legacy assertions. These are unverified, not failures.

## Source and live callers

Source identity was unchanged: App a304dce02a185a4774ff514d5aa451c9702aa46f; Agent 6efc81500a0e0688c2bb41e736503f0fc3e04abb; Runtime/producer 95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c; schema sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816; manifest a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d; 76-artifact schema 6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d.

Live callers unchanged:

    onTimelineDrop -> useExternalDrop.ts -> external-drop-utils.ts
    -> useAssetManagement.placePreparedAsset -> createTimelineCommands.addClip
    -> existing commit-session/outbox path

## Tests and disposition

- Central preflight ...-1021054051-11866: PASS, exit 0.
- Central actual ...-1021054752-6715: FAIL, exit 1.
- No local browser/full/install/source test was run.
- App worktree is clean; no deletion or product fix was made.
- Qualification is blocked on the response-envelope mismatch. Decide whether request_id is an approved 404 field or whether Runtime must match the exact assertion; only then review any downstream proof or rerun.
