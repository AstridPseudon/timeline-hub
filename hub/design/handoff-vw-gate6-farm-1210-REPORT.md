# Gate6 farm transport 1210 — handoff report

Status: HOLD.

The corrected, independently reviewed 1153 packet is now available through
normal design sync as flat `handoff-vw-gate6-farm-1210-*` files. All eleven
reviewed packet files were copied byte-for-byte. The original reviewed
manifest digest is
`0ee53582e55a4f9eb8464a2d7581924cf42bb5a56f3d75de362991f3e196299e`.

The issuance source is present only to preserve the complete reviewed packet;
it was not run. No secrets, grant/token/marker artifacts, generated
operational JSON, source checkout, node_modules, media, Runtime stage, browser,
or install/build output was exported. The complete stage, helper carrier,
graphs, dist, package archive, and pinned toolchains remain external inputs for
normal write-once farm transport. Their identity and inode requirements are
recorded in [the request](handoff-vw-gate6-farm-1210-REQUEST.md).

The request also records the only permitted farm-local path relocation: apply
it to a private materialized copy, recompute its hashes, and never claim the
reviewed packet digest for rewritten files. No relocation patch was applied
here.

## Verification

- `sha256sum -c design/handoff-vw-gate6-farm-1210-SHA256SUMS` — PASS.
- Byte comparison of every exported reviewed file against its 1153 source — PASS.
- `git diff --check` — PASS.
- No local test request, install, build, browser, socket, Runtime, physical
  run, marker issuance, or grant/token creation was performed.

The 1153 assertion review approves one central preflight only and makes no
physical/browser/pass claim. The 1209 farm request remains HOLD pending fresh
authorization, complete independent 1054/b70 transport, and the unverified
central preflight/final gate.
