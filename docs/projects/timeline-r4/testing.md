# Testing: the load-bearing points, and nothing else

Execution authority: [run.yaml](run.yaml) and the current [orchestrator goal](agent_goal.md) govern models, stages, custody and escalation. Historical names do not launch agents or override them.

There are three levels:
- **Per card:** small, done by the worker and checked by the manager.
- **At merge:** a re-run of the card's bounded checks, by the merge manager.
- **At nine named integration points:** the only big runs.

Nothing else runs on a schedule.

## 1. Per card (the worker runs it; the manager checks it)
- **The affected tests:** the tests for the modules the card changes, plus any tests the card names.
  - Python: `rg -l '<changed module>' tests/` and run those files.
  - App: `npx vitest related <changed files> --run --config config/testing/vitest.config.ts`.
  - Minutes, not hours.
- **The card's own check:** its "Done when", including the failure/recovery case when the card touches save, commit, migration or security.
- **Bug fix → red before, green after.** The new test fails on the trunk and passes on the branch.
- **Preservation → unchanged.** This covers refactors, extractions, migrations, pins, characterization and the compiler. The existing tests and golden outputs pass before and after, with no edits to them (moving an import is fine). There is no red-before step, because nothing should be red.
- **A card that is both** (an extraction that also fixes a bug): the fix gets red→green, and everything else stays unchanged.
- **New behaviour:** its tests pass. No red-before ceremony.
- **A card that adds a GATE scenario** runs that one scenario once, through the lease, with the merge manager's go. It does not run the whole journey.
- **Never per card:** a full suite, a render, a film journey, a parity matrix, or a fake standing in for a merged dependency.
- **xfails are strict.** A fix removes its own xfail in the same commit. GREEN turns on `xfail_strict` and audits the rest, because tonight four stale xfails hid a fixed bug.

## 2. At merge (the merge manager; light, no lease)
Rebase onto the trunk, re-run the card's bounded checks (its "Done when" and affected tests, never a render, journey or full suite), then fast-forward. That is all. Heavy runs happen only at the integration points, through the lease.

**When regressions surface:** between integration points, a regression shows up at the next point. The merge manager bisects it over the merges since the last green point and turns it into a card; merges are small and daily, so that is cheap.

**Escape valve:** add a ≤ 5-min smoke per merge only if two points in a row catch a regression that such a smoke would have caught.

## 3. Integration points (the merge manager, through the lease)
Every point starts with GATE's **bounded smoke** (a real-film save, reload and preview on a clone, ≤ 5 min). If that is red, the point stops and the failure becomes the next card. A point runs once, when its last milestone merges. It runs again only if code in its area changes before release.

