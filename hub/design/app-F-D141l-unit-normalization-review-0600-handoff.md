# D141l handoff

Independent data/provenance result: **PASS**.

The corrected controlling bracket is `5433016320` admission bytes to `4839120896` in-body normal-run minimum bytes, giving `X=593895424` and floor `4793895424`. The pristine `23581` comparator was checked for the MAX rule; its justified timestamped delta is only `11431936` bytes. Sampling gaps are disclosed and no continuous peak is claimed.

Both normalized files are ordinary receipt-format projections and are permanently classified as `DERIVED_DATA_PROJECTION_NOT_ORIGINAL_STDOUT`. They do not claim historic stdout, create a sample, or create a consumption measurement. The existing validator accepted them only in the private fixture `d141l-unit-normalization-review-0600`; no production receipt was attached.

Composition remains unchanged at `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` / tree `5ab5191a296980a0a6bcd1178ab6902d6478a148`. The App caller binding is the exact `4de54db14bdc9ddc2ce2e5887258b03acbffd30d` / tree `84c3fb7f73f08c22220f8e808962fe3f24aaa0aa`, with registered `app/full` command `npm test -- --maxWorkers=3`.

Manager next step: retain all raw KEEP/D130/D141/owner gates and attach only a real generated job receipt after the appropriate normal gates and source binding. No worker merge request is needed for this source-only review.
