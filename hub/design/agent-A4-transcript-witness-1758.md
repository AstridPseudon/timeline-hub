# A4 transcript-shaped `doc.patch` witness

## Source boundary and decision

- Agent base: `079580ca46af77e0292d49dc34386b25c8391f99`.
- New test blob SHA: `3784be40e08802d3aa2a864d08cf7eafc30e3bd7`.
- The witness uses the existing Agent `doc.patch` registry/provider path and the existing private `source_fixture("transcript")` exact source pin. It does not add an operation, schema, client pin, guard waiver, or product code.
- The App-shaped fixture is nested under `parent.config.bundle`, matching the existing transcript capture shape. The request source names the actual mounted App save boundary, `localSaveSession`; it does not claim the dormant `commitSession` path.
- The App source evidence was read from the existing `project-transcript-host` and `importTranscriptHandoff` tests/implementation plus the transcript association capture test. Those App files were not modified.

## Covered behavior

`tests/editing_conformance/test_a4_transcript_doc_patch_witness.py` covers:

- preservation and mutation of `transcriptReferences`, `itemsBySchemaRef`, unrelated schema data, and opaque JSON through generic `doc.patch`;
- explicit JSON null versus absent values and authenticated write effects;
- exact current and prior transcript source pins as provider-retained dependency bytes;
- C0 request metadata, declared nested reads, labels, steps, merge mode, source, rationale, group id, dry-run preview/null receipt, accepted canonical document, receipt, records, bindings, writes/effects, dependencies, undo metadata, and evaluated-head boundaries;
- structured previous-value and identity-collision refusal with atomicity;
- fields rebase versus atomic-scope refusal over an intervening edit;
- exact source-pin mismatch refusal before nested writes.

The assertions intentionally do not claim `transcript.associate`, reconciliation, word-anchor behavior, caption ownership, relational timing, or referential integrity between arbitrary opaque metadata and a source document. Those remain uncovered because the current provider does not supply that behavior.

## Verification

Commands run from the assigned worktree:

```text
PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_a4_transcript_doc_patch_witness.py
7 passed in 2.06s

git diff --check
passed

/home/user/work/venv-agent/bin/ruff check tests/editing_conformance/test_a4_transcript_doc_patch_witness.py
All checks passed!

PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m mypy tests/editing_conformance/test_a4_transcript_doc_patch_witness.py
Success: no issues found in 1 source file

rg -n -i "(api[_-]?key|secret|token|password|BEGIN .*PRIVATE KEY|credential)" tests/editing_conformance/test_a4_transcript_doc_patch_witness.py
no matches
```

No full, browser, live-socket, HTTP, daemon, or native journey suite was run; the task requested targeted coverage only.
