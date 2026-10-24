# H30 census reconciliation

Updated evidence: [agent-D32-current-node-reconciliation-H30.json](/home/user/work/wt/agt-F-census-reconcile-0350/agent-D32-current-node-reconciliation-H30.json)

- Total original nodes: **267**
- Confirmed closed: **136**
- Open: **131**
- Held/unknown: **131**
- Newly closed since 0118: **0**
- Authorized full-267 PASS: **none**
- Farm checkpoint: **pending**

All 267 IDs remain tagged `ours`; exact body/assertion mappings and proof references are preserved. Source-only, aggregate, installed-unqualified, stale, and failed evidence received zero original-node credit.

Active owner counts:

`Viewing/H30 failover 33; Agent fixture780a+independent2257 22; Agent helper review 13; Agent G2/G3/G4 13; Runtime isolated child-import 7; Agent F-R2 7; Viewing render-wire 6; Agent G5 5; Agent SDK fixture 4; Agent D09 3; Agent CLI fixture 3; respective task owner 2; Agent F-capture 2; Agent F-schema 2; Agent external-trust 2; remaining singleton owners 7.`

H30 Viewing failover is an exact **33-node** subset covering:

- `test_native_sheet_current.py`: 24 nodes
- `test_cli_native.py`: 7 nodes
- `test_scene_dispatch_contract.py`: 2 nodes

Viewing owns the cluster; Agent owns home merges; no local source author was assigned. Exact IDs are recorded in the JSON.

Current integration:

- Commit: `252cf33d02184abcba4664634802291cfc791ca3`
- Tree: `1660dfef13b27e253d21b3ff5e0a3daea21ae967`

Validation:

- `python3 -m json.tool agent-D32-current-node-reconciliation-H30.json` — PASS
- Custom census validation — PASS: 267 unique IDs, 136/131 status split, 33 H30 nodes, owner totals sum to 131
- No tests, full suites, browser/HTTP runs, or original body reruns were performed per task restrictions.

Known limits include the current ABA service failure, alias fork-ID failure, image foreign-setup error, unqualified D40 external-positive result, historical last-owner failure, and render/H3 mechanism-only evidence. U2c readiness failures remain outside the original 267 unless exact membership is proven.

`commit-msg` and `DONE` markers were written.