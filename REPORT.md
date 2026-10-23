# V4 seven original residual failures: source diagnosis and owner handoff

Diagnosis complete; **V4 acceptance remains held**. No product, test, recipe,
generated, pin, package or manifest changes; no tests or probes executed.
This report uses PLAN §3 V4 and the approved C0 contract, not a replacement
implementation. The four observed error statuses agree with C0. The retained
rebase exposes a production provider metadata defect. The two undo failures
expose a conflict between the preserved positive behavior and C0's literal
derived-write guards; they do not authorize weakening those guards.

## Original evidence and seven-way disposition

Every node below is in `tests/editing_conformance/test_native_word_anchor.py`.
The full existing trace and original author report are
[`handoff-vw-V4-anchor-created-fixture-targeted-test.log`](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-V4-anchor-created-fixture-targeted-test.log)
and
[`handoff-vw-V4-anchor-created-fixture-REPORT.md`](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-V4-anchor-created-fixture-REPORT.md).

| Original node | Actual error | Current contract expectation | Source cause | Existing owner / minimal next action |
|---|---|---|---|---|
| `test_native_acceptance_refuses_review_source_counterexamples_before_writes[short-occurrence]` | L131: `invalid`, expected `refused`; `invalid_anchor`, message contains `half-open occurrence interval` | C0 §4: 422 `invalid` for a declaration invalid at its claimed base | `native_word_anchor.binding` L110–116 → `declare` L323–327 → `commit.py` L1160–1174 → `_commit_errors.is_invalid/failure` L64–71,98–107 | Agent R3/V2, through existing G234 owner: no production status reversal. Orchestrator may approve narrow v2 expectation adaptation; retain reason/message, no-write, unchanged-history and direct-recorder guards. No assertion changed here. |
| `test_native_acceptance_refuses_review_source_counterexamples_before_writes[raw-source-window]` | L131: `invalid`, expected `refused`; `invalid_anchor`, message contains `supported source map` | C0 §4: 422 `invalid` for unsupported source geometry at base | `native_word_anchor.py` L86–92 rejects unrecognized source mapping, then same error path | Same R3/V2/G234 disposition; preserve source-map refusal and all positive cases. |
| `test_undo_recovers_before_binding_even_when_text_writes_are_equal[True-False]` | L214: `intervening_write`: `an intervening publication wrote a guarded address` | Literal C0 §5 requires overlap refusal, including derived effects. Original test requires successful inverse B after source move, preserving the move and restoring A's choice | `commit.py` L1012–1020 → `_step_undo.py` L144–167,181–209 → `inverse.py` L218–222,320–338: B and later move both have derived `parent/clip:card` timing effects | Existing Agent R2/G234 owner with Runtime native14/P5 owner as guard reviewer: resolve the C0/positive-behavior incompatibility explicitly. No approved safe one-line source correction exists. Any approved causal-cache reconciliation must be limited to authenticated recomputation, retaining authored-write/read/ABA and surviving-consumer scans. |
| `test_undo_recovers_before_binding_even_when_text_writes_are_equal[True-True]` | Same L214 refusal; B's declaration text write is byte-equal, but its stored exact word choice and canonical revision differ | Same C0 §5 conflict; equal text cannot erase a distinct authored binding or publication | Same early overlap scan; failure occurs before inverse installation or `_validate_inputs`. It is not caused by dropping B's equal-valued authored write | Same R2/G234 handoff. Preserve this separate equal-text positive claim and all ABA negatives; never filter equal-valued writes or all `derived_writes`. |
| `test_follow_rebases_original_choice_after_source_move_and_reorder[True]` | L234: `invalid_records`: `provider dependency union omits a captured read` at Runtime auth L278 | C0 §§1,3,4: retain exact source/word selection, replay against landing head, complete authoritative dependency union, new success `merged` | Legacy semantic branch `commit.py` L1105–1112 calls replay without `commit_request`/`evaluated_head`, then copies original-base `steps`. Replayed captures resolve to the new physical internal image; copied dependencies name the old image | Existing Agent G234/R1/R3 owner: thread authenticated request/head through the actual replay execution and regenerate landing steps/dependencies. Runtime R2r/native14 owner keeps `covers`/auth strict. Do not add fixture `reads: []`, weaken auth, copy old bindings, or reselect the word. |
| `test_half_open_window_and_exact_rational_fps_are_validated_at_acceptance` | L515: `invalid`, expected `refused`; `invalid_anchor`: `outside the half-open source window` | C0 §4: 422 `invalid` when this request makes its existing anchor unresolvable at base | `native_word_anchor.compile_recorded` L378–381 converts completed-candidate compiler error; R3 classifies at the current base | Existing R3/V2/G234 owner: approved narrow status adaptation only. Preserve exact rational-FPS/boundary success, restart, and unchanged-head assertions. |
| `test_stale_anchor_refuses_when_intervening_window_excludes_selected_word` | L533: `conflict`, expected `refused`; same `invalid_anchor` half-open-window message | C0 §4: 409 `conflict` for valid-base intent invalidated by intervening narrowing; actual head must be reported | `commit.py` L1056–1112 replays on the changed head; `_commit_errors.py` L64–71,103–107 distinguishes base/current pairs | Existing R3/V2/G234 owner: preserve later-head conflict classification. Approved narrow status adaptation may retain window, head and no-write guards. No assertion changed here. |

