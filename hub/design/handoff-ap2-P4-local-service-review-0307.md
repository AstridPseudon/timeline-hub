# P4 local-service route review handoff

## PASS — source readiness only

Independent operational review of the existing `agent p4-v2-http-nodes` row and the `ddff86c18b8f8eef2092715d7804f8b50f2ef39f4` Agent source passed. The official Runtime 780 checkout is clean at commit `780da6d605033ca71dbe2ad48c10ec2870ea4865`, tree `a2850bcaf0b37bd04613b02f071457b66f0987e3`; the existing `/home/user/work/venv-app2-native/bin/python` is executable and Python 3.12.3. The actual row plus only the original node collected exactly one positive test and exited 0. The existing `*-nodes` request route refused a missing `--files` with exit 2. No body, HTTP/socket, localhost, browser, or full suite ran.

The config was recorded before and after this review. Full-file SHA-256 was `3a70311e8ab18cdfed3acde55b3a82885992491d978986c45a6417740d44779b` at both points, and `cmp` passed for the full file and the agent-row extracts. This is an author-before/after record for this review interval; it does not falsely claim preservation before the route worker's prior one-line addition. Evidence is under the worker's private `tmpdir` path recorded in its report.

## Exact later request

Once the compatible future owner source exists, replace `OWNER_JOIN_WORKER` with that worker's actual name. Do not recycle an old source-review worker or author path:

```bash
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test OWNER_JOIN_WORKER p4-v2-http-nodes --files 'tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py::test_cli_sheet_v2_runtime_preserves_document_and_reads_back') && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

The named row supplies `ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-780da6d6`, `PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-780da6d6`, the existing app2-native interpreter, and `-m integration`; `request-test` appends exactly the one node above. `test-run` snapshots the requested worktree, runs from the detached snapshot, and sets `PYTHONPATH=$SNAP`, so `$PWD` in the row resolves to the actual snapshot. No alternate launcher or wrapper is needed.

## Future v2 body scope

The production caller remains the real CLI/sheet/session/outbox/generated-HTTP/Runtime/show/history path used by the test. The future owner run must qualify the complete v2 wire rather than only collection:

- Request scope: API version, `project_id`, `timeline_id`, `base_revision_id`, `base_publication_id`; `commands`; `label`; `steps` including each step's `patch` and declared `reads`; request `merge`; request `reads`; `dry_run`; and the transport idempotency key.
- Accepted/merged data: status, canonical document, document digest, base and previous head/revision/publication identity, accepted head/revision identity, receipt, authoritative commands, steps, per-step patches/reads/dependencies, and effective `merge_mode`. Preserve the Runtime contract's `rebased_onto` head where returned, rather than reducing a merged result to a boolean.
- Conflict/refusal: preserve the conflict head (`details.current` / current head), base head, reason, and conflict entries; do not turn a conflict into acceptance.
- Invalid: preserve the invalid code, path, hint, and suggested command from the structured failure details.
- Preview: preserve `status: preview`, `would_status`, evaluated head, canonical document, digest, authoritative steps/dependencies, and merge mode, with no mutation receipt.

The test's existing single accepted case is only the CLI/sheet readback slice. Conflict, merged behavior, invalid diagnostics, preview, ten-note per-step undo, conflict re-run, restart/lost-ack recovery, and other P4 wire qualifications remain open until the compatible owner body run. This handoff makes no P4 acceptance or H3 go claim.

Retained source evidence: the independent 0242 review's Ruff/mypy and source-path checks remain valid and were not rerun because this review changed no source or config. `git diff --check` and clean product-worktree checks passed here.

