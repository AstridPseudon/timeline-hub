## D33 Report

Investigated read-only at base `d98fdb83ef`.

Finding: Luna-1300 fixed only the first `effect_diff/logical_parent` refusal. The two original M1 failures remain downstream:

- `null-payload`: final validation passes `parent["clips"] is None` into `_identity_rows`.
- `null-config`: production `emit_document_commands → _payload_for_emit → validate_payload` rejects `config["clips"] is None`.

The smallest justified Sol-1308 production fix is the unmerged two-file hunk:

- `validation.py`: select the surviving list mirror, permit only unchanged legacy nulls, and pass a detached list/list view to the timing validator.
- `emitter.py`: validate a temporary projection with the null mirror removed, while refusing any null-mirror transition and preserving raw payload shape.

Do not broaden `logical_parent` further: null must not become absent/empty, and raw null must not be rewritten. Physical writes/before-values remain authoritative; normalized list effects are projection-only.

Evidence:

- Retained pre-fix M1: `124 passed, 2 failed`.
- Sol-1308 focused command: `pytest ... test_remove_last_clip_keeps_exact_container_shape`
- Result: `5 passed in 14.13s`, covering payload/config/both/null-payload/null-config, including inverse/redo. This was source-owner evidence; I did not rerun originals.
- Base commit: `d98fdb83ef522ceec20a21571718da303b9bea1d`.
- `_commit_patch.py` is unchanged by Sol-1308; only `validation.py` and `emitter.py` are modified.
- Durable evidence: [source-facts.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-null-whole-path-1310/evidence/source-facts.md)

No product/test changes were made. No full, gate, child, acquisition, or independent neighboring-suite run was performed. Next step: merge/review Sol-1308, then run the prescribed targeted R2 neighbors on the integrated tree.