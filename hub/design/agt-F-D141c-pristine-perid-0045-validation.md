# D141c pristine per-ID extraction validation

Result: finite evidence packet PASS for extraction/custody; this is not behavior PASS, REG classification, or ship credit.

- Input XML: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141b-plain-command-2358/run-pristine-comparator/pristine-comparator.xml`; SHA-256 `ceeb66095a1e00929da0007639dd3d7c8267126b4541c0da2c86011dab63009a` (required `ceeb66095a1e00929da0007639dd3d7c8267126b4541c0da2c86011dab63009a`).
- Parsed XML testcase elements: 3082; concrete PASS: 3077; FAIL: 4; ERROR: 1; SKIP: 0.
- Retained pytest summary contributes 173 PASS subtests. No unique subtest selectors are retained, so no synthetic IDs were fabricated.
- Accounting check: 3255 total = 3082 XML testcase elements + 173 subtests; 3250 PASS = 3077 concrete PASS + 173 subtest PASS; 5 non-pass = 4 FAIL + 1 ERROR.
- Duplicate `(classname, name)` IDs: 0. Five bad IDs match the retained XML exactly and are listed in `bad-nodes.json`.
- Full node IDs are mapped mechanically from XML `classname` to `tests/...py` plus XML `name`; no mapping ambiguity exists for the 3082 concrete records. The 173 subtests are explicitly unresolved at selector level.
- Source-before/source-after witnesses are byte-identical and clean for all four actual pristine repositories. Interpreter and version are retained from actual run bytes.
- Body/monitor exits and disk minimum are retained from actual bytes. Central service `log.txt` is empty by design of the wrapper; authored raw stdout is present and hashed separately.
- Direct source mapping checks were read-only: retained source lines map the timeout to `astrid/sdk/generation_publication.py:280`, the Remotion generated-registry assertion to `tests/packs/rendering/test_render_export_task_adapter.py:271`, the render executor import to `astrid/packs/rendering/actions/render/run.py:9` / `astrid/core/execution/persistent_supervisor.py:17`, and the publication import to `astrid/packs/rendering/actions/assemble_timeline/run.py:29` / `astrid/core/foundation/atomic_io.py:16`; the live-scene selector is retained at `tests/packs/rendering/test_live_scene_composition.py:259` but its setup frame is not retained. No product imports, test collection, tests, or reruns were performed by this worker.
- Four environment-type nodes are returned as rerun-required Farm inputs. The timeout node remains UNKNOWN. No node is labeled pristine behavior FAIL, preexisting, REG, or zero REG.
