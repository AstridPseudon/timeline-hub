# WC8 font/color current-preserving Agent packet

## Exact base, parents, and source trees

- HOME base: `hub/timeline/agent/tl/integration` at
  `f777b04d1c90c189ee2565a0d68060692cb24287`; base tree
  `e384e32b9ac9dbdb29e44655012eaca32a840215`.
- The harness must use the supplied second parent
  `fd90a99575d795869faa6cbc5573613783c79664`; no local merge, rebase,
  checkout, or `.git` write was performed.
- Qualified product source: `5ad4b7c26871c18ba01449a6d3c4d5bde6aa9a2b`.
  Its product source is byte-identical in `fd90`; the frozen qualified source
  tree for the HTTP proof is `070a75eed14a85465269289e143fd5b26cbaab31`.
- Qualified corrected refusal tests: `fd90a99575d795869faa6cbc5573613783c79664`.
- Qualified actual HTTP proof node: `6e19af6a61a7b2843c6859994262602713a1c208`.
- The frozen proof’s actual source tree is `070a75eed14a85465269289e143fd5b26cbaab31`;
  the new central snapshot qualified the current packet at tree
  `aff1d8ad167b9503b43b48fbda11aadd2fcaef54`.

## Final authorized blobs and qualified origin

| Path | Final blob | Qualified origin and preservation |
| --- | --- | --- |
| `astrid/sdk/timeline_sheet.py` | `eec3f1f6c49bfd95139a5800b8e60d1bfd09d9ca` | The retained `size/font/color` translator hunk is from product `5ad4`; HOME’s current transcript/source-input, word-anchor, authored-bundle, and related current behavior remains from base blob `901bc69038b182d0d34d7d8c0bf5213af65af6d5`. The final blob is therefore intentionally not the stale whole-file `5ad` blob `4b4bf67d3e62806128b1ea512e59e0fe9a6616c5`. |
| `tests/sdk/test_timeline_sheet_native.py` | `69edb1e781aea40ed1024cf4375ecb4544f4aa6b` | Byte-identical to corrected approved `fd90` (`git rev-parse fd90:path` gives the same blob). It includes the existing HOME size assertions plus the font/color cases and corrected refusal boundary. |
| `tests/editing_conformance/test_native_sheet_ordinary_runtime.py` | `04c4ff7e55a2d4d3d7a0ccc29be04916667ab0aa` | Byte-identical to actual proof `6e19` (`git rev-parse 6e19:path` gives the same blob), including the font/color fixture and one new ordinary HTTP node. |

Only those three paths differ from HOME. No schema, generated client, lock,
store, remote, Runtime, or unrelated source/test path changed. Current
transcript, installed-origin, document-adapter, typing, and existing size
packet assertions were retained.

## Live caller

The retained-sheet path is live through `astrid/sdk/timeline/checkout.py`:
`_stage_sheet` and `_pending_sheet` call `_duration_sheet`; the ordinary CLI
caller enters through `_cmd_apply` and `apply_sheet`. The new central node
exercises that `apply_sheet` path through `tl.save`, the normal `/v1`
`clip.set-params` commit, restart, guarded inverse, and redo.

## Evidence

- `git diff --check`: pass.
- Direct compact lane, with shared dependencies read-only:

  ```text
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/sdk/test_timeline_sheet_native.py -k \
  'detached_static_type_string_uses_retained_native_params_command or detached_combined_size_and_type_string_edit_preserves_literal_neighbors or detached_type_string_clear_uses_presence_aware_native_command or detached_mixed_edit_with_supported_font_is_staged or detached_mixed_edit_with_unknown_neighbor_is_not_staged'
  6 passed, 63 deselected in 1.88s
  ```

- Central actual-node run, request/result
  `rt-m2-wc8-font-color-current-forward-0826-rt-wc8-current14-integration-1021082755-12180`:

  ```text
  tests/editing_conformance/test_native_sheet_ordinary_runtime.py::test_current014_detached_font_color_uses_one_native_http_commit_and_guarded_inverse
  1 passed in 4.16s
  ```

The earlier `6e19` HTTP result and the refusal review’s `21`/`12` evidence
were reused as qualified source evidence; they were not replayed here.
The refusal delta review’s final source authority is APPROVE21+12; the earlier
full-source HOLD is not relabeled as an original product approval.

## Whole-WC8-open limitation

This packet intentionally did not run the full WC8 suite, the old size/text/
duration or old HTTP cases, browser/render/install tests, or any full suite.
Only the new direct font/color/refusal/combined lane and the one new actual
HTTP node above are fresh evidence. The manager must keep the whole-WC8-open
limitation visible when submitting the true two-parent commit.
