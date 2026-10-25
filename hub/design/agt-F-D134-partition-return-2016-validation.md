# F/D134 reviewed OWN-344 derivative validation

## Scope

This artifact validates only the evidence derivative. It does not run tests,
collection, a service, a browser, a socket, or any production route. The
author2003 packet is read-only input and remains byte-for-byte unchanged.

## Required exact checks

The following read-only Python check parsed all JSON, parsed both TSVs, checked
the exact 344-member universe, computed the exact nine-row category delta,
verified all outside rows, reconciled cluster totals and the 132/0/212
equation, and checked the retained log/source/tuple values:

```text
python3 - <<'PY'
... read-only JSON/TSV/hash/membership/count assertions ...
PY
```

Result: PASS. The check reported 344 author rows, 344 reviewed rows, 344
unique nodeids in each, zero added IDs, zero removed IDs, exactly nine changed
categories, and no outside-row changes.

The exact nine are the nine `projection_fixture_missing_item` nodeids listed
in `partition.json`; the author and reviewed category counts are respectively
`141/0/203` and `132/0/212` for setup/product/unknown.

## Hash bindings

The derivative binds every author evidence hash and all three review2011 input
hashes in `partition.json` and `source-manifest.json`. The retained service log
hash is unchanged:

`65def166348d4ffde949d530bff1a7bcba820ad674ca85b8ccc3e708c781ae8e`.

The source tuple remains Agent `a4e016b6`, Runtime `5e9ad1c6`, App `d8a1cd40`,
Composition `635f4de0`; no source, pin, generated, assertion, or production
file was changed.

## Disposition

REG14 remains `UNVERIFIED_CURRENT_REG` (14), prior UNKNOWN remains 12, missing
XML/final-count remains UNKNOWN, and retirement remains 0. No product fault is
proved. No tests/typecheck/lint were run because this is an evidence-only
classification derivative, as required by the task.
