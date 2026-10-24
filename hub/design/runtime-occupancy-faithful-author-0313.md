**PREPARED PASS — static preparation only.**

Changed only `tests/test_timeline_legacy_occupancy.py`:

- Newer edit and source-preservation checks use the accepted source’s actual timeline, including `reference-source`.
- Added proof of changed publication, parent revision, shot head and internal revision.
- Restored complete `receipt.result == data` equality.
- Restored real whole/per-step inverse acceptance **after historical placement**, preserving the existing `source_ref` / `source_occurrence_id` carrier.

AST comparison against `fad2ddd1e` and `60fedb573` retains all **65 original test predicates**, including all 12 historical predicates: source existence, nonempty tracks, genuinely newer shot head, accepted status, unchanged global head, exact shot/internal closures, shot identity, nonempty authoritative step patch, inline `steps == {newer_receipt: ["newer"]}`, reference omission of `steps`, and exact history `undo_steps` mapping/null. All 31 assigned-base historical predicates remain; every other base function is unchanged.

Checks run:

- `/home/user/work/venv-runtime/bin/python /tmp/w-13774a134e/static/verify_assertions.py` — in-memory compilation and assertion/scenario map passed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-runtime/bin/python -m pytest --collect-only -q -p no:cacheprovider --basetemp=/tmp/w-13774a134e/collect-final tests/test_timeline_legacy_occupancy.py` — **16 collected**.
- `PYTHONPATH=/tmp/w-13774a134e/lint-tools /home/user/work/venv-runtime/bin/python -m ruff check --no-cache --output-format=concise tests/test_timeline_legacy_occupancy.py` — four pre-existing diagnostics, identical locations/identities to parent; no new diagnostics. Ruff used a private overlay because the shared venv lacks it.
- `pyright -p /tmp/w-13774a134e/static/pyrightconfig.json --outputjson <file>` — both originals, parent and final each analyzed **one file**, using the same real `/home/user/work/agent` path: **zero diagnostics**, including no missing imports.
- `git diff --check` — passed.

Decision: retain the original undo semantics as a subsequent action on the actual source timeline; inverse never creates the historical-sharing fixture.

No provider, HTTP, service, family-body or full-suite execution occurred. Qualification remains held pending independent Agent inverse and Runtime retirement passes. Next step: review this prepared diff, then qualify after those handoffs.

Commit message and `DONE` written. No Git writes performed.