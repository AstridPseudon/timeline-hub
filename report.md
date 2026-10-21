# WC8 retained layer omission result

## Result

Blocked without a product change. The requested detached literal layer row is
not representable by the published `clip.delete` operation: the retained
fragment binds a cut layer to an occurrence-owned identity, while `clip.delete`
v1 accepts only a `parent/clip:<id>` identity. I did not synthesize a parent
owner/source, broaden the operation, or replace the existing detached writer.

## Evidence

- `astrid/sdk/timeline/checkout.py:551-560` retains the native bundle and
  publication basis, but binds each single-occurrence cut layer as
  `occurrence:<occurrence_id>/clip:<clip_id>`.
- `astrid/sdk/timeline_sheet.py:597-599` documents the current boundary:
  omitted parent clip rows use `clip.delete`; occurrence-row omissions remain
  refused by `NativeSheet.preview` at lines 725-733.
- `astrid/sdk/timeline/_delete_commands.py:54-57` rejects every non-parent
  identity with `unsupported_ownership`; `capture_clip_delete` is explicitly
  documented as a parent removal at `astrid/sdk/timeline/capture.py:264-267`.
- The focused carrier probe produced:

  ```text
  NativeSheet omission: only an addressed parent clip row may be omitted: occurrence:occ-1/clip:card
  clip.delete capture: clip.delete v1 requires one parent clip identity [unsupported_ownership]
  ```

The existing local-only detached omission behavior remains a Main positive.
When a retained native artifact is present, `_duration_sheet` rejects the
changed row set before native preview; mapping that row to a fabricated parent
row would violate the task boundary. This worker leaves both behaviors
unchanged.

## Tests

Successful targeted command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/sdk/test_timeline_sheet_native.py \
  tests/packs/timeline/test_cli_native_sheet.py \
  tests/sdk/test_timeline_sheet.py \
  tests/packs/timeline/test_verbs_working_copy.py
```

Result: **147 passed in 24.36s**.

`git diff --check` was also run after preparing this report and passed. No
Runtime HTTP, actual/full/browser/render/install/socket suite, or prior actual
proof replay was run.

## Next step

Revisit when an existing authoring entrypoint supplies a published carrier and
operation for occurrence-owned clip deletion. Until then, retain the current
legacy omission path and the existing NativeSheet parent-only delete path.
