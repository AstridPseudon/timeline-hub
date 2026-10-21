# WC6 exact hello carrier correction review

## Decision

**APPROVE the exact narration correction.** The candidate is `f386a1205`
(`test(timeline): preserve exact voiceover source fixture`) on top of the
previous WC6 native proof. It fixes the specific `a3a694312` review finding;
it does not claim that all legacy WC6 writer positives are migrated.

No product source was changed in this review.

## Exact carrier verification

The prior finding was correct: the old positive created a Runtime
`voiceover_script`, `slot: None` binding containing UTF-8 `b"hello"`, then
placed Runtime's returned descriptor and text in the shot snapshot. The `a3a`
native proof instead carried the pre-cut fixture's different `transcript`
binding (`Open on the river`). That was not equivalent.

The correction restores the exact behavior in the native fixture:

- `tests/timeline/test_authoring_media.py:565-583` fixes the expected bytes to
  `b"hello"`, computes the exact SHA-256 media identity and natural binding
  identity, and declares the expected `voiceover_script`/`slot: None`,
  `text/plain`, 5-byte descriptor.
- `:599-621` calls Runtime's normal
  `set_project_shot_text_binding(... expected_head=0)` and verifies the
  Runtime-returned descriptor field-for-field, the list/get reads, and the CAS
  bytes. The descriptor is an expected value, not a synthetic authority: the
  live binding and object are created and read by Runtime APIs.
- `:654-660` reads the binding through the public client with text included and
  checks the exact text.
- `:680-684`, `:725-729`, and `:746-750` assert the exact descriptor at native
  checkout, accepted publication, and fresh reload respectively. The complete
  `text_bindings` list is also compared at publication and reload.

The original pre-cut transcript remains in the source closure: the correction
appends the hello binding to the existing list (`:584-585`) rather than
replacing it. The Runtime fixture independently identifies the original
transcript as `Open on the river`; full-list equality carries that original
binding through publication and reload.

## One-to-one original/new map

There are no removed or converted assertions in `f386a1205`; its diff against
`a3a694312` is additions only. The earlier setup removal at `25d4b9040` is
covered as follows:

| Original behavior | New evidence |
| --- | --- |
| `set_project_shot_text_binding` with `kind=voiceover_script`, `slot=None`, text `hello`, `expected_head=0` | Runtime call at `:599-606`; returned live binding checked at `:607-621` |
| Runtime identity, media hash, MIME, size, stream and head | Exact descriptor equality at `:607-614`, plus public read at `:654-660` |
| `text: "hello"` attached to the authoritative descriptor | Public `include_text=True` read at `:654-660`; checkout/publication/reload descriptor assertions at `:680-684`, `:725-729`, `:746-750` |
| Narration survives the native accepted publication | Full binding-list equality and exact voiceover row at `:725-729` |
| Narration survives fresh checkout/reload | Full binding-list equality and exact voiceover row at `:746-750` |
| Existing transcript, media/source-window, opaque/order, receipt/history, retry, inverse, and ABA behavior | Existing assertions remain in the same native test; `f386a1205` adds no deletion or weakening. |

The original legacy integration test remains present and is neither skipped nor
xfail. The correction therefore does not hide a lost positive or restore the
whole writer.

## Guard preservation

The candidate preserves the prior native guards for the original transcript
list, source window and timing, alias/clip order, opaque registry and payload
values, selected old/new media and mirrors, untouched second shot, accepted
receipt/history, lost-HTTP-ack outbox identity and byte-identical retry after
restart, disjoint rebase, atomic opaque-input refusal, and A-to-B-to-A inverse
refusal. The candidate diff contains no edits to those assertions.

## Remaining real legacy boundary

The one actual unsupported positive still outside this bounded native proof is:

`tests/timeline/test_authoring_media.py::test_real_runtime_import_and_parent_publication_roundtrip`

It still explicitly exercises `service.publish_parent_composition` and
`publish_authoring_candidate` at `:367` and `:417`; it is a retained legacy
whole-parent publication positive, not evidence for the native document-script
route. That is a separate deferred migration item, not a defect in this exact
hello correction and not a reason to reject the correction.

`test_catalog_import_remains_reusable_after_later_parent_cas_conflict` is a
negative catalog-reuse guard around a deliberately failing `StaleWriter`, not
an unsupported legacy success claim and not a blocker here. Other old writer
unit fixtures are likewise outside this bounded correction review.

## Evidence

- Task-provided direct qualification: **70 passed**. Not rerun, per the task
  instruction against repeating the qualified direct lane.
- Central exact HTTP qualification on the corrected tree:
  `pytest -q -o addopts= -p no:cacheprovider -m integration tests/timeline/test_authoring_media.py::test_real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba`
  — **1 passed in 10.14s** (Runtime95 environment; result
  `agt-m2-wc6-exact-voiceover-source-fixture-wc6-exact95-http-env-qualification-integration-1021034654-6288`).
- Local `git diff --check` — **passed**.
- No new audit, repeated 70-test lane, repeated HTTP lane, full suite,
  browser, renderer, or render test was run.

## Recommendation

Merge the exact hello-carrier correction. Keep the named legacy whole-parent
positive above separately tracked for the later bounded writer migration; do
not treat it as closed by this review.
