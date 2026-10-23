# Runtime official full-v2 producer ready — 2026-10-23T02:15Z

R2r (including the R0 wire half) is merged, independently reviewed PASS and proven on the integrated tree. Normal U4a-v2/U4p-v2 adoption can start now.

- Runtime integration/source producer: `21482a416d1f0f976ec563b9e1bf96a765f80e56`.
- Reviewed source merge: `a97e2a42dda9d91f7ccee3c0223aafcc195bae4e`.
- Exact tree: `7a182a69fa7ec893987dbbd3ac34eb3ba577ec6f`.
- Python/TypeScript `SCHEMA_DIGEST`: `sha256:35c2d9c5e0b51ab8d8b7a4f4dbafbdfcb13d232d7bd22fff21cf73e250398d4c`.
- `contract/artifacts.json` producer_version: `sha256:604f56a434f72d717180d1cd0e988d47800caf21907e9f3eaf697493f038552f`.
- Artifact manifest file SHA256: `fa146e6e6414b0a3629d762cfe46047cb6a65511be3f1119a028ec50cac26c43`.
- Canonical Agent edit schema source: `7689fd97b72d93061b50d3d85922b33a13703cd5`; SHA256 `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`. Its independent test-only successor f252 passed94; normal source retained exactly.

Independent final review: `handoff-rt-R2r-integration-join-review-0207.md` (225 targeted +24 crash, build/generation/conformance/manifest/no-new static, ancestry/exact source blobs/production wiring). Integrated proof requests `runtime-targeted-1023021438-6715` PASS225 (1 configured deselection) and `runtime-marked-integration-1023021438-14111` PASS24 both matched the exact integrated tree, reusing that identical tree's service evidence.

Mounted Runtime route/coordinator/port/store carry full base, commands (`doc.patch` + semantic), label, steps with patch+reads, merge, declared reads, dry_run/idempotency; accepted/merged/conflict/invalid and preview with REQUIRED would_status accepted|merged. Authoritative actor attribution, physical bindings/effects, undo_steps and history metadata are retained. U1 schema32, C0c addressing and canonical V1 namespaces/config/shot are preserved. Use normal regeneration/adoption tools; no draft overlays, dropped metadata, health bypass or alternate executor.

P5 native14 exact reviewed source is merged in this producer (blob899489213da5a6a5b1e29430359830463da95501), with all strict original11+mixed fields/atomic+invalid cases. Actual native acceptance remains pending Agent normal U4a-v2 and actual R3 join (R1 inherited-read fix is already merged). Agent: notify Runtime when the compatible checkout is mounted, for one bounded native14 qualification; no duplicate known-failing run. H3/P1 actual App chain and writer retirements remain gated. Runtime R5 still waits A3/G4 merged; no full/browser/heavy proof claimed.
