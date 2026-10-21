# AP2-M2 parent newborn final custody review 0801

## Verdict

**APPROVE — custody/source review only.** This does not claim that the
mounted parent actual passed, and it does not authorize or submit that actual.

The true committed App source is:

```text
path=/home/user/work/wt/ap2-m2-parent-newborn-current-proof-source-0748
HEAD=af1605a28f31a53b5a3472251493d44941b618fe
TREE=b0cb1f973c0e1b465241ebef38bd267fd39f0434
spec=tests/e2e/local/three-products.spec.ts
spec_sha256=5c12370fe8a14439f6c82ddbf088bcfcc2fcdcbfb8af90cbba4ec30e72bb1603
```

The source worktree was clean at review. `af1605a28` is a child of
`0c9b7bf01`; its committed source diff is one file, six insertions and one
deletion. The only change is the reviewed strict refusal assertion:

```diff
-expect([404, 409]).toContain(wrongVerified.status());
+expect(wrongVerified.status()).toBe(404);
+await expect(wrongVerified.json()).resolves.toEqual({
+  code: 'not_found',
+  message: 'selected media is not a managed project generation/variant/object',
+  request_id: expect.stringMatching(/^[A-Za-z0-9][A-Za-z0-9._~-]{0,127}$/),
+});
```

The recorded preparation tree was `00bce13c888dda845b69a944c71aae7142e2e21e`;
that tree object is not present in the local Git object database, so it was
not treated as an authority and no unverifiable direct tree diff is claimed.
The committed diff above is the authoritative replacement. The final spec
hash equals the approved 0604 source hash and therefore rejects any
unaccounted source or assertion loss. The original parent journey retains the
full 404 body (`code`, `message`, `request_id`), import/selection/verified
reads, parent placement (`V1`, `at`), raw/opaque/order checks, native
`clip.add-media`, no `afterClipId`/`removeClipId`/`replaceClipId`, lost ACK,
exact retry body/key/response, reload, Runtime restart, undo, and zero legacy
traffic assertions.

HOME newborn ancestry is present and verified: `6bdb7dfad` (and its fix
`0a3b3eb79`) is an ancestor of the final source; the required ancestry
anchors `5d36b0e5`, `968bbad0`, and `6bdb7dfad` all pass
`git merge-base --is-ancestor`. The hold behavior is intentional: the
detached newborn row gets `hold = to - from` only for a finite positive
speed-one window, while the raw input remains unchanged and unsafe cases are
refused. The HOME oracle explicitly expects this (`hold: 5`, `from: 0`,
`to: 5`) and the original parent E2E oracle does not require an accepted row
to omit `hold`; it only checks the preserved placement/media fields. No
assertion conversion or source/helper/spec edit was made in this review.

## Custody verification

The owned final gate and unchanged promoted driver hashes are:

```text
gate=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-newborn-final-binding-preflight-0756/final-keeper-gate.sh
gate_sha256=cbf3bca135919ab43f3e6a02f1906df150448cd992e7501a7436cc4d68440270
driver=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-current-driver-durable-promotion-0535/run-parent-manual-drop-evidence.sh
driver_sha256=34ee03d1ea6f25ae4f68b8965f5c9b050d8892214416ec3bf551dfa81b17a2d2
helper=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-source-common.sh
helper_sha256=a0ed2bd7d6688799f22bc8f17f89631c603e4e692a8d5e71f3ee3b26437b27b3
```

Compared with immutable gate `0617` (`515931b8700aba3bf7b1a98e5013ecbe3c5769925b9ce21e44f4fb03b1a4a1e5`), the owned gate has exactly four binding edits: `KEEPER`, `FINAL_HEAD`,
`FINAL_TREE`, and `HELPER_SHA`. It retains independent captured-tree and
keeper HEAD/tree/clean/KEEP checks, ancestry, final95/pins, 76 artifacts,
manifest/schema, all77 and Composition archive `9412ae25`, locked graph,
exact argv/list-one collection, child and zero-test guards, and wrong
captured-tree/wrong keeper/wrong helper/wrong argv refusals.

