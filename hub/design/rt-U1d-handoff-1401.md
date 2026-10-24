## U1d-final handback

- Integrated Runtime: `e68cf231641db98a72805a586b51ab5c4fae2c16`
- Tree: `a2cbedd185c7e576e20ed060d993deba17111b78`
- Parents: `becfe6db88b2cc034dba3fafa6c050117cdf2b06`, `60e7838d8b4735a41686f82fb081969e75363c0b`
- Upstream parent `d4f496ec4fbcae7a1f3a51d47ed5147c561117ad` is present in ancestry.

### Contract/client identity

Read-only comparison against `becfe`:

- OpenAPI: `contract/openapi/workspace-v1.yaml` — `sha256:302523509996d42fb1d978912f4e6ea022d8ba596896c6cc307161d2cdc5c075`
- Contract schemas: 38/38 byte-identical.
- Runtime schema: byte-identical.
- Canonical generated clients: 15/15 byte-identical:

```text
conformance/second-client-core-v1.yaml 3a0a5aff4e66435212ba567850a0a27c5555601a33ecbd3ed7e21737948662e3
packages/python/astrid_runtime_client/__init__.py d095328fdfadc0883aa103147eb8be8d91f24de2f5fc81c6a9ac37be1809ecc2
packages/python/astrid_runtime_client/contract_metadata.py 51e8ce94a7149f6b3160a6e5e66bafe17c7f94cfd3beb6733bbf8abd63125ab6
packages/python/astrid_runtime_client/generated.py e3f51c05342088bc34a562e17997cbf8ff8065c3df795da1cb6cd374216b51b7
packages/python/astrid_runtime_client/timeline_commit_types.py 88c67d9eb650b445b8ad04c9011c1f44f1ec5e9f72a4a733050515de7ec0b616
packages/python/pyproject.toml 6c15723214b1d240f1e9fbea6692019da4893acc486dabcb74ab28e2efaf879f
packages/typescript/package-lock.json bb5b79bd79ddd6c780a16e658763f7d534718a739703abcf809b75b664957d66
packages/typescript/package.json 8510b0cb8e15630ef999539e697b4f480e6b640d8c9b56c121fa58b66fb451f3
packages/typescript/src/contract-metadata.ts 1028aaeca1cd15f860994c1e830ba69f55405e648841877eff4d43f466f40c79
packages/typescript/src/generated.ts 7be7f351d485fdb24a7ebb0329fea7c65037675b11a96c581d33e60a14a581a4
packages/typescript/src/index.ts 2d23f8ee1cb38e6b1d3366663887b88a4981ec298d8c8d5a758a62a7ad8cc0e4
packages/typescript/src/operation-handle.ts 3f8c69044a0efd5171290f925b0bc3706495c4c0da0252d0008d8056671fa460
packages/typescript/src/timeline-commit-types.ts bf4728831e35bdfec96ffa0188feb439f3c89a2aecfa8682925019eba5855470
packages/typescript/tsconfig.json 48bc718286b70c7ff5af00d1ad727ad7c7f8820d3050117dc9d6aea239181b
runtime_protocol/contract_metadata.py eddaa15a86a1c23ebf3f7e456363176bb9d49db3759bf5de29fdb52398c6b30a
```

### Manifest and visual fixture

- `contract/artifacts.json`
  - previous file SHA: `sha256:2f3d56b6f83834b4529ecb86657e2a5948bce072342bf46f9a2ab983cae369c3`
  - current file SHA: `sha256:f74b0e3041fe45422e6f4f349ee65401fe7222cacefdfa782aaac59354ff4d20`
  - previous version: `sha256:65085756a96619a74de401b90d6e1b4ff0590d5090e4d4d411c50de476f345b8`
  - current version: `sha256:9af2df7561a7e7d6793ad9f82acb7770ddbecf03dbdc753496c42ff86466eb24`
  - 79 → 80 entries; only addition is the visual fixture.

- Fixture: `conformance/fixtures/visual-seam-cases-v1.json`
  - file SHA-256: `1f8363394e0b7049096365d38d00bf2dfed888eab30c3b2bce95cd44537a02e7`
  - Git blob: `1f3d845cf056d3fc45498fbbdce295ac12da09c6`
  - Same blob in upstream `d4f496ec4…`; verified byte-identical. This is a genuine published upstream fixture, not a synthetic copy.

- Source:
  - `runtime_protocol/visual_seam.py`: Git blob `9bb0bfb04c4cb17c539ffc3f8565f4987df0bb65`, SHA-256 `52de571a667a53e8f60deda7cdd7b27abfab753af67a2d4f2156739ac7341aa4`
  - `docs/visual-seam-policy.md`: Git blob `dca6a01c79472c713edfa35d7e98a5299cb91619`, SHA-256 `665374d51241720b2917f54c05d69f3c03b46db60c2648bacba04e0527faf579`

No D39 regeneration/adoption was triggered. Client bytes are becfe-compatible, but producer identity changed: current consumer locks still name `source_commit=becfe…` and old producer version, so a future source/vendor-lock rebind to `e68cf…` is required. I did not edit or certify Agent/App consumers.

### D60 fixed tips

Verified present locally:

- Runtime upstream: `d4f496ec4…`, tree `1d3e06f4…`
- Agent final924: `92443771676ef2bbb547d0a103d708fa8bec4c63`, tree `a81a8c7f…`
- App09c: `09c84403303d617af4bd7426d29bb80002253e08`, tree `77c72a50…`

Agent/App heads remain owner-controlled.

### Callers and limits

Production caller remains Runtime `commitTimeline` via `runtime_protocol/server.py:302` and `RuntimeService.commit_timeline` at `runtime_protocol/service.py:2435`. No mocked-unit all-fields claim was made; the full v2 request/reply contract remains unchanged.

Checks:

- Read-only ancestry/tree/diff checks: PASS.
- `git diff --check`: PASS; worktree clean.
- Existing generator and artifact-manifest `--check`: PASS per independent core1346/author evidence.
- No duplicate targeted tests, full suite, build, ZIP, install, browser, or live service run; those belong to the integrated/service owners.
- No product changes were made. `DONE` marker created.