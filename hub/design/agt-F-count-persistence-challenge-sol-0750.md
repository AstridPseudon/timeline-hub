Updated only the five permitted evidence artifacts. Candidate census: **262 closed / 5 open / 267**, derived from **+restart +two-writer −giant**. Preserved 264 unaffected records, all original IDs/phases/tags, prior proofs and contract inventory. Mapping inventory: **122 rows = 121 unique current closures + 1 historical challenged restart**.

Exact remaining open originals:

- `tests/packs/rendering/test_threejs_backend.py::test_threejs_support_rejects_unsupported_timelines_with_clip_reasons`
- `tests/sdk/test_timeline_helper_capture.py::test_cut_nudge_restart_merges_other_cut["second"]`
- `tests/sdk/test_timeline_persistence.py::test_publish_after_a_restart_merges_other_clips_onto_the_moved_head`
- `tests/test_generic_host.py::test_structure_pack_members_survive_harvest_cleanup_and_reopen`
- `tests/test_structure_contracts.py::test_giant_file_inventory_matches_rationale`

Validation passed:

- `python3 "$TMPDIR/validate_count.py"` — membership, delta, ownership/families, preservation, CSV parity, source blobs and ten body/assertion pairs.
- `python3 -m json.tool` on both JSON artifacts.
- `sha256sum -c agent-D32-current-node-reconciliation-H30-corrected.sha256`
- `git diff --check`

No product tests, probes or source execution. Raw Runtime XML is absent locally; independently verified0736 membership/digest is retained explicitly. Future docs repair receives no current credit.

Census SHA: `286047a522d61e57f8c46bb655d63d96bd82fd21e6f597fa72a2e017b2552eb2`

Five-file package SHA: `d1aa34872d19e515861130103f3aa49b1e31b5b170a18ed22fde2893503a92f8`

Commit message and `DONE` created. Next: independent cumulative package review; candidate status remains pending.