# Runtime review: selected PARAM authority port

## Verdict

**ACK for the bounded Runtime port review; no Runtime counterpart is needed.**
The exact Agent successor is present and includes the authentic legacy-alias
positive repair:

- Agent `6868e16a590af64fc764159489b8e4ed22f526d0`, tree
  `8a6b41c79e5975856f0c2bde24546c2ae90ff412`, parent `654da693...`.
- The product/provider source is the reviewed `654da693...`, tree
  `d35d0a36e4bc1f0a33f278a1bd798e4e857ec557`; `6868e16a...` adds only the
  authentic historical fixture and tests.
- Runtime reviewed here is `388eff42a644aeafa5d4605d0bb235e1ca849741`, tree
  `708df14c75ef739a2c6130ca39f9e67b2758a571`.

The selected-PARAM helper uses only the existing authenticated
`history`/`history_entry`, `revision_closure`, `config_source`, and
`document_object` APIs. The current Runtime port already supplies the required
scope, ancestry, immutable retained-input, and authorization checks. No new
port method, DTO, schema, endpoint, table, caller-authority field, or inline
authority was added or requested.

This is **not** approval of the full strict-inverse claim. The known F1 gap is
still open and is Agent-owned: a same-batch `[set-element P2, inverse(T)]`
can bypass the existing strict intervening-write check because the inverse
checker receives accepted intervening records but not earlier staged records
from that batch. The independent native reproduction fails identically on the
654 base and successor, so this is inherited rather than a Runtime-port
regression. Keep the orchestrator's existing hold until the Agent staged-record
guard is repaired. Do not weaken the old positive or relabel this gap green.

## Port and source findings

- `RequestCommitPort.history` authenticates the exact `through` pair, pages
  from the request ancestry, and checks predecessor continuity. `history_entry`
  only returns same-project/timeline ledger-backed publications and verifies
  accepted recorded entries. `revision_closure` rejects revisions outside the
  request ancestry/declared sources and verifies the scoped closure.
- `config_source` reads the exact retained DocumentPin through the existing
  link/content binding and immutable digest/size checks. `document_object`
  requires the captured source, validates the selected object descriptor and
  bytes, and rechecks captured custody at acceptance. The existing Runtime
  tests also prove this after V2 admission, source removal, and restart.
- A PARAM caller pin cannot bootstrap authority. The Agent resolver first
  derives the selected target's authority from authenticated accepted history;
  the provider then compares the supplied `schema_source`, selected element,
  and exact snapshot descriptor. An explicit `clip.set-element` may establish
  a new selection only through the existing source/object validation.
- Same-batch stage selection is supported through the existing Agent command
  record staging (`ctx.prior_records`). The equal-canonical-JSON opposite
  selection order test proves P1/P2 publication order, not manifest order,
  controls the next PARAM source. Inverse and revision-restore resolution use
  authenticated publication boundaries and `restored_from`; ambiguous restore
  leaves later PARAM authority unavailable, while inverse-of-restore recovers
  the exact prior boundary.
- The helper performs no direct database/filesystem/renderer/launcher IO. Its
  reads are through the existing Runtime port; no hidden extra IO or inline
  authority cache was found.
- The repaired legacy positive is real: the final source contains the normal
  authenticated old accepted-history fixture and preserves the original alias,
  opaque-data, inverse, and exact selected-object assertions. It is not an
  equal-JSON recertification or fabricated accepted record.

## Evidence

Exact final Agent archive, against current Runtime `388eff4`:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-param-authority-port-review/agent-final-source-8a6b41c7 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-m2-param-authority-port-review /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_selected_schema_runtime.py::test_native_retained_schema_replay_inverse_reload_and_exact_retry tests/sdk/test_timeline_selected_schema_runtime.py::test_native_equal_json_opposite_selection_order_and_inverse_restore tests/sdk/test_timeline_selected_schema_runtime.py::test_pre_enforcement_alias_history_reopens_with_current_authority
# 3 passed in 9.38s
```

Closest Runtime retained-document/object neighbors:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/rt-m2-param-authority-port-review /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_pack_document_read.py::test_native_capture_commits_against_retained_v1_after_v2_removal_and_restart tests/test_timeline_pack_param_retained_read.py::test_v1_declaration_is_read_live_and_survives_v2_removal_and_restart
# 2 passed in 2.31s
```

Additional source hygiene: `git diff --check 654da693... 6868e16a...` and
Runtime `git diff --check` both passed. No full suite, matrix, browser, socket,
or live-host suite was run.

## Next step

App may consume the bounded authenticated selected-PARAM read contract after
its own WC4/browser/outbox qualification. Agent must separately repair and
prove the inherited same-batch strict-inverse guard before claiming full
selected-PARAM/inverse compatibility or activation.
