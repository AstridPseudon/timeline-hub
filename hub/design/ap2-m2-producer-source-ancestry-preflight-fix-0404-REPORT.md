# AP2 M2 producer source-ancestry/preflight repair

## Result

Repaired the harness/source-guard failure only. The source guard now preserves the exact approved ancestry:

```text
4ef89267f00d193273441ff6dbb955f30d27d708
  -> 70dec48e88ea036bf160539b58b68bb64c38f3b3
    -> 00bbc22d63b4abe7275cfe9ad5f3762157d7394f
```

Final source identity:

- HEAD/source SHA: `00bbc22d63b4abe7275cfe9ad5f3762157d7394f`
- source tree: `f41a45c01293b0248a27c490bb9e8aa02be33ecd`
- immediate parent: `70dec48e88ea036bf160539b58b68bb64c38f3b3`
- original baseline tree: `8c7393050ded32854503dfb7719a102b5dec94eb`
- final central preflight snapshot tree: `4acab858b0f12a1878fc231a33f3d06af9b0bdc0`

The guard accepts the exact approved source or the test service's one synthetic child of that source. It does not accept an arbitrary ancestor. The approved body/helper/config hashes remain unchanged:

- body/spec: `d91d0c1cce22f68119cd30fcb0a288346474b0ad4b64c84dcee3b730fa468d89`
- helper: `50cbe5341f24c9a1ecc999018e2c6d975380a3440570abce151f9173c9752016`
- config: `5b880ceff883abce2575a3a85aaa4eda69d3bcb848768ff0e91f337d50cca4c0`

Allowed delta:

- App source path: `scripts/testing/run-producer-public13-list.sh` only, SHA-256 `3069891ce3c1f56fd66d138ccd5be2960bfb0158b368209704fc215ed3761b48`.
- Existing external runner, same path, updated only for the closed preflight/check aggregation: SHA-256 `be59b3da5c01e0df22ec556cc84cd25a2a1a4304cf4542035829003eecb2e75b` (previous approved runner `40c25724…`).
- One owned suite entry was added: `ap2-m2-producer-existing-graph-command-preflight`.
- No product, journey, pin, generated, bootstrap, graph, or framework files changed. No live callers changed.

## Preflight behavior

`run-producer-public13-list.sh` now has closed `list`, `run`, and `preflight` modes. The preflight aggregates named failures for source ancestry, approved delta, body/helper/config hashes, Agent/Runtime cohort, graph/archive/Composition bytes, disk, isolation, and argv/test-path checks. It invokes the existing runner with `PUBLIC13_PREFLIGHT_ONLY=1`; the runner performs the same source/graph/cohort/isolation setup and resolver check, then exits before build, list, browser, or actual body. Actual mode uses the same checks. Existing one-child, zero-body, and child-RC traps remain.

The original cause was confirmed from the exact chain: the old guard required the snapshot's immediate parent to be `4ef89267`, but approved source `00bbc22d` is correctly based on `70dec48e` and carries the approved runner change. The repair records both parent links and the exact approved source instead of weakening ancestry.

## Evidence

- `sh -n scripts/testing/run-producer-public13-list.sh` — PASS.
- `sh -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-public13-effective-build-attachment-fix/public13-integration-runner.sh` — PASS.
- `git diff --check` — PASS.
- Final source-only central command:

  ```text
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-producer-source-ancestry-preflight-fix-0404 ap2-m2-producer-existing-graph-command-preflight --no-cache
  ```

  Result `ap2-m2-producer-existing-graph-command-preflight-1021041126-12161`: PASS, exit 0. The runner emitted `public13 preflight PASS checks=10` with Agent `8130a401…`, Runtime `2c4ac180…`, public13 graph, and private isolation. No build, list, browser, actual, or full suite ran.

- Planted stale-parent and wrong-source controls — FAIL closed with `source-ancestry` named.
- Planted body-drift control — FAIL closed with `body-helper-config-hashes` named.
- Planted graph-drift control — FAIL closed with `graph` named.
- Forwarder controls — PASS: one pass/zero, one fail/nonzero, zero output, pass/nonzero, fail/zero, and list-only output were all classified correctly.
- Dirty-tree control — FAIL closed with all applicable names, not an empty log.

## Not run / next step

No actual producer authorization was present, so the actual run, browser journey, and full suite were not run. The next authorized action, if the orchestrator chooses it, is one actual suite run against this final source snapshot; the preflight is now available as the required first command.
