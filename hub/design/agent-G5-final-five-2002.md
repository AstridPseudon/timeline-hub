# G5 final joined five — 2002

Status: **DRAFT; P1 remains gated.** This was a harness-only correction on
Agent f27d; no product or test source changed.

## Qualification

The exact five explicit node IDs were collected and executed once. The
collection removed the erroneous `-m integration` filter and selected **5/5,
0 deselected**. The execution produced **4 passed, 1 setup error in 92.81s**:

1. `test_checkout_reload_undo_cli_redo_uses_retained_history` — PASS.
2. `test_open_bundle_keeps_http_rows_raw_and_round_trips_canonical_images` — PASS.
3. `test_retained_restore_does_not_reopen_consumed_draft_steps` — PASS.
4. `test_catalog_recover_uses_real_http_and_preserves_closure_before_revision_restore` — PASS.
5. `test_restructure_whole_inverse_redo_and_intervening_overlap_refusal` —
   ERROR during fixture setup at `tests/sdk/test_timeline_restructure.py:359`.

The final fixture assertion observed that `runtime_protocol.__file__` came
from `/home/user/work/wt/rt-pin-2a9e347f` while `use_runtime()` selected a
temporary authentic-archive checkout. The c271 test body and all its
assertions were unreached. This report assigns no source or Runtime ownership;
it records the exact harness/fixture identity mismatch. No retry was made.

## Identities and preflight

- Agent: commit `f27d524798b14d11bcbe654ce7eee49d47e0b739`, tree
  `cf7395cc986fab4d9c6feb48b5a0be69ef7eac30`.
- Runtime execution: commit `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`, tree
  `f79a2355cfb39d9ada7721978bd20d5702105778`.
- Frozen client producer freshness: `/home/user/work/wt/rt-pin-34eac004`,
  commit `34eac0041b0891e9011966b39bcbd26053fde5bc`, tree
  `9853574865f25e08284e82ffb26c0bdecaa16a30`.

Report-all passed with archive SHA-256
`2915bd4ac0d46954d19c30f87a517b82074218699978e650fab03fcba81b72d3`, schema
31, restored head pair `a3e671256f1c42b8837d3e118c97b21b` /
`txn-11c90075be6c4c8bb9e2627366f0fe4f`, 3 shots, 3 internals, 5 CAS media,
registry/null/raw/opaque/legacy-word coverage, and credential scan 0. Source,
outside-file, whitespace, vendor, artifact, and all five AST/body-lock checks
passed. Vendor freshness was checked against 34eac, never against execution
2a9e.

## Packet

The complete lossless packet archive is
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-final-five-2002/evidence/g5-final-five-2002-packets.tar.gz`.
It has 61 members, 4,794,006 bytes, and SHA-256
`a44b8b3af9077e085828e307351ce39eb81979c083713f31e03576fa59485ea8`.
The packet manifest is adjacent at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-final-five-2002/evidence/packet-manifest.json`.
It records the retained actual request/context/prepared/private/original/
landing/history/native/effects/bindings/dependencies/pins/canonical/reply/
receipt/error/guard/path/base/theirs and SQL/head/history/origin evidence where
available. Child observer results: 56 entries, 56 exits, 0 seam exceptions, 0
observer failures, 0 origin mismatches.

## Reused evidence and limits

The already-qualified 1957 joined-58 guard result (58 passed, 21.88s),
independent code70be/1944 PASS143, and oracle68fbe/1948 no-weakening PASS1
were reused without rerunning. No full suite, extra FOUR/c271 run, P1/P4,
browser, prohibited lane, installation, marker edit, skip/xfail, guard waiver,
source/Runtime/pin/generated/Git change, merge, or activation was performed.
