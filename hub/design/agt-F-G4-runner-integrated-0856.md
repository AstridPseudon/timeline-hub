## PASS — F-G4 runner-integrated

No product changes. Worktree is clean; `DONE` and commit message were created.

Integrated home:

- HEAD: `67d5f19716d1e6b2f30445e14bfdcbf3927108de`
- Tree: `404c0d69bf58e58770fd5f9ba793b680c4ce7430`
- Only diff from base: the two approved runner files.

Exact blobs, equal across home, author `0842`, and independent `0848`:

- Discovery: `0f14d14940f261d279e50b4ca9dd57acc4730dee`
- Generic reopen: `15b7b62ad308addff8a3e09cf5ccc6cf9a1313fa`

Carriers verified physical, clean, and unchanged pre/post:

- Agent `0ff3d103...`, tree `1d613f...`, `/home/user/work/wt/agt-pin-0ff3d103`
- Runtime `becfe6db...`, tree `7edc08e3...`, `/home/user/work/wt/rt-pin-becfe6db`
- Runtime lock: 15/15 mappings exact.
- Canonical client identity: `d79568df4fe4bed2a217b519d73824e8fd1ca17f61dfe0ce8492f1903764eb44`

Checks:

- Private-cache `py_compile`: PASS
- `ruff check --no-cache` on both runners: PASS
- `mypy --follow-imports=skip` on both runners: PASS
- `bash -n` on both wrappers: PASS
- Read-only AST/source/diff audit: PASS
- Original bodies preserved: discovery 9 assertions/10 calls/45s watchdog; generic 12 assertions/30s watchdog.
- Store, RECORD, lease, context, profile, client, and pre/post custody guards preserved.

No runner, preflight, candidate, original body, provisioning, browser, network, or process probe was invoked.

Recommended next step: normal merge queue.