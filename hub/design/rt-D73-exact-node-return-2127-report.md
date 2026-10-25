Implemented the private D73 candidate:

- Corrected pytest argv ordering and per-request `D66_OUTPUT_DIR`/request-ID binding.
- Added source/hash guards and positive/poison control dry-check helper.
- Added required evidence files under the worker evidence directory.
- Preserved `NOT_READY`; no central config, product, test, install, or live request changes.

Validation passed:

- `bash -n ops-d73-exact-nodes/dry-check.sh`
- JSON parsing for both evidence manifests
- Synthetic two-ID binding check
- `git diff --check`

`--source-check` and `--controls` remain unrun because the eligible single Agent receipt and rendered manifest are missing. No full suite was requested.

Files: [README.md](/home/user/work/wt/rt-D73-exact-node-return-2127/ops-d73-exact-nodes/README.md), [dry-check.sh](/home/user/work/wt/rt-D73-exact-node-return-2127/ops-d73-exact-nodes/dry-check.sh).