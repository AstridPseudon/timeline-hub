# BLOCKED — ordinary retained Scene caller needs an invocation contract

Base: Agent `5d1faff480b82affe8ea727839ef4594d684bb00`.
Read PLAN.md, the prior `sdk-scene-existing-retention-join/owner-sdk.patch`, and the independent `sdk-retained-scene-proposal-final-gate/REPORT.md`.

The independent approval correctly qualifies the retained helper, but its remaining owner activation step is not an existing ordinary caller. There is no original-request/workspace handoff from the host to `Checkout.check()`. D09 remains held. No activation patch is supplied: another optional tuple/helper would repeat the previous result, and manufacturing the missing request or Runtime claim would violate this brief.

## Exact source evidence

Paths and line numbers below are relative to this worktree.

- `astrid/packs/timeline/cli.py:3555`: ordinary `_cmd_check` finds the draft, calls `Checkout.load(path)` at 3563 and `tl.check()` at 3564. Its Runtime client is used for draft lookup and later optional verification, not retained scene input acquisition. Verification starts **after** the report is already computed (3568–3570).
- `astrid/sdk/timeline/checkout.py:35`: Checkout retains authored bundle/path/editor state. `open` (83) fetches a bundle and returns `cls(bundle)`; `load` (113) reads a draft. Neither retains a render request or host attempt. `astrid/sdk/timeline/check.py:534` calls `_check(diagnostics=True)`; its `_on_screen` at 81 constructs the old authored coverage input. There is no `_scene_inputs` assignment/consumer in this source tree. The proposal adds the consumer but no production assignment.
- The real working-candidate capture port exists: `astrid/sdk/timeline_filmstrip.py:414` calls `candidate_projection`, validates target scope, and carries the real working-copy marker. `prepare_filmstrip` (675; candidate branch 818) returns a capture snapshot with config, registry, exact closure, extent and `metadata.scene_clips` (889–913). This is **projection/admission input**, not a host attempt or original RenderRequest. Reading it locally does not produce the retained original pair.
- `astrid/core/execution/generic_host.py:9170` calls `_materialize_inputs` inside execution of an admitted task. Its authorization checks start at 6452. `astrid/core/rendering/verified_source.py:124` mints the source only from those admitted inputs. Calling this with a locally manufactured `input_object_ids`/`authority_context` envelope would be a caller fake certificate, not ordinary SDK integration.
- `generic_host.py:8016` hands the source into the **child's** environment. `verified_source.py:182` binds `{ref, authority, snapshot, prepared}`; it does not retain RenderRequest, backend settings, review context or theme selection. `inherited_source` at 190 validates a supplied path pair; it neither acquires a host attempt nor recovers the original request. Successful ephemeral attempts can be deleted at `generic_host.py:9976–9981`. Returning their paths to a later CLI call would not preserve lifetime.
- The original request is constructed in the executor-side render facade, `astrid/packs/rendering/actions/render/run.py:472–489`, including backend settings, review metadata and materialized objects. It is immediately sent to `RenderService.render` at 493. The service adapts it for segments at `astrid/core/rendering/service.py:1357–1369`; `_segment_request` at 1053 delegates to materialization. There is no Checkout object or callback from this retained original-request scope to ordinary `check`.
- The other real candidate port, `astrid/sdk/authoring_render_preview.py:216–233`, freezes the candidate and calls `client.invoke_result("rendering.render", ...)`. It returns the managed result, not a Python continuation inside the host's original-request lifetime. `Timeline.for_render` (`astrid/core/timeline/banodoco_composer.py:255`) supplies the existing render view; it does not acquire that lifetime or render settings.
- The existing visual capture caller is `astrid/packs/rendering/actions/timeline_visualize/filmstrip_execution.py:1766–1782`: it owns the materialized pair and constructs `RemotionFrameProvider` inside the executor. Public Scene answers are retained inside that provider's fresh capture (`composed_frame.py:665–715,760–810`). Its outer receipt projects addresses (`filmstrip_cards.py:1675–1695`), not the full-film coverage/content/findings needed by Checkout. Reusing the remote output as a full Scene report requires a contract change, and performing pixel capture would also change this query-only task into rendering.
- `_prepared_remotion_root` holds the desired exact serializer/theme/assets/extent lifetime (`root_preparation.py:17–212`); `_prepared_host_frames_at` correctly queries inside it (`scene_answers.py:117`). The missing part is the source owner's invocation into that lifetime and return of advice to the ordinary SDK caller. Neither helper can supply that missing process/lifetime handoff itself.

