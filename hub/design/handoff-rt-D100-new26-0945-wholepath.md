# D100 NEW26 whole-path trace

## Path under review

The intended path is the registered Agent provider through Runtime’s
coordinator/store: request scope and base pair, commands, label, steps with
patches and reads, merge mode, idempotency key, then accepted/merged canonical
receipt, head, effects, bindings and dependencies; conflict/invalid/dry-run
forms remain governed by C0 §1 and §4.

For the six candidate failures, the actual path is shorter:

`candidate test fixture -> RuntimeService.create_timeline ->
_adopt_empty_shell_create -> TimelineCommitStore.adopt_empty_shell ->
history_unavailable -> ConflictError(timeline already exists)`

It does not reach `runtime_commit`, `commitTimeline`, the coordinator, the
registered Agent producer, or document/store acceptance. The retained stderr
shows the exact `history_unavailable` cause at
`timeline_commit_store.py:2030` and the public wrapper at `service.py:1771`.

## Why this is not a production CAS conflict

The Runtime source checks an existing timeline ID before insertion. Provider
registration makes the first `chapter-1` creation bootstrap a published head.
The candidate fixture then asks to create the same ID again. Adoption is only
allowed for an empty, unpublished shell; a published head must be refused.
This is an intentional history/ownership guard, not a concurrent head CAS
collision. The relevant create/adopt source regions have identical hashes in
Runtime `0c62` and `1daca`:

- create region: `1f38dc56aaefe332d0b29be4e05b14e357cc1b6c64653a9cf98fc77643d7cb1f`
- adopt region: `19e2b84d49cb45f9f2046537c82d52edfec26f8574a5e8299e65c65693ab118e`

The proven minimum owner is the candidate Agent fixture’s duplicate call in
`registered_seed`, introduced by `8d43cc7c6c2`, interacting with the existing
`chapter-1` creation in graph-roots setup. No guard relaxation is justified.

## Boundaries and limitations

The old-red tuple used Runtime `0c62` and failed earlier in Agent identity
resolution; the candidate used Runtime `1daca`. Those facts prevent an isolated
Agent causal claim. The candidate’s local source paths pass their source-level
cases, but the registered Runtime behavior for these six cases is not a PASS.
The corrected durable XML, manifests, preflight/control exits, source checks,
and registry restore are summarized in `handoff-rt-D100-new26-0945-outcomes.json`.

The initial zero-test green collection failure is preserved as private setup
history and is not counted as a product result. No new replay, probe,
collector, body, record, test input, or guard change was made.
