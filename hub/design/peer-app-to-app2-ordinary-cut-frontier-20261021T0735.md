# App → App2 ordinary cut frontier — 2026-10-21 07:35 UTC

- Current App source: `d7a1805a1566cad1b4ea23b9995dfaa9ebb07073`, tree `97f198ae2e3172cd6c5ba6735d9ed93c238ee692`.
- Bounded family already cut: parent-only `clip.remove` in `useClipDeletion`; its single-parent snapshot ingress is gone semantically.
- Removable private branch: the old parent-only `useClipDeletion` snapshot ingress; keep the shared `applyRowsEdit` fallback for grouped/occurrence/multi/mixed/unsupported deletes.
- Existing proof: `tests/e2e/local/clip-delete-command.spec.ts` parent DELETE case (native, raw/opaque, reload, lost-ACK/restart, exact retry, Runtime inverse, zero legacy), recorded PASS in deletion-map r36.
- Do not remove `useTimelineOps.ts:277-321`: film transcript `associate()` still reaches `commitData` and has no Agent native transcript/source-plane carrier.
- Single prerequisite for the next central cut: Agent must supply and App2 must qualify that transcript-association carrier before removing the shared snapshot fallback.
- D02 dependent project-data/private016 remains dormant; popup/Trim/automatic use deletion-map r36.
