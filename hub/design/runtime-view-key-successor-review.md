# Persisted-view key successor review

**APPROVE `44bf74420c1276aae86928f6b2416190fc97b1c7` relative to rejected `9db719c2f8bc24308c2506c3b61d4620bb1c6b2e`.** This review closes the prior P2 finding: the normal TypeScript conformance generator now requires and forwards the persisted-view idempotency key. The previously approved server/service authority and retained-view behavior are unchanged and remain accepted within the prior review scope. This is approval of the corrected successor as a release input; it is not approval of a final composed Runtime tree or consumer pin.

## Exact source and scope

- Successor commit: `44bf74420c1276aae86928f6b2416190fc97b1c7`
- Successor tree: `914d0ac3b0268696f9a43a9091e11b32415982ec`
- Relative parent: `9db719c2f8bc24308c2506c3b61d4620bb1c6b2e`
- Parent tree: `b7993c7d87913874ad28683a961adaa2ff6aa780`
- Changed paths: `tools/generate_typescript_conformance.mjs`, `conformance/typescript/generated.ts`, and `conformance/typescript/smoke.ts` only.
- `contract/openapi/workspace-v1.yaml`, `contract/manifest.json`, `contract/component-manifest.json`, `contract/artifacts.json`, and `generators/release.json` (private staging `0.2.12`) are byte-identical to the rejected candidate parent. No schema/version or artifact-manifest mutation was introduced.

The authoritative generator method and normally generated output both now declare:

```text
createTimelineView(projectId, timelineId, options, idempotencyKey)
```

and send `Idempotency-Key: idempotencyKey`. The plain `Record<string, unknown>` response, encoded route, and `JSON.stringify(options)` request body are unchanged. The generated output was regenerated through the normal generator; it was not hand-patched.

## Reproduction and evidence

I recreated the exact prior transport probe against private copies of the corrected package and conformance generated sources:

```text
node client-probe.mjs
=> 2 passed, 0 failed:
   packages/typescript/src/generated.ts sends the explicit view key
   conformance/typescript/generated.ts sends the explicit view key
```

The probe asserted POST, `/v1/projects/p/timelines/t/views`, `Idempotency-Key: view-key`, unchanged `{ formats: ["md"] }` JSON body, and successful plain response decoding for both clients.

I also reran the exact prior conformance TypeScript probe:

```text
tsc --noEmit --strict --module NodeNext --target ES2022 \
  --allowImportingTsExtensions conformance-key.mts
=> exit 0
```

That probe accepts the keyed four-argument call and consumes `@ts-expect-error` for the missing-key call. A separate package-client TypeScript API probe independently confirmed the same four-argument acceptance and missing-key rejection. The corrected conformance smoke compiled and ran successfully:

```text
tsc -p conformance/tsconfig.json --outDir <private output>
node <private output>/conformance/typescript/smoke.js
=> independent TypeScript conformance client smoke passed
```

The smoke's real generated-client transport assertion also passed, including encoded path, authorization, key header, unchanged options body, and unchanged plain response. The package client transport probe passed with the same assertions.

Normal-generation and invariant checks passed on the exact successor source:

```text
node tools/generate_typescript_conformance.mjs \
  --contract contract/openapi/workspace-v1.yaml \
  --schema-manifest contract/manifest.json \
  --component-manifest contract/component-manifest.json \
  --fixture-root conformance/fixtures --check 
=> exit 0

node tools/generate_typescript_conformance.mjs ... --output-root <private output>
=> generated client, metadata, component manifest, and all generated fixtures byte-match tracked artifacts

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python generators/generate.py --check
=> exit 0

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python scripts/artifact_manifest.py --check
=> contract/artifacts.json is current

git diff --check 9db719c2f8bc24308c2506c3b61d4620bb1c6b2e 44bf74420c1276aae86928f6b2416190fc97b1c7
=> exit 0
```

Same-tree evidence from the implementation worker was reused as requested: the 11-test generator/artifact/parity/release lane passed; the 78-test generated-client/parity/release lane passed; and the package TypeScript suite passed all 18 tests. No full suite, broad repeat, socket, browser, merge, publication, or pin operation was run for this review.

## Disposition and limits

The rejected `9db719c2` successor is replaced for release-composition purposes by approved `44bf744`. This approval covers the corrected generator/output and the two-client transport/type contract only. It does **not** claim final composed server readiness, Agent caller port readiness, App copied-client/pin readiness, or a final consumer pin. The release composer must include this approved successor together with the separately reviewed current Runtime inputs and rerun its composed release checks before publication.
