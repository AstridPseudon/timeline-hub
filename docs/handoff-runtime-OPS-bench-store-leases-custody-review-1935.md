# OPS-bench-store leases custody review 1935 — PACKAGE PASS

2026-10-23. Independent Luna package-only review of Sol1931 at Runtime2a9. The
package is custody-complete and source-byte exact. This is not a behavioral
qualification: the retained independent1923 result is **24/24 PASS in 8.631s**
and was not rerun. Combined store remains **FAIL/UNQUALIFIED/NOINSTALL** and
permission1905 remains **STOPPED**.

## Scope and result

- Reviewed the stable Sol1931 packet in `docs/` without changing product source,
  tests, generated files, pins, branches, or merges.
- Ran the packet's portable validator with `--originals --runtime`; exit 0.
- The validator independently confirmed custody SHA/cmp for 23 artifacts,
  shell syntax, five Python compiles, embedded seam byte equality, both patch
  replays/cmp, lossless independent1923 log retention, Runtime2a9 cleanliness,
  the preserved prior 15/16 mismatch, and fresh manifest 27/27.
- `sha256sum -c` over the new manifest passed 27/27. Packet payload is 960K;
  private scratch stayed below 5MiB.

The final stable 1931 report is self-contained for this review: it is hashed in
the new manifest after its final write, and this review does not depend on a
mutable worker `report.md`. The old mutable-report mismatch is disclosed and
preserved rather than rewritten: expected `a90a816b...d209286`, actual
`d66d2072...0192d143`.

## Exact hashes

- New packet manifest: `6fe5b56b44c452d4521f58cd258fba55dcb250e8a49f23ec027b845b231feae3`.
- Stable 1931 report: `fddeb3d1f10837f8612c0f8e0da5670bbb74b86e1fa6e5b6ad2341c4ce31304a`.
- Core `bench_store.py`: `88ae9e5af3425639b7eba0b79aa6b84e78a319fe810c0c6a2d3ceece1be8b5f3`.
- Caller-only patch: `321abc86fbac8c8fe4aa533ecaf439ebc8b6db0cd7c3bc23cb123435f88cc949`.
- Embedded seam: `c20bcba62165c3498899e731c3dfcaaff8316bffbeb48008cbe0307beb9a2bc9`.
- Lease fixture: `0081fff4a924346674686399570234fae4c64a054575709fee7e18fcbb3c3577`.
- Final executable test-run: `f599c5ad7bf3cd61aeb01791d903ce6edfa87d5d04a39b3ebb630b3517b17ff4`.
- Original test-run: `2d1240303c0c82bf908377eeff3323a899d8929454ac2c316b05bf076fc35d35`.
- Final test-run patch: `e6bd990d4d3a49cc64709aabe94a73beb958bd9e1bf591e69212ad5a7762e044`.
- Retained compressed independent1923 log: `21451bf43b3d125237a3d58727af04856ab20fb87517447e5eaa1d16a39864b1`.
- Its decompressed original: `8270363f759051e4b1fd2ead11b1d628ea40e3cd061c480cf876665f0d99d669`, exactly 2,617,735 bytes.

The independent1923 source path and result remain bound to the exact retained
log; no new behavioral claim is made. The old manifest, old reports, old
validator, source logs, predecessor fixture, caller, seam, core, fixture and
patch copies all passed exact custody comparisons against their recorded
1918/1923 originals.

## Commands and limits

```text
TMPDIR=$TMPDIR python3 -I docs/handoff-runtime-OPS-bench-store-leases-package-sol-1931-validate.py --originals --runtime /home/user/work/runtime
(cd docs && sha256sum -c handoff-runtime-OPS-bench-store-leases-package-sol-1931-hashmanifest.sha256)
git -C /home/user/work/runtime status --porcelain
git -C /home/user/work/runtime diff --check
```

All returned success; Runtime2a9 was clean at
`2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`. No 24-lease, 15-projection, or
18-core behavioral suite was rerun. Product typecheck/lint are not applicable
to this documentation-only custody review. No combined child, Store.ensure,
readonly publication/deletion, HOST, test service, chmod, denied-path retry,
alternative cleanup/publication, live kit/config/queue/bench, install,
provision, network, or product/test/generated/pin mutation was attempted.

Recommended next step: orchestrator disposition of this package evidence;
combined qualification and installation remain separately blocked by the
settled permission and core-red findings.
