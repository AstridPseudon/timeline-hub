# Runtime OPS-bench-store leases flat export 1936

2026-10-23. Byte-for-byte flat publication of the sealed Sol1931 evidence
packet from Runtime commit `3264e70f1f0469302de7b4c3bc5b0a987cf9849e`.

- Exported artifact count: **28**.
- Exported bytes: **925012**.
- Exact packet manifest SHA256:
  `6fe5b56b44c452d4521f58cd258fba55dcb250e8a49f23ec027b845b231feae3`.
- Every exported file was checked for equal size and `cmp` equality against
  the committed Sol1931 source; the relative manifest references are
  unchanged.
- Final design-side `sha256sum -c
  handoff-runtime-OPS-bench-store-leases-package-sol-1931-hashmanifest.sha256`
  passed **27/27**. The manifest excludes itself, so the flat export contains
  28 files including that manifest.

The existing independent custody review 1935 reports **PACKAGE PASS** for the
Sol1931 packet and confirms the same manifest hash and 27/27 verification. Its
review document is present in the 1935 review worktree but is uncommitted and
has not been copied into this export; therefore its status is recorded as
review complete, publication of that review document pending. No review or
behavioral tests were rerun here.

The packet remains evidence only: combined store status is
**FAIL/UNQUALIFIED/NOINSTALL**, and permission1905 remains **STOPPED**.
This export makes no installation, readonly-publication, product-source,
test, generated-file, pin, or integration change.
