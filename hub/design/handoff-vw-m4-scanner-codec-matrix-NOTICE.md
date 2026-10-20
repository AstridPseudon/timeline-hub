# Scanner codec matrix ready

`vw-m4-scanner-codec-matrix` has published the bounded Agent codec diagnosis for scanner 1.0.8 repair:

- [REPORT](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-scanner-codec-matrix-REPORT.md)
- [JSON input matrix](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-scanner-codec-matrix-input-matrix.json)

Key action: enumerate `FieldSpec.stored_at` plus `stored_at_audio`; use the general entrance/exit specs for shared visual storage, `to_stored(..., audio=True)` for `params.fadeIn/Out`, and `audio_curves.validate()` for the separate curve paths. `describe()` is presentation, not acceptance. Preserve explicit clears, open params/extension data, and free-form transition policy.
