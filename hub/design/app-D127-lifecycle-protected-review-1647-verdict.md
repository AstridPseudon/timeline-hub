# D127 independent lifecycle protected review

Verdict: **FAIL (source)**. Focused proof: **NOTRUN (source gate)**.

The review commit is source-scoped to the permitted App test file and retains the normal and reviewed-legacy arms, the exact reviewed-new helper hash, keysets, privacy checks, bounds, sampling/loss/denominator relationships, retention checks, and the requested mutation test. The required source test, scoped ESLint, App typecheck, node typecheck, and diff check pass.

Blocking finding `D127-LIFECYCLE-001`:

- `tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts:243-267` does not bind `lifecycle` to the `dispatch_queue` phase state for `returned_without_response` or `pending_at_stop`.
- The frozen helper at Runtime candidate `231ddb5a...`, `tests/helpers/p2_commit_phase_capture.py:497-504`, derives `pending_at_stop` only when `dispatch_finished` is false; once dispatch finishes, `dispatch_raised` takes precedence over `returned_without_response`.
- The App validator accepts a pending summary whose dispatch queue is `status: raised` or already ended, and accepts a `returned_without_response` summary whose dispatch queue is raised, provided the other currently checked fields are adjusted. These are meaningful lifecycle/phase contradictions, not the valid pending stop race.
- The existing D127 mutation test covers pending duration, response-count, and retention contradictions but does not reject these phase-state contradictions, so the source gap is not self-caught.

The validator correctly avoids an overstrict pending/no-response rule: the helper can snapshot while an HTTP response has been observed but before the dispatch-scope return trace sets `dispatch_finished`; that valid race is not a finding.

No repository files were changed. No focused endpoint/bootstrap proof was run because the brief requires it only after SOURCE PASS. Existing central Runtime proof was not duplicated.
