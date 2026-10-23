# R2r normal sequential input-authority classification — 2026-10-23

## Result

**Classification PASS; end-to-end qualification FAIL/HOLD.** This is the normal sequential-step input-authority boundary, not the inverse-leaf case. Runtime 859 is already correct to refuse Agent peer 1335's moved-head step-2 request when the submitted command/step claim names the original unlanded physical ID. No Runtime guard waiver, alias retarget, fabricated continuation, contract change, or provider-wire rewrite is justified.

Disposition: the required original-sequential authority is present in the Agent 1335 flat capture and must be authenticated at the Runtime landing boundary. The Agent provider owns producing and transporting the source-bound capture; Runtime owns the existing authenticated-boundary refusal and the eventual verification seam. This slice authorizes no code correction.

## Source identity

| item | exact source |
|---|---|
| Runtime tree | `8592822fd11275540f596562f43c715676f2bc0f` |
| Runtime auth | `runtime_protocol/timeline_commit_auth.py`; SHA-256 `d79f2da9f47cbc4aef8d51a899d47ec04458d9140e67636c7c83e0675d0072e2`; blob `7f803cbf69f104cafa5542ba8db842d0f00c8fda` |
| Runtime port | `runtime_protocol/timeline_commit_port.py`; SHA-256 `d78dd313220634baaf37c9a6cb7a578b4453c3c94060eb13c02778834eeac867`; blob `438e22b54047b1450f9d812f61be460077314a35` |
| Runtime store | `runtime_protocol/timeline_commit_store.py`; SHA-256 `243d312fe404f5ed80f0ef1aa9d7405b93ff77949eef5157827a7779c6323b9f`; blob `6fcee8073936c68c8cb6c5d402196547c1877c19` |
| Runtime inputs | `runtime_protocol/timeline_commit_inputs.py`; SHA-256 `bf04dc5d26fd6e6283ae11c7d0fa55fa5730c45f19e1c55bda529062cab696e4`; blob `6c3ed33bacfada65f37fb4b9bc4285653ce71794` |
| Runtime materialization | `runtime_protocol/timeline_materialization.py`; SHA-256 `92ec9b7f105d5e0fd1c5f9e9f2a4602ee3dd005365a570e7ba91a573bb8b31fb`; blob `bfb1217ed19d6071ecafc2b4941f38fdfabeef6d` |
| Agent provider tree | `851439d95647820815e69b4d7163e179540f28db` (`agt-R1-sequential-rebase-sol-1317`, held) |
| Agent patch | `astrid/sdk/timeline/_commit_patch.py`; SHA-256 `2de28bab7756e03f57f119c2049cf79cdd8195c6b726ebea0f06d7d1eb7ff664`; blob `e5fdb6c471fb5e486814af4b72d2aa938753ec5a` |
| Agent execution | `astrid/sdk/timeline/commands.py`; SHA-256 `d1439159267154f36bda603c030b6b5299058411628b18edcbeea0779743bebf`; blob `e06810281e6aafced856b3d0efce1753a733833c` |
| Agent regression | `tests/editing_conformance/test_doc_patch_sequential_rebase.py`; SHA-256 `75ccd026898b241d2241f5c058342aeb728e3a70f039a8701343b55f6fc648f6`; blob `89e359f2f611d1b214eee530fd316d061456ed2b` |
| Agent current review | `e44b4854ce32db55d922b27352cee20589d48e45`, `design/agent-R1-sequential-current-review-1335.md`; blob `195a17e1e7313a74ecd5bda21be98497d0fe77a7` |