| # | Runs when these merge | What runs | Why it is load-bearing |
|---|---|---|---|
| **IP0 Base and gate** | `A#base`, `A#checkpoint-astrid`, `A#checkpoint`, `A#green`, `A#golden-baseline`, `A#gate`, `G#pins-astrid` | **The base check:** every freeze-era feature in the port reports and the carry ledger, exercised on the base. Full Astrid, Runtime and App suites, once (the red list is recorded, the xfails audited); `make doc-refs`. The golden baseline is frozen on a clone of the live film. The **full journey on today's behaviour**, including a render. | Every later "unchanged" and "red before" is measured against this. Tonight's port silently lost features, and on a red baseline a new red can't be seen. |
| **IP1 Preservation (R1.0)** | `B#preservation`, `B#compat`, `G#pins` | Journey scenario 1: a real App save and reload keeps opaque fields and explicit clears, for both providers. One exact-revision preview and render on the clone, with the App and Astrid on one renderer closure (the same composition artifact), audio included. GOLDEN's frame and audio compare on the v8 duplicate on the new pin; each difference is fixed or listed with an owner. | The first user-facing data-loss fixes, in another team's code. Today the renderer pins differ between Astrid and the App. |
| **IP2 Compiler** | `F#compiler`, `F#timing-fixes` | Golden compare on the v8 duplicate: compiled-document bytes, 45 cut rows, intent reads (unchanged except for TIMING-FIXES' listed fixes). The journey's re-flow phase (narration retime → render). The full Astrid suite. | The compiler replaces timing logic spread over many callers, so a drift shows up as data loss far from its cause. "Unchanged" is the whole claim. |
| **IP3 Commit path** | `D#merge`, `D#commit-service`, `C#acceptance` | Journey scenario 4 through the CLI against a real Runtime on a clone: a lost response retried after the head moved returns the original, with one publication. A crash between the head move and the response recovers exactly once. The dry-run rebase returns the suffix and stores nothing. Full Astrid and Runtime suites. (COMMIT's independent review call on the rebase and commit diff happens just before.) | The atomic boundary every later card trusts. "Never invents intent" is the claim the implementer's own tests tend to mirror. |
| **IP4 App save** | `E#save-rebase` (after `E#gestures` and `E#save-routing`) | Journey scenarios 1–4, driven through the real App → commit → Runtime → CLI checkout: the anchored gesture survives a retime; a held response plus a newer edit gives A′ + B. The full App suite. Re-forecast Release 1. | The first real producer → consumer across all three repos. It is release-contract §5's re-forecast point. |
| **IP5 Preview** | `G#evaluator-film`, `G#render-parity`, `G#verify-loop` | The parity harness on the v8 film at every cut boundary, for frames and audio, once; the shared evaluation's layer order and opacity equal the renderer's there. Planted 1 px and 0.5 dB changes fail. Journey scenario 5: exact-revision render, then revert and restore, with audio. The verify loop measured once: single-client p50 (warm) and p50/p95 with 3 agents, with machine load beside each number, against targets re-stated after CAPTURE's measurement (old: 5 s, 15 s, 45 s). | "Preview = render" is a Release-1 promise, and renderer alignment is protected work. This is the one place it is proven before release. |
| **IP6 Release 1 candidate** | every R1 milestone except `A#practice` and `A#r1-accepted` | Full suites in all three repos. The full journey, scenarios 1–5. **REPLAYS' v9 and v11 scenarios** pass: orphans resolved in ≤ 3 and ≤ 10 commands with no intent hand-edited, zero unexpected word-anchor entries, one music bed with listed seams and unique ids. **SEC-1…5** on the paired relay with disposable data (SEC-MATRIX), and real traffic on it once: pair, load, save main, save popup, history/restore, render, Range seek, reconnect. Two agents and the App on one duplicate see each other's work. WRITERS' census has zero "fallback" rows. RELEASE-1 then adds FINAL-E2E stage 3 on astrid.haus, `codex-accepts-base`, and **the owner watches the film**. PRACTICE gates nothing. | This is the definition of done (agent_goal). Security comes before any real data (I6). |
| **IP7 Release 2 candidate** | every R2 milestone (`C#schema-warn`, `D#script-edit`, `D#script`, `F#repairs-1`, `F#repairs`, all of I) | Full suites. The full journey. The golden's 8 chapter start frames exact. v9 to v11 takes one script edit plus one re-home pass. The v11 replay on a duplicate of film-5898e92b with the three-arrangement music bed: one bed, seams listed, unique ids, two re-flows idempotent. The parity harness re-run for the audio and motion rows. | Release 2 changes timing-bound features (the music clock, story ranges, envelopes) on the real film. Exact chapter frames are the contract's Release-2 check. |
| **IP8 Release 3 candidate** | every R3 milestone except `A#r3-accepted` (`G#full-parity`, `J#proofs`, `E#review`, `D#retention`) | The full parity matrix (every supported row passes, including contributed components/transitions and all five extension kinds), the full E2E, the golden on the migrated duplicate, and the examiner round (FINAL-R3). **The owner watches the film** before the live migration, which happens only on the user's go. | The only point at which the live film can change. |

**Not integration points:** the contracts (`A#contracts-v1`/`A#conformance` → `A#contract-commit`/`A#contract-command`). Their schema review is one independent review call inside CONTRACT-COMMIT, and the shared fixtures run in each repo's suite as that card's own check. Neither needs a heavy run.

**Recording:** one line per point in status.md: `IPn green|red|not observed | Astrid <sha> Runtime <sha> App <sha> composition <sha> (artifact <digest>) | lease <id> | failures → <cards>`. Retain concise receipts in existing status notes; link actual output/digests when produced, without introducing a new acceptance gate.

**Failures:** one card per owning project per run, placed at the top of its queue. Nothing that depends on the red milestone starts until it is green. Once a scenario has passed at a point, it must stay green at every later point.

## 4. Heavy runs and machine custody

Follow [source-custody.md](source-custody.md#resource-custody): retain original weights, bounds, sharing, one-at-a-time admission and deadline semantics, using a recorded compatible shared lease without an Otto runtime. A is the sole broad-check owner. No heavy run begins until its current execution/lease/data custody is explicit.


## FEATURE-PARITY C5 execution binding — 2026-10-15

Every card’s affected-check set must include `make parity-guard` from the verified Astrid worktree, and every named GATE integration point IP0–IP8 must run it alongside its existing bounded checks; record the exact command, exit status, and elapsed seconds in each applicable receipt before acceptance, and treat future GATE execution as prospective until actually run.

The named target is implemented on the clean FEATURE-PARITY candidate `23f6ea58e9cb381273067d214666565f861d2401`; first target validation: 10 passed in1.06s, wall1.353849958s. Receipt: `projects/A-integration/receipts/FEATURE-PARITY-C5-correction-1-result.md`, SHA256 `89387ad666c3a8815180990271ee4b198c7a0fab1ff36e660621fcafcd7ccccc`. Until FEATURE-PARITY is accepted/merged, its C3 hold and all downstream dependencies remain. This command is a bounded guard, not a new review, release gate, or a substitute for other affected tests.

## Astra098 focused additions to existing checks

Use the detailed cases in [the Astra098 amendment](amendments/20261016-upstream-transcript-extension-integration.md) at existing owner boundaries; these additions do not create a test stage or product PASS. Test a baseline client requiring v1 against additive `listEvents: [1,2]`; missing optional rename or `from=latest` must leave unrelated baseline flows working and refuse only use of that feature; missing/incompatible baseline requirements must deny before realm load or mutation; Runtime support `[2]` must not satisfy a version-1 requirement; a legacy scalar descriptor means a singleton. Preserve exact health/handshake Runtime identity and digest agreement, generated wrapper admission, request/response validation, and every existing grant case. Inventory membership alone must not grant call/write permission. Also cover generated inventory, namespace ownership/version/clear/opaque preservation, document CAS/idempotency/pagination, and denial of timeline documents through `documents.write`. Extend timing/replay cases for missing or mismatched snapshots, offline replay, same-lineage correction, ambiguous/repeated words, explicit retake maps, segmentation, occurrences, trim/speed, undo, and no latest lookup. Verify coexistence and round-trip fixtures with required `source_id`, `source_version`, `producer`, `file`, `media` containing exactly one `asset_key` or `source_id`, `sha256`, optional registry-validated `media.sha256`, and unknown metadata alongside `config.app.transcript.references`; test equal migration and conflicting/malformed legacy `transcriptReferences` while preserving both originals. Verify default changes do not retarget `clip.app.transcript.binding`, generic owner writes cannot forge import provenance or timing, and no hidden post-publish refresh occurs. Cover synthetic chapter flatten/split and canonical track round-trip, disjoint metadata merge versus real conflict, and Caption Foundry facade read plus the validated binding operation or separately declared data. Reuse IP2/IP3/IP4/IP5/IP8 and the current parity policy; do not repeat unchanged cohorts or touch live film/media.
