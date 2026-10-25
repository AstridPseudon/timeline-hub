# D128/F service validation

- `bash -n /tmp/w-4d8825d3a3/inventory_whole_maker.sh` — PASS.
- Protected helper, candidate maker, source1747 manifest, and parsed service row guards — PASS.
- `request-test ... inventory-whole-maker` — service returned immediately with exit 2.
- Failure occurred at the wrapper disk guard before `--write-inputs`; no Store initialization, Git fixture commit, maker, verifier, or registration ran.
- Wrapper corrected to ignore the `df` header; no second service submitted per task rule.
