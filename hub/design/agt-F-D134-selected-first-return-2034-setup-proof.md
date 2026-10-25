# Setup proof

The retired HTTP setup payload is authored explicitly as:

```json
{"config":{"tracks":[]},"registry":{},"clips":[],"occurrences":[]}
```

`config.clips` is intentionally absent. The replacement uses the real registered
`commitTimeline` provider and the canonical Runtime route. It first captures the
actual bootstrap parent closure as the guarded `before` value, then applies two
sequential `doc.patch` changes: replace the root with the retired payload, and
restore the top-level empty `clips` list after mirror handling. The seeded receipt
asserts equality with the retired payload, not with the bootstrap baseline.

An isolated source probe against Runtime commit `e319fdbcd512bd5fc9bc5b2c43abfa4d749c34d9`
confirmed the two-change request is accepted and returns the exact payload above.
No product, Runtime, fixture, schema, pin, or generated file was changed.
