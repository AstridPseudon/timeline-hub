# F-D86 report

Implemented the one-line `document_from_bundle()` repair in `astrid/sdk/timeline/commit.py`: authenticated hydrated document pins now merge even when `_copy_manifest` already exists. Inverse removal, closure validation, ordering, and Runtime authorization remain unchanged.

Caller trace verified:

`Runtime commit_timeline → Agent provider → _hydrate()` authenticates captures → `_copy_manifest` is set → `document_from_bundle()` builds manifest → Runtime validates captured dependencies.

Original 11 selectors preserved; no new selector added. Predicate groups remain exact: six text-binding inverse/absence cases, two timing rebase/reselection cases, and three Python/CLI/sheet pin roundtrips.

Checks:

- In-memory compile: pass.
- Ruff baseline comparison: pass, `current=2143 baseline=2143`.
- Targeted Ruff: pass.
- Targeted mypy on touched production file: pass.
- `git diff --check`: pass.
- No pytest, collection, fixture, helper, service, build, or function execution run.
- Full mypy comparison is environment-blocked: shared `venv-agent` is Python 3.13 and lacks `types-PyYAML`; unrelated repository-wide diagnostics result.

Hashes:

- Candidate `commit.py` SHA-256: `eec60cd2520730e5ccfa8ebde6ad6a1fa986df62520c57d6575f5512c79b9cf7`
- Test file unchanged, SHA-256: `058d82106471efe8d586007f78784775622d962ce551e882fb65d95a62f4b60c`

Commit message written and `DONE` created. A fresh independent core/custody review and later affected-node qualification remain required before merge.