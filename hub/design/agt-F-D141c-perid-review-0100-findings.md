# D141c independent evidence review

Result: `PASS_EVIDENCE` for packet integrity, custody, accounting, and XML correspondence. This is not a behavior PASS, REG/non-REG verdict, or ship credit.

## Verified

- The seven published design originals are byte-identical to the seven worker originals. Their published SHA-256 values are retained in `review.json`.
- Retained XML is 4,690,547 bytes with SHA-256 `ceeb66095a1e00929da0007639dd3d7c8267126b4541c0da2c86011dab63009a`.
- The inventory has exactly 3,255 records: 3,082 concrete XML testcase records plus 173 aggregate PASS records. Accounting is `3255 = 3082 + 173`, with `3250 PASS = 3077 concrete PASS + 173 aggregate PASS` and five concrete non-PASS outcomes (`4 FAIL + 1 ERROR`).
- All 3,082 concrete IDs are unique. Set membership, `classname`, `name`, `time`, original testcase attributes, observed status, and serialized testcase hashes match the retained XML field-by-field. All five bad-node IDs and statuses match XML.
- The four packet-level source authorities (Agent, Runtime, App, Composition) are recorded clean before and after. The actual pristine source identity is explicitly distinct from the frozen Agent cut `28e56cacb42d3da85b02e5b3543895b44f3d0f70`.
- The retained custody hashes, body/monitor exits, interpreter identity, and disk floor match the source manifest. The empty central service log is explained by wrapper redirection; retained raw stdout is separately hashed.

## Finite findings and limits

1. The published file is a full 3,255-record status inventory, not a full 3,255-unique-ID table. The 173 aggregate PASS records have `node_id: null` and ordinal-only accounting because no unique selectors are retained. This is the correct explicit missing identity; no IDs were fabricated.
2. XML supplies testcase attributes and result status/type. `classification`, `reg_status`, `ship_credit`, `safe_error_class`, environment labels, first-frame annotations, and aggregate ordinals are packet-derived or custody fields, not XML fields. The review checks that sanitization preserves the XML-observed result; it does not attribute those fields to XML.
3. The five concrete bad outcomes are:

   | ID | XML status | safe class | environment label | first frame where retained |
   |---|---|---|---|---|
   | `tests/sdk/test_generation_publication_adapter.py::test_compose_is_deterministic_and_uses_real_capability_outputs` | FAIL | `timeout` | UNKNOWN | `astrid/sdk/generation_publication.py:280 (_capability_digest)` |
   | `tests/packs/rendering/test_live_scene_composition.py::test_real_render_scene_window_audio_and_overlay` | ERROR | `remotion_site_registry_absent` | ENVIRONMENT_SITE_REGISTRY_ABSENCE | pytest setup precondition; no setup frame retained |
   | `tests/packs/rendering/test_render_export_task_adapter.py::test_render_export_adapter_writes_real_mp4_and_is_callable` | FAIL | `runtime_publication_import_missing` | ENVIRONMENT_IMPORT_RUNTIME_PUBLICATION | `astrid/packs/rendering/actions/render/run.py:9` |
   | `tests/packs/rendering/test_render_export_task_adapter.py::test_forced_caption_uses_server_owned_executable_routing_and_isolation` | FAIL | `remotion_generated_registry_absent` | ENVIRONMENT_SITE_REGISTRY_ABSENCE | `tests/packs/rendering/test_render_export_task_adapter.py:271` |
   | `tests/packs/video_editing/test_runtime_publication_chain.py::test_daemon_backed_host_executes_authoring_and_final_render` | FAIL | `runtime_publication_import_missing` | ENVIRONMENT_IMPORT_RUNTIME_PUBLICATION | `astrid/packs/rendering/actions/assemble_timeline/run.py:29` |

4. Under the later MAIN 00:52:33 ruling, `env-rerun.json` is a conditional candidate list, not an unconditional four-job gate. Only environment-type pristine nodes that also fail the Farm cut core receive matching-environment pristine reruns. The four environment nodes remain raw evidence pending that intersection; the timeout remains UNKNOWN and is not an Agent rerun candidate. No REG/non-REG classification is made here.
5. No raw stdout, stderr, traceback, XML, or private payload is republished in this review.

## Unchanged scope

No product, test, generated file, pin, kit, schema, source, guard, or original evidence file was edited. No pytest, product import, collection, provider investigation, child, environment investigation, or rerun was performed.
