# Validation

Generation checks passed in the read-only builder:

- 370 unique per-ID rows mapped from 370 retained-log sections.
- Classification totals conserve 344 + 14 + 12 = 370.
- Root-cluster member totals conserve all 370 IDs with no additions or removals.
- Retained log hash is bound to the required D134 SHA-256.
- Source input hashes and frozen Agent/Runtime tuple are recorded in
  `source-manifest.json`.
- Raw stacks, XML, private payloads, URLs, and complete runner receipts are not
  copied into the publication.

The generated JSON and TSV were validated offline after generation; no test
suite or service was run.
