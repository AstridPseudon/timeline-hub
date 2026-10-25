# F-D86 / D95 retirement appendix and replacement map

Append-only evidence for the manager-owned `design/deletion-ledger.agent.md`.
The worker does not modify that design file or create a ledger/process file.

## Decision and scope

- D95 source disposition: `legacy-only` for exact actual9211 IDs 99 and 101.
- D95 ruling: current `word_anchors` choices bind an immutable transcript
  document pin; these originals retain the historical `elementRef.binding_id`
  form and must not be migrated by changing their inputs or guards.
- C0 citations: §1 requires the existing `commitTimeline` request/base and
  transactional command path; §2 requires authenticated closure addressing;
  §3 requires conflict/dependency preservation; §4 requires the structured
  invalid reply; §5 preserves guarded inverse/history semantics.
- No broader legacy, D14, or D23 retirement is claimed.
- Functional status of the retired originals is unknown/unverified by this
  source-only worker; they are retired because their exact inputs are legacy,
  not because a runtime behavior pass was established.

## Exact original IDs, source, and hashes

Original source was read from parent `tl/integration` candidate HEAD
`f51844083737a484422bb07a9d6679f489bbcd78`, file
`tests/editing_conformance/test_commit_runtime_text_binding.py`.

- ID 99: `test_rebind_existing_main_descriptor_undo_is_exact`
  - original source lines: 245–261
  - exact source SHA-256: `89fe35961b080093706962b2d3183f6f3adac813038e2b4701154e33a87df094`
  - exact body SHA-256: `1ddf1928857b17b05c1c7528ec09e9886297cd50e4e9463ade82a192f42a9594`

```python
def test_rebind_existing_main_descriptor_undo_is_exact(editing):
    binding = {'kind': 'transcript', 'slot': None}
    pin = put(editing, b'replacement transcript')
    accepted = submit(editing, body(editing, [call(binding, pin)]), 'replace-main-transcript')
    baseline = editing.closures[0]
    original = baseline['shot_revisions'][0]['payload']['text_bindings'][0]
    assert original['mime_type'] == 'text/plain'
    before_bytes = editing.service.object(original['media_id'])[1]
    assert len(before_bytes) == original['byte_size']
    restart(editing)
    undone = submit(editing, body(editing, [inverse(accepted)]), 'undo-main-transcript')
    assert undone['data']['canonical_document'] == baseline
    assert live(editing, binding)['mime_type'] == 'text/plain'
    assert len(editing.selected) == 1
    assert editing.service.object(original['media_id'])[1] == before_bytes
    redone = submit(editing, body(editing, [inverse(undone)]), 'redo-main-transcript')
    assert redone['data']['canonical_document'] == accepted['data']['canonical_document']
```

- ID 101: `test_clear_existing_main_descriptor_and_inverse_are_exact`
  - original source lines: 345–367
  - exact source SHA-256: `481335a01f05363a4460873466a2c6b3ac8efb96185a8528793a28161a5a0a6d`
  - exact body SHA-256: `e574005395ace38751bca03738afd2bba8e87f0880fb0861d8ef3c11322ef22a`

```python
def test_clear_existing_main_descriptor_and_inverse_are_exact(editing):
    from runtime_protocol.errors import NotFoundError

    binding = {'kind': 'transcript', 'slot': None}
    prior = live(editing, binding)
    assert prior['mime_type'] == 'text/plain'
    data = editing.service.object(prior['media_id'])[1]
    assert len(data) == prior['byte_size']
    request = body(editing, [call(binding, clear=True)])
    cleared = submit(editing, request, 'clear-main-transcript')
    original = editing.closures[0]
    assert not editing.service.list_project_shot_text_bindings(editing.project, kind='transcript')['items']
    with pytest.raises(NotFoundError):
        editing.service.get_project_shot_text_binding(editing.project, prior['binding_id'])
    restart(editing)
    assert submit(editing, request, 'clear-main-transcript') == cleared
    restored = submit(editing, body(editing, [inverse(cleared)]), 'undo-clear-main-transcript')
    assert restored['data']['canonical_document'] == original
    assert live(editing, binding)['mime_type'] == 'text/plain'
    assert editing.service.object(prior['media_id'])[1] == data
    assert editing.selected == []
    redone = submit(editing, body(editing, [inverse(restored)]), 'redo-clear-main-transcript')
    assert redone['data']['canonical_document'] == cleared['data']['canonical_document']
```

## Replacement map

| Retired exact ID | Disposition | Current replacement/coverage | Status |
| --- | --- | --- | --- |
| 99, bound-main rebind + exact undo/redo | D95 `legacy-only` | `test_bound_main_descriptor_invalidating_set_and_clear_refuse_without_writes`, parametrized `action='rebind'`; refusal/no-write assertions at lines 263–275 | New assertion body is unverified until the main targeted run; no source behavior claim |
| 101, bound-main clear + exact inverse/retry/redo | D95 `legacy-only` | Same parametrized test, `action='clear'`; refusal/no-write assertions at lines 263–275 | New assertion body is unverified until the main targeted run; no source behavior claim |
| Current unbound rebind inverse | Live, unchanged | `test_rebind_retains_v1_after_v2_restart_exact_inverse_and_redo`, especially lines 140–147 | Must wait for its real source fix; not claimed passing here |
| Current unbound clear inverse | Live, unchanged | `test_clear_removes_row_and_undo_restores_empty_exactly`, especially lines 170–186 | Must wait for its real source fix; not claimed passing here |

The new negative test uses the genuine `editing` fixture, `put`, `body`,
`call`, and `submit` helpers through the registered Runtime commitTimeline
provider. It imports legitimate replacement text before the no-write snapshot.
It asserts the actual C0 guard envelope (`validation_error`,
`invalid_document`, empty structured path, and the exact historical-source
message suffix), then checks unchanged head/history/canonical closure, live
binding row, and source/replacement CAS bytes.

## Static conservation record

- Only `tests/editing_conformance/test_commit_runtime_text_binding.py` is a
  worktree code change.
- The two named original functions are the only deleted functions.
- All other functions, assertions, parameters, helpers, fixtures, and imports
  remain byte/AST-conserved except for the one new parametrized test.
- No guard, policy, authority, schema, Runtime, generated file, pin, fixture,
  or other test was changed.
