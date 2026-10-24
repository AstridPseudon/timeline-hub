## Review report — `agt-R1-native-order-review-1122`

**Verdict:** STRICT SOURCE/SECURITY PASS for the bounded native inverse-order repair only. No full-suite or all-five PASS claimed.

Commit/tree:

- Commit: `0eab665187eae593abfc91556f402f4c616e8864`
- Tree: `3512be070423bfbfd410367ad3ce2076bb6e8a13`
- `_step_undo.py` blob: `5c390de538b5a596273f1d9d3153709add20385e`
- New test blob: `27bcd60373889b0d5250095ead546199b066588c`
- Parent source blob: `1c46a7564aee8bee56be5a6b446c19a1c0177436`

The diff is limited to the 10-line native-order validator repair, one new conformance test, and evidence. Existing callers, schemas, clients, pins, baselines, guards, and protected test bodies are unchanged.

Proof:

- Focused native controls: **8 passed**
- Relevant targeted suite: **147 passed**
- Existing guard neighbors: **3 passed**
- Public source classification probe: **3 passed**
- Ruff: `current=2143 baseline=2143`
- Mypy: `current=1902 baseline=1902`
- `git diff --check`: passed
- Production caller instrumentation confirmed `inverse_address_resolver` invokes `validate_nested_history` for both inverse and source entries.

Retained limits:

- Public cached-source checks: **3 expected failures** (`pair`, `foreign`, `digest`); fresh public opens still reject tampered backing data.
- Captured redo codec check: **1 pre-existing failure** (`shot item source changed`), owned separately by `inverse.py` / captured redo work.
- No full suite, live Runtime, browser, ABA, or gate run performed.

Authenticated fixture inspection confirmed valid inverse records carry source publication, step, ordinal, native/effect ranges, and owner/pin data. The repair enforces native reference order and parent storage-path order while intentionally allowing authenticated child item-path re-encoding. Tampered commuting parent order raises `history_unavailable` without mutating history.

Commit message written and `DONE` marker created.