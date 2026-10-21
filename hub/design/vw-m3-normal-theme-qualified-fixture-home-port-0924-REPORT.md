# Agent HOME gate — qualified normal Theme fixture port

Current HOME had no equivalent of the qualified 0913
`test_generic_host_normal_imported_theme_reaches_props_and_rejects_local_source`.
The worker port is one file only:

```text
tests/integrations/test_generic_host_remotion_render.py
```

It carries the exact qualified test and only its required fixture/import
seams. The assertion map is the ordered imported descriptors and one captured
normal SDK admission; managed `theme.json` materialization; one resolver;
Root explicit Theme props; omitted builtin/default separation; and forged
caller-local source refusal. Actor/worker credentials, empty registry,
private fixture dependency copy, and scoped `ASTRID_PACKS_PATH` restoration
are retained. No product/API/DTO/pin change is present.

Central evidence reused (not rerun):

```text
vw-m3-theme-reviewed-context-one-proof-0913-integration-viewing-theme-normal-props-reviewed-context-one-proof-0913-1021091621-2747
1 passed in 110.30s, exit 0
log sha256 43fc1408974cc1e66ad9575409bf26d86d90248ae1a571d18a9990a66a9d462a
central snapshot tree 58d9ca46ee80316647c774f9e8a2c9025b9c62a9
```

Worker source SHA-256:
`39c4260d2868df9781b1a543fb5d8c1a1721264e37e1ee8fab820ee5a6c6772f`

Projected final tree after the harness commits this one-file patch:
`a2516f71a2e28af47e09dddde628f8e98b3aea27`.

The harness commit SHA is intentionally pending because workers do not commit.
After harness completion, record `git rev-parse HEAD` as the final commit SHA
beside the unchanged projected tree above.
