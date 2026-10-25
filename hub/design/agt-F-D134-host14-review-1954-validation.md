# Validation

- Read-only Git object checks confirmed identical relevant blobs between Agent
  `a4e016b6a9f91fbe372672bdcf382c630bf59186` and `96df3f5b4862b1c267e3816237bae8a64b5dc31f`.
- Read the permanent 1948 report, wholepath, per-ID, source-manifest, findings,
  and validation files from the orchestrator design directory.
- Read-only source inspection confirmed the actual caller lines, Remotion
  guard, and launcher environment exports.
- Private retained-log parsing confirmed all 14 REG14 IDs are present and
  `FAILED`, with the common exception/path/line signature and 14+14 phase
  diagnostics.
- Read-only TSV parsing confirmed 370 unique IDs, no duplicates, status counts
  190 failed and 180 errors, and the exact 344+14+12 partition.
- Retained bounded XML parses as 14 tests / 0 failures / 0 errors; retained
  pristine XML parses as 14 tests / 0 failures / 0 errors.
- Current XML is EXACTMISSING; no XML reconstruction or fabricated custody was
  used.
- No tests, collection, provider, package/profile acquisition, sockets,
  browser, render, pristine rerun, production write, or hub write was run.

Validation commands run after editing:

```text
python3 -m json.tool evidence/review.json
python3 -m json.tool evidence/classification-bounds.json
python3 -m json.tool evidence/source-manifest.json
git diff --check
```

All listed commands passed. No product test command is applicable or allowed
for this read-only review.
