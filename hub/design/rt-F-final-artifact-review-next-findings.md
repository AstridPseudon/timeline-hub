# F-final findings

Overall result: PASS with non-blocking observations.

- **OBS-001 (nonblocking)** Meaningful git diff --check base..result reports preserved whitespace diagnostics: Agent exit 2/153 lines (136 added-whitespace lines), Runtime exit 2/4 lines, App exit 2/56 lines; Composition exit 0/0 lines. git am itself exited 0 for all four and all resulting trees match exactly.
- **OBS-002 (informational)** The rendered README retains the template/canonical historical PENDING language and older historical receipts, while generated per-repository sections and the D141jj suffix name the actual final tuple and App fc24f849 option B. Historical receipts are not retargeted.
- **OBS-003 (bounded-custody)** The detached sampler shell was reaped by the harness after one valid sample; its initial attempt also logged a quoting error. A foreground sampler then recorded valid 5-second samples at 18:46:09Z and 18:46:14Z, exited 130 on explicit Ctrl-C, and the review guard armed a 4,000,000,000-byte process-group threshold. No threshold trip occurred; no continuous historical peak is claimed.
- **OBS-004 (informational)** The archive has no separate machine-readable manifest beyond SHA256SUMS; README, patches, bundles, extras, and SHA256SUMS are the actual contents authenticated here. No invented manifest was required.
