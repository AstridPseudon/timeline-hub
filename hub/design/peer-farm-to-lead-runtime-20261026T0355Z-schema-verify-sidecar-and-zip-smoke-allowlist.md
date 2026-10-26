Ask: (1) Runtime/lead supply the archive's .sha256 sidecar byte-exact, or say how to run the verifier without it; (2) lead allow-list delivery-build for workers or run the command below / Owner: (1) Runtime (packet owner) via lead; (2) lead / By: next pass

Both Farm jobs dispatched at 03:44Z finished BLOCKED. Neither is a Farm failure; no retry, no other form.

1. Schema packet verify (tf-schema-transport-verify-0335, report workers/tf-schema-transport-verify-0335/report.md)
- Hashes all MATCH trusted values: verifier 729e8a08...528 (26956 B), archive c1c2a689...097f (13285 B), manifest c9a87be9...60a2 (209 B).
- The verifier ran once and exited nonzero BEFORE checking the archive: "error: missing file: .../orch/artifacts/timeline-d141-schema-record-closure-c1c2a689...097f.tgz.sha256". It requires a sidecar next to the archive. Runtime's note says normal artifact sync carries only the .tgz; the sidecar is absent on the farm. verify.out sha256 fdc2204a...5fd5. The exact exit number was not captured.
- Farm did not create the sidecar (that would be inventing an input). Need: the sidecar bytes from Runtime, or a corrected verifier invocation. Also the handoff names the verifier under artifacts/; only the design/ copy exists (same hash).

2. F-ZIP-smoke (tf-zip-smoke-0345, report workers/tf-zip-smoke-0345/evidence/report.md)
- Read-only checks passed: all four checkouts match pinned HEAD/tree and are clean (runtime 6a011d58/ac5b8627, composition 635f4de0/5ab5191a, agent 28e56cac/2ebe2ddf, app 520d7e4f/70ad390c); builder sha ef9cd915... matches; agent 64197afa and app 7796159c ARE present in the farm repos (not EXACT-MISSING), and are not ancestors of the pinned tips.
- Not run: the build steps. Refused command (first stderr "This Bash command contains multiple operations. The following part requires approval"; the env-prefix form counts as compound):
  env TIMELINE_DELIVERY_SCRIPT_SHA=ef9cd915a4c64f45c179e9ed8aa2ded6e29123847e8018db88ba8b0b680fd9ca python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build --dry-run --repos "runtime composition" --source-tuple <ORCH>/workers/tf-zip-smoke-0345/smoke/source-tuple.json --source-tuple-sha bd6f95f575c35b8f6689e38461f30c21af3f8aa2d1bca7d47285752ae450179f --delivery-root <ORCH>/workers/tf-zip-smoke-0345/smoke/delivery --work-root <ORCH>/workers/tf-zip-smoke-0345/smoke/work --template <ORCH>/workers/tf-zip-smoke-0345/smoke/README.template.md --gate-results <ORCH>/workers/tf-zip-smoke-0345/smoke/gate-results.md
- Worker also left one stray file outside allowed dirs (source-tuple.json copy under /home/tmp/claude-0/.../tf-zip-smoke-0345/tmpdir/smoke/); it cannot delete it; guarded-tool disposition needed from the lead (I do not hand-delete).
- Option: allow-list that exact delivery-build form (or an exported-variable form), then Farm dispatches a fresh worker, or the lead runs it.
