# Handoff: P1/P3 exact-seven retired registration proposal

Status: **proposal PASS; no live operation authorized; source race requires refresh**.

This packet is limited to exact generated registrations at `tests/suites.conf`
lines 162–168 and their matching env files:

1. `agent-remotion-ap2-p1-f611-1346`
2. `agent-remotion-ap2-current-8c355-1402`
3. `agent-remotion-ap2-current-8c-cfa-1415`
4. `agent-remotion-ap2-current-583-cfa-1451`
5. `agent-remotion-ap2-current-583-9ce-1513`
6. `agent-remotion-ap2-current-98ef-259-1608`
7. `agent-remotion-ap2-current-bac-d9e-1643`

The proposal is exact-name based. It does not authorize retrying the refused
targets, retiring runtime directories, deleting anything live, changing a
guard, or changing any schema/API/behavior. The current protected
`agent-remotion-ap2-current-079-2a9-1743` row/env/runtime remains untouched.

## Review packet

- Proposed patch: `handoff-ap2-OPS-retired-registrations-1841.patch`.
- Machine-readable manifest: `handoff-ap2-OPS-retired-registrations-1841-manifest.json`.
- Original evidence directory:
  `handoff-ap2-OPS-retired-registrations-1841-evidence/`.
- Worker report:
  `../workers/ap2-OPS-retired-registrations-1841/report.md`.

The original full `suites.conf` is SHA-256
`07dfac86a0a63b3449a5d3393327ea95cc5688c342413fe1d9e323f3cfd9a330`.
At final recheck the live suite had SHA-256
`b53dde1222f2625f4c5b81c45a126277dbdfde022cbf87b043092a161b6d7c95`; only
unrelated position 36 (`ap2-P3-gate5-h6-0348`) changed. The target rows and
protected rows/envs remained unchanged. This is an external source race, not
an owned mutation. Refresh and independently review the patch before applying
anything; do not apply the captured patch to the raced live file.
The patch is SHA-256
`5984d485a2840c780c00a6461e3d6cb98462cef21428e8a9bbc233d18bf18b6a`.
The manifest is SHA-256
`acb5cf9d2e4f989650e9dfd6eba98f53e89d45db835eeafad1f693091f777678`.

The private-baseline verifier confirmed that the patch applies only as one
seven-row suite deletion hunk plus seven exact env-file Delete File hunks.
The normalized hash of all non-target suite rows is identical before and
after. Protected rows, the current row 169 (which becomes proposed line 162),
general remotion rows, and protected env inputs are byte-invariant.

## Use-status classification

The seven historical registrations have completed runtime receipts and
refused retirement records, but no exact reference in pending queue metadata,
manager-running metadata, test request metadata, or active worker metadata.
Historical worker briefs/reports contain completed evidence references; those
are not active use and were retained. The protected current tuple has two
later worker records and is excluded. The runtime directories remain present;
no process, daemon, lease service, or dependency operation was performed.

This evidence is sufficient only for Runtime’s independent review of the
registration scope. It does not certify whole-host idleness. A final normal
guard/activity recheck is required before any supported lifecycle request.
