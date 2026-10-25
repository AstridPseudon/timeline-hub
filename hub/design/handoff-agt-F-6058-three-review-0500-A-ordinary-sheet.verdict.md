# A — ordinary sheet setup review

Verdict: `PASS_SOURCE` for the candidate patch, with functional qualification intentionally unverified.

Refs and exact file blobs:

- Captured base/parent: `tl/integration` at `6cd767b6afd157b3f12e14dde5e9ef50dcb1f70a`.
- Candidate: `tl/agt-F-6058-ordinary-sheet-0451` at `ccfe0a354a04584f8a44cb14e38df7020a26e863`; parent is the captured base.
- Parent test blob: `aa158fb50aefd6edea8a5e811b90b8f31044ae16`.
- Candidate test blob: `f4de0ab3e34341a7654bef037c828c4b12d9b5db`.
- Candidate delta: exactly `3 insertions, 0 deletions`, only in `tests/editing_conformance/test_native_sheet_ordinary_runtime.py`.

PASS_FACTS

- The candidate adds `media.admit` only in the detached branch, with the exact ingested pin `{media_id: media, content_digest: media}`. The media is ingested by the same RuntimeService in the fixture as `video/mp4`; no authored MIME, bytes, or digest is changed.
- Production `commit.py:1188` captures all `media.admit` inputs through the authenticated Runtime port before `execute`; `native_media_admission.py:62-65, 75-92` requires the raw object ID and digest to equal the submitted pin and records the dependency. `validate_admissions` at `:95-118` requires the admitted media to be consumed by the final candidate, so this is not unused authority or admission-without-consumer.
- The candidate closes the fixture service before `_preflight_detached_fixture` constructs a second `RuntimeService` on the same realm. The preflight then checks the public head pair, parent/closure identity and payload mirror, occurrence ownership/track/timing, clip order/source window, opaque values, registry/MIME/duration, manifest shot/internal/media pins, CAS ownership/digest, and child revision ownership. All 21 named `check(...)` predicates are byte-preserved; the 7 test functions, 150 assertions, and 2 raises are AST-conserved.
- No OwnerBusy bypass, inactive service, synthetic accepted record, direct store write, alternate writer, manifest overwrite, fake history, or authorization bypass was introduced. The durable bootstrap remains `service.commit_timeline(..., route_path(...), authorize=lambda: None)` and the preflight reads only through RuntimeService APIs.
- The command-array order places `media.admit` after the detached `doc.patch`, but Runtime captures admission before execution; the review does not treat the commit-message phrase “before the source patch” as literal array order.

FAIL_FACTS / LIMITS

- No functional test, collection, service startup, or Runtime execution was run, by the source-only brief. A full qualification of the detached fixture remains manager-owned.

Static evidence:

- In-memory AST parse/compile: PASS for parent and candidate.
- `/home/user/work/venv-agent/bin/python -m ruff check <parent file>`: PASS; candidate: PASS.
- `/home/user/work/venv-agent/bin/python -m mypy <parent file>`: PASS; candidate: PASS.
- `git diff --check 6cd767b6..ccfe0a35 -- tests/editing_conformance/test_native_sheet_ordinary_runtime.py`: PASS.
