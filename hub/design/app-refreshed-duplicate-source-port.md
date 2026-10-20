# Refreshed independent duplicate source port — BLOCKED

Native contract gap; stopped as required by the brief. Final App source remains **85efd0ffa** (full HEAD `85efd0ffa5cefc4ba38c63e0fb75e50258c5c28c`), with **zero changed files / +0/−0 LOC**. No UI migration or source port is delivered. `BLOCKED` is written; no `DONE` or `KEEP`.

## Concrete blocker

`occurrence.duplicate` records a whole-root create whose `after.value.stable_deep_link` and `after.value.output_identity` still carry the source values. The native compiler correctly re-derives those two fields on the RAW destination row through the existing factories against the compiled destination. After `document_from_bundle` → `bundle_from_document`, the root-create inverse compares the reloaded destination with the pre-compile recorded source strings, and rejects its own otherwise unchanged duplicate: **`CommandError: original authored guard changed`**, ref `occurrence:occ-copy`, path `[]`.

For example, recorded output identity ends in `occurrence/occ-0/output/final-video`, while the raw compiled and reloaded value ends in `occurrence/occ-copy/output/final-video`. Neither a user edit nor an intervening publication exists. The source stays unchanged and the new shot/internal closure is correct. Either identity field alone causes the failure. Removing both fields makes exact guarded inverse after reload pass. This control removes fields only from separate diagnostic input, never from a behavior expectation or product path.

Reproduces on official frozen Agent S2 **26ef2bbb31b4892fdd7c15ee5b20700bd40cb933** and frozen current Agent **78d548cf059a5875f5333590e6ae84051504f809**. Source archives are read-only files under this worker's notes, imported with `PYTHONDONTWRITEBYTECODE=1`; dependency venvs were not changed. Native source hashes are in `notes/native-source-hashes.json`.

Minimal repro: [`repro-native-duplicate-inverse.py`](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-duplicate-source-port/notes/repro-native-duplicate-inverse.py). It asserts the factory results against the **raw parent before opening**, closure linkage, immutable source and opaque history before attempting the required successful undo. S2 failure log: [`repro-s2-both.log`](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-duplicate-source-port/notes/repro-s2-both.log); no-identities positive: [`repro-s2-none.log`](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-duplicate-source-port/notes/repro-s2-none.log); current failure: [`repro-current-both.log`](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-duplicate-source-port/notes/repro-current-both.log).

Native locations: `native_occurrence_duplicate.py:52–56` creates the copied root; `core/timeline/authoring_bundle.py:1045–1048` re-derives fields; `sdk/timeline/inverse.py:366` guards the original whole-root after value. The existing **33 native tests pass** because identity re-derivation and duplicate→reload→inverse are tested separately. They miss their combination. This is an implementation gap in the settled contract, not a reason to change the owner identity rule, invent suffixes, weaken guards or request App replacement identities.

## Source/parity and scope

Located approved retained stage **4969238c5d400dda48553b2bfcddf8fafb12a616** (+4425/−3 over 55e7e217b; historical 440 passes), design `m2-occurrence-duplicate.md`, and the 03:52 root-derived identity decision. The retained enriched golden remains byte-identical, SHA256 `c599078b807bd536874c7755eb194e50d025706eb9940fe071f41f3ac4f6c06e`. The complete original bundle, capture command, records, after-bundle and raw compiled document match both frozen native sources exactly. No hand-generated client pin or new wire/op/schema was introduced.

The brief's published Runtime **0132c4 S2 / 22 ops** includes the required op; missing admission is **not** the blocker. The inspected official S2 schema at Runtime `f7081c14efd9a5b834987e7a1e2abf597b66313b` has 48 defs and the exact closed two-ID `OccurrenceDuplicateArgs`, raw SHA256 `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`. App's 029 development pin was left intact. No actual installed-pair acceptance is claimed.

