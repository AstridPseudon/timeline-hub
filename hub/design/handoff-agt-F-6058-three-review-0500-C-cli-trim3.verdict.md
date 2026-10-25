# C — CLI trim NOCANDIDATE review

Verdict: `NOCANDIDATE / LEGACY-ONLY DISPOSITION FOR ORCHESTRATOR` for the unchanged current test setup. The three selectors and all behavioral assertions remain retained; no deletion is proposed here.

Refs and exact file blobs:

- Captured base/parent: `tl/integration` at `6cd767b6afd157b3f12e14dde5e9ef50dcb1f70a`.
- Candidate branch: `tl/agt-F-6058-CLItrim3-0451` at `6cd767b6afd157b3f12e14dde5e9ef50dcb1f70a` (parent `786385631b8096e50e66b8ecff1e7034c5bc1da9`; merge parent includes the captured base); the assigned file has no diff from the captured base.
- Assigned file blob on both sides: `c1899ab0704056f01412c60ad17ef89327931a41`.
- Exact selectors: `test_cli_trim_exact_retry_restart_dependent_suffix_and_peer[disjoint-rebase-undo]`, `test_cli_trim_exact_retry_restart_dependent_suffix_and_peer[relevant-conflict]`, and `test_cli_move_exact_retry_restart_and_undo_over_real_http`.

PASS_FACTS

- The original pre-migration fixture at migration parent `034f9375c3^` used the same exact 1x1 PNG bytes, `image/png`, authored `from=1`, `to=6`, `hold=5`, `speed=2`, and `app.astrid.for=2.5`; the current setup preserves the PNG/MIME and moves only `for=2.5` to a guarded `doc.patch` after the native birth. The trim, move, lost-ACK, exact retry, restart, peer rebase/conflict, inverse, and no-write assertions are unchanged.
- The current provider route is source-supported: Runtime `import_media` preserves the submitted media type; `_media_inputs._verified` classifies `image/png` as `image`; `native_parent_media_commands.add_media` calls `_clip`; and `native_occurrence_media_commands._clip:179-181` explicitly refuses an image with either `from`/`to` or `speed != 1`. Therefore the preserved authored source window is incompatible with the authentic PNG role.
- The current `for` relocation is faithful as a separate guarded authored declaration, but it cannot repair the media-kind mismatch. It does not bypass the native guard or alter authority.
- Current replacement coverage exists for the roles separately: native image births use image semantics with hold-only timing (for example `tests/sdk/test_checkout_publish_media_admission.py:15-42` and `tests/editing_conformance/test_next_command_cohort_runtime.py:145-147`), while video source-window/speed coverage exists in `tests/editing_conformance/test_commit_runtime_occurrence_media.py:201,297-300`. No current replacement covers this exact PNG-plus-video-window combination.

FAIL_FACTS / DECISION BOUNDARY

- There is no faithful same-role route preserving all original inputs: switching to actual video bytes/MIME changes the original fixture; removing `from`/`to` or changing speed changes authored behavior; weakening `_clip` would change policy/authority and is outside scope.
- The exact three selectors above must not be deleted, skipped, or weakened by this review. If the orchestrator chooses legacy-only disposition, it must name the current role-separated replacement coverage and record the behavior decision. If the orchestrator instead chooses migration, it needs an approved authentic input change, not a fake PNG/video pairing.
- No pytest, collection, service, or functional execution was run.

Static evidence:

- In-memory AST parse/compile: PASS.
- `/home/user/work/venv-agent/bin/python -m ruff check tests/editing_conformance/test_cli_trim_runtime.py`: PASS.
- `/home/user/work/venv-agent/bin/python -m mypy tests/editing_conformance/test_cli_trim_runtime.py`: PASS.
- `git diff --check 6cd767b6..6cd767b6 -- tests/editing_conformance/test_cli_trim_runtime.py`: PASS (no candidate delta).
