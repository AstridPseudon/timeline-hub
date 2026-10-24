## FAIL — PREPARED mechanical caller package

Reviewed target `b5fc832b78a3ce6702543d064c5bbefe61df3fc3` against PLAN §3 A2/A3/P2/P3, D21, `commit-v2.md`, author report, qualified design, and source-target-0644 report.

Findings:

- `caller-publication.py:313` does not rebind the actual mounted row source tokens. Rows contain `P2APP/P3APP=663…` and `P2TREE/P3TREE=9a…`; replacement logic only targets older `ROW_*` values. A modeled final source/tree leaves the mounted caller on the stale qualified source.
- C0 wire inventory is incomplete. Missing request fields include `dry_run`, `source`, `rationale`, `group_id`; missing response/preview fields include `records`, `dependencies`, `effects`, `history`, `undo_steps`, `preview`, `required`, `would_status`, and structured conflict/invalid fields.
- `git diff --check` fails: `caller-publication.py:392: new blank line at EOF` (exit 2).
- `final_source_input()` accepts any clean separate repository with a self-asserted `"review": "PASS"`; it does not authenticate that the target is the authorized proof-worker snapshot.

Checks:

- `python3 -m py_compile caller-publication.py` — PASS
- `python3 -m json.tool caller-custody.json >/dev/null` — PASS
- Decoded inner/outer rows with `bash -n` — PASS for both rows
- Missing final manifest refusal — PASS
- Wrong caller-artifact target refusal — PASS
- Source tuple positive and mutated source/tree/parent refusal controls — PASS
- Actual mounted-source replacement audit — FAIL
- `git diff --check` — FAIL, exit 2

No product, suite, browser, backend, HTTP, build, provision, or full-suite execution was performed. Worktree remains unmodified. No commit message was needed.