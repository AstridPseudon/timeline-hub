# Timeline v2.1 delivery, {{UTC}}

This ZIP is a delivery candidate for the `tl/integration` branch of each Timeline repository: agent, runtime, app, and composition. Each repository is carried in two forms: a git bundle of its integration history and one binary-capable patch series based on the pinned `origin/main` shown below. Nothing in this candidate has been pushed, and this candidate is not a release receipt. The final build must perform one live-upstream refresh per repository and record the resulting identities before delivery.

The patch series is based on the pinned `origin/main` commit and has the `tl/integration` tree. Its commit message lists the merged commits, one per line. Per-commit history is carried by the bundle.

The patch route is intentionally linearized: `git am` creates a synthetic commit, so its commit ID is not the source integration commit. The tree ID is the delivery identity. Do not report the synthetic patch commit as a producer or publication identity.

At build time, the patch series is applied with `git am` to a fresh repository holding only the pinned `origin/main`, and the resulting tree is compared with the immutable `tl/integration` tree. Every bundle is checked with `git bundle verify`, fetched, and compared with that same tree. The generated per-repository sections below are authoritative for the build that produced the README; all final SHA, tree, and live-tip values remain pending until that build supplies them.

The final F-final source refresh is isolated delivery staging: it retains fresh upstream additions while applying and verifying this delivery's patches against the refreshed sources. It does not merge later upstream into the frozen gating integration tuple. Other D68 packaging changes are outside this document.

## Contents

- `README.md`: this file.
- `bundles/<repo>.bundle`: git bundles of `tl/integration`. A ranged bundle holds only commits after `origin/main` and needs `origin/main` present. A full bundle holds all history and clones on its own.
- `patches/<repo>/*.patch`: the binary-capable linearized patch series from the pinned `origin/main` tree to `tl/integration`.
- `SHA256SUMS`: checksums of every other file in this ZIP.

## Delivery status

**PENDING.** This draft deliberately contains no final acceptance receipt, ZIP identity, source pin, tree identity, or live-main refresh result. The delivery owner must install the final receipts before release.

## D65 owner release order

The owner performs this release sequence: (1) merge the Runtime patches; (2) merge the Agent patches; (3) from the owner App root, run the one guarded manifest update below against those owner-merged checkouts; then (4) merge App. The updater writes only the installer pins: it does not publish a release, invent a tag, or treat a worktree branch name as an identity.

Before the updater, App's adopted `runtime.lock.json` must have `source_commit` equal to the exact `HEAD` of `/path/to/owner-merged/runtime`. If the adopted lock still names an earlier Runtime, use the supported App vendor-rebind seam first, from the App root:

```sh
node scripts/sync-runtime-client.mjs /path/to/owner-merged/runtime
```

That seam delegates to `node scripts/vendor-lock.mjs update runtime.lock.json --producer /path/to/owner-merged/runtime` and regenerates the adopted Runtime bytes and lock hashes. It is the supported source rebind; do not bypass it with a tag, release label, fabricated SHA, or direct lock edit. The D65 manifest write then runs exactly once:

```sh
node scripts/installer/update-manifest.mjs --runtime-checkout /path/to/owner-merged/runtime --agent-checkout /path/to/owner-merged/agent --write
```

These paths and flags are the actual App [manifest updater](app/scripts/installer/update-manifest.mjs) (`scripts/installer/update-manifest.mjs:11-27`). Before writing, it reads the full Runtime and Agent `HEAD`s (`:81-89`), requires Runtime `HEAD == runtime.lock.json.source_commit` (`:92-112`), and requires the Runtime generated digest at `packages/typescript/src/contract-metadata.ts` to equal App's `src/integrations/runtime/generated-contract-metadata.ts` (`:113-117`). It then updates `agent.sha`, `runtime.sha`, and `runtime.schema_digest` (`:119-150`). The rebind seam is [sync-runtime-client.mjs](app/scripts/sync-runtime-client.mjs) (`scripts/sync-runtime-client.mjs:7-30`), delegating to [vendor-lock.mjs](app/scripts/vendor-lock.mjs) (`scripts/vendor-lock.mjs:45-105`).

The source contract is [`contract/commit-v2.md`](contract/commit-v2.md). Runtime is the only writer. App, Agent, CLI, Python, scripts, and sheets use the v2 commit door; there is no document-overwrite route, TypeScript executor, or force-conflict option. Existing permission refusals remain stopped. This candidate adds no trust backend and does not authorize Farm or schema-source access.

