# F/D141b progress

`PASS_SOURCE_READY_REVIEW_PENDING`; production body `NOTRUN`.

Corrected the command/row/admission/evidence packet on exact return0008 base
`a8118e9a51ccb629e88cb6dcde981b22ba448b98`. Read original0003, final0014 and
consumed independent wholepath0019's complete finite findings, including
`D141B-LIFETIME-010`. All remaining issues are returned together in findings-map.

- Custody probes all fields and all four repos despite earlier failure; trap
  handling is installed before any fallible admission or initialization.
- Checked exit/status/log/XML evidence cannot false-PASS. Actual body/monitor
  exits remain distinct; a nonzero original return is preserved.
- Disk failures stop the owned body process group before fallible failure
  logging. Wrapper signals stop/reap its own processes before final capture.
- Initialization/output failures are NOTRUN; impossible durable writes are
  reported honestly on service stderr. Output ownership is locked before
  truncation so a contender cannot overwrite an active run.
- Exact pristine sources, 17 roots, interpreter guards, environment/settings,
  two approval gates and decimal 4.6/4.7/4.0 GB thresholds are preserved.
- Seven shell-only plumbing smoke cases and static checks pass. No product
  tests, collection, imports, body, service request or suite installation ran.

The exact seven files are published under this worker's absolute evidence path,
with command/row hashes in admission.json. No REG or ship credit is claimed.
Next: independently review the corrected bytes; only after review PASS and U2
final freeze may the controller install one normal service row and dispatch.
