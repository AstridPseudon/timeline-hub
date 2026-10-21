# Document mirror-key delta review

## Verdict

**APPROVE** the actual repair at commit `e51732a644f632830a06499807b4d98a4a7bc163`,
tree `f157ce2451296d8de1ba59a8567a46f4e112bd75`.

This is the bounded repair requested for the previously rejected `f137c06a5`
candidate-only mirror-key case. It adds a `reject_candidate_only` check only to
the `parent.config.clips` mirror comparison. The primary authored rows and
the existing derived-result comparison remain unchanged.

## Delta reviewed

On the prior rejected `f137c06a58a6a957af5fc0836ba690bff74eeb29` tree
`c5feb99cff850d5b5a50843294493efd7196bdf2`, this input was incorrectly
accepted as one `clip.move` while retaining an authored mirror-only `app` key:

```python
work["parent"]["clips"][0]["at"] = 4
work["parent"]["config"]["clips"][0]["at"] = 4
work["parent"]["config"]["clips"][0]["app"] = {
    "astrid": {"fixed_start": True, "for": 1.0}
}
```

The repair rejects any explicit candidate-only key in the config mirror row,
before comparing it with the native result. The refusal is atomic: the
candidate draft and pinned base remain unchanged. This does not reject
native-derived keys that are absent from both authored inputs: the existing
identity-map/native-move positive still accepts the derived primary-row
`app` field produced by `clip.move`.

## Evidence

The requested nearest-control command was run directly on the repaired tree:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/timeline/test_authoring_feedback.py -k \
  'refuses_candidate_only_mirror_field_matching_move_result or \
   accepts_identity_map_spelling_and_new_native_move_fields or \
   emits_native_command_for_explicit_parent_timing or \
   preserves_native_writes_and_literal_script_slots or \
   clears_present_null_hold_without_zero_command or \
   clears_a_present_nonnull_param'
```

Result: **9 passed, 52 deselected**.

That run covers:

- the exact candidate-only mirror counterexample: refusal plus draft/base
  preservation;
- identity-map spelling and native move, including the derived `app` field
  absent from both authored rows;
- ordinary native parent move;
- native trim;
- present-null hold clear, both parent and child;
- ordinary parameter clear.

Disposition of raw presence/value requests is closed for this slice: the
candidate-only mirror add is atomically refused; retained mirror-only
remove/null and unsupported null/absence evidence is atomically refused;
native-derived fields absent from both authored rows are represented by the
native result; and supported trim, hold-clear, and parameter-clear requests
are represented by their native commands.

The retained prior closure evidence in
`design/agent-review-document-complete-presence-final-0702.md` records all
twelve original presence counterexamples refusing atomically on `f137`, and
the current repair changes only the additional mirror-key boundary. I did not
broad-replay those twelve cases or the historical 255-test surface.

Additional checks:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-agent/bin/python -m ruff check \
  astrid/sdk/timeline/document_diff.py tests/timeline/test_authoring_feedback.py
```

Result: **All checks passed**.

```text
git diff --check f137c06a5..e51732a64 -- \
  astrid/sdk/timeline/document_diff.py tests/timeline/test_authoring_feedback.py
```

Result: **passed**.

## Exact blobs

- Commit: `e51732a644f632830a06499807b4d98a4a7bc163`
- Tree: `f157ce2451296d8de1ba59a8567a46f4e112bd75`
- Product source blob, `astrid/sdk/timeline/document_diff.py`:
  `e61de49fc6ccbcf66ab47fb41f254c47ab8110ba`
- Test blob, `tests/timeline/test_authoring_feedback.py`:
  `679526471cc840bdcff3947f760d5ded4d9ea899`
- Compared rejected commit: `f137c06a58a6a957af5fc0836ba690bff74eeb29`
- Compared rejected tree: `c5feb99cff850d5b5a50843294493efd7196bdf2`

## Limits

No source edits were made. No HTTP, Runtime-door, browser, or full-suite
test was run, as required. The verdict is for this bounded Agent adapter
delta and its nearest controls; it is not a transport or end-to-end
qualification.
