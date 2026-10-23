# F-D22 profile clean port verification

PASS: root `report.md` was preserved byte-for-byte outside the product tree,
then removed as the only worktree change. The exact preserved evidence copy is
`agent-F-D22-profile-clean-1525.md`; this verification records the cleanup
checks and provenance.

- Source: `42476c08a6ffd318d7eb7100d48edceff7313ad6`.
- Review: `225fe3f6c697f90c25d4f3e4394d61b974009b22`, independent PASS for the
  test-support correction; overall qualification remains 34 passed/6 failed.
- Root report preservation: 12,402 bytes,
  SHA-256 `719312091e134298facda9a861b43751b60e04999fbb9cb6adafb2c48658b278`.
- Final product diff: only `D report.md`.
- Four reviewed424 blobs unchanged: `6d13a3a2…`, `5b4241f0…`,
  `9428061c…`, `d929834c…` for backend, layer-tail, mapping, and AM plate
  tests respectively.

`git diff --check` and compileall of all four files passed. Previously recorded
evidence was reused without rerunning known-red nodes: 34PASS/6FAIL,
6PASS/3FAIL representatives, 3 mapping PASS, mutation probe PASS, Ruff 2149,
private Mypy 1912. No product change, assertion weakening, integration merge,
Git write, or branch operation occurred.