Flat packet: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-R1-sequential-current-runtime859-packet-23d309fb6f841fbb.json`, SHA-256 `23d309fb6f841fbba8560317c336b495ec4fcf2700a7e4c69bb7e1ea5c0f7ca7`. Manifest SHA-256: `f575352cab8a1821f209b38b7b689c2c9fbd366499e2e705abac541874add560`.

## Exact captured request and custody

The direct qualification uses the complete v2 request shape:

- `api_version: 1`; project `903cf7da34dd4f019308e99179850493`; timeline `t`.
- Base pair: revision `saved-parent`; publication `txn-26303dd2212b43d4bf85457da7570d0a`.
- Commands: two `doc.patch` commands, version `1`, schema `1`, `select: null`, one `set` change each. Step 1 is `internal-revision:internal-film` (`3.5 → 4.0`); step 2 submits original staged `internal-revision:authoring-timeline-revision-dca4ac169a752675550e48131b94c457954bd12799648975c1a70ce7b8c519a6` (`4.0 → 4.1`).
- Label `Two nudges`; `merge: fields`; top-level `reads: []`; `dry_run: true` for the diagnostic preview; source `{via: python}`; rationale `Sequential physical inputs`; group `sequential`.
- Steps: `first` and `second`, intent `Nudge cross`, tag `nudge`, ordinals `[0]` and `[1]`, each with its own patch. The no-declared-read case has `second.reads: []`; the declared-read case carries field reads for `clips/id:cross`, `clips/id:vo2/app`, and the ordered `clips` collection.
- Idempotency is transport custody, not a request-body field: the retained Agent regression sends preview with key `preview`, acceptance with key `sequential`, and the peer edit with key `peer`.

The provider records preserve the full step/command custody: ordinals `[0,1]`; each command has one read and one write; step 1 has 9 bindings; step 2 has 9 bindings without declared reads and 12 with them. Each step binding carries the base pair, evaluated landing head, step id, command ordinal, phase, submitted alias, physical image, revision/content digest, and occurrence owner set. The declared-read case additionally carries exact field and collection dependency states, members, and order. No accepted history entry is claimed for the refused diagnostic; the captured `history` is null. The continuation map contains only accepted peer materialization edges, for example `internal-film → authoring-timeline-revision-a8dc…` (first failure) or `internal-film → authoring-timeline-revision-4dc…` (second failure); it does not contain the Agent-generated original staged ID.

For the first moved-head capture:

- base parent: `saved-parent`, digest `sha256:f0d3cf169ce9d4e701201b32c4087c8577977d44839bca11cc30685a60432716`; base internal: `internal-film`, digest `sha256:69293b4720ccf38e793b261d5c2dd3cd58bbdb4d86bf927e98dde361310db116`;
- landing/evaluated head: publication `txn-f1ba87d58945456dabb65f7dde81072d`, revision `authoring-parent-revision-cb1e8eb9512715e6e156e1b7692e66c6ebb2e4593547b77a82d1c5f72e3acf4`, parent digest `sha256:64655aa46862413b229727f71fb0bbd4d0343299de735fdc87e6c7a8b4accbf3`, internal landing image `authoring-timeline-revision-a8dcce6ee1d6d85d200876afb934b27138a0870b548e71930f939a40e2b1bd67`, digest `sha256:8fb0b63e0984edbc26f9157866e46230fde285160bdc3ea2fdfa79bea8108917`;
- step-1 actual input binding resolves the base alias to the landing image above; step 2 retains the original staged alias in the request and records a replay input `authoring-timeline-revision-3d119adba2712190c455947ba7991bf62857aed8a6ae61fbaf1a218540be3584`, digest `sha256:84298a66636b73e2e0592cb5b504e343594a62fdc14e5f5f5d75492ef48f6561`, owner `occurrence:occ-film/shot`.

The second declared-read capture is equivalent: landing head `txn-c05291bb56594280b25df9811ae88fd9` / `authoring-parent-revision-606205d5a633e66a2ec5872cd04bc811b69152f63cbb4296251bea6164ec51a8`, step-2 replay image `authoring-timeline-revision-babe5f2156f6ffceb343eb89dd2bda55a733d069a5cab61c7651efdcd4090bd3`, digest `sha256:84298a66636b73e2e0592cb5b504e343594a62fdc14e5f5f5d75492ef48f6561`, same owner. The flat packet contains the complete payloads, bindings, base/source/landing images, execution plans, and tracebacks.

## Runtime boundary and causal result

Runtime 859's existing path is source-backed and conservative:

1. `timeline_commit_store.py:807-813` constructs the accepted landing `source`, the original `base`, `_binding_continuations(base_publication, expected_head)`, and authenticated inverse history, then calls `timeline_commit_auth.validate`.
2. `timeline_commit_auth.py:1346-1352` creates `boundary = images(source)` and `original = images(base)`, validates base reads, then validates request reads against the landing boundary.
3. `validate` starts each step at the landing boundary (`:1361-1363`) and derives later command inputs only from prior command outputs (`:1388-1392`).
4. `validate_step` validates submitted step reads through `validate_read → normalized → site` (`:309`, `:232-233`, `:208-210`) and submitted patch claims through the same `normalized` path (`:338-346`). `site` (`:99-172`) accepts direct boundary roots or a unique authenticated continuation for shot/internal refs; the original staged Agent ID has neither.
5. The moved-head no-read case fails at `validate_step:344`; the declared-read case fails at `validate_step:309 → validate_read:233`. Both are `invalid_records` / `provider alias is outside its authenticated boundary`, before write or accept. The no-write/refusal behavior remains visible.

`RequestCommitPort` is also correctly scoped: `history_entry` (`:193-215`) walks only observed/base ancestry; `revision_closure` (`:225-254`) admits base, observed, or declared/ancestral revisions; source/document captures (`:256-300`, `:367-393`) are request-private and exact. It has no existing normal sequential API that turns an unlanded provider-generated physical ID into accepted-history authority. `_binding_continuations` (`timeline_commit_store.py:752-764`) derives only from accepted `commit.materialization` records. That is why the current refusal is not an inverse-leaf bug and must not be bypassed by copying or fabricating a continuation.

## Qualification evidence

Exact retained command:

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8592822f PYTHONPATH=.:/home/user/work/wt/rt-pin-8592822f PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_doc_patch_sequential_rebase.py
```

