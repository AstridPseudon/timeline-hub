# D73 findings

Verdict: **FAIL_SOURCE_ONLY**. The private candidate is correctly marked
`CANDIDATE_NOT_INSTALLED`/`NOT_READY`, but it is not installable as written.

1. **Blocking — launcher argv is malformed.** Both candidate rows at
   `ops-d73-exact-nodes/README.md:28-29` pass `-o` as the first argument after
   `run --`. The reviewed production launcher uses `python -P "$@"` for `run`,
   so Python rejects `-o` before pytest starts. Add `-m pytest -q` before the
   required cleared-addopts/integration/no-cache/timeout options in both rows.

2. **Blocking — request evidence is not per central ID.** The rows hard-code
   `P4_D73_REQUEST_ID` and the JUnit filename. `request-test` generates a
   unique ID, but `test-run` does not export it to the suite command. Repeated
   runs would overwrite the same launcher evidence and XML. Bind the row to a
   supported per-run output/ID (or add a separately reviewed runner adapter)
   before claiming durable per-ID artifacts.

3. **Blocking — the exact Agent origins do not contain the reviewed launcher.**
   Both exact Agent commits contain launcher SHA `cec561…`, which exports
   `PYTHONNOUSERSITE=1`; the independently reviewed launcher is SHA `9f668e…`
   and unsets it in both child shells. The candidate cannot use the reviewed
   launcher from the exact-origin paths as written. Copying it or substituting
   another checkout would violate source identity; this needs a
   receipt-backed/orchestrator-approved source-manifest decision; no supported
   checkout satisfying both frozen commits and the reviewed launcher exists
   today.

4. **Blocking admission — five declared inputs remain unapplied:** selected4
   Agent checkout receipt, fork Agent checkout receipt, receipt-rendered
   four-repository manifest, both suite rows in central `suites.conf`, and
   fresh per-ID body/result receipts. The exact Runtime receipt is available;
   the Agent receipts and candidate rows are not.

Passed source-only controls: exact selected4/fork origin separation; immutable
Runtime commit/tree; reviewed launcher identity; exact four-plus-one selector
counts; accepted `--files` syntax; no whole-file/filter/fallback/retarget;
retained positive-17/one-call and poison-zero controls; and source-reported
preservation of original predicates. Those controls are not fresh functional
execution evidence.

The minimal next installation is therefore limited to receipt-backed source
checkouts, a fully rendered manifest with launcher-required keys, corrected
pytest argv, per-run evidence binding, and the two exact named rows. No path
or additional scope should be invented.