## Reproduction and tests

All changes used for reproduction were in a disposable overlay below this worker's own scratch directory. Product SDK/core/tests remained untouched. COMMAND.sh copies the prior proposal into that overlay and loads its two methods on Checkout, exactly as the independent review did. The existing fixture uses real candidate compilation, `prepare_filmstrip`, host materialization, Root preparation, serializer and public12 Node transport; Runtime read/admission and host admission/unused port selection remain doubles. No live Runtime or pixels are claimed.

Exact command:

```sh
bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-sdk-scene-ordinary-retained-caller/COMMAND.sh
```

Result: **29 passed, 2 strict xfailed in 5.75s**, exit 0 (`pytest.log`). The 29 controls comprise the prior two registered-Node saved/candidate positives, 11 stale/forged/unavailable negatives, and all 16 saveNoNode tests. No passing behavior test was rewritten, removed or weakened.

The two added scratch-only tests express the missing requirement: ordinary `Checkout.check()` must reach public Node **without** the manual tuple. They preserve the actual prepared pair, workspace and inherited source, removing only `checkout._scene_inputs`. This gives the ordinary call an even more favorable environment than CLI. Both still fail to query Node.

To expose those failures without xfail handling:

```sh
PYTEST_ADDOPTS='--runxfail -k ordinary_check_activates' bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-sdk-scene-ordinary-retained-caller/COMMAND.sh
```

Result: **2 failed, 29 deselected in 3.56s**, exit 1 (`ordinary-required.log`); both fail exactly at `assert observed` with `ordinary check never reached public Node; prior _scene_inputs setup is necessary`. This is deliberately unmet acceptance evidence, not a green activation claim.

The fixture reuses the CLEAN f816 peer graph read-only, pinned OWN Node and public12 archive, with all 77 package files checked unchanged by fixture teardown. It creates real private scope parents and only leaf peer symlinks. No install, network, browser, sockets, full suite, shared cache/dependency mutation or central-service request. `git diff --check` passed; worktree status is clean. Disposable scratch was removed by the command trap.

## Smallest contract request to the orchestrator / Agent owner

Authorize **one internal scene-only request/result handoff through the existing managed visualization invocation**, rather than a new source authority or endpoint:

1. Ordinary explicit `Checkout.check()` freezes its real `preview_authoring_candidate` and uses the existing saved/candidate `prepare_filmstrip` admission path. The frozen candidate must reach the task as plain data; native/CAS-only input stays UNCERTIFIED under the approved rule.
2. The existing executor consumes the host-owned original full materialized pair and admitted render settings, queries all canonical extent frames using `_prepared_remotion_root` before any segmentation/cleanup, and returns the frame Scene answers plus the existing occurrence/address map in its result artifact while that lifetime is valid. No PNG render, new projector, new authority factory, provider or store is needed.
3. Checkout formats that returned advice with its existing `_scene_problems` reader; absent/stale/mismatched results are advisory unavailable. `_check_core`, save, publish and transaction stay unchanged.

What needs approval is the internal invocation mode and full Scene result carrier: neither exists today. Reusing generic JSON transport does not make its new semantics an existing shared contract. Do not apply the previous SDK proposal as if that owner step were already implementable by an assignment in `_cmd_check`.

Local draft/native-CAS uncertainty is **not** a reason to blanket-refuse old positives: no such behavior change was made here. It also does not conjure a live original RenderRequest, its theme/review/settings, or an executor-to-Checkout result carrier. Ordinary saved/candidate Node activation remains unverified and unmet until the owner supplies/approves the missing handoff. The next qualification should replace these two strict expected failures with actual ordinary-call positives, keep existing stale/forged refusals and all 16 saveNoNode controls, and leave the full suite to its existing owner gate.
