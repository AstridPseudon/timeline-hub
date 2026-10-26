# D141ee schema8 bounded review

Decision applied: `(a) same test body OR assertions exist under ours under a new ID, and it passes; (b) owner-approved retirement; (c) otherwise dropped by our patches and REG`. The earlier AND-based relay is not used. No owner retirement is assumed.

- Six rendering IDs are `(a) RENAME_OR_MOVE`. The pristine assertions are exactly `assert not status.available` and `assert missing_file in (status.reason or '')`; the current function retains both exact assertion expressions and the six current parameterized XML cases pass. The body/setup changed to the canonical `_local_schema.READER_INPUTS` closure. This qualifies only as assertion-preserving migration under the OR rule: it does not claim `__init__.py`, `generated.py`, `materialize.py`, `theme.py`, `timeline.schema.json`, or `validate.py` are individually equivalent to any one new basename.
- The two installer IDs are `(c) DROPPED_BY_OUR_PATCHES_REG`. No current installer candidate has the original body or assertion set. Current PASS candidates use local canonical-schema / Composition-archive checks and are not exact identity. No generic migration commit is treated as owner approval.

The six moved current XML IDs are recorded in `map.json`; the two exact restoration entries are in `restoration-manifest.json`. Pair accounting remains unchanged: 397 cut bad outcomes, 19 FAILS_BOTH, 5 source-backed N/A, and 64 unrelated pristine-only rows. This review does not issue REG0 or ship.
