# WC8 current Agent landing

## Result

The WC8 retained-basis slice was forwarded from Agent `56de3c8f6c31020fb7cd67748673cb1df7f6f455` (tree `35c76c6e0c095bbe00b267c2afc3eb3c4820200d`) onto the current Agent hub `3f1c13a47c5c701bf8d2bb963b23c47412eb9f20`. The resolved-tree procedure produced tree `1e9f61e72fdee4775208baa12a531a3da901d850` with no conflicts. The hub was unchanged at the final audit; `/home/user/work/agent` and all hub integration refs still resolve to `3f1c13a47c5c701bf8d2bb963b23c47412eb9f20`.

The resolved source keeps all six WC8 product/test paths byte-identical to the qualified current base. It takes only the hub's two non-overlapping files: `docs/architecture/timeline.md` and `tests/editing_conformance/test_recipe_scalar_commands.py`. Whole WC8 remains OPEN; this landing does not claim deletion of the remaining legacy paths.

## Exact replaced duplicate product lines

The qualified first-duration slice replaced these seven old product lines from the common ancestor `cc37291af12ac6504eb48dd71ea39b9dfdb56d71`:

```text
astrid/packs/timeline/cli.py
    # Connected callers already have the retained NativeSheet basis. Keep the
    # detached path for no-client Main callers until their remaining grammar
    # has a bound command replacement.
    if parsed.native or parsed.client is not None:
    from astrid.sdk.timeline_sheet import apply_sheet
    changes = apply_sheet(tl, Path(parsed.sheet_file).read_text(encoding="utf-8"))

astrid/sdk/timeline_sheet.py
    return "\n".join(out) + "\n"
```

The replacement reads/parses the sheet once, routes eligible connected clip/track sheets through the existing retained NativeSheet path, passes the connected client, and retains the rendered text before returning it. No Runtime schema, DTO, endpoint, source pin, or new writer was added.

## Remaining local and mixed callers

- `astrid/packs/timeline/cli.py:3585-3597` still enters `apply_sheet`; the
  native/connected route is the WC8 entry, while unsupported legacy or mixed
  shapes fall through to the existing local path.
- `astrid/sdk/timeline_sheet.py:833-855` retains `merge_sheet` and
  `_apply_parsed` for the unqualified local/mixed grammar. `on`/`until`, music,
  looks, sound-window, cut/line creation, omissions, rollback, opaque/null,
  absence, and order behavior remain local and covered by the existing tests.
- `astrid/sdk/timeline/checkout.py:151-175` remains the local draft save seam;
  only a retained pending WC8 sheet is handed to NativeSheet before local draft
  history is retired. `astrid/packs/timeline/cli.py:2983`'s separate
  `Checkout.publish` consumer remains outside this slice.
- The `publish_bundle` occurrence in
  `tests/sdk/test_timeline_checkout_history_boundaries.py:69-81` is a test
  stub, not a production caller.

## Qualified first-duration mapping

1. `render_sheet` calls `_retain_sheet` in `astrid/sdk/timeline_sheet.py:130`.
   `_retain_sheet` stores the existing native bundle/basis, verified
   project/timeline and realm/actor scope, original text, stable occurrence/
   clip bindings, and checkout snapshot in the existing outbox `sheet` value.
2. `_stage_sheet` plus `_duration_sheet` recognizes only an existing static
   `am-type` layer's numeric `for` duration. It reconstructs the existing
   `clip.set` from the retained native bundle and refuses unsupported/mixed
   shapes without converting them into a duration-only request.
3. `Checkout.save` uses `_pending_sheet` and the existing NativeSheet/session
   acceptance path. The existing outbox retains the exact pending command,
   in-flight body, retry key, and original basis across reload; same-row
   conflicts keep the local draft, while disjoint edits use existing rebase
   and guarded inverse behavior.
4. The corrected historical fixture keeps the detached occurrence's canonical
   `track: picture` in both occurrence and placement, and aggregates current
   provider/ownership/source/closure preflight failures. The separate central
   three-new-node live result `27413` is PASS (3/9.64s) on tree `35c76c6e0c0`+
   compatible Runtime b92 and normal published95 client. The prior `2321` and
   `6260` setup failures remain historical failures, not rerun or relabeled.

## Preservation audit

- Six WC8 paths equal both the current base and resolved tree. Their exact
  hashes are recorded in the worker's DetailedReport.
- Runtime lock/published tuple files are unchanged: `runtime.lock.json`,
  `artifacts.json`, `remotion/package.json`, and `remotion/package-lock.json`.
  The lock still names source commit `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`
  and producer `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`.
  Composition 0.0.13 tarball bytes remain SHA-256
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
- No management files, pins, generated artifacts, or shared ledgers were
  modified. Only the two intended upstream files are dirty relative to the
  current base before the harness creates the true two-parent commit.

## Evidence

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/sdk/test_timeline_sheet.py \
  tests/sdk/test_timeline_sheet_native.py \
  tests/packs/timeline/test_cli_native_sheet.py \
  tests/packs/timeline/test_verbs_working_copy.py \
  tests/sdk/test_timeline_checkout_history_boundaries.py
142 passed in 22.51s

git diff --check
PASS

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_structure_baseline
Structure violations: current=13 new=0 fixed=0

AST parsing of 10 changed/neighbor Python paths and Ruff comparison against
the current base source paths: PASS; no new Ruff findings.
```

No full, browser, renderer, install, or duplicate live-socket suite was run.
