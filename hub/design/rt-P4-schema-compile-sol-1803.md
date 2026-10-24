**Measured limit: no production optimization qualified.** The single scratch trial reduced native `evolve` calls, but showed no stable whole-history improvement. I stopped it; all 519 previously tracked files remain unchanged.

| Control | Schema + finite checks | Median paired trial/baseline CPU |
|---|---:|---:|
| Genuine capture | 56 + 56 | 0.943 |
| Historical control | 58 + 58 | 1.005 |

Native keyword counts matched exactly. Raw profiles showed cache overhead offsetting preparation savings.

Added [four focused controls](/home/user/work/wt/rt-P4-schema-compile-sol-1803/tests/test_timeline_schema_preparation.py) covering dialect selection, nested error context, relative JSON pointers, and concurrent fresh-value mutations.

Validation:

- Focused controls: **64 passed**.
- Selected history/ABI controls: **41 passed**, 48 deselected.
- Ruff 0.16.8, compilation, whitespace: **passed**.
- Pyright: **zero new diagnostics**; one unchanged existing error.

[Exact commands and results](/tmp/w-6b00e3cca0/commands.txt), [raw profile data](/tmp/w-6b00e3cca0/schema-profiles.json), [JUnit XML](/tmp/w-6b00e3cca0/targeted-complete.xml), and [source hashes](/tmp/w-6b00e3cca0/source-hashes.json) are in the required harness-cleaned TMPDIR. **The orchestrator must archive them before cleanup for durable retention.**

D47 remains held. The original P4 first-redo 45-second gate remains **OPEN**; no original or full suite was repeated. Independent review remains pending before normal merge. Commit message and `DONE` are written.