Result: **2 failed, 7 passed in 8.95s**.

- Fresh-head positives: 2 passed (provider and Runtime accept).
- Moved-head positives: 2 failed at the Runtime auth boundary (declared-read absent/present).
- Strict refusal controls: 5 passed (field, consulted read, membership/order, changed source, forged continuation), preserving no writes and exact refusal reasons.

The retained Agent source report also records provider quality checks as passing (ruff 2149/2149, targeted ruff, vendor lock, artifact manifest, diff check) and explicitly keeps the two positive expectations unchanged. No full suite, browser/live socket, native, P1–P4 duplicate, daemon, host build, or dependency mutation was run in this slice.

## Minimal seam and owner needed

Before any fix is authorized, the Agent 1335 flat artifact must arrive as a normal hub source and contain, for every sequential physical input:

1. immutable original staged physical ref and path, original revision/content digest, source step id/ordinal, source boundary/base pair, owner and complete owners list;
2. exact landing/evaluated head pair and landing physical ref/digest;
3. authenticated source→landing/replay mapping, including edge-before/edge-after and the complete owner closure, tied to the same invocation and command ordinal;
4. request command/step patch, declared reads, before-values, membership/order, dependencies, and the provider's actual replay input/output captures;
5. accepted-history records only where they actually exist; no synthetic history edge and no retargeted wire reference.

The minimal existing seam is the current provider binding/`command_inputs` path plus Runtime's authenticated continuation/history machinery. The missing proof is normal-step source-to-landing authority for the original unlanded ID, not a new generic tuple or guard relaxation. Once the source artifact is available to the normal hub, Runtime can be assigned a narrowly scoped verification change; until then this report remains report-only.

## Checks performed in this worktree

- `git diff --check`: PASS after report creation.
- Protected Runtime source diff check (`git diff -- runtime_protocol/timeline_commit_auth.py runtime_protocol/timeline_commit_port.py runtime_protocol/timeline_commit_store.py runtime_protocol/timeline_commit_inputs.py runtime_protocol/timeline_materialization.py`): PASS; no product source changed.
- Protected source hashes and Runtime HEAD above match the checked-out 859 tree.
- No Runtime test was rerun because this slice authorizes no code correction; the exact targeted Agent/Runtime command and result above are the retained qualification evidence.

## Next step

Keep Agent 851 unmerged, G5 draft-only, and P1 NO-GO. Queue a future Runtime normal-sequential-auth verification task only after the flat source artifact is present in the normal hub and its five custody items above are independently checked. Do not merge inverse-leaf work into this issue.
