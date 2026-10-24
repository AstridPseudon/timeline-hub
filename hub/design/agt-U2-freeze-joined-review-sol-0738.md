**SOURCE FAIL — reviewed `5783ae65c279518ba55f47ece98e138de0ff86f6`.** The intended union is intact, but the assertion-restoration acceptance is incomplete. No worktree files were changed.

Three findings remain:

1. [D18 line 3639](/home/user/work/wt/agt-U2-freeze-joined-review-sol-0738/tests/core/execution/test_generic_host_child_bridge_d18.py:3639) still calls unbounded `future.result()`. The original used `future.result(timeout=5)`. Five of the six original bounded future waits were restored.

2. [Activation line 253](/home/user/work/wt/agt-U2-freeze-joined-review-sol-0738/tests/integrations/test_generic_host_activation_acceptance.py:253) places claim-denial/no-attempt/queued assertions behind an unreachable branch on the asserted success path. `checked_accept()` requires an existing activation before readiness, and the final event sequence excludes the denial event. These predicates are present textually but do not exercise the promised refusal.

3. [Activation line 417](/home/user/work/wt/agt-U2-freeze-joined-review-sol-0738/tests/integrations/test_generic_host_activation_acceptance.py:417) patches `_parked_host_identity_matches`, but [production `abort()`](/home/user/work/wt/agt-U2-freeze-joined-review-sol-0738/astrid/sdk/host_bootstrap.py:1090) calls retained-process `terminate_group()` without that helper. The required `observed == ["identity"]` cannot be established through this setup. This is an inherited fixture incompatibility restored by the repair, not a new product guard regression.

The earlier boundary/coverage PASS reports overstate effective restoration.

Verified preservation:

| Area | Result |
|---|---|
| Joined tree | Exact blob-and-mode union of `cb6ce`, home delta, `9920`, `4ea033`, and `4c700`; zero mismatches |
| Ancestry | `3f7e63b0cf` is the actual second parent; upstream `25359ed…` is ancestral |
| Home preservation | Persistence fixture and all four discovery/reopen harness files retained exactly |
| Excluded work | Held `a181136220` absent from ancestry; no D39 tuple adoption |
| Deleted coverage | H3’s 3 tests/40 assertions, discovered-run hype invariants, CPU pin checks/30 managed-positive assertions, and C06 positive/five corruption cases restored |
| Boundary coverage | Discovery waits, admission deadline, materialization-budget refusal, lost-reply-after-claim condition, media identity/digest/confinement checks and exact decoded-frame equality retained; exceptions above |
| Other original0702 inventory | External-generation identity, JSON manifest media type, provider inline/upload provenance, executor identity, publication CAS readback, BT.709 filters and shared Remotion validation retained |
| Registry changes | Upstream workflow/lane migrations retained; five obsolete removal records eliminated, leaving `removed.yaml` identical to the original home |
| Guard integrity | Repair deltas add no skips, xfails or baseline increases |

R1/R2 implementation, generated interfaces, lock and editing-conformance sources remain unchanged from original home. Authenticated item/root ownership, previous-value/read/binding guards, undo and ABA handling therefore have no merge delta.

The production path remains `music pack → duck.run`, with adoption through `Checkout.publish → _commit_document → TimelineSession.submit → persisted outbox → timelines.commit`. Transport preserves the full request: API/scope/base IDs, commands, label, complete steps, merge, reads, dry-run, source/rationale/group and idempotency key. Replies retain canonical closure, IDs/digests, commands/id-map, records/steps/dependencies/effects/bindings, undo/history/publisher/receipt, preview status/null receipt, conflict head/reason and structured invalid diagnostics.

D40’s source-custody class and captured worker loader are AST-identical; executor/orchestrator loaders, owner fixture and custody tests are unchanged. Darwin-only peer-token refusal remains; no Linux relay or RunPod custody backend was introduced. No aggregate “12 guards/6 attacks” execution credit is claimed.

Checks performed:

| Exact command/check | Result |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 make ruff PY=/home/user/work/venv-agent/bin/python` | PASS, 2145/2145 |
| `PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR="$TMPDIR/mypy-joined-cache" make mypy PY=/home/user/work/venv-agent-typecheck-v2/bin/python` | PASS, 1902/1902 |
| Raw mypy with `--hide-error-context --no-color-output --no-pretty --show-error-codes` | 1902 diagnostics; zero duck diagnostics |
| `/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-45c3a7f4` | PASS |
| `/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check` | PASS |
| `git diff --check 1f15f27482 HEAD` and `git diff --check` | PASS |
| In-memory `compile()` over changed Python from `git diff --name-only 1f15f27482 HEAD -- '*.py'` | PASS, 57 files |

The six light controls passed: **6 passed in 4.16s**, using the existing VibeComfy fixture, explicit Runtime environment and `pytest -q -oaddopts= -pno:cacheprovider`. Selectors were the synthetic hype invariant, public CPU preflight, asset-map contract, synthetic readiness profile, candidate-manifest resolution and symlink rejection controls.

Retained **135-pass** evidence and zero-new-mypy-identity evidence remain applicable: the eight reviewed selectors, entire `astrid` and `scripts/reshape` trees, and `pyproject.toml` match `9920` exactly. A fresh parent diagnostic comparison was not repeated.

**Managed-workflow limitation:** seed/invocation/adoption/tagged-rerun execution remains unqualified here. Its 17 assertions and repaired Astrid authoring profile are retained; separate0738 owns the 136-test service row. No full, browser, gate, renderer or managed-service bodies were run.

Recommend repairing the remaining deadline and activation test setups, preserving production custody guards, then obtaining focused independent review and the separate service qualification. Review completed; required commit message and `DONE` were written.