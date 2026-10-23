# G5 SDK original FOUR provider-failure packet

Status: provider validation failure after authenticated request bodies reached the Runtime. No acceptance credit.

## Run

Command:

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration tests/sdk/test_timeline_checkout_history_runtime.py
```

Result: `3 failed, 1 passed in 22.43s`.

The passing test was `test_open_bundle_keeps_http_rows_raw_and_round_trips_canonical_images`.
The three failures were `test_checkout_reload_undo_cli_redo_uses_retained_history`,
`test_retained_restore_does_not_reopen_consumed_draft_steps`, and
`test_catalog_recover_uses_real_http_and_preserves_closure_before_revision_restore`.

All three failures occurred after the normal authenticated move/setup requests were accepted.
The provider rejected the inverse/restore candidate with:

```text
candidate.timing: legacy word anchor is missing
code=validation_error path=[] reason=invalid_document status=invalid
hint=Read the timeline and submit a valid canonical document change
suggested_command=timeline edit
```

## Full request bodies

The failing flight bodies were:

```json
{"api_version":1,"project_id":"7b6f2bae8ffe42bf925216c38249ed79","timeline_id":"film","base_revision_id":"authoring-parent-revision-7ed5930576800b6e4f2420a43eb9cb5d576e11fab4b81b5821f308034810b9e1","base_publication_id":"txn-3e068a1110a54b2fb515983b2c976588","commands":[{"schema_version":1,"op":"timeline.inverse","version":"1","select":null,"args":{"publications":["txn-1172eb8136b845e4b54a8f1be6a03f8a"]}}],"source":{"via":"python"},"dry_run":false,"label":"Undo timeline edit","merge":"fields","steps":[{"id":"inverse","label":"Undo timeline edit","intent":"","tags":[],"command_ordinals":[0],"patch":[]}]}
{"api_version":1,"project_id":"7b6f2bae8ffe42bf925216c38249ed79","timeline_id":"film","base_revision_id":"authoring-parent-revision-99d2b01b77f19dc4264c7bc8a0d8b86a6a15ebb9ae8c9b7f473d980de13f3f89","base_publication_id":"txn-2bbcd60edb7345adbe1356e59704ad55","commands":[{"schema_version":1,"op":"timeline.restore","version":"1","select":null,"args":{"revision_id":"a3e671256f1c42b8837d3e118c97b21b","content_digest":"sha256:b6069d1ddccc0279e871b142773b63b73b107ebf9d0adc11ab73832b69097afb"}}],"source":{"via":"python"},"dry_run":false}
{"api_version":1,"project_id":"7b6f2bae8ffe42bf925216c38249ed79","timeline_id":"film","base_revision_id":"authoring-parent-revision-42a8f4903559f495650b124d3c9d78a530f9a8957c47342ea3e1bac63b790311","base_publication_id":"txn-f25cbfce1bf044e6b3c77304c74eb574","commands":[{"schema_version":1,"op":"timeline.restore","version":"1","select":null,"args":{"revision_id":"a3e671256f1c42b8837d3e118c97b21b","content_digest":"sha256:b6069d1ddccc0279e871b142773b63b73b107ebf9d0adc11ab73832b69097afb"}}],"source":{"via":"python"},"dry_run":false}
```

No separate prepared response was exposed: the provider rejected during candidate validation.

## Capture and state

- Normal route: authenticated SDK timeline commit; native route was not invoked.
- No direct SQL, SQL write, history injection, CAS write, or forced revision/publication substitution was used.
- Private captures:
  - `/tmp/w-251e17093e/pytest-of-root/pytest-0/test_checkout_reload_undo_cli_0/client-data/timeline-outbox/2948465edd5a75430c08b14997a6f1bad9f18a30911b929f56a6c9f7cae3c9aa.json`, SHA-256 `c1cd38a46e685fd346a4dc75f0e986b43f3e0d0db21d917fd257999d067ff17a`
  - `/tmp/w-251e17093e/pytest-of-root/pytest-0/test_retained_restore_does_not0/client-data/timeline-outbox/2948465edd5a75430c08b14997a6f1bad9f18a30911b929f56a6c9f7cae3c9aa.json`, SHA-256 `b0d74859b95a6f1b98ee30598a6ddf69f73cff381ff985447ee9f01d5ff8ee99`
  - `/tmp/w-251e17093e/pytest-of-root/pytest-0/test_catalog_recover_uses_real0/restore-outbox.json`, SHA-256 `863b5317cd479de59358c9a99a8817e7d7f1777c9662f4eb3d60e0b8aa7b9b73`
- The catalog recovery also retained `/tmp/w-251e17093e/pytest-of-root/pytest-0/test_catalog_recover_uses_real0/edit-outbox.json`, SHA-256 `f691d4840143fe6e378178a980b8f4dfd1a2ddcc46df843e9148c0719b8840ef`.
- Initial restored head: revision `a3e671256f1c42b8837d3e118c97b21b`, publication `txn-11c90075be6c4c8bb9e2627366f0fe4f`, predecessor `film-parent-v1` / `txn-55c0651b2cd64255ae06e73f9708220a`.
- Post-failure first-root head: revision `authoring-parent-revision-7ed5930576800b6e4f2420a43eb9cb5d576e11fab4b81b5821f308034810b9e1`, publication `txn-3e068a1110a54b2fb515983b2c976588`, parent digest `sha256:cb6b86f9e211075f40abe867713ce5735c46b6ada70ef98a921aa3cff1fe08e5`.
- Accepted source history: `txn-55c...` / `film-parent-v1`, `txn-11c...` / `a3e...`, then accepted move publications `txn-1172...` / `authoring-parent-revision-99d...` and `txn-3e068...` / `authoring-parent-revision-7ed...`.
- Current canonical readback retained the transcript document ID `transcript:c49d7d673dc883c363f95ea19d01d75b66c00ba849b09cb833966e39d392133d`, media `sha256:f39a...`, and shot-1 source binding `fa141364-9d4d-57ca-b7dc-9a23d259312e` for `Open on the river`; the accepted move canonicalization had no legacy word anchor.
- Current effects: `music-bed` has `music-fade` (`direction=in`, `duration=0.25`); `music-other` has no effects.
- Dependency manifest remained the qualified 3-shot / 3-internal / 5-media closure with no documents.

The fixture's only post-run adjustment was metadata-only: it now obtains the accepted head revision/publication through the existing read-only `verify_baseline` current reader and returns those source-bound values. The original FOUR body was not rerun under the no-repeat rule.
