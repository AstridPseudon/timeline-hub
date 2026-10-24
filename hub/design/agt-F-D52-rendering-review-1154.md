# D52/G4 Rendering Review

**Verdict: SOURCE FAIL, bounded to action gating.** Source attribution passes; the next-action wording must explicitly honor the active 10:16 hold.

- Exact membership: **23 nodes across 11 files**, matching the classification:
  - conformance: 6
  - service: 3
  - freeze: 1
  - Remotion host session: 1
  - Three.js: 6
  - builtin: 1
  - ffmpeg: 1
  - Remotion contract: 1
  - adapter: 1
  - Remotion backend: 1
  - stage1: 1
- **14** nodes have retained `runtime_protocol` attribution: service (3), freeze (1), host (1), Three.js (6), builtin (1), ffmpeg (1), and Remotion backend (1).
- **8 unknowns** are correctly identified: six conformance cases, adapter, and stage1. Their retained evidence ends at missing result files or generic return-code/stderr reporting; no child cause was invented.
- The single Remotion-package mismatch is correctly tied to the stale `255b` selected runtime. It must remain distinct from the immutable corrected `819acf` profile; the corrected profile does not establish that the 14 runtime-protocol cases are fixed.
- Caller/input spans are supported:
  - conformance transport and SDK delegation: `test_conformance.py` 74–101, 132–139; `sdk_render.py` 44–48
  - service: `test_service.py` 949–1228; production `service.py` 1905–1946
  - freeze: 163–190
  - host: 18–38, 241–315
  - Three.js: 67–119, 176–428
  - builtin: 188–255
  - ffmpeg: 260–282
  - Remotion contract: 49–215
  - adapter: 81–142; production adapter 291–300, 453–466, 533–549
  - Remotion backend: 113–158, 672–700
  - stage1: 172–236
- Production callers are present: service/SDK use `CommandTransport`; adapter/stage1 use `run_executor`. No dead-code credit is justified.
- Historical scope remains intact: 276 total failures/errors, with no original-267 closure, no D32 pre-existing credit, and no dead-scope/deletion proof.
- The report’s requalification recommendation must be conditional: the existing 10:16 auth/schema/child-admission hold remains active. No rerun, overlay, setup waiver, remote-provider deferral, acquisition, or alternate child request is authorized. After owner clearance only, use meaningful changed input and capture child stderr, return code, argv, cwd, and result-file state; do not blindly rerun unchanged inputs.

The v2 request/response contract remains preserved, including the production-caller requirement and durable receipt/dry-run/conflict/invalid-command fields.

Checks performed:

- `git status --short --branch`: clean.
- `git diff --check`: passed.
- Target branch identity verified at `8c223d77fef71e52b1bdc42f205c82af5cfc5d25`; unrelated two-file diff only.
- No tests, source execution, environment/render/process execution, live calls, or new evidence gathering performed, per task constraints.