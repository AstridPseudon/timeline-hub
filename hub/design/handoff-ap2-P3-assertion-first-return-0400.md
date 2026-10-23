# P3 assertion-first return

## Source correction

App source `tl/ap2-P3-assertion-first-return-0400` is based on `7116a8e2` and changes only `tests/e2e/local/three-products.spec.ts`.

The Gate-5 helper now proves, from actual request/history/recorder data:

- exact optional request-level `reads` projection, including omission semantics;
- exact optional step-level declared reads;
- effective atomic fallback for omitted request reads on `doc.patch` requests, without injecting `reads: []` or rewriting the request;
- exact accepted/history/recorder step equality and command-ordinal linkage;
- complete authoritative step patches/dependencies against each command's real captured reads, writes, and derived writes, while allowing an empty submitted semantic patch;
- exact `document_digest` recomputation from the complete canonical closure using the existing canonical JSON/SHA-256 utility.

All original Gate-5 behavior assertions remain, including A/C/B ordering, lost ACK, restart, exact retry, mounted Undo, immutable closure/component preservation, opaque-data preservation, history counts, and zero legacy traffic. The existing dependent success spelling remains `merged`, while the helper still accepts historical `rebased` only where its compatibility contract applies.

## Static evidence

- Exact title collection with `--list`: **PASS**, 1 test.
- `npm exec tsc -- --noEmit`: **PASS**.
- `npx eslint tests/e2e/local/three-products.spec.ts --max-warnings 0`: **PASS**.
- `git diff --check`: **PASS**.

## Source versus actual scope

This return qualifies the strength of the source assertions only. It does not qualify the production journey. Browser/service/body execution was intentionally not run by this worker; the environment-repair worker owns the first same-case successor after the earlier hosted setup failure. That earlier run failed before browser launch because `@banodoco/timeline-composition/effects.generated` was unavailable, so no Gate-5 runtime assertion result is inferred here.

This helper covers the applicable accepted/merged/history/undo subset exercised by the Gate-5 journey. It does not claim coverage for conflict, invalid, preview, or unrelated historical reply families.

