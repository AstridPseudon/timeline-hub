# F-D86 D107 current-equivalent source handoff

Status: `SOURCE COMPLETE / STATIC ONLY`.

Added exactly one new test file, `tests/editing_conformance/test_m1_current_equivalent.py`.
The original `test_commit_runtime_m1.py` is unchanged.  The new test uses the
supported `native_word_anchor_fixture.retained` fixture, whose setup ingests
genuine media and a transcript, registers the current Agent provider, and
creates the current word binding through a real `commitTimeline` request before
the journey begins.

## NEW-OURS journey

The test then uses the production SDK/Runtime route to cover the missing
combination: current word authority, a real native move, persisted outbox
flight, lost acknowledgement after durable acceptance, exact retry after a
Runtime restart, a disjoint head edit, current v2 merged/rebased landing,
inverse, redo, and history/readback assertions.  It also checks authenticated
restart identity and exact idempotent replay.  Renderer-off guards come from
the supported current fixture and are retained.

No legacy declaration, copied archive, synthetic history/SQL/CAS/pin, or
provider bypass was added.  No product, shared fixture, Runtime, schema,
client, pin, ledger, or original-M1 file was changed.

## Original selector mapping

The ten approved `original550` selectors remain legacy-only and are not
reclassified.  The companion TSV maps every selector to its preserved purpose
and to the exact NEW-OURS assertion family.  The new test closes the missing
current word-bound/outbox/restart/head-conflict/inverse combination.  The
existing current view-authority and auto-placement tests remain named partial
coverage for their respective selectors; they are not claimed as a combined
M1 replacement.  No current run was executed in this source-author turn, so no
success or by-design refusal is claimed.

## Static evidence

- `python3 -m py_compile tests/editing_conformance/test_m1_current_equivalent.py` — PASS
- `/home/user/work/venv-agent/bin/python -m ruff check tests/editing_conformance/test_m1_current_equivalent.py` — PASS
- `git diff --check` — PASS

Per D107, pytest/import/collection/helper or fixture execution, probes,
services, browsers, rendering, package installation, and full suites were not
run.  Runtime qualification and protected review remain required.
