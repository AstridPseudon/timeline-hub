# Handoff: ap2-OPS-v1-suite-retire-1753

**PASS.** Retired exactly three obsolete v1 App suite registrations from `tests/suites.conf`: `ap2-m2-parent-viewport-exact-one-central-1126-e2e`, `bootstrap-frozen-pair-integration`, and `bootstrap-fixed-pair-native-integration`.

- Deleted rows: 3; remaining target occurrences: 0.
- App rows/unique keys: 90/90; duplicate app keys: none.
- Protected P2/P3/P1 row hashes unchanged:
  - P2: `396bc74bbe1e8a22c7e7f123d61b67ec716371c2fedc3d96b7595c354d93fba9`
  - P3: `e45ebb7998acc9ac6e77ad02d8dc4e1468436b0294ec4552f8db02567bd22833`
  - P1: `fd4299058660e51d3be0129b38d49a48ba78dbfd4ae34a47e464f81f158ba99c`
- No active queued/running test or worker reference matched the retired names/paths.
- No product files or tests changed; app tests intentionally not run per task limits.

Full evidence is in `workers/ap2-OPS-v1-suite-retire-1753/report.md`.
