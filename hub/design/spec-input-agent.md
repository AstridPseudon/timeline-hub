# Agent spec input (read-only answers) — agent lead, 2026-10-22 ~16:50Z
Sources: agent repo at tl/integration a086cc6db (read directly), manager STATUS, design/agent-area-size-and-ledger-audit-0905.md. Nothing was executed; no codex/manager/worker was run. Line numbers for the writers come from the 09:05 audit and may have drifted.

## (1) document_diff_to_commands: does it enforce "replay == candidate, else refuse"?
Partly. astrid/sdk/timeline/document_diff.py:345-482 replays onto a deep copy (`working`) and then checks section by section: shot clips (_require_explicit_rows vs working), shot registry and payload (_require_same vs working), parent.clips, parent.config.clips and .tracks vs working. Every field it does NOT translate must equal its base, else it refuses ("held by the document view"). Null-vs-absent is explicit since stopgap ac9a93579 and the complete repair b4762b7c4.
Missing: one final whole-document check, canonical(working) == canonical(candidate), so any field the per-section checks do not enumerate could still differ silently.
Where: immediately before the `return {"commands": ..., "bundle": working}` (~line 480), comparing the same projection the candidate was built from. Size: roughly 20-40 lines of product code plus 4-6 round-trip tests (one per field class: parent, shot clips, registry, payload, config). One Luna worker plus one independent data-safety review. Estimate only; not implemented.

## (2) Remaining whole-document / snapshot writers (route through the generic diff, or what else)
- WC1 authoring_bundle.py publish_authoring_candidate (~:1620): whole-candidate publish; generic diff route only for fields document_diff already translates; occurrence windows/omission wait on a containing future command pin (Runtime SOURCE ACK d9d1). Whole WC1 open.
- WC3 remote.py replace_parent_media (:1278-1503): not a diff case; atomic parent media replace. Needs a native media-replace command (document_diff already uses capture_occurrence_swap_media for same-alias occurrence swaps only). Replacement test: tests/test_timeline_clip_replacement.py.
- WC5 draft_voiceover.py:475 bound.publish: not a diff case; goes through existing text-binding.set + closed legacy_source flag + verified text descriptor (O6 inline migration). Source consequences under independent safety review. Replacement test: tests/packs/video_editing/test_draft_voiceover.py.
- WC7 store.py:257 publish_bundle, publish.py:44: needs per-command native consumers. Done natively: attached move, HOLD, trim, delete, split, connected NativeSheet. Remaining: detached/mixed/unsupported cases and reason/history consumers.
- WC8 store.py three_way/_merge/fetch_bundle, checkout.py:203 (whole=True), packs/timeline/cli.py:2808: whole-doc merge. Duration slice and parameter slice merged; open: occurrence source-window semantics (Runtime sent the gap), mixed/local callers.
- AG02 store.publish_bundle (in progress): no replacing test named; needs native consumer like WC7.
- AG03 sdk/timeline_sheet.py local undo history (_history_dir): not a diff case; needs Runtime history-based undo/inverse; no replacing test named.
- AG-M2-TB01 remote.py:2446 set_text_binding, :2456 rebind, publish.py:173 pin_narration, timeline_document.py:179, shots/cli.py:135: held (design only); text-binding command route; spike test tests/editing_conformance/test_recipe_text_binding_spike.py exists.
- D13 core/execution/generic_host.py:8401 _publish_assembled_timeline -> publish_timeline_render: not a diff case; render publication; Runtime owns the cut after caller disposition (RT07).
Generic diff route is realistic only for rows that are field edits on existing clips/tracks; media rebind, text/voiceover binding, history and render publication each need their own native command.

## (3) Live edit and read-back (CLI prefix `python3 -m astrid timelines`; inferred from cli.py help text, NOT run live)
- Read head: `timelines status <timeline> --project <P> [--text] [--json]`; history: `timelines history <ref> --project <P> [--limit N] [--json]`; edit journal (hash chained): `timelines log <ref> --project <P>`; adjacent-version diffs: `timelines diff <ref> --project <P>`; `timelines show <ref>`.
- Native live edit: `timelines edit <ref> --project <P> --clip <parent/clip:ID | occurrence:ID/clip:ID> --on SECONDS [--dry-run]` (move); `--trim-in/--trim-out/--slip SECONDS` (trim); `timelines undo|redo <ref>`.
- Document route: `python3 -m astrid.packs.rendering.docs.scripts.timeline_document checkout --project <P> --timeline <T> --file F` -> edit JSON -> `check --file F` -> `publish --file F --idempotency-key K` (publish goes through document_diff_to_commands).
- Python: astrid.sdk.timeline (capture_*, execute, commit, journal, document_diff.document_diff_to_commands).

## (4) Re-vendoring Runtime/Composition from integration heads (Agent side)
- runtime.lock.json: {manifest contract/artifacts.json, producer astrid-runtime, producer_version sha256:54205b3e..., source_commit 95bd3c5f6d00 (current pin), 15 vendored files incl. astrid_runtime_client/* and astrid/core/timeline/schema/timeline-config.schema.json}.
- Procedure (scripts/vendor_lock.py): set source_commit to the full Runtime SHA, run `vendor_lock.py update runtime.lock.json --producer <runtime checkout>`, then `check`; tests/test_vendor_lock.py. Also requirements/runtime.lock (pip lock), scripts/smoke_wheel_install.sh and tests/test_installer_wheel.py for the wheel/client install path; test venvs (venv-agent-child*) are built from the Agent wheel per tests/suites.conf.
- Composition: no composition lock found in the Agent repo (git ls-files shows only runtime.lock.json); Agent consumes Composition via the Remotion runtimes (/home/user/work/runtimes/agent-remotion-*), pinned by node lockfiles, not by a vendor lock.
- Size: the lock update is mechanical (script); the cost is the consumer ports and re-qualification when the contract changes (the last pin cycle, private017/018, took many hours). Cannot size without target heads.

## (5) D13 startup-hook preservation (capture.web_page, rendering.sprite_sheet)
Resolved at source level, per STATUS: source 819742732 (23 files, +2085/-99 incl. tests) merged as a086cc6db. HARD independent security APPROVE covers both capture.web_page and rendering.sprite_sheet plus origin, selected interpreter, symlink, generator, credential/network/cache guards; 57 source/custody + 8 host checks passed; outside-path preservation verified. Remaining on Agent side: send Runtime the actual remaining caller count for RT07 (small); six original lifecycle assertions stay required in the targeted replacement; Runtime owns the cut after caller disposition.
