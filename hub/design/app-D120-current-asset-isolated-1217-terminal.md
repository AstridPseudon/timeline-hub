# D120 current isolated registerAsset terminal

Service `app-pin-34d46445-d73-p2-register-asset-34d46445-submit-1025122001-8974` completed PASS with exit 0 in 204 seconds; D66 duration was 199.166 seconds. The preflight service passed first on `app-pin-34d46445-d73-p2-register-asset-34d46445-submit-preflight-1025121931-5383`.

Readiness: PASS, 1/1, `tests/e2e/local/three-products.mounted-readiness.spec.ts:268`.

registerAsset: PASS, 1/1, `tests/e2e/local/three-products.p2-elements-assets.spec.ts:1133`. The original test reached all assertions, reload, history, and guarded native Undo. There was no unmet predicate.

Outputs:

- XML: `d66/readiness.xml` (SHA-256 `06739d2d28de7ff3e67cfba3b01e0b25ce5861d41a39c368173436f9a3243e86`); `d66/p2-register-asset.xml` (SHA-256 `48d8e860da172814af1ed95cf3c6acd33fb9e00eb773b95b9197368060705813`).
- Manifest: `d66/manifest.json` (SHA-256 `babaaa8eda80f24e1b40dd5dfbb4758728b65042c430d9437322b53bb8c8edb2`); test hashes before/after were unchanged.
- Profile: Node 20.19.4, npm 10.8.2, schema `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`, protocol `workspace.v1`, Runtime `AstridRuntime/0.1 Python/3.13.16`, provider `astrid-v1`, compiler `authoring-bundle-1`.

Diagnostics searched by filename: `d66/runtime-private/p2-commit-phase.jsonl` (57 records, request 1) and `d66/runtime-private/launch-2bcea480-bcb1-4e77-b116-3c5303dc2672/p2-commit-phase-2.jsonl` (128 records, requests 1–4), plus `runtime.stderr.log`, `runtime.stdout.log`, and the corresponding `launch-2bcea480-bcb1-4e77-b116-3c5303dc2672/runtime.stderr-2.log` and `runtime.stdout-2.log`. No retained phase file contained a reason, class chain, redacted frame file-line-function, or correlation field. Stderr was inspected only by filename/size; no raw diagnostics, auth, body, URL, or private stack was exported.

No product, test, pin, generated, manifest, registry, kit, or shared-dependency files were changed.
