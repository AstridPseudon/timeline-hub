# Stored-cap scalar/consumer: BLOCKED on missing serialization ownership input

No implementation candidate or merge approval. Stopped at the task's explicit “If impossible within one scalar and existing boundaries” condition. Stored4000 policy and Viewing STEP1 approval remain valid; this finding concerns the additional lossless serialization requirement, not those decisions.

Exact source: App branch `tl/app-m3-stored-cap-scalar-consumer`, HEAD **b1ef4b9b910ba72375c34cf319692f90d22edc25**, tree **8d8a10b057ed31fed69517e18a23b8ec3811447a** (the requested label-live-policy base). Product/test/pin delta: **zero files, +0/-0**. Source tree remains exactly that HEAD. No integration worktree/ref mutation.

## Smallest concrete source blocker

`src/tools/video-editor/lib/serialize.ts:22–23` calls `sanitizeTimelineClipSnapshot(clip)` with **only the untagged clip**. At `lib/timeline-domain.ts:2462–2464`, the entire app is cloned. No verified raw counterpart or raw/view ownership input reaches this boundary. It is shared by raw authored objects and resolved display objects.

Earlier, `data/shotCompositionProjection.ts:424–435` has overwritten raw `app.canonical` and `app.canonicalTiming` with derived overlays. The prepared graph still has the raw bytes, but the returned config and identity maps do not carry their overwritten values. The command projection at `hooks/useTimelineCommandSession.ts:85–92` keeps only the projected config; its editProjection fact identifies revision/base, not the raw child clip contents. Its recovery `remember(head, parent.config)` call at line108 does not forward the pinned child graph.

The other side of the same blocker is `hooks/useTimelineSave.draftConfig.ts:13–25`: remember explicitly excludes clips and app; snapshot clones the display config. `hooks/useTimelinePersistence.ts:971–977` sends that result to durable draft storage. Sanitizing the final HTTP adapter cannot solve this storage path.

A known-derived overlay must be removed/restored from its **verified raw counterpart**. Neither the new duration number, canonical IDs, the revision fact, nor a key/shape test supplies those raw values at these boundaries. Stripping by names loses genuinely raw same-named opaque data; retaining the overlay leaks the derived duration. The popup's existing name-filter at `shotTimelineDataProvider.ts:135–150` is subject to the same raw-collision requirement, so copying it is insufficient.

I did not add an ownership cache/store, another metadata carrier, or a shape-based blacklist to bridge this gap. I also did not scrub outbox/pending/retry JSON or broaden the task into a raw/view state redesign. The requested one-scalar addition cannot by itself supply the missing serialization input. A candidate that leaves this unresolved would violate the explicit storage/wire requirement even if its cap regression passed.

## Concrete diagnostic evidence

Private `notes/ownership-blocker.test.ts` has three source-level diagnostic cases, deliberately not permanent product acceptance tests:

1. Two source graphs differ only in genuinely raw `app.canonical`/`canonicalTiming` opaque values. Their projected configs are strictly equal. Even injecting the proposed stored-duration scalar from each original prepared occurrence leaves the serializer inputs strictly equal; the raw values differ and have already been overwritten. Immutable identities/digests are deliberately held fixed for this controlled information-loss diagnostic; this is not a claim that two verified accepted revisions can share an immutable identity.
2. A known projected clip with the proposed scalar and a genuinely authored JSON clone have identical own keys/content and produce identical `serializeClipForDisk` output. There is no hidden existing ownership tag differentiating the calls. A key/shape-only solution cannot meet their different required outputs.
3. The hypothetical view scalar survives `buildTimelineData` → recovery snapshot → real repository IndexedDB draft writer/readback. An unrelated ordered/null/false/zero sibling and an opaque root also survive. This uses fake IndexedDB and injected data only, with no socket/browser.

This substantiates the audit's missing-input constraint; it does not establish that every possible explicitly expanded ownership design is impossible.

## Commands and results

Exact reproducible commands: [commands.txt](../workers/app-m3-stored-cap-scalar-consumer/notes/commands.txt). Runner config: [vitest.config.ts](../workers/app-m3-stored-cap-scalar-consumer/notes/vitest.config.ts). Node v22.22.0; read-only private Composition0.0.12 at `/tmp/app-coherent-deps12/node_modules`. Runner uses owned cacheDir, `--configLoader=runner --no-cache --maxWorkers=1`; no default shared cache writes. Required Agent inputs are an owned minimal `git archive d8749a9ce12a699672faf3ad96b4e4cbea9245c2` copy under worker notes.

| Command | Result |
| --- | --- |
| Scoped Vitest: private ownership diagnostics + `serialize.test.ts`, `timeline-data.test.ts`, `useTimelineSave.draftConfig.test.ts`, `shotCompositionProjection.test.ts` | **exit0, 5 files / 94 passed (91 unchanged repo + 3 private),8.80s**; `notes/targeted-final.log` |
| Exact captured `canonicalCompositionState.mainImageCap.test.ts` from `tl/app-m3-render-stored-occurrence-cap-boundary` | **exit1,1 test failed,3.57s**; unchanged assertions: hold5 instead of4; f105opacity1 instead of0.5; frame120 still has a layer; `notes/captured-regression.log` |
| Scoped ESLint of projection/data/domain/disk serializers/recovery/popup source, `--report-unused-disable-directives --max-warnings 0` | **exit0**, no diagnostics; `notes/lint.log` |
| `git diff --check`, `git status --short`, root dependency-link check | **exit0**, no source changes; link restored to `/home/user/work/app/node_modules` |

Captured fixture SHA256 **ad3d0ad35876665489080703c2323a8840c9187428dbe28a913e8ab4ada53f04**. Both captured test and fixture are byte-exact git-show copies under notes, not rewritten tests in this worktree. The regression remains failing; no lost behavior was encoded as a new positive or weakened assertion.

Initial attempts retained in notes: runner startup failed until the owned notes dependency link existed; first private run had one mistaken array-length assertion (2 diagnostics passed,1 failed), corrected only in the private diagnostic; first neighbor batch had80 passes and one import/setup failure because the borrowed frozen Agent copy no longer existed. An owned minimal archive fixed that runner input. The final94pass run is the qualification cited above.

## Disposition / resume point

**BLOCKED**, not DONE; no KEEP marker for a nonexistent candidate. `app-stored-cap-scalar-consumer.patch` and `.files.txt` are intentionally empty and document the zero source delta. They are not a scalar+consumer candidate. Commit-msg is supplied for the harness, but there are no worktree changes to commit.

Recommended next step for the orchestrator: clarify/authorize the smallest additional **verified raw-to-view ownership propagation into disk/edit/draft/popup exits**, including overwritten raw child app counterparts. Existing command bundles/graphs must remain the raw authority; persisted intent/request bytes stay untouched. Then resume one shared scalar+consumer unit and give Viewing its exact source plus permanent serialization/4000vs4500/atomic-delivery tests. Do not accept a scalar-only or consumer-only partial patch.

No full suite, project typecheck, build, browser, live socket, install, package/pin change, shared dependency/venv/cache mutation, merge, push, renderer capture or parity claim. New scalar production/consumption,4000vs4500mailbox delivery, local/recovery/accepted/bootstrap recomputation and safe stripping remain **unimplemented/unverified**.
