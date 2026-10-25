# D124 fallback acceptance — candidateNOTAPPLIED

## Required decision

Manager/orchestrator decides whether the existing D124 fix-or-revert condition is active. This packet does not create a new approval flow and does not authorize a competing current-host author.

## Accepted fallback input

Use only the exact, independently reviewed upstream pair:

- Agent `b742893426a46a99a2f30583a54faeebe2bd98b7`, tree `ccb2f286eae9419b95a3f54b11208f68c57b27cf`.
- Runtime `d4f496ec4fbcae7a1f3a51d47ed5147c561117ad`, tree `1d3e06f4d59ed6d459646d24ab185c36eb5be075`.
- Existing original14 selector set and unchanged authored input.
- `PYTHONNOUSERSITE=1`, `-n 3`, timeout `45`, unchanged startup budgets and Farm resource guards.

The existing b742 proof was `runtime-d118-upstream23-targeted-1025130322-26621`: 14 passed, 0 failed, exit 0, 2.29s. Its receipt had a source-path congruence caveat (rendered metadata named Agent `08e6b905` / integration Runtime), but independent four-process origin records proved b742/d4f496 execution. This caveat must remain visible; it is not permission to retarget or synthesize a source receipt.

## Must remain exact

- `tests/sdk/test_host_bootstrap_source_identity.py` SHA-256 `08dfa8dcafeb80c347923630864a29d58dea97e257428e204fc316567795161b`.
- No assertion, selector, budget, authored input, `PYTHONNOUSERSITE=1`, installer/profile/acquisition, generated file, source pin, credential, or Runtime guard change.
- No new original/body/replay/collector/full/P4/profile/acquisition/installer stage.
- No product file is authorized by this evidence packet.

## Retained C0 wire contract

The host fallback is outside the commit writer, but any integrated acceptance must preserve C0 v2 sections 1–7 exactly:

- Request: `api_version: 1`, `project_id`, `timeline_id`, `base_revision_id`, `base_publication_id`, `commands` with `schema_version`, `op`, `version`, `select`, `args`, plus `label`, `steps`, `merge`, `reads`, `Idempotency-Key`, `dry_run`, `source`, `rationale`, and `group_id`.
- Step fields: `id`, `label`, `intent`, `tags`, `command_ordinals`, `patch`, and `reads`; provider-owned bindings/dependencies remain authenticated and are not caller overrides.
- Replies: `accepted`/`merged`, complete `canonical_document`, `head`/previous-head information, `receipt`, `records`, `effects`, `bindings`, `dependencies`, `history`, and `undo_steps`; conflict preserves reason/head; invalid preserves code/path/hint/suggested_command; preview preserves `would_status` and `receipt: null`.
- Preserve strict closure/reference, previous-value, source/identity, authorization, idempotency, CAS, and guarded undo/history behavior. No overwrite/force option and no second writer.

These are the C0-required exceptions to any generalized “upstream behavior” description: a host fallback cannot justify removing or weakening them.

Source citations: C0 `contract/commit-v2.md:60–274` (request/idempotency), `276–595` (closure/source bindings and refusal guards), `595–702` (conflicts), `703–1562` (replies/preview), `1563–4543` (undo/history scans), `4544–4608` (meta preservation), and `4609–` (authoritative history). D40 security review `runtime-D40-security-review-0240.md:4–9` requires captured-byte consumption or execution-time revalidation and private owner grants.


