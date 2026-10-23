# G4 bootstrap/current independent review

## Verdict: FAIL for final qualification

No production source or test files were changed by this review. The current
G4 merge does preserve the three requested resolutions:

- `astrid/packs/rendering/docs/scripts/timeline_document.py` hydrates the exact
  original publication source, captures verified media as
  `occurrence.swap-media`, then emits residual edits as `doc.patch` and posts
  through the existing atomic `TimelineSession.commit_many` path.
- `astrid/sdk/timeline/emitter.py` resolves a unique materialized successor
  owner/physical revision from the authenticated closure and refuses ambiguous
  provenance or managed-edge changes.
- `astrid/sdk/timeline/inverse.py` authenticates the `timeline` scope against
  the `commit.read`/`commit.atomic` pins and keeps input, previous-value,
  selection, physical-binding, later-write, per-step, and ABA guards.

The source behavior is not the reason for the FAIL. The qualification gate is
still red and cannot be waived:

1. `tests/timeline/test_authoring_media.py::test_real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba`
   still asserts the pre-G3 operation kinds at line 907:

   ```python
   ["occurrence.swap-media", "clip.move", "clip.set"]
   ```

   The current G3 contract is one media semantic command followed by one
   guarded document patch. A deterministic reproduction using the current
   `document_fixture`, `bundle_from_document`, same-alias media rebind, and the
   test's `at=0.125`, `hold=0.75` edit emitted exactly:

   ```text
   occurrence.swap-media
   doc.patch
     set clips/id:clip-a/at: before 1 -> 0.125
     set clips/id:clip-a/hold: before 2 -> 0.75
   ```

   For the real film fixture, the original values are `at=0`, `hold=1.8`, so
   the exact minimal unapplied assertion mapping is:

   ```python
   assert [c["op"] for c in commands] == ["occurrence.swap-media", "doc.patch"]
   changes = commands[1]["args"]["changes"]
   assert [(c["op"], c["path"], c["before"], c["value"]) for c in changes] == [
       ("set", ["clips", "id:clip-1", "at"],
        {"state": "present", "value": 0}, 0.125),
       ("set", ["clips", "id:clip-1", "hold"],
        {"state": "present", "value": 1.8}, 0.75),
   ]
   assert changes[0]["ref"] == changes[1]["ref"]
   ```

   This is a command-kind-only stale assertion, not observed product loss;
   the unchanged assertions after it still cover canonical timing/source
   window, media identity and alias order, opaque fields, child closure,
   narration/metadata/sibling preservation, history/reload, lost-undo retry,
   ABA, disjoint rebase, and invalid opaque refusal. No waiver or test edit was
   applied, so final join remains FAIL.

   Central command `request-test agt-G4-bootstrap-current-review-0324
   wc6-exact95-http-env-qualification-integration` followed by `wait-test`
   (result directory
   `.../tests/agt-G4-bootstrap-current-review-0324-wc6-exact95-http-env-qualification-integration-1023032531-15418`)
   did not reach line 907: Runtime health reported
   `sha256:7d4afa...` while the Agent client expected
   `sha256:35c2d9...`. This is a current fixture/client metadata mismatch and
   is a separate first blocker from the stale operation-kind assertion.

2. Provider collection is not comparable to the original 112-test result.
   The first-parent delta deletes the entire
   `test_timeline_scope_inverse_binding_skips_entity_dispatch_but_keeps_guards`
   test from `tests/sdk/test_timeline_commit_provider.py` (33 lines). The
   current file therefore reports `111 passed`; this is a collection/source
   regression, not the no-renderer exception. With `-k
   'not move_reload_and_inverse_import_no_renderer'`, the current result is
   `110 passed, 1 deselected`, and the excluded test itself passes when the
   Runtime checkout is configured. The author log's no-renderer failure was
   caused by missing `ASTRID_RUNTIME_CHECKOUT`.

## Checks

- Focused authoring media/resolution tests: **4 passed**.
- Focused emitter/doc.patch/inverse guards: **29 passed**.
- Current provider file with Runtime checkout: **111 passed**.
- No-renderer control alone: **1 passed**.
- `scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-780da6d6`: **passed**; lock has **15** files and source commit `780da6d605033ca71dbe2ad48c10ec2870ea4865`.
- `scripts/artifact_manifest.py --check`: **passed**.
- `git diff --check`: **passed**.
- All six approved V4 `live-scenes` paths are absent.
- Canonical edit-command schema hash matches Runtime exactly:
  `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`.
- The requested central original-three bootstrap command was
  `request-test agt-G4-bootstrap-current-review-0324 targeted --files
  'tests/v10/test_timelines_create.py::test_remote_create_empty_real_runtime_bootstrap_acceptance'`.
  It failed during collection with `ModuleNotFoundError: runtime_protocol`;
  therefore no
  current real-bootstrap PASS is claimed. Historical a8c2b5b88 evidence was
  **3 passed** on Runtime 780 and is not substituted for current evidence.

No full/browser/farm/native14/P4HTTP suite was run. No skips, xfails,
assertion deletions, dependency writes, or product edits were made.

