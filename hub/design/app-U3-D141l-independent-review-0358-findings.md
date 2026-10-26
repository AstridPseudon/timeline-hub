# U3 D141l independent review — FAIL

Candidate: `8f278b91accec5852e39bb84822e99124fccb81d`, tree
`99d79cb47496c0ca682b0cd42aa911177761bb31`.

Parents, in order: local `520d7e4fc12a03392afaed3f486aba34a2b5c319`; upstream
`d822d2f5d2bd05187b4ff5b6071c3e13945d4747`, tree
`2af40a015057779ceb4e4b37cad62e1469aa7e36`.

## Blocking finding

`public/install-manifest.json` preserves the qualified App tuple (Agent
`28e56cacb42d3da85b02e5b3543895b44f3d0f70`, Runtime
`6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d`, Runtime schema
`sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`,
and VibeComfy `31f90bb03d330283b76e7dbdda51197be787090d`) and the manifest is
tool-generated. However, upstream `61062e5556829be54139408c6e039861557c6621`
pins Agent `e1c751def40f8fde59277226b6c190354d22744c`, whose
`astrid/installer/tools.py` adds the required
`User-Agent: astrid-installer/<ASTRID_VERSION>` header to installer downloads.
The candidate producer `28e56cacb42d3da85b02e5b3543895b44f3d0f70` does not
contain that behavior, and the two commits are unrelated in ancestry. Thus the
freeze-2 installer behavior is lost behind the candidate manifest pin.

Exact fix scope: qualify the exact later Agent freeze-2 receiving producer that
contains the installer-UA behavior, then regenerate the manifest through
`scripts/installer/update-manifest.mjs`. This is an Agent qualification /
U4p dependency, not an App-side manual pin or source fix. Until that producer
receipt exists, this candidate is FAIL.

No additional product/test findings were found in this pass.

## Conservation accounting

The 16 unique upstream paths are the 15 paths changed from the local parent
plus the manifest conflict path. The nine `d0853acbc5` preview paths are
present; `61062e5556` is represented only by the manifest pin and is the
blocking loss above; `7796159ce8` whole-chat Markdown export paths are present;
and `d822d2f5d2` sent-request filtering / composer Stop paths are present.
The four conflict paths were inspected against both parents: manifest,
`AgentChat.tsx`, `AgentChat.test.tsx`, and `RemotionPreview.tsx`. No conflict
markers remain in the candidate.

The Tour early gate remains before session hooks and the production transcript
anchor remains present. The live Runtime door/status path, voice path, menu,
draft/outbox queue persistence, dependent queue recovery, and existing
semantic/doc.patch/undo callers were not overwritten. Sent-request filtering
uses transcript request IDs plus active/optimistic guards. Markdown export
includes the complete session snapshot, editor actions, optimistic input, and
assistant draft. Calmer preview transport retains hover reveal, compact/touch
behavior, volume/speed/fullscreen, and removes the loop Player prop/control.

Protected `src/tools/video-editor/commands`, `src/integrations/runtime`,
`src/tools/video-editor/hooks`, `src/shared/lib/placement`,
`TourChatPanel.tsx`, and `TourChatPanel.test.tsx` have zero changed paths from
the local parent.
