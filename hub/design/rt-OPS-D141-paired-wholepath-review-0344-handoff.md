# Handoff

## Verdict

FAIL. Do not CAS-install or authorize this candidate.

## Supported source-level interface

The candidate's normal caller contract is the existing `test-run` request
directory under the orchestration root: `repo`, `suite`, `target=body`,
`files`, and `nocache`. The paired extension additionally requires
`pair=paired-admission-v1`, a distinct `pair_preflight_suite`, and an empty
`pair_preflight_files`. The runner performs one dispatch floor check, starts
the heavy trace/lease path, runs the preflight, and runs the body only after a
successful preflight under the same process/trace unit.

This is only a source-level supported interface. The review found no genuine
D66 `--submit` controller receipt or registered pair. The synthetic
`D141g-paired-control` path must not be treated as production authority.

## Exact historical binding

The App 0309 artifacts support only the prospective 520d tuple:

- target `app-pin-520d7e4f`, selector `p2-automatic-child-placement`;
- normal suite `d141g-p2-automatic-child-placement-520d7e4f-submit`;
- paired preflight suite with `-preflight`;
- body command SHA-256 `600fca0fa7852eac45179b2a485b9b160d4d807ebb752456e292636b69a85eaa`;
- preflight command SHA-256 `82f4ad3c8a4bc940c10d52c9b9bf230f49c59c7e8865a3c0144498e412cafe8d`;
- App head/tree `520d7e4fc12a03392afaed3f486aba34a2b5c319` /
  `70ad390c56b0e45d9279b4179598b6cdbad9ed65`.

The App source artifact explicitly says `registration=false`; it is not a
receiving release or body result.

## Installation/publication layout

The source-only manifest has five direct production files under `bin/`:
`d141-append-final.py`, `d141-disk-trace.py`, `d141-validate-receipt.py`,
`d141-validate-trace.py`, and `test-run`, mode 755. The private controls and
manifest are not published. The manifest's declared route is
`ORCH/bin/* -> hub/kit/bin/* -> receiving ORCH/bin/*`, with helpers before
`test-run`, existing hub-sync unchanged. No installation claim is made here.

## Required next steps

1. Fix the descriptor/inode custody and validator TOCTOU, with the requested
   symlink/FIFO swap control.
2. Remove or tightly bind `D141g-paired-control`; synthetic controls cannot be
   an installed production admission decision.
3. After App merge-forward to freeze-2 head `7796159ce894`, regenerate both
   commands with the same pure builder, obtain the genuine atomic D66
   registration, compare registered bytes before either part, and re-review.
