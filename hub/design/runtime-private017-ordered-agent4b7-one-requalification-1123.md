# Runtime PRIVATE017 ordered Agent4b7 one-node requalification

Date: 2026-10-21 UTC

## Result

PASS. The original ordered project-data remove/restart/exact-retry/inverse/redo
proof passed once on the reviewed Agent alias correction and unchanged Runtime
42a product/artifacts.

- Agent source: commit `4b7a27127fb9b642be8ad118e6aa663bd7761611`, tree
  `a6126ed13a7b4dad8124894ebced1cf1b5977d5f`, clean checkout
  `/home/user/work/wt/agt-pin-4b7a2712`.
- Runtime source: commit `d6534421043386548a0c41a8c2a688dd072d0562`, tree
  `ab5a6548c8d158e1952961cc681af737ff211ce0`, clean assigned worktree.
- Runtime42a reference: commit `42a7203f49bb89f299ec854cfbf2b1444e815a7c`,
  tree `1f220b3d3a27e8eb061b15c944bad784c8fdb82e`.
- Test file SHA-256:
  `tests/test_timeline_owned_reference_integration.py` =
  `28583b4adda23d464207a43c71b3f134ff960363050908b51187fab646705b13`.

## Exact central evidence

Result ID:
`rt-m2-ordered-agent4b7-one-requalification-1123-private017-agent4b7-integration-1021112600-9900`

Exact command:

```text
env ASTRID_RUNTIME_CHECKOUT="$PWD" ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-4b7a2712 PYTHONPATH="$PWD:/home/user/work/wt/agt-pin-4b7a2712" PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/test_timeline_owned_reference_integration.py::test_actual_provider_removes_ordered_project_data_and_retries_inverse_redo
```

Result: `1 passed in 1.37s`, exit `0`.

This single test retained and passed the existing assertions for null/presence,
opaque values and namespace order; source-created namespace pruning; durable
serialized readback; restart exact original key/body/receipt retry without
provider re-execution or duplicate history/storage; changed-body refusal; and
exact inverse/redo/history/full-closure restoration.

## Preflight and source controls

- Agent checkout was requested at the exact commit and verified clean at the
  required commit/tree.
- Agent diff from approved `6c1989adf723ae0ea0f4205c1cc8f1c0e4b22e79` was
  exactly `astrid/sdk/timeline/_command_state.py`, the two existing regression
  edits in `tests/editing_conformance/test_recipe_m2_project_data.py`, and the
  added `tests/editing_conformance/test_project_data_accepted_inverse.py`.
  The product correction is the reviewed one-line
  `copy.deepcopy(state["value"])` ordered-state assignment.
- Runtime `git diff 42a7203f49bb89f299ec854cfbf2b1444e815a7c`, excluding the
  existing proof file, was empty. Runtime worktree status remained clean after
  the run; no Runtime product, schema, client, artifact, lock, pin, or test
  file was edited.
- Agent protected-path delta from 6c was empty for normal17 locks, all15
  consumer/client bytes, all76 producer/artifact bytes, and schemaed5. Current
  protected hashes included `artifacts.json`
  `6aa137e78b47112fdd1a9406592e288067c2997c725e748e81f53d5a560e156e`,
  `package-lock.json`
  `6e20180e88e99b7ddfec3bbb11cd0fb99c4c1d3344017cda7a90231d3396b1c9`, and
  `runtime.lock.json`
  `a9046ae72a4ee1ff9cb7e8062f301d599803f826eb6f2dbb025e7cc5b1d27a6c`.
- Astrid imported from `/home/user/work/wt/agt-pin-4b7a2712`; the loaded
  provider was `astrid.sdk.timeline.commit.RuntimeCommitService`.
  Existing dependency versions were pytest 9.0.2, jsonschema 4.26.0,
  referencing 0.37.0, and filelock 3.32.4.
- Positive collection command collected exactly 1 test. `--setup-plan`
  resolved `tmp_path`, `film`, `monkeypatch`, `astrid_importable`, and
  `agent` and completed without running the body.
- Shared dependency realpaths were `/home/user/work/venv-agent` and
  `/home/user/work/app/node_modules`; neither was modified. Disk floor check
  reported 10,779,060 KiB available after the run.

An initial request was mistakenly targeted at `integration:runtime`, which did
not contain the proof file and exited 4 before collection (`no tests ran`). It
was withdrawn from the central cache; the authorized worker-targeted request
above was the only body execution. No retry or second body run was made.

## Limits

This is direct private Runtime service/provider evidence only. No RT03 replay,
old44/186 node, other materialization, HTTP/native HTTP, browser, renderer,
full suite, install, generation, pin regeneration, public adoption, or caller
activation was run. No Runtime persistence/schema defect was observed; the
reviewed Agent alias correction is the operative fix.
