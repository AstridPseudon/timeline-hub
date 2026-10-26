# Producer and acceptance handoff

## Final status

- Exact-15 source custody: PASS, restricted to these 15 REG selectors.
- Final producer mapping: PASS, actual 15 Agent client mappings in `producer-corrected.json`.
- P5 applicability: PASS for the retained 38/38 receipt; no P5 rerun.
- Full-suite GO: NO.

## Canonical producer identity

Runtime producer is `/home/user/work/runtime`, `tl/integration`, head `95d98f038320d5d46bd679ac000ab3e15825c935`, tree `78df31d62c5b9ba4c84dee4ea346e43a767718c1`, parents `857e4c3bce8fd7fc862d7e6e5831e63f24e8cce5` and `012889c1b0bbfe5f290f757cb6d31dd7d995ccc7`. Its `contract/artifacts.json` bytes are unchanged from original Runtime `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d` and report version `sha256:084f3f2510edff28c18d33aac4a459f8aa6df3cb4fd71cba4fb292274ea8ade5`.

The actual Agent consumer is `/home/user/work/agent`, `tl/integration`, head `8585ed9c0404d0187b2ce70242d25114a32747c2`, tree `92a3ffdb5a8bf476e10bfa1bbda3e2856fb9938c`, parents `28e56cacb42d3da85b02e5b3543895b44f3d0f70` and `5d202569f3af3852476d182ff49683787bb1e881`. The 15 source mappings and hashes are immutable in `producer-corrected.json`; do not substitute the historical REG test-body hash field.

App is `/home/user/work/app`, `tl/integration`, head `5344c53e3063001bb3255bd0c9cd32cc5e77967f`, tree `dd989783046aeff652486a1ba39db42aea86e201`, parents `520d7e4fc12a03392afaed3f486aba34a2b5c319` and `dc1a86cf4797b6ca3799d9ad1dee7e7d949caf04`. Its Runtime lock has 14 consumer mappings and is not the canonical Agent 15 mapping.

## Normal commands for future producer/consumer checks

Run only through the existing normal tools, with the exact Runtime checkout at the pinned `source_commit`; do not fabricate a release/tag or edit a lock by hand:

```text
python scripts/vendor_lock.py check runtime.lock.json --producer <Runtime checkout>
node scripts/vendor-lock.mjs check runtime.lock.json --producer <Runtime checkout>
node scripts/build/verify-astrid-vendor-sources.mjs
```

The App callers were inspected in `scripts/testing/current013-parent-split.mjs` and `scripts/testing/auto-real-proxy-main95.mjs`. These commands were not run by this read-only review.

## Boundary finding

P5 remains attached to the original Runtime 6a / Agent 28e receipt. Runtime’s changed upgrade hunk is not in the P5 migration call path. Agent’s 54 changed paths include changed conftest/lanes, but the P5 process resolves those modules from Runtime, while Agent is supplied only through `ASTRID_CHECKOUT` for the retained provider modules. No changed Agent path is an executed P5 boundary. Separate Agent full/P4 work remains required.

## C0v2 caller reminder

Any production caller must preserve the full request/response contract: API version, project/timeline, base pair, labeled ordinal steps, per-step patches/reads, merge fields and atomicity, declared reads, idempotency, dry-run, source/rationale/group; and accepted canonical closure with authenticated receipt bindings, effects, dependencies, history, guarded undo. Conflicts expose reason/head; invalid requests expose code/path/hint/suggested command; preview remains mutation-free.
