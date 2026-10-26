# D141ii writers15 return handoff: FAIL

Manager disposition: do not merge. The return has 22/22 execution PASS and the complete return-plus-prior-neighbor union has 29/29 execution PASS, but F5 remains a protected caller-coverage failure. F7 remains `FAIL_ENVIRONMENT` for the exact mandated mypy command.

## Changed reply shapes for owner

These are the intentional migration shapes observed in the reviewed tree; they are not silently counted as literal legacy-body equality:

1. **Accepted commit / key-and-force purpose** (`tests/packs/timeline/test_cli_status_publish.py:29-62`): legacy publish's `new_head`/narration result becomes the C0 five-key envelope (`ok`, `data`, `error`, `receipt`, `idempotency_key`) with accepted status, canonical document, accepted revision/publication IDs and receipt identity. `--force` becomes parser refusal, with no Runtime call.
2. **Human summary / JSON purpose** (`test_cli_status_publish.py:381-410`, `:35-49`): human output remains the bounded three-line summary; JSON is the C0 envelope and `receipt.result` equals data except the explicitly documented presentation fields `accepted_publication_id` and `show_command`.
3. **Partial publication** (`test_cli_status_publish.py:331-356`): legacy partial narration receipt is carried in the typed `partial_publication` error details with the original idempotency key and one attempt.
4. **Empty create** (`tests/v10/test_timelines_create.py:517-570` and following): legacy `publish_parent_composition`/small result is replaced by shell plus authenticated `commit_timeline` (`timeline.init` and `doc.patch`), returning the canonical document and history/bootstrap data. The test retains the authored name, defaults/output, registry, occurrences, empty child revisions, exact init args, base pair and step reads.
5. **Render publication**: generic host hook is replaced by the requester-owned guarded commit/render chain, preserving attempt/lease/timeline/expected-version authority and no local save/invoke.
6. **409 conflict, approval, restart**: old endpoint/private promotion route names become the supported `commit_timeline`/authoring caller while preserving typed details/request identity, candidate/base approval binding, recovery and single-generation guarantees.

## Open repair required

For both actor parameters in `tests/packs/timeline/test_verbs_working_copy.py:595-627`, exercise the real `commit_document`/CLI handler with the authenticated Runtime conflict result and assert the actor-specific discard-first message, rather than constructing `Refusal` and calling `_document_error` directly. Preserve the no-force/no-write behavior. No repair was made by this reviewer.

## Validation handoff

Exact mypy is an environment failure due the configured Python 3.11 target versus the installed NumPy stub syntax. The explicit Python 3.12 target check passed but is only a diagnostic. Ruff, private py_compile, diff check, targeted 22, and union 29 passed. No full suite was run.
