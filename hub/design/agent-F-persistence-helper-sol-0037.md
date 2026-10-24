Blocked; no source or test changes retained. Wrote `BLOCKED` and the conventional commit message.

Found two distinct problems:

- Saved intent survives restart: `nudge(0.5)`, exact base pair, 137 reads, and commands remain in the verified journal. Legacy intent normalization changes the “before” digest, so `_saved_helper_calls` rejects the chain and publish falls back to atomic.
- A reverted capture experiment repaired that mismatch. Same-clip edits still refused with `value_conflict`, but the original disjoint positive then failed with `invalid_document`: `missing exact word binding for ('occ-A', 'A', 'a-rocket').on`.

The original manifest has `documents: []`. The operation changes `"viral"` to `"viral" +0.5s` without an authenticated transcript/word binding; current validation also requires parent ownership for authored word anchors. Stopped implementation rather than inventing that authority.

Captured complete requests, history, journal reads, exact pairs, import origins, structured replies, and database equality across refusals:

- [Original evidence](/tmp/w-47f497f5ab/original-evidence.log)
- [Reverted experiment evidence](/tmp/w-47f497f5ab/experiment-evidence.log)

All pytest runs used the supplied qualified environment and `--timeout=45`:

```text
python -m pytest -q -oaddopts= -p no:cacheprovider --timeout=45 \
  tests/sdk/test_timeline_persistence.py \
  tests/sdk/test_timeline_helper_capture.py \
  tests/sdk/test_timeline_journal.py
```

Result: **38 passed, 17 failed** on restored production source, using the exact donor persistence fixture temporarily. Persistence was **9 passed, 1 failed**; same-clip refusal passed. Helper capture had 16 failures; journal had none. The donor fixture was restored afterward.

Exploratory regression attempts never reached green and were removed. Separate original/experimental request-and-no-write diagnostics each passed **2 tests**; those establish refusals, not successful merging.

Checks:

- Private Mypy: **1,911 errors**, matching reported parent count.
- Ruff: **2,148 diagnostics**, matching reported parent count.
- Runtime lock, artifact manifest, `git diff --check`: passed.
- Final worktree clean. No full suite run.

Next decision required from the orchestrator: identify the authenticated binding contract for modifying this legacy internal-shot word moment. A persistence-only repair cannot qualify the original positive without it.