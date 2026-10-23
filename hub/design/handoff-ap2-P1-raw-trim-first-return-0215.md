# Handoff: ap2-P1-raw-trim-first-return-0215

**Verdict: PASS for the bounded test-only requalification; H3 remains NO-GO.**

The authored-payload-only oracle was removed. `p1RawHandoffCorpus.test.ts` now compares the complete structured-cloned `after` document after rebinding only `parent_revision.revision_id` and `parent_revision.content_digest` to the exact `before` values. The separate original project/timeline/revision/digest assertion and all original delta, preservation, outbox, no-send, and provenance guards remain.

Pre-edit complete-document probing found exactly two trim-only differences: `parent_revision.revision_id` and `parent_revision.content_digest`. The label case had no complete-document mismatch. These are fixture semantic-executor identity vs local pre-acceptance identity, not authored payload loss.

Targeted result: 20 passed; 8 unchanged provenance checks failed because the sandbox rejects their `spawnSync git` calls with `EPERM`. Typecheck, target lint, and `git diff --check` passed. Full/browser/socket/install checks were not run.

The test is local/fake evidence (fake IndexedDB and mocked sender). Production is not mounted: `useTimelineSave.ts:72-104` stages `originalLocalSaveBasis`, but `:105-125` passes no `localDocumentSave` to persistence; `useTimelinePersistence.ts:408-412` consequently uses `saveTimelineAtHead`/`saveTimeline`. No production caller constructs the handoff/session.

The requested full v2 ABI is therefore unqualified. Existing shapes cover the basic identity/base/commands/label and outbox idempotency key, but lack or do not prove steps, per-step patches/reads, merge mode, request reads, merged replies, canonical closure/authoritative attribution, structured conflict/invalid details, and authenticated preview `would_status` plus history. `dry_run` is only an older type field and the local outbox does not emit it; the local path blocks `doc.patch`. Existing mock fixtures do not count as mounted production evidence. No wire overlay/drop or handwritten DTO was added. No H3 GO/P4 DONE claim.

See the worker report for exact commands, failure output, differing values, and owner/next-step detail.
