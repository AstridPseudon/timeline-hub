# U4p/U3 D141 handoff

Tool-only final adoption is ready for manager review/normal merge.

The normal App diff is exactly:

- `public/install-manifest.json`: generated Agent pin `28e56cacb42d3da85b02e5b3543895b44f3d0f70`, Runtime pin `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d`, unchanged schema digest `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`.
- `vendor/astrid-browser/provenance.json`: generated from Agent tree `2ebe2ddf5a61f013953ab1e21d51ebaab746e58`; 160-file set and payload bytes match private generation and direct source custody checks.

Agent and Runtime qualified checkouts were clean at the exact dispatched commit/tree identities. Runtime mapped14 and prior independent Runtime source proof were reused; runtime.lock, generated clients, schema, tests, config, and all non-vendor/manifest App paths are unchanged. No source producer, shared cache, branch/ref, or Git metadata was written.

The detailed peer receiving-inputs note was not available in the synchronized ORCH/design paths during this run; the lead relay was the recorded authority and this availability gap is disclosed for manager handling. No final proof/REG0/ZIP/MAIN GO claim is made.
