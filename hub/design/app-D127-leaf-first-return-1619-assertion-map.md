# D127 assertion custody map

Parent source has 19 existing test functions and exactly 160 `ast.Assert` nodes. Current source has 23 functions and 181 assertions: 160 mapped parent assertions plus 21 assertions in four additive adversarial tests. No old test was deleted, skipped, xfailed, optionalized, or weakened. `assertion-map.json` has one record per original assertion with source lines, sanitized predicates, exact AST hashes, and disposition.

Original candidate changes and current disposition:

1. Allowlist event-key assertion: strict extension with `lifecycle`.
2. Ring exact-retention assertion: strict extension with `buffer_complete` and truthful `raised`.
3. Byte-bound lifecycle assertion: strict `failed` → `raised`.
4. Pending lifecycle assertion: strict `pending` → `pending_at_stop`, plus strict `buffer_complete`.
5. Observer receipt assertion: the unnecessary local-variable rewrite was restored exactly; lifecycle is a separate additive assertion.
