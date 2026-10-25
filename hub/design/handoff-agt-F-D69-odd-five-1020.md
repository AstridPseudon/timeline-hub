# D69 corrected odd-five semantic review

## Scope and result

This is the independent D69 review of exactly immutable odd indexes 61, 83, 107, 21, and 49 from `handoff-agt-F-D69-odd-inventory-return-1005.json`. The prior EVEN review is excluded. The old (`08e6b905...`), captured corrected (`d6294843...`), and current-normal (`d0ecf1d...`) source identities were checked. All five current-normal blobs equal the captured corrected blobs.

Result: four functions preserve their original purpose through faithful or approved replacements. Index 107 has two concrete missing predicates. D68's approved Windows Task Scheduler change restores the exact `<Task`-prefix and no-XML-declaration guards, but the corrected `test_windows_task_settings_and_no_console_executable` drops both. Its parsed Task Scheduler fields and `Hidden` check do not prove that serialization contract. The narrow recommendation is to restore those two assertions in that test; do not change product code.

## Per-function review

### Index 61 — bootstrap inventory identity and restart

Function: `tests/sdk/test_host_bootstrap_source_identity.py:123`, `test_bootstrap_passes_inventory_identity_and_restarts_on_change` (old line 121; current body lines 123-270).

Original assertions, each PASS equivalent:

1. `len(inventory_calls) == 1`: one inventory read during the initial launch. The replacement uses `inventory_reads_per_launch`, which is 1 normally and 2 only when the supported Remotion registry-context read is provisioned, and asserts the exact identity sequence. This preserves the one-launch read purpose while covering the real optional provider read.
2. `len(inventory_calls) == 2`: after changing `inventory.identity` to `inventory-2`, the replacement asserts `inventory_reads_per_launch * 2` and the ordered `inventory-1` then `inventory-2` identities. The restart trigger and identity propagation are stronger, not weakened.
3. `len(inventory_calls) == 3`: after clearing identity/sources/roots, the replacement asserts `inventory_reads_per_launch * 3` and the complete identity sequence ending in `""`. The disabled/invalid inventory restart remains covered.

Decision/caller reference: the D72 SDK restart and persistence review found the exact bootstrap restart path unchanged and passed the restart/no-write controls. The current production path is the real Agent provider/bootstrap path; the added source shape (`sources=(SimpleNamespace(pack_root=managed),)`) reflects that provider rather than changing the behavior under test. No additive change is needed.

### Index 83 — parent-config conflict and force

Function: `tests/sdk/test_timeline_store_fixes.py:97`, `test_publish_merge_flags_a_parent_config_key_changed_differently_and_force_wins` (old line 94; current body lines 97-114).

Original assertions:

1. `any("theme_overrides (parent-config)" in line for line in conflicts)`: APPROVED REPLACEMENT. G5 retires the internal `store.three_way` helper and the old helper-level conflict list. The current supported local-draft route has head and candidate change the same parent config independently, asserts `TimelineEditError` with the `parent` collision, and then proves the stored head remains fps 24. That is the same collision/no-write purpose at the supported API boundary.
2. `forced[...theme_overrides] == fps60`: PASS equivalent for the approved local-draft exception. `candidate.save(force=True)` writes the candidate and the subsequent load proves fps 60.
3. `forced_conflicts`: APPROVED REPLACEMENT. The retired helper exposed a conflict list even on force; the supported `Checkout.save(force=True)` contract is a local working-copy override, so the replacement proves refusal without force, preservation of the head, then the explicit local override. It must not be read as Runtime publication force behavior.

Decision/caller reference: C0/G5 require the registered `commitTimeline`/real Agent provider for Runtime publication and do not permit a publication force-conflict option. D72 explicitly records `Checkout.save(force=True)` as the retained local-draft exception and publication force as refused. This test is local `Checkout` coverage, not a substitute for Runtime commit conflict coverage; no source change is needed.

### Index 107 — Windows Task Scheduler serialization and settings

