Fixed only `tools/run_d40_installed_observed.py`: 15 insertions, 6 deletions.

The mismatch was representation: 0520 uses location-bearing AST dumps (`include_attributes=True`) and a source slice without an appended newline. Both now reproduce every immutable digest. Baseline 0520, original file SHA `3d8538d03b59eeb0f5cf0b397f639af0dfa3f5cbb5ce3b102001c427d6eb48ef`, three assertions, and observer capture remain unchanged.

Validation passed:

- `python -I "$TMPDIR/identity_checks.py" old`: expected **RED** identity guard.
- Same command with `new`: **GREEN**, 32 actual custody checks, five negative identity checks, **zero child/body invocations**.
- Synthetic preflight: **6/6 PASS**.
- Scoped Ruff, compile, and `git diff --check`: **PASS**.

[Exact commands/results]( /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D40-identity-sol-0620/evidence/checks.json) · [Exact diff](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D40-identity-sol-0620/evidence/runner.diff)

New runner SHA:
`cddde857a154057b3bea16643a44b65a77b1b85b0043ed259d25cfb4810067db`

Limitation: the temporary 0520 literal script is gone; its retained log omits patch contents. The scheme was established by exact reproduction of all immutable hashes.

No body run occurred. Independent Luna review remains pending. After PASS, the manager can use this unchanged command structure with a fresh owned `$D40_EVIDENCE`:

```bash
/home/user/work/bench-store/entries/child-3b5cb98c4f2dfc20ce8747f68bf2e1124ff47b9dd5f04dabaada3a22278fdfc9/bin/python -I tools/run_d40_installed_observed.py run-original --root "$PWD" --evidence "$D40_EVIDENCE" --reviewed-source-sha256 cddde857a154057b3bea16643a44b65a77b1b85b0043ed259d25cfb4810067db
```

Commit message and `DONE` written.