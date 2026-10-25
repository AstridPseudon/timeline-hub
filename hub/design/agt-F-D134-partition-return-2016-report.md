## Completed

- Wrote corrected evidence under the required worker path.
- Moved exactly nine projection records to `UNKNOWN`.
- Preserved all 344 IDs, source/tuple data, log hash, REG14 status, and author2003 bytes.
- Final equation: `132 setup + 0 product fault + 212 UNKNOWN = 344`.
- Added commit message and `DONE` marker.

## Validation

- `python3 -m json.tool` on all output JSON: PASS.
- Read-only Python JSON/TSV/hash/membership/diff/count audit: PASS.
  - 344 rows and unique IDs
  - 0 added/removed IDs
  - exactly 9 category changes
  - outside fields unchanged
  - REG14: 14 unverified, 12 prior unknown, missing XML/final count unknown, retirement 0

No tests, lint, typecheck, collection, or production code were run; this was evidence-only work.