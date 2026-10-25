# Runtime D115 normal-home release — RELEASED

Published from the actual clean normal Runtime head after exact-tree verification.

## Identity

- Normal branch: `tl/integration`
- Actual normal HEAD: `369ffa7c00bd3d45c610fac7651ff79e7a283a1a`
- Actual normal tree: `9bf331d68df8c966e8927a3f083ba03687803c99`
- Reviewed author: `274bbf7d73c543d72058ce3563eba2af5cdc4bd1`
- Reviewed author tree: `9bf331d68df8c966e8927a3f083ba03687803c99` — exact.
- Normal merge receipt: `merge-rt-D115-intermediate-image-1002` → `369ffa7c0`.
- `/home/user/work/runtime` was clean. `git diff --exit-code 274bbf7d73c543d72058ce3563eba2af5cdc4bd1 -- .` exited 0.

The merge changed exactly `runtime_protocol/timeline_commit_auth.py` and the new `tests/test_timeline_intermediate_image_auth.py`. No source, client, schema, or test blob differs from the reviewed author tree.

## Qualified evidence and applicability

The existing independent security review is explicit `PASS`. Because the actual normal tree is exactly the reviewed tree, this publication reused its evidence and ran no additional tests.

- Candidate regression: 5 passed.
- Parent comparison: 1 genuine RED (`provider intermediate parent lacks an effect image`) and 4 strict refusals passed.
- Strict neighbors: 321 passed, 74 deselected.
- Real registered-provider smoke: 2 passed, no skips/deselections.
- Release smoke control: 1 passed.
- Authentication integration: candidate 39 passed/1 failed; exact parent 39 passed/1 same failure.
- Sequential verifier: candidate 66 passed/1 known excluded failure; exact parent 66 passed/1 same failure.

The failures are preserved and disclosed. The integration failure is the baseline-identical `sequential original or landing input does not match its authenticated head`. The verifier exclusion is the baseline-identical synthetic `SimpleNamespace` missing `db_path`. This packet makes no 83-closure, full-suite PASS, final-tuple, gate, core, or ZIP claim.

Evidence paths and SHA-256 values, including raw exit statuses, candidate/parent JUnit, smoke, service, and custody paths, are in the companion JSON and the worker evidence file:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D115-home-release-1025/evidence/release-verification.txt`

## Source custody and unchanged surfaces

The changed auth source is SHA-256 `68e594537c09cc1c49f02ab9657fb8c76166763098b6932fc6c75741b957d9dc`; the new regression test is `90c09fa44d098333e6b7dcbbd20ed0af5c653ebd5c37f7667d0d9883e18ad6c1`. The parent auth source is `357d7c473d8e1af42646aea57657222123cc039adde16f2700629991d25beafd`.

The source custody chain is the mounted App/registered Agent provider through Agent `_commit_preview.py` and `commit.py`, Runtime `RequestCommitPort` and `service.py`, then Runtime auth validation. The 15 canonical client/schema paths remain byte-identical to the preserved D112a source. D112a store/history/render source remains preserved; no DTOs changed.

The public C0v2 request and reply surfaces remain unchanged: request fields include `api_version`, project/timeline/base revision and publication IDs, commands, label, steps, merge/reads, dry-run, and `Idempotency-Key`; replies retain accepted/merged canonical document, receipt, head, effects, bindings, dependencies, conflict head/reason, invalid code/path/hint, and dry-run forms.

## Handoffs

- Agent: normal tool adoption is required before the next unfiltered-core count can qualify 83 actual nodes. Do not retarget inflight core. The existing D115 regression is accepted; no 83-body/full repeat until a D118-authorized batch.
- App: current 15203 remains captured `96d475/070dfc/d23a8/635f`; no retarget/repeat. Only the future D59 matrix decides adoption/gate rerun.

This is normal integration provenance only. No upstream, proof/evidence branch, credentials, private payloads, or extra stage was used.
