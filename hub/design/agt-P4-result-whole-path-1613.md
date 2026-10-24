## P4 report

Read-only investigation complete. No product, test, schema, client, lock, registry, or service-row changes.

- Current retained run `29577`: Agent tree `781241f…`, Runtime `8b32cac…`; `2 failed, 1 passed in 64.22s`.
- Exact command used existing `venv-agent`, normal Runtime checkout, and `--timeout=45`.
- CLI failure is a stale `parsed.native` assertion; production caller is `apply → cli_native.commit_edit → NativeSheet.load(session).apply`.
- Ten-note timeout occurs during first redo in Runtime historical verification:
  `_historical_sequential → validate_sequential_capture → _capture_document_images → validate_commit_value(CanonicalDocument) → jsonschema $ref resolution`.
- Smallest causal seam: Runtime R2r commit `5328241c`, which introduced full canonical-document validation on every captured boundary. Historical passing Runtime `a5d4258…` lacked this call.
- The 45-second timeout is an existing budget, not shown to be introduced by row preparation. No timing/profile evidence identifies a finer-grained schema cause.

Historical genuine receipts retained without rerun:

- Ten-note integrated PASS `11615`, 106.28s.
- Staged ten-note PASS `20083`, 101s.
- Historical Runtime used `a5d4258…`.

Evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-P4-result-whole-path-1613/evidence/p4-readonly-causal-finding.md`

No further rerun or budget/assertion weakening is recommended. `DONE` and commit message were written; worktree remains clean.