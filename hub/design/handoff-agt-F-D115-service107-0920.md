# D115 service.py:2524 exact-107 split

Read-only classification of the retained D108b run. No product, test, Runtime,
Agent, collector, or body-log edits were made.

## Accounting

- The authoritative join is `outcomes.json.nodes[].failure_location` containing
  `service.py:2524`: 107 unique node IDs, 27 `failure`, 80 `error`.
- The XML contains 9,269 testcase elements (the suite attribute says 9,442,
  which includes 173 subtests). The retained JSON reports 8,763 passed, 159
  failed, 347 error; those sum to 9,269.
- The body log has 219 textual `service.py:2524` markers because traceback/source
  material is repeated; it is not a node count. All 107 exact node IDs occur in
  the retained body log. `d102_discriminating_bytes_absent_ids: [3934]` only:
  ordinal 3934 has RuntimeErrorBase plus frames, but no retained message that
  identifies a guard or underlying class. No cause is invented for it.
- Exact selected nodes have 19 unique `source_sha256` values and 107 unique
  `failure_text_sha256` values. The per-group ordinal index is in the TSV.

## Disjoint root-cause / ownership split

The labels below are safe labels for the captured Runtime guard/message, not
raw stderr. Every group reaches the unchanged registered Agent provider at
`astrid/sdk/timeline/commit.py:1444` before Runtime authentication. Runtime
`runtime_protocol/timeline_commit_auth.py` is the strict authority and remains
unchanged; the bounded fix route is to repair the provider's prepared candidate
or recorded stage, then prove one RED/GREEN sample before the cluster.

| count | ordinals | captured boundary | smallest bounded route / owner |
|---:|---|---|---|
| 83 | 1297,1298,1301,1303,1305,1307,1310,1313,1317,1320,1322,1326,1330,1334,1357,1373,1411,1427,1442,1455,1468,1472,1476,1482,1488,1492,1497,1501,1506,1512,1520,1527,1529,1532,1535,1538,1541,1543,1547,1550,1555,1564,1584,1601,1618,1637,1653,1669,2370,2373,2375,2395,2399,2403,2404,2747,2756,2761,3625,3627,3943,3946,3952,3980,4309,4369,4394,4397,4585,4630,5216,5219,5257,5347,5429,5432,5436,5439,5509,5516,7527,7598,7611 | `auth.py:838`, effect image | Agent `astrid/sdk/timeline/commit.py` candidate/document assembly at 1419–1437; preserve Runtime effect-image guard. Sample RED: 1297. |
| 5 | 1211,1221,1234,1293,5667 | `auth.py:1755`, inverse native coverage | Agent `astrid/sdk/timeline/_step_undo.py` stage selection plus `commit.py` prepared-record assembly; do not relax native/effect coverage. Sample RED: 1211. |
| 3 | 1266,1270,1274 | `auth.py:535`, binding input image | Agent `astrid/sdk/timeline/commit.py` historical inverse/source-image reconstruction; compare with passing `test_timeline_inverse_historical_image.py`. Sample RED: 1266. |
| 3 | 3655,3691,3817 | `auth.py:1607`, inverse materialization turnover | Agent `astrid/sdk/timeline/_step_undo.py` inverse-stage materialization selection; keep physical turnover guard. Sample RED: 3655. |
| 3 | 7051,7053,7055 | `auth.py:1338`, inverse provenance attached to non-inverse | Agent `astrid/sdk/timeline/_step_undo.py` inverse-stage provenance partition; preserve command-kind check. Sample RED: 7051. |
| 3 | 3908,3913,3916 | `auth.py:1646`, inverse source image | Agent `astrid/sdk/timeline/_step_undo.py`/`commit.py` source-stage image selection; sample RED: 3908. |
| 2 | 2436,2438 | `auth.py:2243`, physical promotion image | Agent `astrid/sdk/timeline/commit.py` ordinary command output/materialization assembly; preserve authenticated promotion. Sample RED: 2436. |
| 1 | 3714 | `auth.py:1610`, inverse materialization owner | Agent `astrid/sdk/timeline/_step_undo.py` owner binding; preserve owner/physical-root relation. |
| 1 | 6978 | `auth.py:1329`, inverse provenance absent | Agent `astrid/sdk/timeline/_step_undo.py` stage provenance emission; preserve required provenance. |
| 1 | 8710 | `auth.py:2431`, sequential command metadata | Agent `astrid/sdk/timeline/_commit_preview.py` sequential capture, with `commit.py` caller; preserve prepared-candidate equality. |
| 1 | 3887 | `auth.py:2539`, sequential head input | Agent `astrid/sdk/timeline/_commit_preview.py` sequential original/landing capture; preserve authenticated head. |
| 1 | 3934 | Runtime store `timeline_commit_store.py:1434` after provider `commit.py:1444`; D102 discriminating message absent | **Unresolved / no fix dispatch.** Exact retained frames are present, but the cause bytes needed to choose Agent vs Runtime ownership are absent. Do not infer from the wrapper; only a separately retained prepared-record/D102 artifact could unblock. |

The 83-row effect-image group is one invariant and one owner route despite its
many test families. The remaining groups are disjoint by the first retained
strict guard/message boundary. Runtime guard source is evidence of the rejected
invariant, not permission to weaken the guard.

## Current comparator read

The current passing comparator seams read were:

- `runtime/tests/test_timeline_inverse_stage_authentication.py`, including
  current-agent inverse round trip and authenticated native membership;
- `runtime/tests/test_timeline_inverse_historical_image.py`, exact retired-image
  reopen and guarded tamper rejection;
- `runtime/tests/test_timeline_inverse_sequential_authority.py`, sequential
  inverse scope round trip and guarded mutations.

These comparators support the Runtime authority boundary and the ownership
routes above; they do not claim any D115 behavior fix.

## Validation

- JSON parse: PASS for retained outcomes and this handoff JSON.
- In-memory XML/TSV/accounting checks: PASS; selected 107, group sum 107,
  unique node IDs 107, body-log presence 107, missing discriminating D102 IDs
  exactly `[3934]`.
- In-memory Python AST parse/compile: PASS for inspected Runtime auth and Agent
  provider/helper source blobs.
- `git diff --check` on the composition worktree: PASS (no repo changes).
- Product tests, typecheck, lint, and full suite: N/A by the initial-read-only
  brief; no rerun was made.
