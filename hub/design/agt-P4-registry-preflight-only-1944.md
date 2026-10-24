# Report: PREPARED

- No product/test/registry changes; worktree remains clean.
- Exact registered command reconstructed with the `test-run` awk: `bash -n` exit `0`.
- Positive row-equivalent probe: launcher preflight `0`, stub/body exit `17`, stub count `1`.
- Poison wrong-Agent-SHA probe: exit `1`, stub count `0`; rejected before body/evidence initialization.
- Original test bodies untouched; aggregate hash `8e336b1ce059770f63e3026e0ee9fc0a3f29bd6e557fbba4725138065c453753`; timeout remains `45s`.
- Registry SHA unchanged: `ad72a53f20f1786e5f284e0f030e41e8418b080f119b368fb14b8085c2f534e9`.
- Exact pinned tuple: Agent `3b2db4bdf9014de013338521dd038ebdecd25f02`, Runtime `e89eb8c7dfa8cb2c451653ab200dbf77df28b173`, App `e771ce1426022d1a10bab93323d40222c5ce9c3d`, Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`.

Durable evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-P4-registry-preflight-only-1944/evidence/`

No service request or pytest collection/body was run. Prior 5907 zero-body failure and 1939 WIP remain preserved. Commit message and `DONE` were created.