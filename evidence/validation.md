# F/D134 independent final review validation

Scope was read-only evidence validation. No product tests, collection,
service request, rerun, browser, socket, acquisition, or source mutation was
performed.

Commands and results:

- `python3 -m json.tool` on every JSON artifact in the author2003,
  independent2011, and firstreturn2016 permanent evidence directories: PASS.
- `sha256sum` over all permanent evidence files and their matching
  `design/agt-F-D134-*` flatdesign copies: PASS; all compared hashes match.
- `diff -u` on author2003 `per-id.tsv` versus firstreturn2016 `per-id.tsv`:
  PASS; exactly nine rows differ and each difference is only the category
  value.
- Read-only Python assertion validator covering JSON parsing, TSV headers and
  row counts, 344 unique-member conservation, exact nine-row mapping,
  non-category field preservation, cluster/category conservation, source/log/
  tuple equality, author/reviewer hash bindings, flatdesign byte custody,
  retained log hash, raw-log membership, and REG bounds: PASS (62 checks).

Observed totals:

```text
author:  141 setup/expectation proved + 0 product fault proved + 203 UNKNOWN = 344
reviewed: 132 setup/expectation proved + 0 product fault proved + 212 UNKNOWN = 344
delta: 9 projection_fixture_missing_item rows, category only
membership: 0 added, 0 removed, 344 unique IDs on each side
REG14: UNVERIFIED_CURRENT_REG=14, prior UNKNOWN=12, missing XML=UNKNOWN,
       final count=UNKNOWN, retirement=0
```

The retained log is bound to
`65def166348d4ffde949d530bff1a7bcba820ad674ca85b8ccc3e708c781ae8e` and the
same service/tuple/source fields as original2003. The result is a
classification review only, never migration or product-fault evidence.
