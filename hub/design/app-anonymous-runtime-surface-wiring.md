# Anonymous recovery on Runtime task surfaces

`TasksPane` selects `RuntimeTaskList` and `RuntimeActivityDock` in Runtime mode. Both now render the existing old-task recovery presentation beside the actual retained managed output. This completes bounded read/presentation wiring; Runtime manual-placement chooser acceptance remains blocked below.

## Read and action behavior

- Successful old `placement_intent` / `timeline_placement` tasks show **Placement unconfirmed: place manually** only alongside an available/promoted image/video output from the selected project, task, run and current attempt. Modern `generation_intent` tasks, including intents inside params/spec, remain outside recovery.
- The existing exact degraded `completion_follow_up` retirement issue is the sole route to **Not placed: place manually**. No retirement evidence is added to the captured Runtime fixture.
- Reads reuse the existing paginated managed-output helper. Missing/foreign/reclaimed/noncreative rows do not acquire recovery labels. The normal object address supplies a view link; neither params nor the output filename supplies object identity.
- The existing media-selection read receives `{association_id, object_id, version}` from the actual managed row. Only its returned generation/variant IDs enable **Open output** through the existing TasksPane lightbox hook. An association ID or digest never becomes a generation/variant ID in this path.
- Opening re-reads the Task, named managed output and media selection. Changed object/version/lifecycle or modern/bound task state refuses the open. Task/project/read replacement and unmount invalidate pending results. Output reads refresh every five seconds; stale label/media pairs are hidden immediately when task/project inputs change.
- Existing Runtime inspect/export/cancel/retry controls remain. The existing lightbox navigation, download and task-details entry are retained, as is reopen. No notification invokes a placement action.

## Exact chooser blocker

The current `AstridShotsProvider` explicitly supplies an empty compatibility shot list (`src/shared/contexts/ShotsContext.tsx`). It does not supply Runtime-authoritative destinations for the selected timeline.

More significantly, `TasksPane`'s existing `useShotActions` path takes a generation ID and global current/last shot, calls `useAddImageToShot` → `runAddImageMutation` → `placeGeneration`, resolves a default timeline, and saves through `RuntimeDataProvider.saveTimelineAtHead`. It cannot carry the selected Runtime timeline and immutable selection into the canonical command path. The workflow's target-shot callback signature also differs from the existing `useShotActions` handler signature. Passing these callbacks through would not qualify a Runtime manual chooser.

Consequently Runtime-mode `TasksPane` withholds this legacy `shotWorkflow`. The recovery card explicitly says **Manual placement unavailable here. Recover this output from the project gallery.** A verified binding allows **Open output**, not a pretend **Place manually** action. Non-Runtime lightbox shot-workflow inputs/expectations remain intact. Existing other lightbox actions are outside this bounded change; opening is tested to issue only normal reads plus session negotiation, not a placement.

Smallest follow-up: give the existing chooser the selected Runtime timeline's authoritative destination choices and an existing command-service callback that retains the captured selection and uses the user's explicit chosen destination. Adapt its target-shot/generation argument order. Keep missing bindings unavailable; no client-generated identity, hydrator, new DTO/endpoint or retroactive placement is needed. This is a proposal for the owner, not a new writer in this change.

## Fixture and qualification boundary

`src/features/tasks/components/TasksPane/__fixtures__/runtimeRecoveryGeneration.json` was captured directly from Runtime's supported `generation.publish_v1` settlement fixture: a real 68-byte 1×1 PNG, a real succeeded Task admitted with old intent, its actual managed association, and its actual immutable selection. No generation intent or retirement result was injected. The capture uses the existing Runtime fixture helpers and public-equivalent resource/page projection, without a socket. It is a test fixture, not an owner project or a completed browser qualification.

Reproduction, source heads, exact targeted commands/results and the unapplied browser fragment are in the worker's absolute notes/report path. The fragment uses this supported generation fixture seed; it does not reuse the CPU marker as canonical media. Browser selectors, seeding into the final matched harness and the manual chooser remain unqualified. No full suite, build, typecheck, install, browser or socket was run. No merge, current-pair qualification or writer-retirement claim is made.
