# F/D69 CLI triage report

Result: **0 confirmed live regressions / 11 exact decision conflicts / 0 env / 3 XML PASS**.

Evidence:

- Authentic XML: `.../agt-F-D69-snapshot-launch-sol-1642/evidence/d69-restored47.xml`
- Service: `agent-d69-restored47-nodes-1024164419-23762`
- Full service result: **39 failed, 10 passed, 17.11s**; zero skips/errors.
- Assigned filter: `tests.packs.timeline.*`, excluding `test_cli_edit_flags`: **14 rows, 11 failed, 3 passed**.
- All restored current test bodies match upstream-924 AST bodies exactly.

| Case(s) | XML result / traceback | Classification |
|---|---|---|
| `test_cli_parity::test_publish_requires_a_message` | FAIL, assertion at `test_cli_parity.py:91`; parser error lacks `-m/--message` because `publish` is not registered | G5/D52 conflict |
| `test_cli_status_publish::test_publish_forwards_key_and_force_to_sdk_once` | FAIL, `SystemExit: 2`, invalid choice `publish` | G5/D52 conflict |
| `test_publish_partial_narration_error_preserves_receipt_and_does_not_retry[False/True]` | FAIL, invalid choice `publish` | G5/D52 conflict |
| `test_publish_human_output_is_a_short_summary_and_json_keeps_the_envelope` | FAIL, invalid choice `publish` | G5/D52 conflict |
| `test_publish_still_requires_a_revision_message` | PASS, but only because any `SystemExit(2)` satisfies the body; it does not qualify publish behavior | PASS, non-qualifying |
| `test_publish_cas_refusal_is_not_retried_or_reported_as_success[False/True]` | FAIL, invalid choice `publish` | G5/D52 conflict |
| `test_publish_of_a_clean_working_copy_publishes_nothing` | FAIL, invalid choice `publish` | G5/D52 conflict |
| `test_verbs_working_copy::...upstream_publish[argv0]` | PASS; retained `checkout` behavior | PASS |
| `...upstream_publish[argv1]` | PASS; retained `status` behavior | PASS |
| `...upstream_publish[argv2]` | FAIL, invalid choice `publish` | G5/D52 conflict |
| `test_publish_conflict_names_the_writer_and_offers_discard_first[...]` ×2 | FAIL at `test_verbs_working_copy.py:612`; `store.three_way` missing before `publish_bundle` can run | G5/D52 conflict |

Exact source binding:

- `astrid/packs/timeline/cli.py:3829-3845` registers `commit` and retained working-copy verbs, but no `publish`.
- `astrid/packs/timeline/cli.py:3955-3971` installs that command registry.
- `astrid/sdk/timeline/commit_session.py:256-260` explicitly retires `save`/`publish` in favor of `commit(label)`.
- Production census found no references to `publish_bundle`, `three_way`, `_cmd_publish`, or `_configure_publish`.
- Separate adjacent caller: `astrid/packs/timeline/cli_working.py:493-494` still calls `tl.publish` for `restructure`; this is outside the assigned 14 and should receive a separate G4/G5 migration decision.

Decision basis:

- PLAN §3 G5 deletes separate publish, `store.three_way`, and `publish_bundle`.
- BOARD-HEADER D52, lines 156–161, authorizes removal of retired routes and tests exercising only them.
- D54a permits this exception only as a deliberate deprecation; these cases bind directly to that decision.
- G5 review confirms no production references remain to the removed helpers.

No product or test changes were made; no original bodies were rerun. Static verification passed:

```text
git diff --check                         PASS
parser registry: publish_registered=False
production removed-symbol census        no references
upstream/current AST body identity      PASS for all selected functions
```

Commit message written to the requested path; `DONE` created.