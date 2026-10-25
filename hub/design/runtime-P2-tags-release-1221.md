# Runtime P2 tags release packet

Status: **RELEASE_PACKET_READY** for the normal integrated Runtime tree.

## Receipt

- Normal full SHA: `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`
- Normal tree: `de2954a0ceadb4455903d9abdfec3b773318a50f`
- First parent: `7070f1378d1917fcce69857ebd33cd2b3015568b`
- Clean authored import: `ef4728a1c07b7d3909d5027fbf1e673f6aec0030`, one commit over `7070`.
- Integrated merge receipt: normal tree equals the clean authored tree and independent 1206 candidate tree `de2954a0ceadb4455903d9abdfec3b773318a50f`.
- Worktree was clean; no product or test source was changed for this packet.

The only paths differing from `7070` are the four Runtime modules and the two history diagnostic/boundary test files. Contract, schema, generated-client and canonical-shape paths are unchanged. All four production source hashes exactly match the independent 1206 proof, so its zero-new Ruff/Pyright and public-envelope evidence is reusable.

## Verification

- Exact diagnostics/boundaries: `56 passed in 8.45s`.
- Genuine Agent provider/native seed controls from `/home/user/work/agent`: `2 passed in 12.77s`.
- Scoped `py_compile` and `git diff --check`: PASS.
- Scoped Ruff: 54 pre-existing findings; zero new findings against independent 1206.
- Scoped Pyright: 432 pre-existing errors, 0 warnings; zero new findings against independent 1206.
- 44 unique allowlisted private diagnostic tags; tag list is in the JSON packet.
- The reference-projection apply fault retains the released public `503 not_ready` envelope. The independent proof records the other 55 parent/candidate public envelopes as byte-equivalent.

## Preserved wire and limits

The C0v2 request remains `api_version`, `project_id`, `timeline_id`, `base_revision_id`, `base_publication_id`, `commands`, `label`, `steps(id,label,intent,tags,command_ordinals,patch,reads)`, `merge`, `reads`, `dry_run`, and HTTP `Idempotency-Key`. Accepted/merged replies retain `canonical_document`, `receipt`, `head`, `effects`, `bindings`, and `dependencies`; conflicts retain `head` and `reason`; invalid replies retain `code`, `path`, and `hint`.

Diagnostics are private, static-tagged and bounded: stderr is at most 4096 bytes, request IDs are 32 lowercase hex characters, and request/payload/message/locals/stack data plus diagnostic IDs in shared commit context remain excluded. No credentials or private payload export was performed.

This packet does not claim the full suite, browser journey, live sockets, replay, P4, or a new security review. Original `11251` SWAP remains **UNKNOWN** and has no root-cause/root claim.
