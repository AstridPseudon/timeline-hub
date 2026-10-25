## F-D86 report — BLOCKED

No source changes made; worktree remains clean.

Findings:

- First atomic-scope selector is already on the genuine current provider path.
- Authoring helper remains detached/synthetic at `test_authoring_media.py:440–473,525`.
- Faithful migration is blocked by the manifest-only `sha256:333…` retained pin; `trusted_seed` derives media only from payload content. Materializing it would alter fixture identity or fabricate Runtime state.
- ABA selector reaches the documented Runtime-owned `sequential source binding is ambiguous` seam. No product change made.

Exact target hashes:

```text
c4e95a4c...deff5a4  tests/editing_conformance/test_doc_patch_atomic_scope_runtime.py
cfd27704...b5c5c  tests/timeline/test_authoring_media.py
```

Dependency hashes were recorded for `trusted_seed`, occurrence-media fixture, document fixture, timeline emitter/commit/store/remote modules, and restructure/source-copy helpers; all unchanged.

Checks:

- In-memory compile: PASS
- Ruff: PASS
- Mypy exact command: blocked by genuine NumPy Python-version stub syntax; Python 3.12 mode: PASS
- `git diff --check`: PASS
- No pytest, collection, service, build, browser, or body execution performed.

Selectors preserved: all 5 requested selectors. Retained trace: `handoff-agt-F-rehearsal-rollup-return-2320-rehearsal-rollup.tsv`, rows 276–279.

Protected review/merge and main batch were not requested because there is no faithful candidate delta. Commit message and `BLOCKED` marker were written.