# AP2 M2 producer external hash command review

## Verdict

APPROVED for the new external binding. No App source files were edited in this review.

The three owned suite registrations check the exact wrapper bytes before invoking the existing wrapper:

```text
cd /home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416 && test "$(sha256sum -- /home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416/scripts/testing/run-producer-public13-list.sh | cut -d' ' -f1)" = 3069891ce3c1f56fd66d138ccd5be2960bfb0158b368209704fc215ed3761b48 && sh /home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416/scripts/testing/run-producer-public13-list.sh /home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416 preflight
```

The list and actual registrations use the same `cd` and hash guard, ending in `list` and `run`, respectively. Because the hash test precedes `sh` in an `&&` chain, a wrapper mismatch is rejected before invocation and a passing guard preserves the wrapper's nonzero exit status. The existing wrapper/runner nonzero, zero-body, and postflight guards remain unchanged.

The exact registered commands are:

```text
cd /home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416 && test "$(sha256sum -- /home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416/scripts/testing/run-producer-public13-list.sh | cut -d' ' -f1)" = 3069891ce3c1f56fd66d138ccd5be2960bfb0158b368209704fc215ed3761b48 && sh /home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416/scripts/testing/run-producer-public13-list.sh /home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416 list
cd /home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416 && test "$(sha256sum -- /home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416/scripts/testing/run-producer-public13-list.sh | cut -d' ' -f1)" = 3069891ce3c1f56fd66d138ccd5be2960bfb0158b368209704fc215ed3761b48 && sh /home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416/scripts/testing/run-producer-public13-list.sh /home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416 run
cd /home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416 && test "$(sha256sum -- /home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416/scripts/testing/run-producer-public13-list.sh | cut -d' ' -f1)" = 3069891ce3c1f56fd66d138ccd5be2960bfb0158b368209704fc215ed3761b48 && sh /home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416/scripts/testing/run-producer-public13-list.sh /home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416 preflight
```

## Bound identities

- Final harness source: commit `97187ce3c1576559239f869067a9cef8ffb5f357`, tree `4acab858b0f12a1878fc231a33f3d06af9b0bdc0`, parent `00bbc22d63b4abe7275cfe9ad5f3762157d7394f`.
- Harness-frozen 0404 source: commit `00bbc22d63b4abe7275cfe9ad5f3762157d7394f`, tree `f41a45c01293b0248a27c490bb9e8aa02be33ecd`; parent `70dec48e88ea036bf160539b58b68bb64c38f3b3`.
- Baseline: `4ef89267f00d193273441ff6dbb955f30d27d708`, tree `8c7393050ded32854503dfb7719a102b5dec94eb`.
- Wrapper SHA-256: `3069891ce3c1f56fd66d138ccd5be2960bfb0158b368209704fc215ed3761b48`.
- Existing external runner SHA-256: `be59b3da5c01e0df22ec556cc84cd25a2a1a4304cf4542035829003eecb2e75b`.

## Evidence

- Wrapper syntax, external runner syntax, and all three suite command lines: PASS.
- One-byte wrapper drift control: PASS. Drift SHA `9ebd32452f8e34078fe4a0cf551b84de8e69047fa7eeb346b6190eab9b20c3f7` returned status 1 and did not create the guarded-invocation sentinel.
- Final central preflight command:

  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-producer-final-external-hash-binding-0416 ap2-m2-producer-existing-graph-command-preflight --no-cache`

  Result `ap2-m2-producer-final-external-hash-binding-0416-ap2-m2-producer-existing-graph-command-preflight-1021041952-21577`: PASS, exit 0. It reported `public13 hosted-build resolver PASS` and `public13 preflight PASS checks=10`, with Agent `8130a401bf44a518d5a40ae274d398b8c560be55`, Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, public13 graph, and private isolation.

No build, browser, producer body, actual suite, or full suite was run. The earlier actual `21671` remains a pre-build failure; this review does not authorize an actual run.

