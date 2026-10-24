## Result: PASS

- ActualHOME conformance: **263 passed in 35.42s**; no skips/xfails.
- Command used: exact requested pytest lane with `PYTHONPATH=/home/user/work/agent`, Runtime `8ea0766f5e...`, `--timeout=45`.
- HEAD/tree stable before and after:
  - Agent: `622b30a8c33b...` / `49c96e0812...`, clean.
  - Runtime pin: `8ea0766f5e...`, clean.
- Reviewed source blobs: **5/5 exact matches**.
- Loaded frozen origins:
  - SDK `11caf1d9de...`
  - Runtime `31c7ac3a00...`
  - App `8f0c248446...`
  - Composition `c82eb7c459...`
- Canonical client vendor check against declared producer `45c3a7f476...`: **PASS**.
- Artifact manifest: **current**.
- `git diff --check`: **PASS**.

The older `34eac004` producer did not match the current lock’s declared producer, so that check was correctly rejected and not counted. No product files were modified. Full, browser, headless, ABA, SDK4, c271, occupancy, and benchmark suites were not run per scope.

Required `commit-msg` and `DONE` markers created.