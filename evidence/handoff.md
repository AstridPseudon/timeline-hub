# U4a D141 handoff

`runtime.lock.json` now points to the qualified normal Runtime producer
`95d98f038320d5d46bd679ac000ab3e15825c935` (tree
`78df31d62c5b9ba4c84dee4ea346e43a767718c1`). Runtime
`/home/user/work/runtime` was clean before and after the normal refresh route.

The adoption is provenance-only: the old `6a011d58…` source pointer is the only
lock value replaced. All 15 mapped Agent client/schema/config/generated/fixture
payloads remain exactly equal to the pre-adoption `8585ed9c…` bytes, the final
Runtime producer, and the independent Runtime 0513 producer-corrected map.

Evidence:

- `receiving.json` — source tuple, route exits, conservation verdict.
- `source-manifest.json` — all 15 consumer/source/hash mappings and equality checks.
- `validation.md` — exact targeted commands and limitations.

Manager owns independent receiving review and the normal Agent home merge route.
No commit, fetch, merge, release, TypeScript check, full suite, or product proof
was performed here. The existing production path remains the generated Runtime
client through `commitTimeline`; no DTO or caller change was made.
