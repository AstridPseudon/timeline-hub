# Handoff: P1 snapshot-independent review

SOURCE_READY: PASS; OPS_READY: PASS.

Independent readonly review passes for the existing `app ap2-P1-chain-h6` row. The exact source is `12ef32054524a3cce449fdcb6d94788415b9571a`, tree `4bf9a980d1d5ef38d485702006e52ee33f5dbc3d`, with complete parents `59f1ad1831d084b466ad7d94b80cecea83c3e3ba 577f7e7572c9296a79f22ca974dab6c7bf7ebead`; 772/577 ancestor checks, all 15 source hashes, clean frozen Agent/Runtime pins, normal producer lock, private graph/public exports, native imports, and exact two-selector discovery all passed.

Target row SHA is `469421c806bd502228d058d827d1f9b03abdc5dbc7c1e72123b5eb3bdf0e64b1`; outside-row SHA is `80009eca65cb605e9a97fa83b6a810de2180a4aef19cbdf7a9983f5286a73e5f`; P3 remains `48499e7d96c570ce32065d5e4981002d416a471c955ad83a17bda65c451668d1`. The mounted P1 body is byte-identical to base `12ef...`.

Cause is confirmed by retained author evidence: service `15187` failed its old direct `APP_HEAD = source` check on a synthetic snapshot HEAD; the corrected branch uses exact source or exact complete parent-list equality while retaining snapshot tree identity. Synthetic object recreation was not repeated because the object is absent and the task forbids Git writes/worktrees. Results `15187` and `28486` remain untouched failures. Live accepted/merged/refused execution is still unverified; manager owns one changed-original service run.

