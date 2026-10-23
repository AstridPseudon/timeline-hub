## R2r audit report

Audit complete; no product, schema, test, generated, pin, or config files changed.

Findings:

- Agent135a `native_text_binding.py:38–67` emits:
  - `occurrence:<id>/text-binding:<binding_key>`
  - `occurrence:<id>/collection:text-binding`
  - `binding_key` is `kind` for null slots, or `kind:slot` (e.g. `prompt:hero`).
- The authenticated physical root is the occurrence’s pinned `shot_revision_id`:
  - `shot-revision:<occurrence.shot_revision_id>`
  - logical row path: `["text_bindings", "text-binding:<binding_key>"]`
  - collection path: `["text_bindings"]`, with members/order derived by the exact `(kind, slot)` binding key.
- It is not the internal timeline root and must not be resolved by `shot_id`, payload equality, array position, or newest revision.
- Runtime schema and store already admit/project these aliases (`edit-command.json`, `shot-composition.json`, `timeline_commit_store.py:22,1091–1112`).
- Runtime auth currently handles occurrence shot/source/registry aliases but falls through for text bindings at `timeline_commit_auth.py:32–91`; collection fallback currently risks broadening to `timeline`. This explains the reported 10-pass/11-fail original regression.

Author guidance:

- Add only authenticated text-binding normalization in `site`/`native_site`, covering reads, writes, bindings, effects, replay, and undo.
- Preserve original alias text for store projection and history while authenticating physical revision, digest, boundary, and composite slot identity.
- Follow only a unique authenticated shot-revision successor on replay; reject outside, ambiguous, unrelated, forged, or duplicate `(kind, slot)` bindings.
- Preserve exact collection membership/order guards, fields vs atomic behavior, dry-run/idempotency semantics, replies, attribution, effects, and undo provenance.
- Do not route unknown aliases to `timeline`, invent public paths, or add an alternate executor.

Verification:

- `git status --short` — clean.
- `git diff --check` — passed.
- Tests, lint, and typecheck were not run per the explicit read-only/no-test-execution brief. The original native regression remains the repair author’s single run.

Required commit message and `DONE` marker were written.