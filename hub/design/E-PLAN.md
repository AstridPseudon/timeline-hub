# E-plan: making the edit and history internals elegant (owner-approved 24 Oct 19:55Z)

**Goal:** keep today's model (one writer, immutable history, undo as a commit, field merges, server-side attribution) and remove the accidental complexity around it.

**Timing:**
- **Now:** design and prototypes, in parallel and NON-gating. They never take a slot from a critical row (D80), never merge into tl/integration, and never change the final tuple.
- **After the ZIP:** implementation lands as a follow-up patch set (E-ZIP), proven by the same gates.

| Row | What | Model | Deliverable now (a design doc in hub/design, plus an optional prototype branch) |
|---|---|---|---|
| E1 | **One rule definition for Agent and Runtime.** A single declarative spec of commit rules (bindings, reads, conflict and inverse guards, recorder ABI), with Python validators generated or shared for both the Agent recorder and the Runtime validator. | HARD Sol (design) + Luna (inventory) | Inventory every rule implemented twice today, with file:line on both sides and the divergences found on 24 Oct (recorder_abi, inverse timeline root, popup observation/owner, private cache). Then the target spec format, the generation/sharing mechanism, a migration order and a conformance test plan (it reuses the D79 replay corpus). |
| E2 | **Retire the legacy ABI1 format.** | Luna | Inventory every ABI1/legacy branch, plus a one-time history migration design (convert legacy entries to v2 records with honest `legacy_unknown` where facts are missing). List what code is deleted afterwards, and how undo is gated for converted entries. |
| E3 | **Prune custody to what one writer needs.** | Luna (audit) → Sol review | For each safeguard (physical bindings, reserved-ID provenance, alias re-resolution, CUSTODY prefixes), say what threat it covers now that Runtime is the sole writer with authenticated history, and recommend keep, simplify or remove, with the tests that prove each. |
| E4 | **History and undo UX.** | Luna | A design for a history panel (who/what/when per step), a blocked-undo explanation ("blocked by <entry>") with an "undo both" option, and conflict drafts shown as a merge prompt rather than silently held. Use App's existing components; mockup-level only. |
| E5 | **History read performance.** | joins the P4 ten-note profile (critical, Runtime) | From that profile, an indexed or incremental-verification design for history reads. The critical P4 fix comes first; E5 is the durable version. |

**Rules:**
- Codex does the work; Luna by default.
- No product source is merged before the ZIP.
- Each doc ends with: size in worker-hours, risk, and the gate that proves it.
- The orchestrator reviews the five docs and sends the owner one consolidated proposal.