## Retired CLI migration (D72 / G5 / R5)

### Timeline write-route migration

The delivery retires the native `edit commands-file`/native-batch ingress and
the other separate native/publish writers (`edit --native`, `apply --native`,
`undo --publication`, `publish`, `publish_bundle`, and the old three-way
writer). A document edit now uses `timelines commit --file ... --message ...
--idempotency-key ...`; the Runtime `commitTimeline` door owns accepted,
merged, conflict, and invalid replies, durable exact-key retry, and the
receipt/history. A single move or trim uses the current native `timelines edit
...` route. Cut-sheet edits use the current `timelines apply <sheet> ...` /
`NativeSheet` route, which emits registered commands through that same Runtime
door and preserves the draft on refusal. No native packet envelope,
commands-file alias, detached document overwrite, or resurrected G5 interface
is included.

The current Agent parser lists `commit`, `edit`, `apply`, `undo`, and `redo`, but not `publish`; see [the current command registry](agent/astrid/packs/timeline/cli.py#L3831-L3839) and the live help from `python3 -m astrid timelines --help`.

Use the supported forms below, according to the input already in hand:

- `python3 -m astrid timelines edit REF --project PROJECT ... --idempotency-key KEY` for the literal clip move/trim forms. Current `edit --help` says that literal moves and trims commit through the durable timeline session; other flags edit a detached working copy. The supported trim/move flags and their guarded dispatch are in [cli.py](agent/astrid/packs/timeline/cli.py#L3624-L3645) and [cli_native.py](agent/astrid/packs/timeline/cli_native.py#L176-L224).
- `python3 -m astrid timelines apply REF SHEET --project PROJECT [--dry-run] [--idempotency-key KEY] [--json]` for the current sheet path. `apply --help` has no `--native` option. The retained `show --native --as sheet` is read/export only; feed its sheet to `apply` (see [the retained projection](agent/astrid/packs/timeline/cli_native.py#L227-L238)).
- `python3 -m astrid timelines undo REF --commit RECEIPT_ID --project PROJECT [--dry-run] [--idempotency-key KEY]` and the corresponding `redo` form. Current help names `--commit RECEIPT_ID`: it reverses an accepted Runtime commit, while `redo --commit` reverses the accepted undo. There is no publication flag; the implementation dispatches these forms through the guarded commit path ([cli.py](agent/astrid/packs/timeline/cli.py#L3532-L3548)).
- `python3 -m astrid timelines commit REF --project PROJECT --file FILE -m MESSAGE --idempotency-key KEY [--dry-run] [--json]` for a detached JSON document. The parser requires the file, nonempty message, and idempotency key ([cli.py](agent/astrid/packs/timeline/cli.py#L3596-L3608)); it does not provide a separate publish command.
- Python callers use `from astrid.sdk import timeline`, `tl = timeline.open(PROJECT, TIMELINE)`, stage supported commands/helpers, then call `tl.commit(label_or_fn, merge="fields"|"atomic", dry_run=..., reads=..., idempotency_key=...)`. `Timeline.commit` permits bounded function re-evaluation only for an explicit conflict and retries an unknown transport outcome with the durable original request/key; see [commit_session.py](agent/astrid/sdk/timeline/commit_session.py#L163-L171) and [open()](agent/astrid/sdk/timeline/commit_session.py#L263-L280).

At the Runtime boundary, legacy timeline document/CAS and direct save routes are rejected with HTTP 410 through `_require_timeline_command`; their replacement is `POST /v1/projects/{project_id}/timelines/{timeline_id}/commit` (`commitTimeline`) with the exact base revision/publication pair, CAS/conflict handling, and `Idempotency-Key`. The route and refusal text are in [server.py](runtime/runtime_protocol/server.py#L522-L544) and [service.py](runtime/runtime_protocol/service.py#L1653-L1666); the accepted context checks the exact base pair and `commitTimeline` operation ([timeline_commit_store.py](runtime/runtime_protocol/timeline_commit_store.py#L337-L345)). Metadata remains separate and supported: timeline create (including the existing empty-shell adoption), rename, archive, and recover ([server.py](runtime/runtime_protocol/server.py#L524-L544), [service.py](runtime/runtime_protocol/service.py#L1697-L1763), [server.py](runtime/runtime_protocol/server.py#L657-L662)).

This migration does not change the v2 request/reply shape. The optional `HistoryEntry.recorder_abi` remains `1|2` (absent is the legacy ABI1 form). Automatic relational timing—anchors and pinned markers—remains deferred; these notes do not claim every deferred timing case passes. D72 protects the replacement path's idempotency, conflict/CAS, clean-copy, and output behavior; it does not turn a deferred or unqualified case into a final-tuple result. Use the Agent D72 family disposition and deletion ledger for test classification; this README does not duplicate that classifier.

## Summary

{{REPO_SUMMARY}}

Line counts come from `git diff --numstat --no-renames origin/main tl/integration`. A file counts as a test when a path segment is `tests`, `test`, `__tests__`, `e2e`, or `spec`, or its name is `test_*`, `*_test.py`, `*.test.*`, or `*.spec.*`. Everything else counts as non-test/product for this diff summary. These counts describe the delivery diff; they are not a qualification result.

## Applying

Start from a fresh clone or checkout whose local `origin/main` is exactly the commit listed in that repository’s generated section. Do not substitute a newer remote commit. Verify the pin before applying:

```sh
test "$(git rev-parse origin/main)" = "<pinned origin/main from this README>"
```

The per-repository sections are authoritative for the build that produced this README: they supply the pinned IDs, whether the bundle is ranged or full, the patch count, and the expected integration tree. The angle-bracket values above and in the commands below are intentionally filled by `delivery-build`; do not replace them with values from another build.

Use exactly one of these two equivalent routes for each repository:

- **Patches:** `git switch -c tl/integration origin/main`, then `git am /path/to/patches/<repo>/*.patch`. Verify that `git rev-parse HEAD^{tree}` equals the `tl/integration` tree listed in the repository section. The result has the same tree as `tl/integration`, but linearized history.
- **Bundle:** for a ranged bundle, run `git bundle verify /path/to/bundles/<repo>.bundle`, then `git fetch /path/to/bundles/<repo>.bundle tl/integration` and `git switch -c tl/integration FETCH_HEAD`; verify the fetched commit/tree against the section. For a full bundle, run `git bundle verify /path/to/bundles/<repo>.bundle` and `git clone -b tl/integration /path/to/bundles/<repo>.bundle <dir>`.

Replace `/path/to/` with the folder this ZIP was unpacked into.

Do not combine the routes on one checkout or force either route onto a newer base. If a pin, bundle verification, patch application, commit, or tree check fails, stop and retain the failure for the next source refresh.

## The v2 commit door

Production callers submit the existing commit route with `api_version: 1` and the v2 request shape defined by the contract. The HTTP `Idempotency-Key` is required for a mutation; it is the request key, not a replacement for the document base.

The complete request carries:

- `api_version`, `project_id`, `timeline_id`, and the exact `base_revision_id` / `base_publication_id` pair;
- a nonempty, ordered `commands` array, where each command carries `schema_version`, `op`, `version`, `select`, `args`, and `created`, plus `label` and `steps`;
- each step’s `id`, `label`, `intent`, `tags`, `command_ordinals`, `patch`, and optional `reads`;
- `merge` (`fields` or `atomic`), request `reads`, `dry_run`, `source`, `rationale`, and `group_id`;
- the required idempotency key, supplied as `Idempotency-Key`.

Commands execute as one transaction. They may use registered semantic commands or `doc.patch`; `doc.patch` is id-addressed, carries previous values, preserves ordered-list rules, and records authoritative effects. A patch request without declared reads is treated conservatively as atomic over the touched scope. The accepted record, not caller-authored claims, supplies the final step patches and dependencies.

Successful `accepted` and `merged` replies expose `data` and a complete `receipt`, including the canonical document, `digest`, `id_map`, authoritative `commands`, `steps`, `dependencies`, `effects`, `base`/`previous`/`accepted` pairs, `versions`, `publisher`, `history`, guarded undo, and `receipt_id`. `merged` identifies the actual landing head; it is not an old publication label. A `dry_run` success is `preview`, has `would_status`, and has a null `receipt`; it does not reserve a key or accept a write.

`conflict` and `invalid` replies are structured. A `conflict` includes its `reason` and `head`; invalid details include `code`, `path`, `hint`, `current`, and `suggested_command` (with the appropriate base/conflict information where applicable). A conflict is not converted into invalid-base prose, and an invalid document is not reported as a successful merge. Exact retries return the original durable reply without another history entry.

## Final qualification

The ship rule is final-tuple only: P1–P5 and the core Timeline suites must be green on the final integrated tuple. All outcomes below are **PENDING** until the final receipts are received. No historical result is promoted to a final GO.

| Proof | Final requirement | Venue / owner | Status |
|---|---|---|---|
| P1 | Real-document chain: split, trim the new ID, intervening Agent edit, lost acknowledgement, restart; accepted, merged, and refused replies all remain correct. | App service, with final Agent/Runtime/Composition tuple | **PENDING** |
| P2 | Core App editing gestures send commits through the door, preserve intended fields, reload, and undo; no old-route traffic. | App service; App owns the verdict | **PENDING** |
| P3 | Gate-5 journey on the v2 path, including exact retry, newer local work, restart/reload, undo, and zero legacy snapshot traffic. | App service; App owns the verdict and independent verdict review | **PENDING** |
| P4 | Agent CLI, Python, and sheet coverage: single edit, ten notes in one commit with per-step undo, conflict/re-run, and show/history readback. | Agent service | **PENDING** |
| P5 | Runtime acceptance carried forward: renderer-off save, commit-door authorization, crash/retry points, and changed payload under the same key. | Runtime service | **PENDING** |

Core qualification covers the end-state model: EditCommand, commit door, undo/redo, history, split/trim/move/placement/occurrence, show/sheet/visualize projections, the App save path, and the Agent editing runner, rebase, and inverse. **Core suites: PENDING.**

F-final is also **PENDING**. The Runtime manager runs the existing builder on main after one final live-main refresh per repository (D51), using fresh upstream clones and the final integrated tuple. The production caller is the existing installed delivery builder: it renders this installed README template and gate-results input, not an unused replacement document. A controlled four-repository stub render checks only placeholder, fence, and link wiring; it is not a build, ZIP, or qualification result. Each lane uses its own service for its final suite; Composition’s final full suite runs on main; App owns the P2/P3 execution and verdicts. The build must supply the final source SHAs, `origin/main` bases, integration trees, live-tip checks, patch/bundle verification, ZIP identity, and receipt paths. The fresh-upstream packaging-only requirements at App `d11417a59` (including the `WelcomeConnection.test.tsx` overlap) and Agent `08e6b90511` (including the installer service/test overlap) remain in scope; after applying that fresh-upstream result, run the full App suite and Agent installer service/tests. None is invented in this draft.

The D87 coverage audit is source evidence only: its 24 retained selectors plus one separate checkout case are mapped with zero current promised capability gaps, while the other six checkout cases remain live. It does not promote D87 coverage to functional PASS or promote the historical P4 result to a current 45-second PASS.
fake-runtime contract: retired-write check now uses POST, because GET became a valid read

Historical bounded evidence may be consulted only at its recorded scope. For example, the historical P1 material is [the retained P1 actual-cause report](design/app-A2-P1-17985-actual-cause-sol-2017.md), P4 material is [the retained integrated P4 symbol report](design/agent-F-P4-symbol-integrated-0023.md), and P5 material is [the retained App P4/P5 registration report](design/app-F-P4-P5-registration-cumulative-0838.md). These links do not establish final-tuple proof or a final GO.

## Known gaps and deferred scope

Under D54a, a failing node may be listed as a known gap only with evidence for exactly one category: environment/setup, upstream-identical/pre-existing behavior, deliberate D52 deprecation of dead or dormant scope with its caller proof, or owner-deferred scope. A regression caused by this integration is fixed or reverted, regardless of whether it is core. Tests of live behavior remain unchanged and visibly failing until fixed; no refusal is encoded as a passing replacement expectation.

Under D62, Runtime does not prove a v2 producer's native coverage is complete at submit (Sol1422's 8 omission packets); such commits fail closed at fork/inverse use. This is the existing Runtime deletion-ledger row D62 ([`design/deletion-ledger.runtime.md`](design/deletion-ledger.runtime.md)), with BOARD-HEADER D62 as its decision source. It is post-delivery hardening, not a new final gate PASS.

Rendering/parity remains deferred, including the unified renderer/viewing parity work. Relational timing (anchors and pinned markers), the M5 extension-model rewrite, push updates, proposals/watch, and the repo-structure decision remain deferred. The deferred relay and remote-provider scope stays fail-closed; no new authority backend or provider-child custody path is part of delivery. These deferrals do not add acceptance criteria or extras to P1–P5.

## Per repository

{{REPO_SECTIONS}}

## Gate receipts

{{GATE_RESULTS}}

# D13 installed native preflight (post-install check)

Run this only after a genuine, non-editable installed Agent/Runtime deployment and its real selected tool inputs exist. It is a check, not an installer or input-provisioning command. The current delivery environment does not provide this tuple; D13 is therefore a known, visible environment gap and is not a core-blocking result.

From the Agent source checkout, with the selected installed environment's Python:

```sh
<runtime-environment>/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  tests/packs/video_editing/test_runtime_publication_chain.py::test_d13_installed_native_preflight
```

The selector reads these required, non-empty environment variables. D13 supplies no defaults or optional names:

```text
ASTRID_D13_SOURCE_PROFILE
ASTRID_D13_EXPECTED_BINDINGS
ASTRID_NODE_EXECUTABLE
ASTRID_D13_NODE_SHA256
ASTRID_REMOTION_PROJECT_DIR
ASTRID_D13_REMOTION_LOCK_SHA256
ASTRID_REMOTION_BROWSER_EXECUTABLE
ASTRID_D13_BROWSER_SHA256
ASTRID_FFMPEG_EXECUTABLE
ASTRID_D13_FFMPEG_SHA256
ASTRID_FFPROBE_EXECUTABLE
ASTRID_D13_FFPROBE_SHA256
ASTRID_TEST_NODE_MODULES
```

`ASTRID_D13_EXPECTED_BINDINGS` must name a regular, non-symlink JSON file whose object has exactly these seven non-empty string keys—no missing or extra keys:

```json
{
  "agent_commit": "<full 40-hex Agent commit>",
  "agent_tree": "<full 40-hex Agent tree>",
  "agent_wheel": "<regular non-symlink Agent wheel path>",
  "agent_wheel_sha256": "<64-hex SHA-256>",
  "source_checkout": "<absolute symlink-free installed source root>",
  "source_digest": "<64-hex source_checkout_digest>",
  "runtime_environment": "<absolute symlink-free installed environment>"
}
```

`ASTRID_D13_SOURCE_PROFILE` must be a regular, non-symlink JSON file with exactly this existing four-field carrier (D13 rejects optional Runtime profile fields):

```json
{
  "profile": "astrid",
  "runtime_checkout": "<the same selected installed tree as source_checkout>",
  "source_checkout": "<the source_checkout binding>",
  "runtime_environment": "<the runtime_environment binding>"
}
```

The source and runtime checkout must be the same absolute, symlink-free installed tree; the environment must be an absolute, symlink-free directory containing a regular, non-symlink `bin/python`, and the pytest interpreter must resolve to that interpreter. The installed origin probe must find `host`, `child`, `action`, `client`, `sdk`, `runtime_protocol`, `runtime_protocol.platform`, and `astrid_runtime` wholly inside that selected tree, without source aliases or symlinks. The selected source's `astrid/packs` digest must equal `source_digest`; the wheel, its Git/source archive members, and installed RECORD/package bytes must also agree with the declared commit/tree and wheel hash.

Tool inputs must be genuine regular, non-symlink inputs matching their declared hashes: Node (`ASTRID_NODE_EXECUTABLE` + `ASTRID_D13_NODE_SHA256`); the Remotion project (`ASTRID_REMOTION_PROJECT_DIR`) with hashed `package-lock.json` (`ASTRID_D13_REMOTION_LOCK_SHA256`) and non-empty, regular, non-zero `public/fonts/*.woff2` plus `FONT_PROVENANCE.md`; the browser (`ASTRID_REMOTION_BROWSER_EXECUTABLE` + `ASTRID_D13_BROWSER_SHA256`); ffmpeg (`ASTRID_FFMPEG_EXECUTABLE` + `ASTRID_D13_FFMPEG_SHA256`); and ffprobe (`ASTRID_FFPROBE_EXECUTABLE` + `ASTRID_D13_FFPROBE_SHA256`). `ASTRID_TEST_NODE_MODULES` must be a genuine regular, non-symlink directory. No placeholder paths, fabricated hashes, copied credentials, or unacquired inputs satisfy this check.

The selector itself only performs this preflight and does not open Runtime or native tools. Runtime’s normal consumer separately accepts `--source-manifest` (or the `ASTRID_RUNTIME_SOURCE_MANIFEST` fallback) and loads/validates its source profile; that runtime variable is not a required input to this D13 selector.
