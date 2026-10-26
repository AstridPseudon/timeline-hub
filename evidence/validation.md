# D141l independent validation

All checks were read-only. No App tests, types, lint, browser, live socket, body, request, queue, source, generated, pin, registry, kit, or Git metadata changed.

- Git object/tree/parent checks for 4de, d822, 82e and reviewed 493: PASS; identities are in source-manifest.json.
- sha256sum of all sixteen raw request/snap/summary/log/trace/receipt files: PASS; hashes are in source-manifest.json.
- jq empty over prior evidence and generated JSON: PASS.
- Pristine full receipt validator: exit 0, stdout 4793895424.
- Pristine Node 11111 receipt validator: exit 0, stdout 4600000000.
- d141-validate-trace: current full 256, current Node 19, pristine full 202, pristine Node 21: all exit 0.
- git rev-parse commit:path checks for package files, both Node failure files and both useTimelineSave files: PASS.
- Final read of app-pin-867cb273/KEEP: present; this bounds the prior 0705 missingness as historical/time-local.

Raw results were not rerun. Historical full evidence stays bound to 4de and is not retargeted to 82e. Pristine Node DATA uses retained derived values 4814028800 and 4625068032, floor 4600000000, and does not claim original stdout or a continuous peak.
