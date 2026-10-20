# M2 transition staged contract review

Date: 2026-10-20

## Verdict

**HOLD for consumer adoption.** The approved Agent transition contract is sound, and the staged App capture is structurally aligned with it, but the staged `ElementsLibraryPanel` activates that native route for built-in/rendering transitions before the current public013 counterpart can accept it.

The source report's statement that there is “no public activation” is not true for the staged App source: `ElementsLibraryPanel` enters the native `clip.set` path for `packId === 'rendering'` at `src/tools/video-editor/components/ElementsLibraryPanel.tsx:99-139`.

## Reviewed identities

- Staged App source: `tl/ap2-m2-element-routes-native-family-source`, consumer commit `88d9ce70568dc9fea2c709ba69595725befc2ce1`.
- Approved Agent repair: clean descendant `ca9f5f8eeba96bb9cb8f9d700c2714c2ed9f9a20`; its code is equivalent to repair `5b3e41941b1263011f52f9f1291cbbc854563dbb` except for deleting the review process document.
- Approved Agent schema/source handoff: schema SHA-256 `a70f0e8898c6acccb34062e73733c93dd4e7bc22c34ef012431e1791907e1f4a`; repaired source hashes and the handoff are recorded in `ap2-m2-transition-repaired-source-review-REPORT.md`.
- Current public013 check: Agent `8130a401bf44a518d5a40ae274d398b8c560be55`; Runtime producer/client contract remains public013/`2c4ac180c2220bdad966bc01e95ad230e99ce26a` in the current App qualification material.

## Contract checks

### Approved Agent source: PASS (source-level, not paired adoption)

The ca9/a70f handoff has the required native behavior:

- complete raw reads/expectations and recorded writes for the transition and paired `elementRef`;
- one `clip.set` with transition and `elementRef` written atomically;
- same-track predecessor selection with stable membership/order/boundary records;
- strict adjacency and shortest-adjacent-clip duration guards;
- retained original selected-pack pin authority for an unchanged reference; a later pin cannot be smuggled into an ordinary same-reference update;
- opaque transition data preserved, and ordinary `clear: ['transition']` kept distinct from paired removal.

Independent bounded reruns from the exact ca9 source:

```text
AGROOT=$(mktemp -d /tmp/ap2-m2-agent-ca9.XXXXXX); \
git -C /home/user/peteromallet/astrid-agent archive \
  ca9f5f8eeba96bb9cb8f9d700c2714c2ed9f9a20 | tar -x -C "$AGROOT"; \
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$AGROOT" \
  /home/user/work/venv-app2-native/bin/python -m pytest -q -p no:cacheprovider \
  --basetemp=/tmp/ap2-m2-agent-ca9-transition-tests \
  "$AGROOT/tests/sdk/test_timeline_transition_schema.py" \
  "$AGROOT/tests/editing_conformance/test_recipe_clip_scalar_fields.py" -k transition
```

Result: **29 passed, 87 deselected** (two existing pytest-config warnings about unavailable timeout options).

The authority subset from the repaired source also passed independently: **7 passed, 20 deselected**. The source report's broader supplied Agent lane was **183 passed**; this review does not claim a full Agent suite or Runtime-door acceptance.

### Staged App capture: PASS as an inert/native candidate

The staged `clipScalarCapture.ts` records the target basis, transition/element identity reads, predecessor selection, and guarded writes. Its `setClip` path rejects a lone `elementRef`, requires matching transition/ref identity, and validates adjacency/duration before any write (`:199-283`, `:351-388`). `clipScalarGesture.ts` sends transition SET preview without an empty `clear` field, matching the native validator's shape.

The hosted branch is correctly refusal-first at `ElementsLibraryPanel.tsx:99-103`: any non-`rendering` pack reports “Hosted transition binding is unavailable for this project pack; the draft was not changed.” It does not manufacture a `DocumentPin`, schema source, provider, wire, or cache. This is the required visible refusal and draft preservation for hosted project-pack transitions.