Before discovery, the bounded port covered native capture/dry-run preview, original guards/reservations, existing durable session and explicit raw occurrence UI ingress. It allocated each UUID once, removed the canonical publish caller, kept legacy positives and wrapped every phase with existing legacy-clean fences. Visual projection remained accepted-closure based, as in the retained stage; no speculative destination compiler or identity remapper was added. Current main/mobile/render/provider/label/clamp code was preserved. The two authorized CORS files were exact copies of 7bb during the attempt.

After the native repro, all task-owned App edits were restored to their original HEAD bytes. The whole attempted delta is saved only as [`attempted-source-port.patch`](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-duplicate-source-port/notes/attempted-source-port.patch), **17 files / +4590/−39**; it is unqualified WIP, **do not apply before native repair and fresh review**. Final product/test/CORS allowlist is empty; final LOC delta is zero. Attempted allowlist (diagnostic patch only):

| Path | Attempted delta |
| --- | --- |
| `src/shared/lib/media/mediaCrossOrigin.test.ts` | +30/−0 |
| `src/shared/lib/media/mediaCrossOrigin.ts` | +18/−6 |
| `src/tools/video-editor/commands/clipMovePrimitives.ts` | +32/−3 |
| `src/tools/video-editor/commands/commitSession.ts` | +38/−1 |
| `src/tools/video-editor/components/AstridTimelineEditor.document-shots.test.tsx` | +60/−3 |
| `src/tools/video-editor/components/AstridTimelineEditor.tsx` | +14/−25 |
| `src/tools/video-editor/contexts/VideoEditorProvider.tsx` | +1/−0 |
| `src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx` | +22/−0 |
| `src/tools/video-editor/hooks/useTimelineCommandSession.ts` | +10/−0 |
| `src/tools/video-editor/hooks/useTimelineState.ts` | +8/−1 |
| `src/tools/video-editor/hooks/useTimelineState.types.ts` | +2/−0 |
| `src/tools/video-editor/commands/commitSession.occurrenceDuplicate.test.ts` | +167/−0 |
| `src/tools/video-editor/commands/fixtures/recipe_m2_app_occurrence_duplicate.json` | +3830/−0 |
| `src/tools/video-editor/commands/occurrenceDuplicateCapture.test.ts` | +136/−0 |
| `src/tools/video-editor/commands/occurrenceDuplicateCapture.ts` | +131/−0 |
| `src/tools/video-editor/commands/occurrenceDuplicateGesture.test.ts` | +48/−0 |
| `src/tools/video-editor/commands/occurrenceDuplicateGesture.ts` | +43/−0 |

## Evidence and remaining pair

Exact commands/results: [`commands.md`](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-duplicate-source-port/notes/commands.md). Preliminary App runs: 44/44 (capture/session), 50/50 (UI/hook neighbors), then 295/295 across 10 existing command/hook files. Those checks apply only to the saved attempt. Native original suite: 33/33. New required-success native repro: three independent failures on S2 (both roots / link only / output only), same failure on current, no-roots control passes. No passing test was rewritten, weakened, disabled or skipped. No 440-pass requalification claim. No full/build/browser/socket/project-tsc/install/live Runtime or paired rendering work was run; no build/temp output remains in the worktree.

Decision: obey **“If native contract gap stop concrete repro”**. Preserve a clean base and hand off the regression instead of binding a UI action whose normal guarded undo fails after immutable reload. No orchestration or owner decision was changed.

Recommended next action: Agent owner repairs native root-create inverse/record consistency for the approved factory-derived fields and adds this combined raw-compile→reload→guarded-undo→redo regression, retaining ABA/history safety and opaque equality. Then re-run native goldens and retry this bounded App source port. The normal safe Runtime/Agent/App pin step remains separate; real acceptance, immutable raw readback, source isolation, guarded undo/redo, conflict/replay, lost-ACK/newer suffix, restart/exact body+key retry and zero legacy publication traffic remain **OPEN**. No operational pair qualification or writer retirement is claimed.
