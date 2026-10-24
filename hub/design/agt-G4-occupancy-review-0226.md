## G4 occupancy source review

**Verdict: FAIL — source proposal only.**

Runtime authority is sufficient: `source_revision_closure` authenticates same-project foreign timelines, exact publication/revision/digest, and revalidates the immutable closure without consulting the newer mutable shot head.

Boundary defects:

- The proposal does not specify how foreign shot/internal images are installed into the destination Agent closure. Existing `document_from_bundle` only accepts destination-scope source bundles and same-timeline historical sources.
- It omits required source-document capture (`config_source`/`transcript_source`). Runtime rejects candidates whose document pins are not captured and recorded.
- Calling `shot_closure` is not a faithful source authority: it searches unrelated parent publications and may reject an otherwise valid exact source closure as ambiguous. The authenticated `source_revision_closure` should remain authoritative.
- Undo/redo retention is underspecified. Existing `shared.source` inverse handling assumes a same-timeline occurrence; a foreign source occurrence is not in the destination state. The accepted record must retain structured `source_ref` plus source occurrence identity and re-resolve that authority on redo.
- The original inline/reference fixture must remain distinct. The existing same-timeline carrier can cover the historical reuse leg; the new foreign branch covers only the cross-timeline leg and must not be claimed as coverage for both.

No public contract, schema, Runtime executor, or new authority is required.

Checks:

- AST parsing of current Agent/Runtime sources and frozen R4 writer sources: passed.
- `git diff --check`: passed.
- Worktree unchanged.
- Pytest, vendor checkers, HTTP/browser, and full suites: not run per brief.

Recommended next step: revise the carrier design with the exact merged-closure, document-capture, and foreign undo/redo record shapes before implementation.