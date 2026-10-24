Implemented [u2-freeze-136-snapshot-0747.row](/home/user/work/wt/agt-U2-service-row-return-0747/worker/evidence/u2-freeze-136-snapshot-0747.row).

- Accepts only committed `5783…` or a direct-parent snapshot of `5783…`; retains tree, ancestry, source hashes, Runtime, origin, cleanliness, and DTO/selector guards.
- Replaced indentation-sensitive grep with whitespace-stable regex.
- Row SHA-256: `a704b8fbe0881057be29add3db7757a28604a3819c1a09c072f6a656836af61c`

Validation:

- Raw and awk-normalized `bash -n`: PASS.
- Sourcejoined guards and fixture indentation: PASS.
- Collection-only: `136 tests collected`.
- In-memory committed/snapshot predicate simulation: PASS.
- Existing 135-test evidence reused unchanged.
- No product, test, harness, registry, or retry-service changes.

The retained service run failed in 1s before tests because awk normalized the original four-space grep literal and the synthetic snapshot made literal `HEAD == 5783` false. Central service rerun remains for manager review/registration. Commit message and `DONE` marker are ready.