These are observed failures, not an unproven “pre-existing” classification.
Status adaptation is justified by the approved C0 text; this diagnosis does
not approve or perform assertion edits. The original status assertions stop
before some subsequent no-write assertions, so those later assertions are
preserved source requirements, not executed evidence from these failing bodies.

## Exact causality and physical boundaries

**Undo:** A selects the first stable word; B selects the second, with either
different or equal declaration text. `declare` writes both
`parent/clip:card/app/astrid/on` and
`parent/clip:card/app/astrid/word_anchors/on`. It records the exact transcript
dependency and `anchor.source` binding (`policy: follow`, L331–335).
`compile_recorded` records changed target `at`/`hold` as derived writes
(L338–342,382–393). Moving `occurrence:occ/clip:voice` to 8 changes the source
timing and causes another target timing write, while leaving the declaration
and exact authored choice intact. `_causal_commands` retains those derived
effects by their command cause; `_effect_writes` includes them, excluding only
the aggregate `parent/config/clips` mirror. The overlap at the target timing
is sufficient to trigger the traced refusal. The traceback does not print
the chosen `location` or complete recorder values; this concrete overlap is
a source deduction, not an executed value dump or claim about first iteration.

The fixture submits ABI-1-style bodies with no label/steps/merge/reads
(`native_word_anchor_fixture.py` L172–176). `CommitPatch.active` is true, but
`v2` is false (L230–234). It synthesizes steps and physical dependency sites,
but does not attach v2 physical bindings/materialization proofs (L384–389,
502–549). `commit.py` L1013–1015 therefore does not select a physical resolver
for these target records. Native aliases use `inverse._root_addresses`
(L125–170), resolving the occurrence's source to the shot/internal address;
the parent target overlap is independent of that alias mapping. Relabeling
this as solely a missing physical-binding fix would not explain the failure.
Explicit v2 physical histories must still use `inverse_address_resolver`
(`_commit_patch.py` L848–925) and `AcceptedRecords`; their authentication checks
in `inverse.py` L586–590 must remain.

C0 §5 L1602–1637 says to preserve derived effects and scan later overlapping
writes/reads, including equal-byte restoration. The later source move has a
target derived write; thus the current strict refusal is supported by that
wording. The original positive requires restoring A's exact authored choice
and recompiling at the moved source time, rather than restoring B's old timing
cache. This is a contract/behavior tension for the orchestrator and existing
R2 owner, **not permission for this worker to implement an exemption**.
`_root_inverse.clip_cache_stages` L12–53 is an existing authenticated cache
proof seam, currently scoped to whole clip-root writes; it does not solve this
declaration-only later-publication overlap. If the positive is reaffirmed,
the owner needs a narrowly specified causal reconciliation at the scan and
inverse guard/install boundaries, not a global derived-write omission. It must
refuse authored target/source dependency writes, ABA, changed identity or
unproven physical continuation, and unsafe surviving consumers. No such
correction is claimed implemented or proven here.

**Rebase:** the same stable `voice` clip and exact transcript word must survive
source move/reordering; rerunning ordinal selection would incorrectly choose
`other`. The move materializes a new internal revision (and owning shot pin).
The captured native read `occurrence:occ/clip:voice`, path `['id']`, state
`present('voice')` (`native_word_anchor.py` L316) normalizes to
`internal-revision:<landing internal> / ['clips','id:voice','id']` via
Agent `canonical_site` L119–145 and Runtime `native_site/site` L140–158,200–205.
Original steps contain the corresponding `<base internal>` dependency.
`rebase.replay` L9–20 executes without commit metadata; provider then copies
the original steps (L1111). Runtime validates the landing records against the
landing source (store L732–737; auth L683–698), and `covers` L208–216 correctly
rejects that old-image dependency as coverage for the new-image capture.
This is the first changed-image read predicted by source order; generated
revision IDs and full dependency arrays are not dumped in the existing trace.
No speculative exact UUID is asserted.

