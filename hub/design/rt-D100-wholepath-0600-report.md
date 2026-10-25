## D100 whole-path report

Read-only comparison completed against the published 30890/7351 packet and recorded source revisions.

- Candidate: 38 PASS, 16 FAIL, 5 ERROR across 59.
- Baseline: 12 PASS, 14 FAIL across 26.
- No product, test, fixture, schema, generated, or pin changes.
- Worktree remains clean; `DONE` marker and commit message written.

Findings:

- `at_ms` failure is a real Agent regression. `capture.py:_duration` creates a `Fraction`, then passes it to `number()`, which only accepts `int`/`float` (`capture.py:25-36, 102-105`). The `at` and `both` comparators pass. Owner: Agent capture path. Proposed fix: keep exact arithmetic but convert/validate at the internal boundary before calling the JSON-number validator.
- `source_offset` refusal is unchanged baseline behavior: `authoring_bundle.py:847-849` intentionally rejects non-default placement offsets without an explicit internal clip trim. The fixture supplies a non-default `{start: 0, end: 10000}` offset. Owner: test/setup or shared authoring caller; do not relax the guard.
- `internal timeline scope mismatch` is also unchanged baseline setup refusal. Runtime rejects the supplied internal owner at `timeline_commit_store.py:1282-1289`; the fixture uses `timeline_id: chapter-1` while the destination is `film`. The packet does not prove the database row state, so caller/setup ownership is reported as likely, not certain. Proposed fix: use a canonical registered internal scope in the fixture/provider.
- Inverse materialization failures are Runtime verifier refusals at `timeline_commit_auth.py:1582-1594`. `service.py:2518` is only the public wrapper. Runtime owns the guard; the producer-side binding defect remains UNKNOWN from safe evidence. Do not weaken turnover, owner, or edge checks.
- Historical text-binding refusals originate in Agent `validation.py:430-437`; Runtime again only wraps the error. This is a retained exact-declaration/source guard and an already-known original-TEN failure, not a demonstrated new regression.

Passing comparators include exact-time `[at]`/`[both]`, strict shared-item identity/no-write controls, the doc.patch physical control, and all 22 historical neighbors.

Tests: no pytest, collection, body, or central suite run; explicitly prohibited by the brief. `git diff --check` passed. D100 remains held/NO-GO pending the narrow owner fixes and a new authorized integrated proof.