# F-D86 batched source review

## 1. `tl/agt-D86-occurrence-opaque-0121` — `FAIL_SOURCE`

Author branch: `6b9e14efd7`  
Delta: exactly `tests/editing_conformance/test_commit_runtime_opaque_items.py`; create/fork files are unchanged.

The rewrite does reach the current provider through `emit_document_commands`, `load_timeline_commit_provider`, and `edit.commit`. It preserves the opaque-value matrix and existing test predicates.

However, it drops the original shared-source topology. The premigration setup re-pointed occurrences 1 and 2 to one `opaque-shot` / `opaque-internal` closure ([old setup](</home/user/work/wt/rt-D86-three-families-review-0129/tests/editing_conformance/test_commit_runtime_opaque_items.py:68>)). The replacement leaves the original distinct occurrence-1/2 source references unchanged ([new setup](</home/user/work/wt/rt-D86-three-families-review-0129/tests/editing_conformance/test_commit_runtime_opaque_items.py:64>)). This no longer tests the intended shared physical-source materialization case.

No create/fork Runtime-cause claim is made; both files are source-identical.

## 2. `tl/agt-D86-manifest-inverse-0121` — `SOURCEFACTS_PASS; FUNCTIONAL QUALIFICATION PENDING`

Author branch: `219b9ca8b1`; no source delta.

The migrated parent-media fixture uses real managed media selection, retained CAS data, current Runtime commit acceptance, and exact source/binding/manifests. `test_commit_runtime_media_manifest_inverse.py` exercises the registered provider, authorization, inverse, restart, retry, history, and integrity paths.

The detached popup file remains intentionally bounded: its `test.popup-media` and `DetachedRealm` seam explicitly does not claim Runtime selection, provider acceptance, or an installed production popup opcode. That materialization guard remains outside this allowed seam; no product closure is claimed.

## 3. `tl/agt-D86-parent-track-0121` — `SOURCEFACTS_PASS; CURRENT QUALIFICATION PENDING`

Author branch: `219b9ca8b1`; no source delta.

Static review confirms:

- grouped track creation plus dependent move uses `TimelineSession.commit_many` against the real Runtime client;
- parent-label tests cover exact caller, managed membership, labels, opaque siblings, absent/null/clear behavior, ordering, source pins, conflict, ABA, inverse, CLI, lost ACK, restart, and suffix recovery;
- transitive M1 fixture construction uses the current source fixture, provider, source mapping, and document emitter.

No function execution was performed. Mypy was not run; existing helper mypy errors are not being claimed green.

## Verification and limits

Read-only commands included `git diff`, `git show`, `git log`, `rg`, `sed`, `nl`, and static archive inspection with `tar -xOf | strings`.

Tests, pytest collection, fixtures/helpers, Runtime services, browsers, builds, and mypy were not run per the task restriction.

No repository source files were modified. Required `commit-msg` and `DONE` markers were created.