The minimal production seam is `commit.py` legacy semantic replay plus
`rebase.py`'s execute forwarding: retain original captured intent and its
native replay guards, pass the authenticated request and evaluated head to
`execute`, and let `CommitPatch.finish` L396–452,491–528 derive current patches
and dependency union. Do not copy old steps over that result. This must cover
implicit ABI-1 normalization as well as explicit v2 bodies; adding optional
fields to this fixture merely selects a different branch. The explicit branch
already passes these values (L1093–1099). Request-level reads, sequential
step boundaries, physical continuation proofs, merge mode, and original-base
validation remain mandatory. A blanket legacy-to-v2 branch switch needs
owner review because it also selects different rebase guards.

A latent contract adaptation is visible at test L235: after the current
exception is repaired it expects `rebased`. C0 introduction/§4 requires
`merged` for a new acceptance; `rebased` is retained only for exact historical
receipt retry. This is not an eighth executed failure and is not changed here.

## Production caller and Runtime authority

The tested fixture calls real `RuntimeService.commit_timeline` and registers
`agent.create_runtime_commit_service`; its hydrate wrapper only observes.
Runtime's production loader has the same factory in
`timeline_commit_provider.py` L18,80. No detached adapter is proposed.
The actual source path at Runtime ad823 is:

1. `service.py` L2434–2483 validates route scope/body, requires publisher/key,
   obtains `_timeline_authorize`, hashes the publisher-bound original invocation,
   and invokes the coordinator with a real `RequestCommitPort`.
2. `timeline_commit_execution.py` L69–89 checks invocation identity, serializes
   execution/replay and invokes `provider.commit`; it verifies the returned outcome.
3. Agent `commit.py` validates original base and ancestry, executes/replays,
   constructs `prepared_records` and calls **`port.preview(prepared)` L1140 or
   `port.accept(prepared)` L1141**. R3's projection cannot substitute for auth.
4. Port L507–537 checks observed head/materialization and delegates with its
   authorization callback. Store `preview` L988–1006 authorizes, checks context,
   head and destinations, then `_validate`; store `accept` L1029–1044 repeats
   auth/context/head checks inside the acceptance transaction before `_validate`.
5. Store L732–737 calls `timeline_commit_auth.validate`; L251–278 authenticates
   the complete captured-read union, L297 onward authenticates physical bindings
   and evaluation boundaries. These are acceptance checks on the real path.

The trace proves the rebase error reaches `port.accept` and Runtime auth; the
undo refusals occur earlier at the provider's authenticated-history scan.
Preview shares the same validation source, but was not executed in this task.

## Published stage comparison and owner boundaries

Read `/home/user/timeline-hub/hub/status/{agent,runtime}.md` and Viewing's
current `STATUS.md`. Agent board L15–21 names the existing G234 join/review
owners and stage **5f0fb2edb72aae37ba86e3ffe28f5e79b63aa026**; create-empty
correction is separately active. Available G234 hub refs still name that stage;
no published G234 successor was found in the inspected refs. Runtime board
L18 names **rt-P5-native-integrated-0400 / rt-P5-native-review-0405** as the
existing strict native14/P5 owner, with Runtime **62c454ac07fb46a1a67847d933f1ed5f53043e30**.
Boards are ownership/evidence reports, not new instructions to implement.

Relevant `git diff f894c3c9d 5f0fb2ed -- <provider files>` shows:

- `_commit_patch.py`, `_step_undo.py`, `rebase.py`, `native_word_anchor.py`,
  `_commit_errors.py`, `_commit_preview.py`, and `commands.py` are identical.
- Stage `commit.py` L1073–1107 retains the implicit-request branch and copied
  original steps. It does **not** fix the captured-read failure.
- Stage `inverse.py` adds authenticated timeline-scope recognition and restricts
  physical-binding handling to `AcceptedRecords` in `_validate_inputs`
  (stage L493–579). `_effect_writes`/`check_intervening` L218–353 and the early
  scan are unchanged. It does **not** fix these two early overlap refusals.
- Status classification is unchanged and already matches C0 for all four rows.
- Runtime ad823 → 62c454 has identical service/coordinator/port/store/auth blobs.
  Existing native14 PASS is relevant guard coverage, not executed proof of these
  original anchor nodes or a reason to weaken auth. No new pin is indicated.

No V4 directory/deletion causality review was repeated. No old branch merge,
Runtime/client repin, parallel implementation or native14 rerun is proposed.

## Source identities and verification

- Agent diagnosed base: `f894c3c9dda25ab03527eeb7f52da5da31d627c1`.
- Fixture-only candidate / this worker's starting HEAD:
  `38e8063162a36a87369561c581bc18fe8fbef37c`.
  `git diff f894c3c9d HEAD --stat` before this report: only
  `native_word_anchor_fixture.py`, 2 insertions / 1 deletion, canonical
  `created: ["parent/track:initial"]`.
