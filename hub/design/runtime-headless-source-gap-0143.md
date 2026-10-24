**Blocked on a source gap; no tracked changes made.** Independent Luna source review reached the same conclusion. The failed candidate remains unsuitable for the merge queue.

`commit_timeline` requires verified revision/publication pins. Historical heads with `publication_id=NULL` reach `commits.head()` and fail with `history_unavailable` before the provider evaluates the replacement command. See [service.py:2510](/home/user/work/wt/rt-R5-headless-sol-0143/runtime_protocol/service.py:2510) and [timeline_commit_store.py:395](/home/user/work/wt/rt-R5-headless-sol-0143/runtime_protocol/timeline_commit_store.py:395).

Same-ID creation evaluates stored scope, but accepts no replacement body and collapses adoption failures into a generic conflict. It cannot prove the original submitted-input predicates. See [service.py:1743](/home/user/work/wt/rt-R5-headless-sol-0143/runtime_protocol/service.py:1743).

| Original scenarios/assertions | Assessment |
|---|---|
| Authored and empty historical parent: stale-head refusal, unchanged SQL/payload/head, retry | No supported replacement submission against their unpublished heads. |
| Hidden authored content: public null head, submitted raw body, content-specific refusal, unchanged content/retry | Create checks stored content, but cannot evaluate the submitted replacement. Existing body assertion remains inadequate. |
| Four scoped-row variants: property-specific refusal and unchanged SQL/retry | Adoption guards exist; generic same-ID conflict does not establish the original publication predicates. |
| Fresh/genuinely empty publication and replay | Empty bootstrap is supported, using generated revision/publication identities and canonical bootstrap content. |
| CAS-correct raw republish | Current pinned commits are supported. The candidate’s reduced `AUTHORED_COMMIT` does not preserve the original raw payload coverage. |
| Fresh secondary creation; retired-route 410 | Valid retained coverage. |

The full C0 response, receipt/event, closure, digest, pin, integrity and replay obligations are **not qualified** by this assessment.

Validation performed:

- `/home/user/work/venv-agent/bin/ruff check --no-cache tests/test_timeline_headless_overwrite_refused.py` — passed.
- `/root/.local/bin/pyright --project "$TMPDIR/headless-assessment/pyrightconfig.json" --pythonpath /home/user/work/venv-runtime/bin/python --outputjson <private-copy>` — run separately for original `458595850` and cumulative candidate: original 4 diagnostics, candidate 0; **zero new normalized identities or multiplicities**.
- In-memory `compile()` of both sources — passed.
- `git diff --check`, `git diff --exit-code` — passed; worktree clean.
- Required pytest acceptance, full suites and gates — **not run**, following the source assessment. No new acceptance claim.
- Read retained census log `runtime-full-1024005856-29085`: historical result remains 36 failed, 6479 passed, including ten original family failures.

Inspected Runtime HEAD `2c3a539895a075c9796d630332daf3b9e04c76bb`; loaded real Agent provider from `/home/user/work/agent/astrid/sdk/timeline/commit.py`, Agent HEAD `521c88802330901281cc37ba25818baf2575f05e`.

**Owner/next step:** Runtime R5 and orchestrator must resolve the supported admission path for these unpublished historical sources before faithful test migration can finish. No production changes were made. Wrote the required `commit-msg` naming **R5-full-headless** and `BLOCKED`; no `DONE` or queue request.