# App trim fixture proportion check

Decision: **keep the exact 2,275-line fixture unchanged**.

The fixture is not unused top-level generated data under the current
compatibility test. `clipTrimCapture.test.ts` passes the complete `input`
document to `authoringBundleFromDocument`; that helper reads and validates the
parent revision, shot revisions, internal timeline revisions, and dependency
manifest, and retains the complete runtime document in `source_mapping`.
The test also consumes `commands[0]`, compares the complete `records[0]`, and
uses the expected output parent/config clip data for exact replay and the
boundary cases. The full input, record, and bundle therefore remain required
by the settled task boundary.

The only current fixture consumers are the 257-line parity test and the
17-case boundary fixture. No assertion case, numeric input, helper, or
production path was changed. Fixture hashes remain:

- `recipe_m2_clip_trim.json`: `4d71a9d184db1b85c220de10842b2dc68e5eb9b48afee180b6c29cf0d5b06152`
- `recipe_m2_clip_trim_boundaries.json`: `5cf496137b9387ef05e8f3b9a5fc7762c529f30670db2c0114d689cba4959d97`

No tests were rerun because the fixture and source are unchanged, per the
task instruction. The disclosed Agent raw-integer discrepancy remains open;
no App resolution is claimed. UI/session/writer activation remains out of
scope.
