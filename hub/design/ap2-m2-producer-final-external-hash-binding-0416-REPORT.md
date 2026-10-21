# AP2 M2 producer final external hash binding

## Result

Closed the independent 0404 HOLD by updating the three owned producer suite registrations in the shared test-service allow-list:

- `ap2-m2-producer-existing-graph-command-e2e-integration`
- `ap2-m2-producer-existing-graph-command-actual-e2e-integration`
- `ap2-m2-producer-existing-graph-command-preflight`

Each command now changes directory to the exact source worker, checks the wrapper SHA externally before invocation, and then invokes the existing wrapper. The wrapper does not contain a self-referential hash. No App product code, producer test body, wrapper, external runner, or live caller changed.

The external wrapper binding is:

```text
sha256sum -- /home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416/scripts/testing/run-producer-public13-list.sh
= 3069891ce3c1f56fd66d138ccd5be2960bfb0158b368209704fc215ed3761b48
```

The existing runner binding remains `be59b3da5c01e0df22ec556cc84cd25a2a1a4304cf4542035829003eecb2e75b`.

## Frozen identities

- Final worker: `97187ce3c1576559239f869067a9cef8ffb5f357`, tree `4acab858b0f12a1878fc231a33f3d06af9b0bdc0`.
- Harness-frozen 0404 source: `00bbc22d63b4abe7275cfe9ad5f3762157d7394f`, tree `f41a45c01293b0248a27c490bb9e8aa02be33ecd`.
- Frozen 0404 source parent: `70dec48e88ea036bf160539b58b68bb64c38f3b3`, tree `0a4e6e46b080843902624eeadd7c288bb5f5d928`.
- Original baseline: `4ef89267f00d193273441ff6dbb955f30d27d708`, tree `8c7393050ded32854503dfb7719a102b5dec94eb`.

## Evidence

- `sh -n scripts/testing/run-producer-public13-list.sh` — PASS.
- `sh -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-public13-effective-build-attachment-fix/public13-integration-runner.sh` — PASS.
- All three updated suite command lines parsed with `sh -n -c` — PASS.
- One-byte drift control in a private `/tmp` copy — PASS: the external hash gate returned status 1 and did not create the guarded-invocation sentinel. Original wrapper SHA remained exact; drift copy SHA was `9ebd32452f8e34078fe4a0cf551b84de8e69047fa7eeb346b6190eab9b20c3f7`.
- Final central service command:

  ```text
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-producer-final-external-hash-binding-0416 ap2-m2-producer-existing-graph-command-preflight --no-cache
  ```

  Result: `ap2-m2-producer-existing-graph-command-preflight-1021041952-21577` — PASS, exit 0. The runner reported `public13 hosted-build resolver PASS` followed by `public13 preflight PASS checks=10`; it did not run a build, browser, producer body, actual suite, or full suite.

The first two diagnostic service attempts exposed the snapshot-layer and working-directory requirements: the preserved 0404 source guard rejects an additional synthetic commit, and the resolver needs the exact source worker as its current directory. The final external command addresses both without changing the 0404 wrapper or runner.

Post-run checks passed: App worktree clean, shared `node_modules` target restored, temporary `.public13-effective-*` run roots removed, and wrapper/runner hashes unchanged. Prior actual `21671` remains a pre-build failure; no actual authorization was requested or inferred.

## Blockers and next steps

No blocker. The orchestrator may separately decide whether to authorize the actual suite; this worker did not run it.
