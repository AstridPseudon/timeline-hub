# OPS D141s independent paired source/control review

## Verdict

Source/control: **PASS** for the exact composition candidate and its isolated
73-purpose control scope. External release: **NOT_READY**. Freeze-2 App
binding: **NEEDS**.

## Findings and dispositions

### D141H-SEC-001 — PASS

The current paired run passed the seven custody attacks: symlink, FIFO,
regular-file replacement and physical-parent substitution before final append,
plus symlink/FIFO/regular replacement before validation. All refusals were
bounded with no redirected writes. The mounted stop-test and frozen-sampler
cases also passed. The immutable Runtime donor `56f2d56e…` / independent 0418
PASS49 remains donor evidence only; the paired receiver now independently
reproduces the required meaning.

### D141G-A-CANCEL-001 — PASS

The mounted `request-stop-test` caller was exercised in the isolated received
bin. It marks cancellation, selects session children with `ps -g`, excludes
the runner, and preserves cancelled/130 while finalizing the trace.

### D141G-A-CANCEL-002 — PASS

The new control records the actual timeout child PIDs before cancellation and
verifies each exited child is reaped. The frozen sampler is SIGSTOPed and
fails closed at exit 125 within the bounded cleanup path; no old unset-status
diagnostic appears.

### D141G-SEC-002 — PASS

There is no production `D141g-paired-control` authority. The synthetic
matching-hash pair and arbitrary suite/command/source/twin/replay variants
refuse before launch and before artifacts. The only paired positive branch is
the exact historical `D141g-next-app-journey` route.

### D141L-APP-001 — superseded; current applicability finding below

The earlier finding correctly rejected the historical prospective 520d
binding as freeze-2 release evidence. Freeze 2 has since published the real
App source identity, so the finding is carried forward as the exact current
source issue rather than silently treated as resolved.

### D141S-APP-001 — OPEN / blocking applicability

`ops-d141-measured-floor/bin/d141-validate-receipt.py:275-304` and the
corresponding `test-run` route still hardcode the historical 520d first
placement source (`520d7e4fc12a03392afaed3f486aba34a2b5c319`, tree
`70ad390c56b0e45d9279b4179598b6cdbad9ed65`) and old command/suite hashes
(`600fca0f…` / `82f4ad3c…`). The approved freeze-2 App source is
`5344c53e3063001bb3255bd0c9cd32cc5e77967f`, tree
`dd989783046aeff652486a1ba39db42aea86e201`, pinned to Agent
`8585ed9c0404d0187b2ce70242d25114a32747c2`, tree
`92a3ffdb5a8bf476e10bfa1bbda3e2856fb9938c`.

No actual production-builder binding, atomic D66 registration, or current
normal/preflight command bytes published from that App source was present in
the reviewed evidence. Historical 520d cannot qualify the new head. This is
named now as a source finding; no hashes were invented, preregistered, blindly
refreshed, or deferred to CAS.

## Preserved contract and scope

Read-only C0 review of `runtime/contract/commit-v2.md` confirms the request
surface remains `api_version`, project/timeline, exact base revision/publication
pair, ordered commands, label, steps with per-step patches, declared reads,
`fields|atomic`, idempotency, `dry_run`, source, rationale and group fields.
Replies retain accepted/merged canonical closure receipts with bindings,
effects, dependencies, history and guarded undo, conflict reason/head,
structured invalid code/path/hint/suggested command, and preview/no-mutation.
No DTO edit was made.
