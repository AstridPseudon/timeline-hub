# G5 return handoff — agt-G5-return-0724

Source: 0f87c51cfce84a503d5af13a5771c9bfdcbf426b.

The reachable duplicate/restructure callers now use timeline.open().commit() with existing semantic identity capture plus the G3 emitter/session. Dead CLI separate-publish code is removed; the deleted publish_bundle test tripwire is retained with raising=False. Narration/transcript follow-up and duplicate archive cleanup remain.

Measured gates: Ruff 2148/2148; private mypy 1904/1904; vendor lock, artifact manifest, compileall, diff-check pass. Targeted evidence: timeline sync 79 passed; P4/emitter/authoring 60 passed, one stale parsed.native assertion; duplicate pure behavior 6 passed. Restructure legacy module is blocked at collection by its retained import of deleted three_way; old duplicate fake client lacks the new session handshake. No full suite run. Do not merge until HEADER P1 GO.

