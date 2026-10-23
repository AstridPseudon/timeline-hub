# Agent V2 D12 baseline-only review — FAIL

Reviewed repaired tree `2ad707b7ab424b707618ae3c78ee8b8d624083eb` against
`266e8eac6faeda5d6502926894395c2ccd818564`.

The repair still exempts valid unchanged `beat`/`downbeat` declarations when
shared-child ambiguity raises `ambiguous cut identity`. In
`_commit_timing_validation.py:138-154`, the fallback allowlist at line 145
omits beat/downbeat, so line 146 returns `False`; lines 171-175 then add the
declaration to exemptions, and `_timing_evaluators.py:506-509` suppresses it.

Real-provider reproduction: two distinct physical shot revisions sharing one
internal timeline, audio `beats: [0, 1, 2]`, unchanged child
`on: "beat 1 after c1"`, unrelated parent `name` patch. The service accepts;
`_legacy_exemptions` and `_legacy_inputs` show the beat declaration was omitted
from compiler validation. A single physical child validates the same
declaration normally. This is a settled D12 violation. **FAIL.**

Evidence: P1 provider 22 passed; focused neighbors 166 passed; scoped Ruff;
Ruff 2151=2151; private mypy 1915=1915; no new import cycles; diff check
passed. No product edits, full/native14/HTTP/browser/farm runs, or merge.
