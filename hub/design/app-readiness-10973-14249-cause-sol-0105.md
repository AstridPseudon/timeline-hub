**Both runs failed at the bootstrap outbox wait, before any original P2/P3 case ran.** The changed P2 lifecycle shows cancellation followed by a restarted basis read. The smallest retained blocker is an unfinished verified-basis read with `/commits` requests lacking a captured response; the underlying daemon cause remains **UNKNOWN**.

No product or test changes, new runs, requests, services, or fixes. Four qualified evidence files were copied byte-exact into the assigned worktree. Commit message and `DONE` written.

**Actual results**

| Observation | P2: 10973 | P3: 14249 |
|---|---:|---:|
| Terminal result | exit 2 / 189s | exit 2 / 194s |
| Door port | 36707 | 45191 |
| Hosted port | 33851 | 37241 |
| Runtime port | 40029 | 45387 |
| Native fixture and authoritative history | PASS | PASS |
| Bootstrap connection and selection assertions | PASS | PASS |
| Outbox database existence checks | Seven false | Seven false |
| Bootstrap failure stage | `outbox-read` | `outbox-read` |
| Subsequent connected-selection / fresh-owner checks | NOTRUN | NOTRUN |

All six recorded ports are distinct. Native/history success belongs to the native preflight; it does not establish that the later browser’s basis request completed.

`bootstrapMountedBaseline()` reached the poll requiring an existing `astrid.command-outbox` database and a settled scoped owner. Both traces report its **5000ms timeout**. The wrapper then failed at `three-products.mounted-readiness.spec.ts:301`, expecting the initial readonly outbox status `verified` and receiving `unknown`.

The bootstrap page’s connection and selection passed. The outer leaf’s connection, verified outbox, selection equality, and fresh-owner observations remain **UNKNOWN**, with its later stages **NOTRUN**. The D21 envelope still says `preflight` / before-load `NOTRUN`; that bookkeeping does not negate the recorded bootstrap execution.

**Lifecycle and source comparison**

- **10973:** seven records: `owner-init` → three `basis-unavailable` → `basis-read` generation 0 → `lifecycle-cancel` generation 1, session absent → **`basis-read` generation 1**.
- **14249:** five records: `owner-init` → three `basis-unavailable` → `basis-read` generation 0.
- Neither records `basis-ready`, `basis-error`, `identity-read`, session creation/recovery, `owner-error`, or `handoff-ready`. Both buffers report zero rejection, overflow, listener errors, and retention losses.
- Compared with the supplied historical 18800 description—six events, 679ms, ending in cancellation—10973 now records the subsequent read restart. 14249 contains no cancellation before capture. Historical missing phases remain UNKNOWN; no old evidence was reconstructed.
- This is an **effect/read restart**, not evidence that a daemon restart journey ran.

Both retained commands guard App source `804134d74782d40855146aa568ff289200b79142`, tree `8437e47666853b62e03a58af3716235346316fba`, parents `22efcda3da4005f8663c078439ff0edbfade69be` and `42db156ede0d0192ec4176a2edd29b366b552a8d`. The fixed hook is present: Git blob **`e79e083dbca9d67fbc0c66051a365ad59b897ff5`**, identical in the integrated source and 42db parent. Actual snapshot directories are no longer retained; neither was rebuilt.

Launcher pins are Agent `079580ca46af77e0292d49dc34386b25c8391f99` and Runtime `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`. Runner `ext` metadata names different integration heads and must not substitute for those pins. Actual daemon import/source attribution remains UNKNOWN. The specified 0053, 0103, and 0046 reports were read; their controls were not rerun.

**Smallest observable cause**

In the private browser traces, P2 has two `/projects/:project/timelines/:timeline/commits` requests and P3 has one with **no response captured** (`status=-1`, `time=-1`). Health requests also lack captured completion late in both traces. These are incomplete observations, not HTTP refusal statuses.

Source order places `loadTimelineCommandBasis()` and its initial history request before identity acquisition and durable session creation. Thus the retained evidence supports a blocked basis-read boundary; it does **not** identify the server-side reason. There is no meaningful census/attempt-root signature supporting `f38e`; attribution remains **INSUFFICIENT/UNKNOWN**. Upstream unique-draft ownership remains Agent-owned.

