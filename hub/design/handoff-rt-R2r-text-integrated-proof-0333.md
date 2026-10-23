## PASS — R2r integrated proof

- Integration: `ad823e0a0f5be4a7acf1d3006df6f794709da63d`
- Tree: `33904550800ee3e2fa34fe0b13c26754b46c7fdc`
- Service: `runtime-targeted-1023033159-11461`
- Central result: exit 0, `133 passed, 1 deselected`

Command:

```text
/home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_commit_authentication.py tests/test_timeline_commit_acceptance.py tests/test_timeline_commit_read_basis.py
```

Provenance:

- Reviewed auth blob preserved exactly: `85325f86fca53c2c487dbd3b064382ec3aa76dec`
- Auth SHA-256: `d23ca9093be62f0dd1b70cbd0f883aa4ab10437eb7cfc6545fc6dec234bda0c3`
- Materialization blob preserved exactly: `bfb1217ed19d6071ecafc2b4941f38fdfabeef6d`
- All 8 client-envelope paths from `34eac0041/tree98535748` are byte-identical.
- Current and pinned Agent `native_text_binding.py` both hash to `19476d6eaba2e9ce8ee379db52e180da10364cd2a5bcfbd119a445b5d64f736d`.
- Isolated origins resolved to this Runtime worktree and `/home/user/work/agent/astrid/sdk/timeline/native_text_binding.py`.

Independent exact-provider 21-case proof was reused: `21 passed`; no duplicate 21/native14/full/browser/heavy runs.

Verified guards include unauthenticated/outside/ambiguous aliases, duplicate slots, owner mismatch, refusal/no-write behavior, inverse/retry/idempotency, read unions, dry-run, accepted/merged/conflict/invalid projections, and authoritative history/effects/undo metadata. Production Agent provider routes through Runtime `port.preview/accept`; Runtime store invokes `timeline_commit_auth.validate`.

Producer/schema metadata:

- Production provider: `astrid-v1`
- Compiler: `authoring-bundle-1`
- Fixture provider: `prepared-auth-1`
- Schema digest: `sha256:35c2d9c5e0b51ab8d8b7a4f4dbafbdfcb13d232d7bd22fff21cf73e250398d4c`
- Artifact manifest: 78 entries; `contract/artifacts.json` SHA-256 `7c541b705a9dbc0827ed2e81a847455402b1d475491de702cde7ef85f4a8235d`
- Component manifest: `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5`

No repository files were modified. `git diff --check` passed and the worktree is clean. `DONE` and the R2r harness commit message were written.