## Report — app-F-caller-whole-path-1307

**Verdict: FAIL/HOLD for caller-custody qualification; production source path is structurally PASS.**

No source changes made. Worktree is clean; `DONE` and commit message were written.

Findings:

- Current tuple is App `bbed290…` / tree `e683465…`, Agent `cba425b…` / tree `d19ce2e…`, Runtime `becfe6d…` / tree `7edc08e…`. The committed `caller-custody.json` still records the older App `0971c645…`; it is historical evidence, not current authority.
- Installed rows are authenticated exactly:
  - P2 `/tmp/.../tests/suites.conf:75`: row `6a45d056…`, body `f6042b33…`, tail `0839e6b5…`.
  - P3 `/tmp/.../tests/suites.conf:24`: row `1b7c7996…`, body `6366048b…`, tail `47deb73f…`.
- `caller-publication.py:310-399` dynamically rebinds source/tree/parent identities and refreshes every matching source guard. However, `SOURCE_PATHS` at `:83-89` is unused. There is no post-rebind protected-body/tail/native-stage equality check; `:446-454` only runs `bash -n` and records whole candidate hashes. Candidate/native hashes are recorded, not compared against authenticated expected protected regions.
- The five qualified D53 source files remain byte-identical to the previously reviewed hashes, so no new source acquisition or extra approval gate is justified.
- `REPLY_FIELDS` at `caller-publication.py:98-106` is not a complete C0 inventory. It omits or misnames normative fields including `status`, `rebased_onto`, `provider_version`, `compiler_version`, `steps`, `label`, `source`, `rationale`, `group_id`, `receipt_id`, `idempotency_key`, `command_kind`, `project_seq`, `created_at`, `message`, `details`, `conflicts`, `evaluated_head`, `records`, and guarded inverse fields.
- The actual generated mapping is correct in `src/integrations/runtime/timeline-commit-types.ts:67-112`. The mounted production caller preserves the scoped request and authoritative replies via `localSaveSession.ts:168-188`, `operationHost.ts:280-305`, and `dataProvider.ts:751-843`.
- `custody_requirements()` / `blocked` at `caller-publication.py:477-490, 594-618` describe coordinator admission, future service snapshot, and final-full results as missing custody. Under D59 these are not separate pre-run gates; they should remain post-request evidence. Normal environment inputs belong to recipe1304.

Checks performed:

- Read-only `git show`, `git diff`, `rg`, and static Python inventory of installed rows/current source mappings — passed.
- `git status --short --branch` — clean.
- No tests, runtime, browser, native, backend, HTTP, service, or original journey invocation, per brief.