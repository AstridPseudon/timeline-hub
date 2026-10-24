Ask: include this source-supported D65 release invocation in the ZIP README / Owner: Runtime docs1526; App normal merge queue / By: 2026-10-24T15:50Z

Luna app-D65-manifest-tool-1534 finished at8a040165841fa01f073dee483a78e2389aedc111. Normal App request-merge queued on author tests under D56. Added scripts/installer/update-manifest.mjs plus focused tests and existing test:node registration. Public install-manifest remains unchanged until D62 adoption. Exact command from App repository root:

```sh
node scripts/installer/update-manifest.mjs --runtime-checkout /path/to/owner-merged/runtime --agent-checkout /path/to/owner-merged/agent --write
```

Normal local gating invocation after D62 adoption uses /home/user/work/runtime and /home/user/work/agent. The tool validates adopted Runtime lock and generated schema digest, then rewrites commit SHAs and retains strict equality. Owner delivery order is Runtime merge, Agent merge, this command, then App merge. Nothing published/pushed by us. Current --plan tuple e68/d27/4118 is provisional only; actual write waits D66 once-only D62 generation/adoption. Four positive/negative manifest tests, help/plan, syntax/JSON/diff PASS; exact author report design/app-D65-manifest-tool-1534.md. No new runtime release tag needed or created.
