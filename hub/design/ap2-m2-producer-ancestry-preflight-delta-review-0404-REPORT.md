# AP2 M2 producer ancestry/preflight delta review 0404

## Verdict

**HOLD — smallest custody defect found.** The finalized service snapshot is otherwise internally consistent, but the source guard does not close the allowed App-wrapper delta.

## Verified final identities

- Final central service snapshot tree: `4acab858b0f12a1878fc231a33f3d06af9b0bdc0`.
- Approved source: `00bbc22d63b4abe7275cfe9ad5f3762157d7394f`, tree `f41a45c01293b0248a27c490bb9e8aa02be33ecd`, parent `70dec48e88ea036bf160539b58b68bb64c38f3b3`.
- Original baseline: `4ef89267f00d193273441ff6dbb955f30d27d708`, tree `8c7393050ded32854503dfb7719a102b5dec94eb`.
- Final wrapper SHA-256: `3069891ce3c1f56fd66d138ccd5be2960bfb0158b368209704fc215ed3761b48`.
- External runner SHA-256: `be59b3da5c01e0df22ec556cc84cd25a2a1a4304cf4542035829003eecb2e75b`.
- Approved body/helper/config hashes and Agent/Runtime/graph identities match the fix report.

## Defect

In `scripts/testing/run-producer-public13-list.sh`, `check_approved_delta` computes the App diff and removes `scripts/testing/run-producer-public13-list.sh` with `grep -v`, but never checks that file's bytes equal the finalized wrapper SHA. The report records the SHA, but the guard does not enforce it.

This is material: the wrapper contains the only checks for exact App source ancestry, approved body/helper/config hashes, and the allowed delta. A drifted wrapper could remove or weaken those checks while leaving the external runner at the approved `be59b3da…` hash; the external runner does not independently enforce the App ancestry/body/helper/config checks. That violates the required immutable ancestry and closed allowed-delta custody, despite the current snapshot itself being correct.

Smallest fix: add a named check that hashes the wrapper at runtime and requires `3069891ce3c1f56fd66d138ccd5be2960bfb0158b368209704fc215ed3761b48`, or equivalent exact-content enforcement, then rerun the final service preflight.

## Evidence run

- `git show -s --format='source=%H tree=%T parent=%P' 00bbc22d...` and corresponding parent/baseline checks — PASS; exact `4ef89267 -> 70dec48e -> 00bbc22d` ancestry confirmed.
- `git show 4acab858...:scripts/testing/run-producer-public13-list.sh | sha256sum` — PASS, `3069891c…`.
- Snapshot wrapper piped to `sh -n`; external runner `sh -n` — PASS.
- Central service suite `ap2-m2-producer-existing-graph-command-preflight`, result `1021041126-12161` — PASS, exit 0. It emitted `public13 preflight PASS checks=10` with Agent `8130a401…`, Runtime `2c4ac180…`, graph `public13`, and private isolation. No build, list, browser, actual, or full suite ran.
- Fix worker evidence reports stale-parent, wrong-source, body-drift, graph-drift, dirty-tree, and zero/return-code controls failing closed; reviewed but not treated as closing the wrapper-hash gap.

## Next step

Do not authorize the actual producer run on this correction until the wrapper hash is enforced and the same final service preflight passes again. No code changes were made in this review worktree.
