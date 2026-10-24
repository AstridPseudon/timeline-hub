# E-plan: making the edit and history internals elegant (owner-approved 24 Oct 19:55Z)

**Goal:** keep today's model (one writer, immutable history, undo as a commit, field merges, server-side attribution) and remove the accidental complexity around it.

**Timing (PAUSED 20:20Z by D83 until the ZIP; resumes after delivery):**
- **Now:** design and prototypes, in parallel and NON-gating. They never take a slot from a critical row (D80), never merge into tl/integration, and never change the final tuple.
- **After the ZIP:** implementation lands as a follow-up patch set (E-ZIP), proven by the same gates.

| Row | What | Model | Deliverable now (a design doc in hub/design, plus an optional prototype branch) |
|---|---|---|---|
| E1 | **One shared Python rules module that both Agent and Runtime import** (both are Python). No DSL and no code generation. | Luna (inventory) → Sol (design) | Inventory every rule implemented twice today, with file:line on both sides and the divergences found on 24 Oct (recorder_abi, inverse timeline root, popup observation/owner, private cache). Then which side's version becomes the shared one, the packaging (inside Runtime, imported by Agent), a migration order and the conformance test (it reuses the D79 replay corpus). Success = fewer lines. |
| E2 | **Retire the legacy ABI1 format.** | Luna | Inventory every ABI1/legacy branch, plus a one-time history migration design (convert legacy entries to v2 records with honest `legacy_unknown` where facts are missing). List what code is deleted afterwards, and how undo is gated for converted entries. |
| E3 | **Prune custody to what one writer needs.** | Luna (audit) → Sol review | For each safeguard (physical bindings, reserved-ID provenance, alias re-resolution, CUSTODY prefixes), say what threat it covers now that Runtime is the sole writer with authenticated history, and recommend keep, simplify or remove, with the tests that prove each. |

**Rules:**
- Codex does the work; Luna by default.
- No product source is merged before the ZIP.
- Each doc ends with: size in worker-hours, risk, and the gate that proves it.
- The orchestrator reviews the five docs and sends the owner one consolidated proposal.

**Trimmed 20:02Z (owner asked whether this is over-engineered):**
- E1 is a shared module, not a spec language.
- E4 (history panel) is a product feature, out of scope here; the owner decides it separately.
- E5 folds into the P4 profile and fix.
- Every remaining row must REDUCE total lines of code.
