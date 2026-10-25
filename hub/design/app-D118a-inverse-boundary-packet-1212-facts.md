# D118a exact inverse-boundary handback

Finite, read-only packet for the existing Runtime/Agent source owners. No source, assertion, guard, fixture, collector, or process file was changed. Raw payloads, auth material, keys, URLs, opaque IDs, and stack dumps are not exported.

## Source pairing

The qualified Runtime is `42aad0e92f6da8ea83dd0a382a87e3acd12651b0`, tree `085a5be70b56353deb41ae7d743336a4ccb7f29c`, clean. Its parent is the retained original-369 reference `369ffa7c00bd3d45c610fac7651ff79e7a283a1a`; that parent is kept distinct from the current qualified source. Runtime guard source is `runtime_protocol/timeline_commit_auth.py`, SHA-256 `72d4611def6491ac39872e04551ed7d2f1c4872eb655c4b0a63055bd4b324b2d`.

Agent producer pairs are retained per family:

- Occurrence: commit `36e44e1c0ed9b454faaf973715a2be7119552d0a`, tree `ad8b2be09adf3b8dfa7d091511e9a25e912adb79`; `native_occurrence_create.py` SHA-256 `962016ffdba404dfd88ed4fbf62bd4882e96e42038a0548549a0cf727ef25d22`; producer functions `occurrence_create:15`, `capture_occurrence_create:53`, and provider boundary `commit.py:1160`.
- Scalar: commit `0ad49261ed36f043b059c07de989bd39cd3a5889`, tree `aa413f6e1712626c0506284c8727057d753f692d`; `_clip_scalar_commands.py` SHA-256 `131ba969cd5fa04ce4af85de5700db57ba27f0917ccc9b2a446980ae5d85f869`; producer functions `clip_set:89`, `capture_clip_set:113`, and provider boundary `commit.py:1160`.
- Numeric: commit `cf7b8d7c2b4cb980de1d873f0498784d5210d508`, tree `6540b10a56c4453609c0da5219ad314d8fda0dcd`; `_scalar_commands.py` SHA-256 `6b5c1a0db9fcf78533f16ca14d9ab14d96ca31ce19875c062b0470954488b34c`; producer functions `clip_set_params:68`, `capture_clip_set_params:150`, and provider boundary `commit.py:1160`.

## Finite records

- Occurrence `False`, allocation ordinal `1286`: the original unchanged node retained `RuntimeErrorBase`, status `422`, reason `unsupported_timing` at `_prove_birth:173` for the authored invalid timing. The approved migrated candidate reached no-write/history checks, then failed during `media_undo` at Runtime `_inverse_stage_boundaries`, `timeline_commit_auth.py:1645`, with status `422`, reason `invalid_records`, message “inverse stage materialization differs from its recorded source image.” Command ordinal and all prepared/stage/physical values are `EXACTMISSING`.
- Occurrence `True`, allocation ordinal `1289`: the same original invalid-timing result was retained. The migrated candidate reached grouped birth, then failed at Runtime `command_output`, `timeline_commit_auth.py:2267`, with status `422`, reason `invalid_records`, message “provider intermediate image lacks an authenticated physical promotion.” Command ordinal and all prepared/intermediate/promotion/read values are `EXACTMISSING`.
- Scalar modes `scalar`/`compound`/`separate`, allocation ordinals `925`/`927`/`929`: all passed provider registration/bootstrap and reached Runtime `command_output:2267`; retained status is `422`, reason `invalid_records`, at the initial scalar commit authorization. Expected source fields are the hold, and in compound/separate also `at`, `app.astrid.fixed_start`, and `app.astrid.for`; accepted effect records, physical image, and content digest are `EXACTMISSING`.
- Numeric cases `int→float`, `int→bool`, and `bool→int`, allocation ordinals `1211`/`1221`/`1234`: all retained exact type predicates through accepted save, reload, and first inverse; failure occurred at redo inverse in `_inverse_stage_boundaries:1755`, status `422`, reason `invalid_records`, message “inverse stage native writes do not cover its authenticated effect image.” The expected safe field is `occurrence-child.clip.params.x`; the retained types are float, boolean, and int respectively. Redo stage maps, effect bindings, physical refs, and content digest are `EXACTMISSING`.

The source guard location identifies the producer-to-authority boundary only; it does not establish Runtime fault. No source fix, guessed record, duplicate writer diagnosis, or broader investigation is included.

## Verification

The packet JSON was parsed successfully and `git diff --check` was run. No tests, typecheck, lint, node/probe/collector, or full suite was run because this task is source-unchanged evidence packaging and the retained worker runs are the evidence of record.
