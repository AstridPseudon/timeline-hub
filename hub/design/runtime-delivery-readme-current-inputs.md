# Runtime delivery README inputs

Updated the existing delivery inputs for the published014 2026-10-21 snapshot:

- `orch/delivery/README.template.md` now makes the rendered per-repository
  pins authoritative, gives explicit one-route-only linearized patch or bundle
  application instructions, and keeps all `delivery-build` placeholders.
- `orch/delivery/gate-results.md` now records the published014 producer/server
  distinction and the Agent091/App3be/Composition13 consumer tuple; it keeps
  the seven gates scoped PASS or OPEN and states the Linux, macOS,
  physical-parity, owner-film, global-consumer, and final-ZIP limits.
- The frozen installed carrier, scanner path/hash, owner-instructions
  path/hash, and exact `--extra` arguments are retained. The prior no-extras
  dry run and private-stage extras proof are not promoted to a final Gate 7
  result.

The README also distinguishes the tree-preserving synthetic commit made by a
linearized patch from the immutable Runtime producer `95bd…` and retains the
existing Runtime bundle/producer-checkout byte-check route. It documents the
tested private installed Runtime/client/Agent carrier and
`astrid-runtime up --profile astrid` separately from generic neutral Runtime
commands. No lock rewrite, provider fallback, registry publication, physical
or parity claim, owner-film result, or final ZIP claim was added.

No product repository or shared dependency was changed. No four-repository
repeat, full suite, browser, renderer, owner-film scan, macOS check, or final
ZIP build was run.
