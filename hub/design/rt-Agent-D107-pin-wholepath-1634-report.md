# D107 report

- Read-only source map completed for Agent `b4b3805d` and Runtime `5e9ad1c6`.
- Whole path remains failing in both retained cases at `test_m1_current_equivalent.py:317` with: `exact transcript pin is missing or revoked or ambiguous`.
- Protected purpose: PASS. Source owner: UNKNOWN. Persisted/private record: `EXACTMISSING`.
- Mapped path: current seed/provider → Agent hydration → canonical dependency manifest → Runtime persistence → daemon restart/closure hydration → `pinned_documents` → word-anchor compiler.
- No blame was assigned from the compiler guard. The smallest next inspection is the accepted head’s `commit_manifest_json`, immutable input content/binding/link rows, and restarted provider’s private capture.

Validation:

- `python3 -m json.tool` on `wholepath.json` and `source-map.json`: PASS.
- `git diff --check`: PASS.
- Worktree: clean; no product, test, fixture, Runtime, schema, or generated-file changes.
- No D107 rerun, full suite, body/family/profile/native suite, or provider/collector rerun performed per scope.

Evidence written:

- `evidence/wholepath.json`
- `evidence/source-map.json`
- `evidence/validation.md`

Commit message and `DONE` marker were created.