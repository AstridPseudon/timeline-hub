# App2 final95 parent binding custody review

## Verdict

**APPROVE** the exact `final95:parent` source/helper/command tuple below.
No product source, live caller, bootstrap proof, hosted build, actual, browser,
or full suite was run by this review.

## Exact tuple

- Captured source / keeper commit: `a304dce02a185a4774ff514d5aa451c9702aa46f`
- Captured source / keeper tree: `a3c82aa91f1336b86491191acf857d88c56179b2`
- Required skeleton `5d36b0e53ff0d17ef045e226a6e6ca7584322858`: ancestor — PASS
- Required ADD forwarding `968bbad09449f419ab63782fca49cad805068333`: ancestor — PASS
- Exact 404 assertion and body remain in `tests/e2e/local/three-products.spec.ts`:
  `404`, `code: not_found`, and
  `selected media is not a managed project generation/variant/object`.
- Keeper worktree was reported clean; source `KEEP` exists at
  `workers/ap2-m2-parent-complete-current-proof-source-0455/KEEP`.
- Ignored dependency link resolves to `/home/user/work/app/node_modules`.
- Durable 0323 driver SHA-256:
  `40c7b57b6f327bafa82f26daaa4053f405e89f7bd48b5aacdadd21b2393867f`.

The closed final95 tuple remains App `10fa2ff9a8216604aa39e3584f89dc9e7a09080a`,
Agent `6efc81500a0e0688c2bb41e736503f0fc3e04abb` / tree
`2ed2b8a12b5b3391ca221ba6ff05390f71a73556`, and Runtime/producer
`95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` / tree
`d3a290b407fa61e6ab2d476f50c068073f70df00`, with the reported artifact,
manifest, schema, wire, private graph, and Composition digests unchanged.

## Shared helper custody

`normal014-source-common.sh`:

- old SHA-256: `b4b142931573d6954af75ee91dd5f1c2c6cbb5a97dc4c65cbdb450ceeec04cb7`
- approved new SHA-256: `af83e829f73ebcf9613e67808f81cab06c2e78f70c21bc850550cde1b5885fa4`

The only diff is the `final95:parent` pair:

```diff
-APP_ROOT_SHA=b833512fcb5ef07013c47fcf8c75c4a083048d99
-APP_ROOT_TREE=a95793cc2179200dd9ef5fe551360a4f6f965ea1
+APP_ROOT_SHA=a304dce02a185a4774ff514d5aa451c9702aa46f
+APP_ROOT_TREE=a3c82aa91f1336b86491191acf857d88c56179b2
```

All other profiles, pins, guards, and the durable driver are byte-identical.
Live callers are unchanged.

## Evidence reviewed

Private evidence directory:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-owned-final-binding-preflight-0501/evidence-final95-parent-a304`

Approved command tuple:

```sh
env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent \
  NORMAL014_USE_BASE_PYTHON=1 \
  NORMAL014_RUN_ROOT=<private-evidence>/run TMPDIR=<private-tmp> \
  sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-parent-media-central.sh \
  preflight /home/user/work/wt/ap2-m2-parent-owned-final-binding-preflight-0501
```

The unchanged normal caller remains:

```sh
env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent \
  sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-composed-driver-label-durable-stage-0323/run-parent-manual-drop-evidence.sh \
  run "$PWD"
```

- Same permitted source-only full preflight: PASS — 76 artifacts, manifest
  `a902387c...`, schema `6ba7b51e...`, marker, locked graph, imports, and
  shell guards verified; no cohort/vendor mismatch.
- Wrong source: refused, exit 1.
- Wrong role: refused, exit 1.
- Wrong graph: refused, exit 1.
- Wrong argv: refused, exit 2.
- Zero-child/failure-trap probe: PASS; simulated zero-test child refused and
  evidence was copied before disposable-root cleanup.
- Exact list-only collection: PASS — exactly one test,
  `three-products.spec.ts:1440`.
- Shell syntax for the helper, durable driver, and parent preflight: PASS.

The worker's first combined negative-check command exited 1 only because it
incorrectly expected a nested source-identity file from the probe after the
probe had intentionally cleaned its disposable evidence. The individual
refusal controls, probe, persistent evidence directory, and collection check
were then verified successfully; this is not a source or binding defect.

No actual authorization is granted by this review. The next step is the
separately authorized single mounted parent ADD, if the orchestrator proceeds.
