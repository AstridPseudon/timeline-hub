# D116 protected review

**Verdict: FAIL_SOURCE.** Manager must not call this candidate fullGREEN.

Candidate reviewed:

- Commit: `21146cd6decaa1c15bca1753ca719f6937040798`
- Tree: `3846a9b41a5fccc455efe7ed43da487307fcc28e`
- Compared against `070dfc`, `26a8c0`, and `e9e3b8f`.
- No product/test edits made in my worktree.

## Per-file verdicts

- `native_word_anchor_fixture.py` — **FAIL_SOURCE**. It builds the required C0 fields, then removes `steps`, `merge`, and `reads` for every `clip.anchor` request (lines 124–127). The exposed `case.request` path also emits only base fields plus `commands` (lines 357–380). Therefore the measured current-form path is not a genuine full C0 request.
- `test_native_word_anchor.py` — **PASS_SOURCE** for its local D116 delta. First-use expectations retain `[case.pin]`; authored timing and short-negative refusal inputs remain exact. Runtime behavior remains unqualified because it depends on the failing fixture envelope.
- `test_word_binding_recipe.py` — **FAIL_SOURCE**. Its `Recording.compile_inputs` monkeypatch and `bundle()` normalization rewrite/strip canonical clip fields, masking the current-form compiler input. The cluster still exposes `clips` versus `config.clips` mismatches.

## Authenticated evidence

Cluster XML:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D116-word-seed-0947/evidence/cluster.xml`

- Exact membership: **95 tests**
- Native: 54 tests, 37 pass / 17 fail
- Recipe: 41 tests, 25 pass / 16 fail
- Skips: 0; errors: 0
- XML SHA-256: `570b43cce443e545a4b6217f7266cc42e41701ce1c1bf5fb2f34964e0c759882`

The final-branch targeted controls recorded **5 passed in 24.43s**, including first-use retention, source refusal, phrase binding, and fresh-process canonical compilation. Short-occurrence, raw-source-window, and outside-window refusal controls pass.

Static evidence passed:

- Ruff: passed
- Mypy: passed, 3 files
- `py_compile`: passed
- AST parsing and `git diff --check`: passed

No full suite was requested or run.

## Unresolved scope

The 33 failures are downstream/authentication scope, not grounds to weaken tests:

- inverse/ABA failures: `test_occurrence_window_is_rechecked...`, `test_undo_recovers_before_binding...`, `test_same_word_in_reused_cas_clips...`, `test_last_write_clear_undo_restore...`, `test_on_until_clear...`, `test_half_open_window...`, `test_first_anchor_inverse...`
- timing/config failures: `test_word_ending_at_occurrence_end...`, `test_follow_rebases_original_choice...`, `test_reference_is_authoritative...`
- legacy paths: `test_legacy_ambiguous_text_refuses_choose_occurrence`, `test_legacy_unique_word_in_reused_cas...`, `test_unique_legacy_word_compiles...`
- recipe-only refusal failures: `test_stale_anchor_refuses_when_intervening_window_excludes_selected_word`, `test_invalid_authored_reference...missing-clip`

Shared caller audit found `test_timing_retained_inputs.py:86-91` still uses `seed(..., current_form=False)`. Named current/archive coverage exists in that file, but no effective legacy retirement claim should be made without the required D107 approval.

## File hashes

| File | Git blob | SHA-256 |
|---|---|---|
| `native_word_anchor_fixture.py` | `9515d56058abf84e91217e5db6bfcb05fa3bb8b5` | `ee7f8c2eb841915f1f51177d1883e3bececa5d7527596eb589771146f550e321` |
| `test_native_word_anchor.py` | `dcd324a3365c78d16886abafb40c70cda5e30e29` | `9397349fbce4c1eeb76af763fc5c4d8ba7317da91f9f171733bcf4d7ff8be9a1` |
| `test_word_binding_recipe.py` | `6e200c16298eb7f64a8d74afa8fd2e096076e759` | `98aec76182e48ce56abbf918cb608485d510b6b96c8885f904c238c942e7d2b5` |

Required D115 commit message and empty `DONE` marker were written.