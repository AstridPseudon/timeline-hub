# P1 Agent feasibility corpus handoff

Status: collection complete; this is not an H3 GO and contains no `doc.patch` provider proof.

Branch: `tl/ap2-P1-agent-cases`  
Source HEAD at handoff: `a086cc6db7928dc4a3516d304dd9a472b050f1cf`  
Final commit SHA: assigned by the harness after worker exit.

The corpus is in `tests/sdk/fixtures/p1_feasibility/manifest.json` and the copied source snapshots beside it. It contains 11 cases:

- nested canonical closure trim with occurrences, media references, metadata, and an unchanged sibling;
- created track/clip IDs and ordered lists;
- absent params, null params, explicit clear, nested/dotted keys, and opaque metadata;
- a real disjoint rebase and a same-field refusal derived from the existing semantic command tests;
- SDK `tiny3` text editing and `tiny_publishable` asset clearing;
- the real sample-project timeline config for the core loader;
- the authenticated selected-PARAM SDK archive as provenance-only evidence.

Every copied snapshot has its source path, source SHA-256, source test provenance, tags, and expected semantic effect in the manifest. The cases use existing `bundle_from_document`/`document_from_bundle`, semantic command execution/rebase, SDK Checkout edits, and the core timeline loader. No provider or golden executor was added.

## Evidence

Run from `/home/user/work/wt/ap2-P1-agent-cases`:

```text
PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_p1_case_corpus.py
13 passed, 2 warnings in 5.50s

/root/.local/bin/ruff check tests/sdk/test_p1_case_corpus.py
All checks passed!

/root/.local/bin/mypy --follow-imports=silent tests/sdk/test_p1_case_corpus.py
Success: no issues found in 1 source file
```

The two pytest warnings are the shared environment's missing `timeout` and `timeout_method` config options. The required system-Python spelling `PYTHONPATH=. python -m pytest ...` was unavailable because system Python has no pytest; the exact shared venv command above is the passing equivalent. Full suites and browser/live-socket suites were not run.

## R1 prerequisites

1. Add the approved `doc.patch` command/provider and its closure address, previous-value, absent/null/clear, list/order, created-ID, and metadata rules.
2. Map each manifest edit to a real `doc.patch` request while retaining the source command and expected effect as provenance; do not replace the cases with synthetic golden outputs.
3. Run the accepted, merged, and refused cases against the actual provider/runtime path. For `disjoint-rebase`, prove the head-only value survives; for `same-field-conflict`, prove refusal leaves the head unchanged.
4. Add the App mixed-command chain around the Agent corpus separately: split → trim the new clip → intervening Agent edit → lost acknowledgement → restart, including accepted, merged, and refused replies.
5. Only after those provider/runtime tests pass should this corpus be used as H3 evidence; the current collection proves fixture integrity and existing Agent-side semantics only.
