# WC5 PRIVATE017 current-source requester prerequisite

Status: dormant Agent source descendant only; not approved execution.

Base: `6c1989adf723ae0ea0f4205c1cc8f1c0e4b22e79`, tree
`cc0a8dd1360324a1b440ba7d318a083e7f8814cc`.
Reviewed source: `f07d97715fbe4efcb80e2db40ef4597e81f75547`, tree
`fb785ef2f9b4bafcfde9b15eacb5f8e3025e3e17`, independently
reviewed APPROVE in `agt-review-wc5-containing-private-entry-1014/report.md`.

Ported only the reviewed optional settled-speech input/context and requester
seam:

- `settled_speech_input` is an optional existing action file input. The
  managed attempt root is supplied by the lifetime-fenced action context.
- Managed execution uses the existing worker read connection and verifies its
  handshake actor/scopes against the trusted outer executor.
- The private consumer rechecks the H3 envelope, task/run/attempt, project and
  capability, task inputs/state/result, managed output binding, Runtime's
  exact five-field media selection, verified WAV bytes/hash/size, and intrinsic
  duration before existing preparation/capture sees a row.
- The dormant `requester_entry=True` path forwards the current candidate,
  pinned scripts, exact four-key admitted target, and outbox path to the
  reviewed requester. That requester queues the existing seven-key proposal
  through `TimelineSession.queue_proposal` and `flush`.

No public caller, default behavior, endpoint, DTO, store, journal, authority,
worker speech root, inner/outer alias, native/HTTP/settlement execution, pin,
schema, generated client, or lock bytes were changed. The original public
voiceover path and no-op behavior remain intact. Live callers changed: none;
the entry remains private and dormant.

Source file blob parity with the reviewed descendant:

```
938dbdf22736f54b4716f2dad6aa4b6f01869298  _action_context.py
d3fd2f0a54c15dd3e130aec7e20d61b6342b4ecd  sync_draft_voiceover/run.py
66c8bf4d1408cef41d3d9d4eda8cc705ac00f720  video_editing/pack.yaml
1192b9f9d8a3a6e93583974490af189b8b3ab714  draft_voiceover.py
309214b579d1c0e5b4960390255d24949736bf83  settled_voiceover_input.py
ef4ec61829828a325689c8d8a0b434062904ce64  voiceover_requester.py
```

The normal client/lock and frozen schema paths were checked with
`git diff --quiet BASE -- PATH` and remain byte-identical, including
`runtime.lock.json`, the generated Runtime client files, the canonical edit
schema, and the frozen current-union fixture.

Later prerequisite: independently review this current-tree source, then a
containing release may qualify a genuine outer workflow. That later work must
reuse Runtime's ordered/RT03/materialization evidence and must not be claimed
by this dormant source port.
