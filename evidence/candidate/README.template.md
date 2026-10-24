# Timeline v2.1 delivery, {{UTC}}

This ZIP is a delivery candidate for the `tl/integration` branch of each Timeline repository: agent, runtime, app, and composition. Each repository is carried in two forms: a git bundle of its integration history and one binary-capable patch series based on the pinned `origin/main` shown below. Nothing in this candidate has been pushed, and this candidate is not a release receipt. The final build must perform one live-upstream refresh per repository and record the resulting identities before delivery.

The patch series is based on the pinned `origin/main` commit and has the `tl/integration` tree. Its commit message lists the merged commits, one per line. Per-commit history is carried by the bundle.

The patch route is intentionally linearized: `git am` creates a synthetic commit, so its commit ID is not the source integration commit. The tree ID is the delivery identity. Do not report the synthetic patch commit as a producer or publication identity.

At build time, the patch series is applied with `git am` to a fresh repository holding only the pinned `origin/main`, and the resulting tree is compared with the immutable `tl/integration` tree. Every bundle is checked with `git bundle verify`, fetched, and compared with that same tree. The generated per-repository sections below are authoritative for the build that produced the README; all final SHA, tree, and live-tip values remain pending until that build supplies them.

## Contents

- `README.md`: this file.
- `bundles/<repo>.bundle`: git bundles of `tl/integration`. A ranged bundle holds only commits after `origin/main` and needs `origin/main` present. A full bundle holds all history and clones on its own.
- `patches/<repo>/*.patch`: the binary-capable linearized patch series from the pinned `origin/main` tree to `tl/integration`.
- `SHA256SUMS`: checksums of every other file in this ZIP.

## Delivery status

**PENDING.** This draft deliberately contains no final acceptance receipt, ZIP identity, source pin, tree identity, or live-main refresh result. The delivery owner must install the final receipts before release.

The source contract is [`contract/commit-v2.md`](contract/commit-v2.md). Runtime is the only writer. App, Agent, CLI, Python, scripts, and sheets use the v2 commit door; there is no document-overwrite route, TypeScript executor, or force-conflict option. Existing permission refusals remain stopped. This candidate adds no trust backend and does not authorize Farm or schema-source access.

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
- a nonempty `commands` array, `label`, and `steps` array;
- each step’s `id`, `label`, `intent`, `tags`, `command_ordinals`, `patch`, and optional `reads`;
- `merge` (`fields` or `atomic`), request `reads`, `dry_run`, `source`, `rationale`, and `group_id`;
- the required idempotency key, supplied as `Idempotency-Key`.

Commands execute as one transaction. They may use registered semantic commands or `doc.patch`; `doc.patch` is id-addressed, carries previous values, preserves ordered-list rules, and records authoritative effects. A patch request without declared reads is treated conservatively as atomic over the touched scope. The accepted record, not caller-authored claims, supplies the final step patches and dependencies.

Successful `accepted` and `merged` replies expose the canonical document and the complete receipt, including `records`, `steps`, `dependencies`, `bindings`, `effects`, `history`, `actor`, and `undo` data. `merged` identifies the actual landing head; it is not an old publication label. A `dry_run` success is `preview`, has `would_status`, and has a null `receipt`; it does not reserve a key or accept a write.

`conflict` and `invalid` replies are structured. Their details include `code`, `path`, `hint`, `current`, and `suggested_command` (with the appropriate base/conflict information where applicable). A conflict is not converted into invalid-base prose, and an invalid document is not reported as a successful merge. Exact retries return the original durable reply without another history entry.

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

F-final is also **PENDING**. The Runtime manager runs the existing builder on main after one final live-main refresh per repository (D51), using fresh upstream clones and the final integrated tuple. Each lane uses its own service for its final suite; Composition’s final full suite runs on main; App owns the P2/P3 execution and verdicts. The build must supply the final source SHAs, `origin/main` bases, integration trees, live-tip checks, patch/bundle verification, ZIP identity, and receipt paths. None is invented in this draft.

Historical bounded evidence may be consulted only at its recorded scope. For example, the historical P1 material is [the retained P1 actual-cause report](design/app-A2-P1-17985-actual-cause-sol-2017.md), P4 material is [the retained integrated P4 symbol report](design/agent-F-P4-symbol-integrated-0023.md), and P5 material is [the retained App P4/P5 registration report](design/app-F-P4-P5-registration-cumulative-0838.md). These links do not establish final-tuple proof or a final GO.

## Known gaps and deferred scope

Under D54a, a failing node may be listed as a known gap only with evidence for exactly one category: environment/setup, upstream-identical/pre-existing behavior, deliberate D52 deprecation of dead or dormant scope with its caller proof, or owner-deferred scope. A regression caused by this integration is fixed or reverted, regardless of whether it is core. Tests of live behavior remain unchanged and visibly failing until fixed; no refusal is encoded as a passing replacement expectation.

Rendering/parity remains deferred, including the unified renderer/viewing parity work. Relational timing (anchors and pinned markers), the M5 extension-model rewrite, push updates, proposals/watch, and the repo-structure decision remain deferred. The deferred relay and remote-provider scope stays fail-closed; no new authority backend or provider-child custody path is part of delivery. These deferrals do not add acceptance criteria or extras to P1–P5.

## Per repository

{{REPO_SECTIONS}}

## Gate receipts

{{GATE_RESULTS}}
