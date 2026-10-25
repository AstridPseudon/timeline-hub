# D108/D69 corrected ODD inventory

Status: **SOURCE_ONLY_CORRECTED_ODD_MEMBERSHIP_INVENTORY**. No semantic verdict is made.

Authoritative original membership SHA-256: `1bd9b4c08c1ade951f28983172c6e76205401c93af5943abc2c3d924ddb6e7d0`. Master handoff SHA-256: `af04bc82117976029346a9a6646b956ab16390627a9d764be6a30ef668ee0411`. Agent old/captured/current trees: `2694ae8d2709526b40fa037bda8b159cf412769d`, `6aeae30f0892a424104a4348bca6fd74ba1315d6`, `e9845f8cf5a6ba80210336d0e2452f80a0918762`.

The immutable sorted 129 records use `enumerate(index) % 2 == 1`: indexes 1,3,...,127. Before exclusions: **64 functions, 67 removed, 178 added**. The exact earlier-reviewed 15-function set contributes **9 odd** and 6 even functions. Exclude only those 9 odd functions, plus the two exact approved original-odd D72 rows (one removed and one added at index 19).

Corrected residual: **55 functions, 31 removed, 55 added**, with 24 functions carrying assertion deltas and 31 zero-delta membership functions. Conservation: `67 = 35 + 1 + 31`; `178 = 122 + 1 + 55`; union `129/113/287 = 64/67/178 odd + 65/46/109 even`.

The prior residual-odd-0945 artifact selected the even partition. It remains historical failure evidence; its 16 FAIL/50 UNRESOLVED labels are not odd findings.

Next semantic-review subset (removed multiplicity descending):

- index 61: `tests/sdk/test_host_bootstrap_source_identity.py:test_bootstrap_passes_inventory_identity_and_restarts_on_change` — 3 removed / 6 added
- index 83: `tests/sdk/test_timeline_store_fixes.py:test_publish_merge_flags_a_parent_config_key_changed_differently_and_force_wins` — 3 removed / 2 added
- index 107: `tests/test_installer_platforms.py:test_windows_task_settings_and_no_console_executable` — 3 removed / 1 added
- index 21: `tests/packs/rendering/test_live_scene_composition.py:test_service_layered_plan_native_renderer_isolates_and_adjusts_once` — 2 removed / 7 added
- index 49: `tests/packs/timeline/test_verbs_working_copy.py:test_draft_flow_checkout_edit_status_discard` — 2 removed / 4 added

The JSON handoff contains all 64 odd function paths/names, source blobs/body hashes/ranges, exact predicate fingerprints, multiplicities, and per-row approval status. Current source blobs match captured-new for 64/64. JSON/hash/source checks pass; tests/typecheck/lint are N/A for this read-only task. Historical XML SHA-256: `005ea787fce46efbba6e5637a6e92ab8e9fb5f83f62e3d48649f0522bf06e2a5`; qualified D72 XML SHA-256: `7c308f7d59512cae0ed0af52a4c99c4f1e64a3b3d4022288e8c4627f4bc53a5f`.
