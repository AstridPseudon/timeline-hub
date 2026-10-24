## P3 report

Implemented the concrete review fixes in the three authorized files:

- Correlated the setup response to the exact request object and exact setup command.
- Added C0 scope/base/previous-head/command/receipt/idempotency validation.
- Reused `expectV2History`, `history`, and `revisionBody` for authoritative head and canonical-position readback.
- Extended offline controls for unrelated responses, identity mismatches, invalid receipts, wrong scope/head/base/command, and readback mismatches.
- Preserved the original reset and downstream Gate5 tail unchanged.

Tests:

- Node 20 offline control: PASS, exit 0.
- TypeScript root/app/node checks: PASS, exit 0.
- Scoped ESLint: PASS, exit 0.
- Playwright `--list`: PASS, 15 tests.
- `git diff --check`: PASS, exit 0.

Preservation:

- Parent whole-file blob/SHA256: `37caf28577d42fbe98afd2320dffa3c72e6e74b1` / `0e69b561a0c750669f45e54259021179b355bde41a52e265b7ea198be7318f14`
- New whole-file blob/SHA256: `c8b8494cfd148bb00f25725239d575a32aea61d1` / `cac725a518e83b2bf4c9254dca869c136d6411bec3ac8b3c2e10339c9c58d488`
- Gate5 body: old 9837 bytes / `d3ead85a96a6fdf7dd76797bc75b24374e39ea640b632697603d16fc286c52ca`; new 12239 bytes / `a555a6d7dd0f9d8518794d81c2ce9707411613cb83615a3df6253a30d6440a12`
- Removing only the setup prefix restores the original body byte-for-byte.
- Required unchanged tail hash retained: `f7e7abd9233a332adfeea03155d78af05a5d631ffffbecd64691c7014936bb67`.

No live browser journey or full suite was run, per instruction; prior 4065 remains NO-GO. Commit message and `DONE` marker were written.