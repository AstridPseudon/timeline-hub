# Next ordinary Agent source — frozen for normal generation

Agent owner gate, 2026-10-20 14:20 UTC. This freezes the source input for a NEW normal Runtime candidate. It does not release a version, authorize a consumer pin, or mutate public 0.2.13.

- Agent source: `tl/agt-m2-next-ordinary-current-core-gate`, commit `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3`, tree `c5a8a3ec7e9e01c61c5ae31834da53bed4be406a`.
- Canonical source: `astrid/core/timeline/schema/edit-command.schema.json`.
- Raw schema SHA256: `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.
- Canonical JSON SHA256: `63ac77b3c3e2c582f76ab4b2499be5011ea4836e8c92264b1938632b3bfacba7`.
- Complete 55 definitions / 29 operations; public S2 48/22 preserved. No private materialization carrier, partial schema, or caller-authored authority added.

Independent final review: design/agent-next-ordinary-final-review.md. Exact source passed 5 F1 unit, 25 native inverse, 103 parent-auto guard, 14 native parent-auto/retry/undo/redo/stale-zero-write, 2 birth/text joint, 2 media inverse, and 34 compatibility-floor tests. These counts overlap prior source reviews and are not full-suite evidence.

Runtime may normally generate its next ordinary candidate from these exact bytes on the current safety server. Publish a NEW immutable candidate tuple (server/source, contract/schema/client/artifact identities and normal package QA); keep existing 013 untouched. Consumer pin and adoption remain gated on the real paired current source and normal generated artifacts. No public 014 release or pin is claimed here.

App capture/golden sources are the existing native modules and tests in this commit. Parent auto is source-ready but still requires actual task/output/approval/continuation binding and durable requester qualification; no legacy writer may retire from the source tests alone. Selected-PARAM original-authority/WC4 is a separate compatible source unit still under review, not part of this freeze. Scene/save-core and current safety descendants may compose without schema mutation, with exact final consumer SHA and paired tests recorded anew.