The helper reverse proof was independently reproduced without writing the
shared helper: replacing exactly the one `final95:parent` SHA/tree pair with
the old pair yielded whole-file SHA
`d9a691dcaafd7d544a467445a3a020a9ad3d02afc1d527870f00be6948fea848`.
The new helper has exactly one occurrence of each final SHA/tree binding.

The 0756 offline preflight was reused as instructed and passed exit 0 with
captured tree `b0cb1f97`, keeper HEAD/tree `af1605a28`/`b0cb1f97`, clean/KEEP,
Agent `6efc8150`/tree `2ed2b8a1`, Runtime/producer `95bd3c5f`/tree
`d3a290b4`, 76 artifacts, all77, archive `9412ae25`, exact one-test list at
`three-products.spec.ts:1440`, and all four refusal controls.

## Durable failure evidence

The parent driver’s existing failure-retention proof is durable before inner
run-root cleanup. The supported packet is:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-central-keeper-command-preflight-0508/evidence-final95-parent-a304-central/run/
```

It contains `playwright-trace.zip`, `error-context.md`,
`bounded-browser-evidence.json`, `runner-tail.log`, `source-identity.txt`,
`evidence-presence.json`, `retention.log`, and `result.txt` with
`runner_status=1`; the packet remains outside the disposable run root. This
is retention/control evidence for the separate parent driver, not a claim
about producer23671 and not final-source behavior evidence. Producer23671’s
lost trace remains unknown; no producer defect is inferred.

## Exact proposed central commands

These are the literal 0756 registrations; hashes above were checked against
the files and were not manually altered:

```text
app ap2-m2-parent-newborn-final-binding-preflight-0756-preflight test "$(sha256sum -- '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-newborn-final-binding-preflight-0756/final-keeper-gate.sh' | cut -d' ' -f1)" = 'cbf3bca135919ab43f3e6a02f1906df150448cd992e7501a7436cc4d68440270' && test "$(sha256sum -- '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-current-driver-durable-promotion-0535/run-parent-manual-drop-evidence.sh' | cut -d' ' -f1)" = '34ee03d1ea6f25ae4f68b8965f5c9b050d8892214416ec3bf551dfa81b17a2d2' && env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent NORMAL014_USE_BASE_PYTHON=1 sh '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-newborn-final-binding-preflight-0756/final-keeper-gate.sh' preflight
app ap2-m2-parent-newborn-final-binding-preflight-0756-actual test "$(sha256sum -- '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-newborn-final-binding-preflight-0756/final-keeper-gate.sh' | cut -d' ' -f1)" = 'cbf3bca135919ab43f3e6a02f1906df150448cd992e7501a7436cc4d68440270' && test "$(sha256sum -- '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-current-driver-durable-promotion-0535/run-parent-manual-drop-evidence.sh' | cut -d' ' -f1)" = '34ee03d1ea6f25ae4f68b8965f5c9b050d8892214416ec3bf551dfa81b17a2d2' && env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent NORMAL014_USE_BASE_PYTHON=1 sh '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-newborn-final-binding-preflight-0756/final-keeper-gate.sh' run
```

## Commands/results and remaining prerequisites

- Read-only source diff/hash, ancestry, helper reverse-proof, gate diff, and
  hash checks: **PASS**.
- Reused 0756 offline preflight: **PASS**, exit 0.
- Reused parent-driver offline retention/child-exit/zero-test/refusal
  controls and existing independent source-safety evidence: **PASS**.
- No targeted source test was run here because this was a read-only custody
  review. No browser, build, daemon, socket, install, actual, test-service
  submission, full suite, or broad retest was run.

Remaining prerequisites are unchanged: separately authorize exactly one
central parent actual using the literal `...-actual` command above, preserve
its resulting durable failure/pass packet before cleanup, and independently
review that actual result. The final source/helper/driver/spec/pins must not
change before submission.
