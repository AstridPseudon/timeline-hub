# Runtime delivery README inputs

Updated the existing delivery inputs for the 2026-10-21 snapshot:

- `orch/delivery/README.template.md` now makes the rendered per-repository
  pins authoritative, gives explicit one-route-only linearized patch or bundle
  application instructions, and keeps all `delivery-build` placeholders.
- `orch/delivery/gate-results.md` now distinguishes current public013,
  qualified-but-not-adopted ordinary014, and isolated private15; records the
  seven gates as scoped PASS or OPEN results; and states the Linux, macOS,
  physical-parity, owner-film, adoption, and final-ZIP limits.
- The frozen installed carrier, scanner path/hash, owner-instructions
  path/hash, and exact `--extra` arguments are retained. The prior no-extras
  dry run and private-stage extras proof are not promoted to a final Gate 7
  result.

No product repository or shared dependency was changed. No four-repository
repeat, full suite, browser, renderer, owner-film scan, macOS check, or final
ZIP build was run.
