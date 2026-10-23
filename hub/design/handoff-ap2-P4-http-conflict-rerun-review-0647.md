# Handoff — P4 HTTP conflict/rerun review 0647

Verdict: **PASS for independent source/assertion review; behavior remains
unverified.** This is not an execution qualification.

## Exact identity and scope

- Base commit: `ba4891a2810788fc0a93ac944f654eb422bea220`
- Candidate commit: `60cd295faeedec40fc73ea28050acbe2e01169c6`
- Base tree: `3a307371dd0b8cc78682c871d3000d9f0a5b8d07`
- Candidate tree: `fb27284c026eee642628795b3b3433f8a3b3718e`
- Candidate test blob: `cbd332db227ecb9c6254e8ced0af72c3de91821e`
- Candidate parent is the named base. The candidate diff is exactly one added
  path: `tests/editing_conformance/test_p4_note_rerun_v2_runtime.py` (296
  lines, 12,610 bytes).
- No product, tracked report, fixture, generated, schema, dependency, lock, or
  pin path differs; the reviewed worktree was clean.

## Independent findings

PASS. The new test carries the reviewed note-04 conflict and bounded callback
rerun through the public `timeline.open` / `Timeline.commit(fn)` facade and
the existing real Runtime daemon/generated-client/provider boundary. The real
peer public commit is scheduled from the first callback evaluation against the
original base pair. Assertions cover the recorded 200/409/200 calls, 409
conflict details and no receipt, a fresh retry key, fresh callback head/source,
absent-to-present guards, and the accepted suffix over the peer value.

PASS. Omitted request reads are asserted as omitted; the SDK conservative
timeline-scope step read and effective `atomic` merge are asserted. The
accepted path checks canonical/document and parent digests, head and receipt
identity, commands, authoritative steps/patch, publisher/provider/compiler
metadata, recorder writes/reads/selections/bindings/created/dependencies/
derived_writes, history label/publisher/merge mode/steps/records, the
unchanged nine-note and full physical shared closure, authored null/opaque
fields, and restart readback with an empty outbox.

PASS. The authentic shared seed and nine-note case data are imported from the
unchanged neighboring P4 test/helper/fixture paths. No monkeypatch, mock/fake
reply, alternate provider/executor, or product edit was introduced. Existing
accepted/merged/invalid and original SDK callback-rerun tests remain
unchanged.

No concrete production-reply mismatch was found by source inspection. The
production caller uses this path. The full-v2 request/reply invariants from the
original review brief remain in scope: request `api_version`, scope, base pair,
commands, label, steps with patch, reads, merge, dry-run, and idempotency key;
and accepted/merged canonical document, digest, head, receipt, effects,
bindings, steps, dependencies, history, conflict, and invalid reply details.

The frozen R4 candidate SDK branch had no corresponding P4 v2 file. Review was
against the named base, current production request/reply code, C0 sections
1–5 and 7, and prior P4 handoffs without checking out any branch.

## Evidence

1. `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-34eac004" ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-34eac004 /home/user/work/venv-app2-native/bin/python -m pytest --collect-only -q -m integration tests/editing_conformance/test_p4_note_rerun_v2_runtime.py`
   — PASS, exactly 1 test collected; only the existing unknown pytest
   `timeout` configuration warning.
2. `PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/ap2-p4-http-conflict-rerun-review-0647 /root/.local/bin/ruff check --no-cache --config pyproject.toml tests/editing_conformance/test_p4_note_rerun_v2_runtime.py`
   — PASS.
3. Private-cache mypy over the new test and its four imported timeline modules
   (`commit.py`, `commit_session.py`, `emitter.py`, `sync.py`) — PASS, no
   issues in 5 source files; only existing annotation-unchecked notes.
4. `git diff --check ba4891a2810788fc0a93ac944f654eb422bea220` — PASS.

## Limits and required next step

Per the review brief, no test body, HTTP/body/socket/service, browser, full
suite, or central test-service run was made. Therefore real Runtime 409
recording, durable no-write behavior, provider effects/bindings, history
persistence, and restart behavior remain unverified. Do not merge this test
for behavioral credit before one clean body run on the current integration
port, after the reviewed Runtime correction.

The known Runtime pin
`34eac0041b0891e9011966b39bcbd26053fde5bc` restart/admission correction
remains owned by Runtime worker 0641: omitted occurrence `gain` versus stored
unit gain. The central body is manager-owned after that correction is reviewed
on a clean current integration checkout.

The existing unknown-outcome-not-rerun control remains in the existing G2
scope; this review claims no new credit for it. The note-04 real-peer,
nine-other-notes, full-closure, and current-Runtime-gain limits above are the
complete scope of this handoff.