The staged App commit changes only six files (capture/gesture tests and sources plus `ElementsLibraryPanel` and its test). It does not touch `ClipTransitionSection` or the transition-none row. The existing App-owned none path remains `ClipTransitionSection.tsx:111-120` -> `clear: ['transition']`, including the existing scalar/batch session behavior.

## Blocking executable mismatch: current public013

Current public013's `ClipSetArgs` schema (`astrid/core/timeline/schema/edit-command.schema.json:1716-1759`) permits only `values.hold`; `transition` is listed only as a clearable field, and `elementRef` is not a SET value. The approved ca9/a70f schema is the future matched counterpart, not part of public013.

I extracted the exact public013 Agent source privately and passed the staged command shape through its real `capture_clip_set` validator using the App scalar fixture:

```text
CommandError
Additional properties are not allowed ('elementRef', 'transition' were unexpected)
```

Therefore the staged rendering built-in path does not preserve current public behavior. It bypasses the existing `adapter.execute({ name: 'timeline.apply_transition', ... })` path, locally prepares/enqueues a native command, and only then receives public013 refusal. The session's enqueue path previews/retains the local draft before the asynchronous server refusal; the panel itself reports “queued through the native timeline session,” not a transition-specific refusal. This is not a qualified activation and can leave an unsupported local draft instead of applying the existing transition route.

## Minimal inert staging seam

Keep this packet **HOLD** until the normal matched Agent source/schema and generated Runtime artifact are integrated and directly qualified. The minimal staging action is to leave the new transition branch in `ElementsLibraryPanel` inert and retain the existing `adapter.execute` transition path for current public013 users. Do not add a guessed feature flag or a new wire/DTO capability.

Once the normal public contract/lock qualification identifies the matched pair, enable the already-staged scalar producer at that existing session boundary and qualify accepted commit, reload, guarded undo, exact retry/restart, refusal/draft retention, and zero legacy transition traffic. The hosted non-`rendering` refusal must remain unchanged. No transition-none edits belong in that follow-up.

## Evidence run

- App bounded controls on the current integration worktree, with the repository Vitest runner shim and no cache:

  ```text
  TMPDIR=/tmp/ap2-m2-transition-staged-contract-review-vitest \
  node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-transport-assertion-repair/notes/vitest-runner.cjs \
    node_modules/vitest/vitest.mjs run \
    --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 \
    --no-file-parallelism \
    src/tools/video-editor/commands/clipScalarCapture.test.ts \
    src/tools/video-editor/commands/clipScalarGesture.test.ts \
    src/tools/video-editor/commands/commitSession.clipScalar.test.ts \
    src/tools/video-editor/components/ElementsLibraryPanel.test.tsx \
    src/tools/video-editor/runtime/element-adapter.test.ts
  ```

  Result: **5 files, 89 tests passed**.

- Exact ca9 Agent transition pure lane: **29 passed, 87 deselected**.
- Exact repaired Agent authority subset: **7 passed, 20 deselected**.
- Public013 pure compatibility probe (`git -C /home/user/peteromallet/astrid-agent archive 8130a401bf44a518d5a40ae274d398b8c560be55 | tar -x -C "$PUBROOT"`, then `capture_clip_set(... values={transition, elementRef})`): **expected `CommandError: Additional properties are not allowed ('elementRef', 'transition' were unexpected)`**.
- `git diff --check 88d9ce705^ 88d9ce705`: **passed**.

Not run: full suites, browser, localhost/socket, Runtime-door acceptance, public-pair adoption, source edits, test conversion, or runtime adoption. Temporary private extractions and pytest/Vitest temp roots were removed.

## Required next step

Integrate the approved ca9/a70f Agent source/schema and publish the normal generated Runtime artifact as one matched pair. Then run the bounded native App consumer qualification before any legacy adapter removal or activation claim.
