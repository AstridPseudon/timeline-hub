# REQUEST CHANGES — WC5 requester/outbox source review

Reviewed exact commit `b34e3f8b76fc454b04a63b0be7a059c9ca45bdec` / tree
`86651884460cc5390ef296172ec1cecf39af7946`, parent `a4da7cbe417aa4a3c0f90681020db6e5fd55b757`.

## Finding

The commit adds only a private definition,
`astrid/packs/video_editing/shared/voiceover_requester.py:167`, and the
test calls it directly at
`tests/packs/video_editing/test_voiceover_requester.py:193`. There is no
non-test caller of `_requester_sync_draft_voiceover` in the target tree.
The existing action entrypoint at
`astrid/packs/video_editing/actions/sync_draft_voiceover/run.py:63` calls
`_sync_draft_voiceover_proposal`, not the new requester adapter. `git grep`
finds no other source import or invocation. Therefore the claimed requester
admission → settled outer proposal → producer outbox path is not reachable
from any containing operation; it is a tested orphan helper, not an actual
dormant top-level call site.

The new test does not close this gap: it monkeypatches speech preparation,
outer observation, managed proposal bytes, and `TimelineSession.open`, then
invokes the helper directly. The previously reported 91/32/4 offline counts
therefore do not qualify the real workflow.

## What passed source inspection

- The exact outer action string is
  `video_editing.sync_draft_voiceover` (`voiceover_requester.py:217`),
  distinct from inner `generation.generate_speech` (`:22`, `:137`).
- The original four-field `admitted_target` is checked and retained in
  `runtime_dependencies.publication` (`:193-198`, `:234-242`).
- `execution_request.inputs` and `input_manifest` both carry the same ordered
  descriptor list/object IDs (`:200-233`, `:243-255`). Speech roots and the
  immutable imported bundle remain requester-owned (`:126-164`); the bundle
  does not serialize caller-supplied duration/latest authority. Its H3 result
  envelope remains locator input that the worker rechecks against Runtime.
- The settled proposal is read from the managed object, validated through the
  existing producer-batch contract, and passed unchanged to
  `TimelineSession.queue_proposal` / `flush` (`:282-310`). The original target
  and base pair are supplied to `TimelineSession.open`, and the durable flight
  key is derived from the existing `proposal_digest` (`:301-310`).
- `git diff --name-status a4da7cbe4 b34e3f8b7` contains only the requester
  source and its test. Public/default caller code, frozen 017 schema, Runtime
  DTOs, endpoints, modes, and authority fields are untouched.

## Smallest remaining prerequisite

Add or identify one private, non-public containing operation that actually
calls `_requester_sync_draft_voiceover` while preserving the existing public
014/default caller. Add one compact source regression entering that call site
(not the helper directly) and asserting the exact ordered input/object-ID
mirror, distinct inner/outer identities, managed proposal/digest handoff,
and the existing durable outbox flight. No new public entrypoint, mode, DTO,
authority, Runtime schema, or live/native/HTTP qualification is needed for
that prerequisite.

## Checks run

- `git diff --check a4da7cbe4 b34e3f8b7`: PASS.
- Target-tree `git grep` call-site inventory: confirmed no non-test caller;
  only the helper definition/resource listing and the direct test invocation.
- No broad, HTTP, native, browser, render, or full suite run (per brief).
