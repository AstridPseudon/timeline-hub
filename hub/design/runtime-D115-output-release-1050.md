# Runtime D115 normal output release — RELEASED

Published from the clean normal Runtime branch after exact-tree and source
identity checks.

## Identity

- Normal branch: `tl/integration`
- Actual normal HEAD: `42aad0e92f6da8ea83dd0a382a87e3acd12651b0`
- Actual normal tree: `085a5be70b56353deb41ae7d743336a4ccb7f29c`
- Normal checkout `/home/user/work/runtime`: clean.
- Reviewed author: `e65422348314084a1a3cb6687fcdc520c73347e8`
- Reviewed author tree: `085a5be70b56353deb41ae7d743336a4ccb7f29c` — exact.
- Full-tree `git diff --exit-code e65422348314084a1a3cb6687fcdc520c73347e8 -- .`: exit 0.
- Queue receipt: `queue/done/merge-rt-D115-output-projection-1037` → `42aad0e92`.

The author changed exactly `runtime_protocol/timeline_commit_auth.py` and
`tests/test_timeline_command_output_manifest_auth.py`. Their blobs and SHA-256
values match the reviewed author exactly:

- auth source blob `66d899edaac201a1700e7ddf9f62091753201bc9`, SHA-256
  `72d4611def6491ac39872e04551ed7d2f1c4872eb655c4b0a63055bd4b324b2d`;
- focused test blob `f8c29e32f8ade76401163c953eb476033343b25d`, SHA-256
  `e516d3280a1ed3606361e41c06add6b0395751b3015f259e57b5333de9590e81`.

## Qualified review

Independent `rt-D115-output-security-1042` is `PASS` for the exact author
tree. The genuine mounted Agent `82b6` regression is parent `369ffa` RED and
candidate `e654` GREEN. The review recorded 7 new manifest tests passed, 5
intermediate-image tests passed, 75 contract tests passed, 180 authentication
verifier tests passed with one exact parent-identical failure, native smoke 2
passed, and Ruff/Pyright/py_compile/diff-check passed.

The one failure is retained honestly:
`test_moved_history_replays_authenticated_original_and_landing` fails in both
candidate and exact parent because a synthetic `SimpleNamespace` lacks
`db_path`. It is baseline-identical and is not attributed to D115.

The prior D115 intermediate-image evidence and D112 store/port surfaces remain
protected. `runtime_protocol/timeline_commit_port.py`,
`runtime_protocol/timeline_commit_store.py`, and the D112 history/render tests
are unchanged from the prior normal tree. All 15 canonical client/schema paths
are SHA-256 identical to the normal parent.

This is normal integration provenance only. No additional approval, review,
body stage, tests, product/test edits, upstream action, or deletion was made.
The publisher ran no tests/typecheck/lint because the exact qualified tree was
reused. No 83-closure, full, P2, gate, core, final-cut, or ZIP claim is made.

Evidence: [release-verification.txt](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D115-output-home-release-1050/evidence/release-verification.txt)

## Handoffs

- Start ask: consume qualified normal `42aad0`.
- Owner: normal adopters and future D59 proof; by UTC.
- Agent main adopter `rt-U4a-D115-output-adopt-1051` may use this exact release;
  no duplicate local adopter and no retarget of full `30693`.
- Agent `82b6` product remains held until Agent home/full-core rules are met;
  the mounted GREEN here is not full-core credit.
- App ordinary normal tool adoption may batch future D111b/tags if not yet
  captured; no unchanged P2 singles or blind root claim.
- D111b held `85639` remains actual flat-gate pending; tags branch `2867` is
  partial, unreviewed, unmerged, and excluded from this release.