**Original case accounting**

The mounted-readiness prerequisite **RUN → FAIL** once in each run.

All eight collected P2 cases were **NOTRUN**:

| Source | Case |
|---|---|
| `p2-tour:564` | Single parent move |
| `p2-tour:595` | Transition None single |
| `p2-tour:613` | Transition None bulk |
| `p2-elements-assets:376` | Real catalog element edit |
| `p2-elements-assets:467` | registerAsset file-drop save |
| `p2-elements-assets:522` | Automatic child placement |
| `p2-popup:811` | Popup ADD on selected child |
| `p2-popup:819` | Popup SWAP on selected child |

P3’s selected original case at `three-products.spec.ts:1533`, **“M2 real gate 5 (M1 real mounted path): Agent edit, lost ACK, newer local gesture, exact retry, restart and undo preserve intent”**, was **NOTRUN**. Other cases in that file were not selected by the retained command.

**Qualified exports and custody**

Run directories under `$ORCH/tests/`:

- **10973:** `app-P2-P3-fixed-source-caller-sol-0053-full-e2e-three-products-1024010015-10973`
- **14249:** `app-P2-P3-fixed-source-caller-sol-0053-ap2-P3-gate5-h6-0348-1024010016-14249`

Every original member below is exactly:

`playwright-output/three-products.mounted-rea-54c87-ed-owner-before-any-gesture/<member>`

Case: `three-products.mounted-readiness.spec.ts:268`; failure stage: bootstrap `outbox-read`, outer `before-load`.

| Export | Original member | Bytes | SHA256 |
|---|---|---:|---|
| [actual-10973-mounted-bootstrap-lifecycle.json](/home/user/work/wt/app-readiness-10973-14249-cause-sol-0105/actual-10973-mounted-bootstrap-lifecycle.json) | `mounted-bootstrap-lifecycle.json` | 12490 | `4c18aff79b0a27598fe66ca70a5d85b5ed25e1df82f7afa4f1797b7ac3926a51` |
| [actual-10973-mounted-readiness-diagnostics.json](/home/user/work/wt/app-readiness-10973-14249-cause-sol-0105/actual-10973-mounted-readiness-diagnostics.json) | `mounted-readiness-diagnostics.json` | 652 | `e2985ee1bef07cb530eb4118b02500c5435cf9221f35849ddb254959e1b116cf` |
| [actual-14249-mounted-bootstrap-lifecycle.json](/home/user/work/wt/app-readiness-10973-14249-cause-sol-0105/actual-14249-mounted-bootstrap-lifecycle.json) | `mounted-bootstrap-lifecycle.json` | 8963 | `ac268ad7a6c397ce9d511a33b7d619cd6b1008d8045b62ae9348416cb5e7931f` |
| [actual-14249-mounted-readiness-diagnostics.json](/home/user/work/wt/app-readiness-10973-14249-cause-sol-0105/actual-14249-mounted-readiness-diagnostics.json) | `mounted-readiness-diagnostics.json` | 652 | `32b2906e374614359955301ffaea318c7b50d03f97a1580aaf5fb4528828456f` |

Strict qualification checked exact nested keys, types, bounds, phase/scalar allowlists, identifiers, endpoints, and forbidden sensitive content. Lifecycle exports also equal their genuine attachment copies.

**Omitted:** D21 files, logs, error context, private trace contents, headers, bodies, credentials, principal values, and environment values. No trace archive was exported. All **43 original retained files** remained hash-identical.

**Validation and next steps**

- `python /tmp/w-9860b60a25/qualify_exports.py` — PASS: four schema/security positives, twelve negative controls, four byte-exact exports, two attachment comparisons, original-file preservation.
- Final custody comparison — **4/4 PASS**.
- `git diff --check` — PASS.
- No new suite or browser run requested.

Investigation complete; server-side cause is limited by retained evidence. Recommended next step: the named independent review, then manager custody-copy of these four exports. Any further causal work should target the outstanding history request’s server-side handling, without assuming `f38e` or changing readiness, authority, or timeout requirements.