Function: `tests/test_installer_platforms.py:106`, `test_windows_task_settings_and_no_console_executable` (old line 106; current body lines 106-137).

Original assertions:

1. `xml.startswith('<Task ')`: FAIL. This checks the exact PowerShell `-Xml` string shape required by D68. The corrected test parses `service.render(...)` and checks Task Scheduler fields, but it does not assert that the serialized string begins with the Task element. Parsed-field coverage is not semantic equivalence for this input-format guard.
2. `'<?xml' not in xml`: FAIL. D68's approved product/test decision explains that `Register-ScheduledTask -Xml` receives a PowerShell string and rejects an encoding declaration. The current corrected test no longer checks this contract. The current service source in the reviewed normal source still emits the declaration, so this omission is concrete, not merely receipt uncertainty.
3. `'Hidden' not in xml`: PASS equivalent. The current test performs the same `Hidden` exclusion against the rendered XML string; the changed local variable does not alter the asserted purpose.

Narrow additive recommendation: restore exactly `xml = service.render('win32', version, data, log)` followed by `assert xml.startswith('<Task ')` and `assert '<?xml' not in xml` in this function, as in D68. Do not use the parsed XML snapshot or fields as a replacement for these guards, and do not alter unrelated settings assertions. The separate D108 Windows registration smoke test also retains these exact guards; it is not this function and is not being reviewed as an additional index.

### Index 21 — native renderer window semantics

Function: `tests/packs/rendering/test_live_scene_composition.py:25`, `test_service_layered_plan_native_renderer_isolates_and_adjusts_once` (old line 25; current body lines 25-78).

Original assertions:

1. `request['window'] is None`: APPROVED REPLACEMENT. D72's native rendering decision retains an absolute `FrameWindow` for native layers; only `supports_windows: false` uses the legacy sliced/null-window path. The current assertion checks the exact serialized native window twice, and the test then runs the approved native-to-legacy projection.
2. `(clip['at'], clip['from'], clip['to'], clip['speed'], clip['hold']) == (0,63,65,2,2)`: PASS equivalent. The current test checks the same tuple on the transformed native scene and additionally checks the scene id/app, source-window metadata, materialized config, and input readback. This preserves the frame-coverage purpose while proving the native isolation/adjustment boundary.

Decision/caller reference: D72 FrameWindow review and `agt-F-D69-failures-render-1646` explicitly reject the old native null-window expectation and approve the native absolute-window comparator. No change is needed.

### Index 49 — working-copy status/discard CLI

Function: `tests/packs/timeline/test_verbs_working_copy.py:178`, `test_draft_flow_checkout_edit_status_discard` (old line 174; current body lines 178-214).

Original assertions:

1. Status output contained `next:` plus `publish timelines status t --project P`: APPROVED REPLACEMENT. G5 retires the publish CLI route; the current test constructs and requires the supported `commit` command and asserts it appears in status guidance.
2. `capsys.readouterr().out.startswith('WORKING COPY "main" · 0 clips changed')`: PASS equivalent. The current test stores status and asserts the same prefix, while also checking exact no-change guidance (`show`/`edit`) and the post-edit commit guidance.

Decision/caller reference: G5/D69 retire the old publish command and require the current working-copy/commit flow. The current status test is an offline CLI working-copy test; it does not claim to prove Runtime's registered `commitTimeline` writer. No change is needed.

## Verification and limits

- Static source/blob, body-hash, line-range, AST parse, and `git diff --check` checks passed; see `evidence/static-source-review.md`.
- No tests, typecheck, or lint were run because this brief classifies them N/A for read-only publication review.
- No source, test, generated, registry, product, or body files were changed. The only substantive recommendation is the two-predicate additive restoration for index 107.
- The exact per-predicate inventory records report no pre-indexed receipt for these five rows; verdicts above use the settled G5/D72/D68 decisions and actual caller/source behavior rather than treating that absence as blanket unknown.