- Runtime read: `ad823e0a0f5be4a7acf1d3006df6f794709da63d`.
- Official client source stays `34eac0041b0891e9011966b39bcbd26053fde5bc`;
  prior fixture report's all-15 mapping check is reused evidence, not rerun.
- Approved C0 file read: orchestration `design/commit-v2.md`, SHA-256
  `4581ea85aada0af405b1b1b9284e9938a6dba3ca4f6980b7c3c0be8f135f9bb7`.

Exact Git blobs (paths under `astrid/sdk/timeline/` unless stated):

| Path | Agent f894 | G234 5f0 |
|---|---|---|
| `commit.py` | `9cbe823d1db166e3701d9d6bc372a7266417d6f1` | `67f8d59089e6b378a697e29f7285bb75f403743b` |
| `_commit_patch.py` | `3852a512d7852ad36a5a4cbbc094317518438668` | same |
| `_step_undo.py` | `9f1cf3b273a691350593c76618f182da403492cb` | same |
| `inverse.py` | `603ab9a6ba5134d57cfe52864ffcf1a3ac29f2a6` | `8d1ead5f132c2c551b142abd64c4e4f79e23d311` |
| `rebase.py` | `31450bc3b263045969b02fca7b7edf6f083c1611` | same |
| `native_word_anchor.py` | `4c8dec68dcd42008158193df195d44b6838335b0` | same |
| `_commit_errors.py` | `084df70928383e915175456dc57775ad9750203a` | same |
| `_commit_preview.py` | `d7332f1a648ea68112ff4d744129eb323191cdf7` | same |
| `commands.py` | `4ae1025f9f694dfac8e44ee9e39d77f90325311d` | same |
| `_recording.py` | `207a7163da7d279bab9c5074fc6a139cc32ee84d` | same |
| `_root_inverse.py` | `ccc97e896ef211f0f0e4047a9e24cd06b0984b9b` | same |
| `_doc_patch.py` | `2807f65e8f3f6890d96554cae576db31d012384d` | same |

Runtime blobs under `runtime_protocol/`, identical at ad823 and 62c454:

| Path | Git blob |
|---|---|
| `service.py` | `d0634c49de7f8b6a82d0af5ec371db2cc51bbcb6` |
| `timeline_commit_execution.py` | `039f63d47ada5ce5f31d2570a0d9b317fe09d275` |
| `timeline_commit_port.py` | `62a0087cabd70015cd0367335aaa9ae100dad376` |
| `timeline_commit_store.py` | `607012dd19b81b933da1c12d5b8011621b35037e` |
| `timeline_commit_auth.py` | `85325f86fca53c2c487dbd3b064382ec3aa76dec` |

Production loader at ad823, `timeline_commit_provider.py`:
`a05812e82ee2930f29e277f260f3329855378932`.

Independently read current protected bytes and compared to `git show f894:<path>`:

| File in `tests/editing_conformance/` | SHA-256 | Equals f894 |
|---|---|---|
| `test_native_word_anchor.py` | `d1ca4b79922d78d7c39a0e64fd8e479dfe725df0de5d348550b54f1f8399a717` | yes |
| `word_binding_recipe.py` | `5f22b3f0c8d9a81a5bd5cc520fc5295c3049ab89c9c9f46f565dd1c87f55307c` | yes |
| `test_word_binding_recipe.py` | `4722227e6e347778bb491f4f660e0a8d049ee074026b23e43de939a65d47142a` | yes |

Original author command (read from existing command/trace; **not run here**):

```sh
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-ad823e0a PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-ad823e0a /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/editing_conformance/test_native_word_anchor.py
```

Original result: **7 failed, 47 passed in 49.04s**; disclosed author capture
rerun: **7 failed, 47 passed in 48.47s**. The durable trace is 102558 bytes,
SHA-256 `ca6a1d829b4e04c4e459733def64cff6fb10baafafaf2ba065e5c212fb97d1e3`.
This diagnosis ran only source/trace reads, Git object comparisons, SHA-256
comparisons and `git diff --check` (PASS). No 54/native14/full/browser/heavy
execution, collection, or minimal probe was needed. No green-54, V4 completion,
new acceptance proof or full-wire successor qualification is claimed.

Next: existing G234 owner consumes the replay metadata defect; orchestrator/R2
owner disposes of the derived-cache undo/C0 tension and narrow status
adaptations without dropping behavior guards; Runtime native14 owner reviews
auth/ABA preservation. Only a meaningful reviewed successor justifies the
later original-54 and integrated-home proofs owned by their existing lanes.
