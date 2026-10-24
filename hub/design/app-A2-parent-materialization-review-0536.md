# A2 review report

Verdict: **FAIL for the whole candidate** against the brief’s full C0 envelope requirement.

- `timeline-data` preservation: **PASS**. Raw unknown/opaque/null/absent fields, siblings, children, and pins are retained for unchanged move metadata/duration. Authored metadata/duration changes still use normal serialization.
- Original capture reuse: **PASS**. The exact six-resource witness changes baseline **2 failed/1 passed** to candidate core outbox success; ready and delayed-identity paths produce one capture/intent/request, and invalidated original reads refuse without dispatch.
- Full envelope: **FAIL**. Candidate move requests omit `rationale` and `group_id` (`undefined`) despite the task requiring them. The wire type marks them optional, and existing code forwards them only when supplied.
- Guards/refusals: **PASS**, 273/273 targeted tests, including stale-head, wrong-source, and extra-authored-field refusals.
- Scope/census: **PASS**. Only the four assigned files differ; contract/schema/client/serialization files are unchanged.
- Runtime acceptance and historical 13583 internal ordering remain unverified.

Tests:

```text
9 targeted files: 273 passed
tsconfig.json: PASS
tsconfig.app.json: PASS
tsconfig.node.json: PASS
changed-file ESLint --max-warnings 0: PASS
git diff --check: PASS
```

No source edits were made. Worktree is clean. Commit message and `DONE` marker written.