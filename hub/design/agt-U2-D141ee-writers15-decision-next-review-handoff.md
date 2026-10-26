# D141ee writers15 protected handoff

## Verdict: FAIL

The author’s commit is source-scope clean and its final 22-node targeted run is green, but it is not eligible for protected PASS. Manager must not merge this review result as PASS.

## Owner-facing changed reply shapes

The author listed these changes; they remain subject to the finite assertion findings in `findings.md`:

- publish success → accepted commit result, with accepted revision/publication fields and receipt;
- publish CAS exception → typed commit conflict envelope with details/head and no receipt;
- clean `published=false` → commit `status=unchanged` with null receipt;
- partial publication receipt → `partial_publication` commit error retaining receipt details, idempotency, and no retry;
- old force-forward success → commit path success without force plus explicit parser refusal;
- legacy actor conflict → commit conflict presenter retaining actor/path/discard-first guidance and refusing force overwrite;
- old parent publication 409 → `commit_timeline` 409 with generated details/request id and recorded request;
- approval promotion → `publish_authoring_candidate` authenticated commit retaining candidate/base/approval binding;
- generic host publication → requester-owned commit followed by render admission with attempt/fence/timeline/base authority;
- empty parent publication → shell followed by `timeline.init`/`doc.patch` commit with canonical empty-head data.

## Required follow-up before PASS

- Restore explicit one-attempt assertions for IDs 5 and 6 on the supported commit caller.
- Assert accepted-head authority and key/one-call behavior for ID 7 while retaining explicit force refusal.
- Exercise both human and JSON output for ID 8, including exact envelope/data identity and read-before-write ordering.
- Assert `status=unchanged` and zero commit transport calls for ID 9.
- Drive IDs 12 and 13 through `commit_document`/`_document_error`, separately for editor and generic actor identities.
- Restore the dropped empty-create predicates for ID 18, including full defaults/registry/occurrences/history/base/step-read checks.
- Resolve or document the shared-environment mypy failure; the exact required command was not reproduced as PASS.

No author repair was made. No old route, force adapter, inverse planner, installer, Runtime source, or broader test suite was touched.
