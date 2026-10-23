# G4 bootstrap independent review

**Verdict:** source review PASS; Runtime wire FAIL/BLOCKED. Reviewed
`681f4c6e7` against PLAN v2.1 §3 G4 and `contract/commit-v2.md` §§1–5.

The candidate restores canonical `Main`/`main` and custom name/slug, native
output defaults including `background: null` and `background_scale: null`,
custom canvas dimensions/fps, explicit output/null preservation, and exact
lost-ack/retry/later-edit/undo guards. `create_empty` reads the Runtime
bootstrap pair and immutable document, emits `timeline.init` plus G3 patches,
and submits the v2 request through the existing outbox/session path. The
request carries scope/base, commands, label, steps/patches/reads, atomic merge,
and session-supplied `dry_run: false`; request-level reads remain optional.
Accepted/merged/preview acknowledgement validation and structured conflict or
invalid draft retention remain in the production session. The synthetic test
writer is labeled as such; the added real Runtime test uses RuntimeService,
the real provider, authoritative bootstrap/read APIs, receipt replay, and
inverse/undo.

The parent-media helper and its direct tests are byte-identical. No product or
test file was edited by this review and no file was deleted.

Evidence:

- Creator/media command: **36 passed, 3 failed**; all three are real Runtime
  positives failing `invalid_records` with “provider binding revision
  provenance differs from the accepted closure.”
- Focused provider/conformance command: **97 passed, 1 failed**; the failure
  is the unchanged schema census, 58 definitions versus expected 55.
- Non-wire provider subset: **26 passed, 1 deselected**.
- Normal Ruff: **2150/2150**. Normal mypy: **1913/1913** after honest
  baseline tightening. Changed-line Ruff: **0 findings**. Raw whole-file Ruff
  and private mypy still show the parent remote.py’s existing findings.
- `git diff --check`: pass; parent-media byte identity: pass.

The author’s original old-wire failures remain failures, not passes: frozen
Runtime rejected `merge`/`steps` in `CommitRequest` and
`label`/`merge_mode`/`steps` in `PreparedCommit.records`. The current Runtime
reaches a later provider provenance refusal. Runtime/schema/provider repair and
real-positive reruns are the next steps for end-to-end wire acceptance. No
full/browser/live-socket/shared-dependency run was performed.
