# D124 next Farm core command review

## Verdict: PASS for source-only preparation

The next packet is bound to the actual merged Agent
`a4e016b6a9f91fbe372672bdcf382c630bf59186` / tree
`60d45288145414ee4702fcce61af7c7810c2a3df` and released Runtime
`5e9ad1c6f74241d8771d3284fdd2ce7a214fd344` / tree
`de2954a0ceadb4455903d9abdfec3b773318a50f`. Both parent lists are recorded
from Git objects, including the second parents for App
`331a58363d1dc6ade1db2d2fa9d58688520c51bd` and Composition
`c05fdb171fe37c1d5817a060ecb716a329ee821a`. The command shell block guards
both complete parent lists. The existing App and Composition source pairs are
retained from the qualified packet, with Composition at the requested
`tl/integration` base.

The Agent target is the merge of reviewed union `16bbd56d` and host fallback
`96df3f5b`; the released Runtime source is read from its authoritative Git
objects rather than the ambient Runtime worktree. The Agent lock blob
`e4f7e2db58ce73bbe69c1ae07566ba56b360bf47` names the released Runtime SHA.

## Source and identity checks

- Comparing Agent `0b586e4b` to `a4e016b6` found exactly 10 changed paths and
  3,555 invariant non-target blobs across 3,563 old and 3,565 new tree paths.
- The exact 22 selector roots are retained against the 23-entry metadata
  inventory. The live-scene composition root remains present, and no marker,
  `-k`, row, default-filter, or other prefilter was added.
- Runtime `5e9ad1c6` is a Git commit with tree `de2954a0`; its generated
  canonical/schema identities match the qualified Runtime source. The
  current Runtime change is source/protocol history only; no client or schema
  regeneration is introduced by this packet.
- Canonical-15 source `6e8ae014`, schema digest `867f3553…1708b`, canonical
  schema `3654ca3c…9815`, and Runtime bundle `e4da5c…96e1` are retained.
  The Remotion tree, schema-source blob, launcher blob/SHA-256, and D73 maker
  blob/SHA-256 are byte-identical to the 1336 packet.
- The qualified1336 parsed-row controls are retained: the positive control must
  exit 17 with one fresh counter line, and the poison control must exit
  nonzero with zero fresh counter lines. The launcher SHA-256, Node `v20.19.4`,
  and stale-manifest rejection guards for `070dfc` and `b545b616` are explicit.

## Scope decisions

This is a source-only derivative. It does not add a Farm checkout request,
installer, profile or child-environment entry, service, named suite, helper,
hub write, harness, body, execution counter, receipt, or execution claim.
The production caller continues to use the existing registered unfiltered
`agent-core-full` launcher and existing D73 maker unchanged.

The existing Farm `0b586e4b/42aad0e9` and `9ea67534/369ffa7c` inputs are not
rewritten. Before qualification, the existing Runtime/Farm owner disposition
must be present: the lead owns source diagnosis and safe disposition and must
report the exact corrected normal maker receipt or an unresolved boundary. The
child-maker refusal concerning unowned local distribution metadata is consumed
as-is; no retry, substitution, overlay, or bypass is specified.

The C0 request/reply field shapes and authentication/privacy/no-write
semantics are carried forward verbatim in the packet. No product source,
tests, generated files, pins, schemas, clients, registries, or locks were
changed in this Composition worktree.

## Local validation

The following source-only checks were run after the final edits:

- `python3 -m json.tool evidence/input-map.json` — PASS.
- Both shell blocks from `evidence/next-farm-core-command.md` were extracted
  into the task TMPDIR and checked with `bash -n` — PASS.
- `git diff --check` — PASS.

No pytest, sockets, browser, full suite, body, profile, installer, collector,
observer, floor wait, or installed-environment proof was run or requested.
