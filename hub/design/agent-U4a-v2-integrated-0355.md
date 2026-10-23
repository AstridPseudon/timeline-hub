# U4a-v2 integrated proof/readiness handoff

**PASS — exact home integration is ready for the downstream owned checks.**

## Identity

| Item | Exact value |
| --- | --- |
| Home integration / worker commit | `f894c3c9dda25ab03527eeb7f52da5da31d627c1` |
| Home integration / worker tree | `d24f25a65be282a56b3fcd814a8718a3c0587b9b` |
| Independently reviewed consumer commit | `723b94bb94d7f21848364204b4930739dfac6703` |
| Producer commit | `34eac0041b0891e9011966b39bcbd26053fde5bc` |
| Producer tree | `9853574865f25e08284e82ffb26c0bdecaa16a30` |
| Compatible Runtime execution | `ad823e0a0f5be4a7acf1d3006df6f794709da63d` / `33904550800ee3e2fa34fe0b13c26754b46c7fdc` |

`f894c3c9…` and `723b94bb…` are ancestors as required; the home integration
branch and this worker have the exact `d24f25a6…` tree.

## Readiness checks

- `python3 scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004` — PASS.
- `python3 scripts/artifact_manifest.py --check` — PASS.
- All 15 lock mappings — PASS; every consumer equals its producer file and manifest hash.
- Canonical `edit-command.schema.json` — exact approved `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`.
- Mounted production caller — PASS: `astrid/sdk/workspace_client.py` imports and constructs the official generated `astrid_runtime_client.WorkspaceClient` and delegates `commit_timeline`.
- R2 provider/undo, R3 structured errors/preview, and meta validator seams remain in the integrated tree; the adoption merge changed only the reviewed client/lock/fixture files.
- Full v2 request/reply fields remain represented by the generated DTOs and runtime response validation, including historical `rebased`, new `merged`, receipts, canonical document/head/digests, records/effects/steps/dependencies/history/undo_steps, conflict/invalid details, and preview `would_status`.

## Evidence

Reused from independent 0353 on the exact reviewed tree: Agent `46 passed,
39 deselected`; Runtime envelope `48 passed, 27 deselected`; Ruff `2151/2151`;
private mypy `1915/1915`. The six requested public-client probes were rerun:
four positive accepted/merged commit/preview cases and two negative malformed
receipt/missing-preview-status cases all passed.

No native14, Viewing failed54, full, browser, heavy, farm, or Proof-owned
HTTP-body suite was run; those remain owned downstream checks.

The brief’s literal `34e9b568` token is not resolvable in the available refs.
The authoritative producer identity is `34eac0041…`, consistently used by the
lock, manifest, generated client, and independent review.

**Handoff: PASS.**
