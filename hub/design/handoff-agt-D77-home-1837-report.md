# D77a G4/V3/F mounted integration qualification

Verdict: **PASS for the bounded D77a mounted-integration scope**.

## Source and home custody

- Actual Agent `tl/integration` HEAD: `a86e4ae79ee34ea509dcf92f30da6cdcca98156c`; tree `f6664b44289647cf09f824cd648d028b5ca30cd5`.
- Normal merge receipt: `a86e4ae79e` merges `dfea1e17b7ed227b73bcb06aa9b334f9edc2fb5d` into prior home `263696c832`.
- Reviewed source commit: `dfea1e17b7ed227b73bcb06aa9b334f9edc2fb5d`, parent `2a1637a1438ec7c373ce369097bfa9a9ec03f997`, tree `5c1be2ae863394457a93c2f9254eeecb26a87979`. The source is present in actual home ancestry and is also the reviewed D77 branch source.
- Source path custody is exact: 10 changed paths, prefix length `10`, and no other D77 paths. Every integrated blob is byte-identical to the reviewed source blob; the exact Git blob map is in the companion commands export. `git diff --exit-code dfea1e17b7 HEAD -- <these ten paths>` passed.
- Agent module origins under the qualified environment resolve to this worktree; `runtime_protocol` resolves to the exact Runtime checkout below. No worker changes were made after the merge; `git status --short` was empty.

## Pins and canonical inputs

- Runtime checkout: `/home/user/work/wt/rt-pin-327da207`, HEAD `327da207ed30880fe2ae0cd0b116722bb2c6f7a6`, tree `0140a9ab2bf8582c4712dbf84498a6d5dcb132cf`.
- Agent canonical schema SHA-256: `4d74a4ae34fcfa89ce66e4ccad90a3871a3ef9d3adb26c9219ae7dec72deb3bd`; `runtime.lock.json` carries the same pinned digest.
- Runtime contract SHA-256: `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`.
- The source review records all 197 shared dependency hashes unchanged; this qualification did not alter or regenerate dependencies, pins, generated clients, registries, schemas, or contracts.

## Bounded tests

Qualified command environment: `PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-327da207:/home/user/work/wt/rt-pin-327da207/packages/python`, `ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-327da207`, existing `/home/user/work/venv-agent`, `PYTHONDONTWRITEBYTECODE=1`, pytest timeout 45 seconds, no cache provider.

1. Exact independent adversarial membership/selection from the reviewed security packet: **34 passed, 134 deselected, 10 warnings, exit 0**. It covers foreign origin/owner, integrity, mutation, missing and foreign references, invalid/nonfinite JSON, canonical-reader enforcement, changed installed content, schema archive fallback refusal, non-isolated interpreter refusal, and strict probe.
2. Named positive probes: `test_staged_canonical_schema_reaches_strict_consumer` and `test_registry_readiness_qualifies_actual_canonical_transport_projection`: **2 passed, 1 warning, exit 0**.
3. `git diff --check`: exit 0.

Raw XML/log files and exact commands are exported beside this report. The independent reviewed 228-case source qualification remains reused by exact reviewed source: **228 passed, 66 warnings**; it was not duplicated here.

## Existing R2/C0 receipt

The existing literal-home4 R2/C0 receipt is referenced without rerun: [`workers/agt-R2-reply-home-1827/report.md`](../workers/agt-R2-reply-home-1827/report.md), with authentic XML [`handoff-agt-R2-reply-home-1827-test.xml`](../workers/agt-R2-reply-home-1827/evidence/handoff-agt-R2-reply-home-1827-test.xml). Its receipt is `4 passed`, exit 0, on Agent `263696c832` and Runtime `327da207`; the reviewed test blob and production caller evidence remain unchanged.

## Scope limits

This is not an authentic installed render, browser, HTTP, child-process, acquisition, network-bootstrap, schema-acquisition, or D13-body qualification. The final installed-render gate remains pending with Runtime/coordinator. The D67 environment gap is unchanged; no fixture/tooltuple was fabricated, and the pre-existing unknown receives zero D77a credit. No candidate-only home label is used.
