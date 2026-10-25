# Findings

## PASS_SOURCE

No source findings.

The cumulative join has the expected ancestry and resolution scope:

- normal ours: `d5a1d1ab6550187e377fd7387d300102b8b82ece`
- first merge: `002a82339c934d75894467032d788606257315fa`
- actual upstream: `36e1ef39c03c2c91a36fd964e3a2385a410bc06c`
- current-tip return: `e9041a262186747548c6a74c1e6fa6cf6313f1f4`
- final model-menu return: `eba8b345c1389402b11412eff52d2ac4e130b4a7`

The independent merge-tree comparison found exactly the seven expected resolution deltas: the five content conflicts (`public/install-manifest.json`, `AgentChat.test.tsx`, `AgentChat.tsx`, `AgentChatMenu.tsx`, `TourChatPanel.tsx`) and the two NewChatMenu modify/delete paths (`NewChatMenu.test.tsx`, `NewChatMenu.tsx`). All automatic non-conflicting blobs were retained. The final return changes exactly the three authorized model-menu sources.

The 2014 warm-up fixture change is faithful deterministic setup: it changes only the modeled `/models?sessionId=` failure status from retryable `502` to terminal `400`; payloads, inputs, session-count assertions, recovery sequence, and generic/setup intent remain unchanged. The two exact warm-up predicates pass under Node `20.19.4`.

The final three sources preserve the unified App menu semantics while restoring upstream behavior: NewChatMenu row selection only records the next choice, its per-model `New chat` button starts once, AgentChatMenu row selection still starts immediately, and compact `· <level>` / selector styling is limited to NewChatMenu. The restored upstream NewChatMenu test file is byte-identical to `36e1ef39c0`.

The mounted App save path and public Runtime `commitTimeline` path were audited read-only. The final menu changes do not touch the persisted outbox, document patch/semantic command construction, idempotency transport, Runtime client, door route, or reply handling. The existing C0 v2 request/reply fields and authority/privacy guards remain in the inherited source.

The manifest preserves Agent `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2`, Runtime `ab1e4f6141987706132916e2da16477f5a019464`, schema digest `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`, VibeComfy `31f90bb03d330283b76e7dbdda51197be787090d`, and OMP `78f0e0960f471c2c62b943272a48c33366f239fe`. Producer-first cut pins remain pending as required; no manual pins or refused-route workaround was introduced.
