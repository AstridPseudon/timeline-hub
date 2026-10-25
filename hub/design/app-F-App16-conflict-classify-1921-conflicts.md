# App16 source-only conflict classification

The qualified App census has exactly 16 conflict paths and 81 merge-preview hunks. Census overlap was not treated as semantic proof. After reading the exact base, ours, and upstream blobs, all 81 conflicting preview hunks are classified `semantic`: each contains executable behavior, a contract/pin, a protected test predicate, or UI/session authority. No accepted merge was invented.

The exact hunk bytes are cited by `(path, @@ header)` in the read-only preview:

```text
git merge-tree --trivial-merge 3881e9440688f774878e18806da2dc5c993a9b00 d5a1d1ab6550187e377fd7387d300102b8b82ece 213318f1ec6ea5c324787bbd1c30a73072d1151a
sha256 6c7cf7073a554a81ddbfe9aca90da2a192e73bed90245e137e030998c4439535
bytes 769114
```

Side blob citations are recorded in `findings.json`; each is an exact `git show BLOB:path` source, with the same immutable base `3881e9440688f774878e18806da2dc5c993a9b00`, ours `d5a1d1ab6550187e377fd7387d300102b8b82ece`, and upstream `213318f1ec6ea5c324787bbd1c30a73072d1151a`.

| Path | Base / ours / upstream blobs | Exact merge-preview hunks | Class | Owner and concrete decision |
|---|---|---|---|---|
| `package.json` | `a91b81db` / `84e4f6e6` / `5bdc5b0a` | `@@ -9,6 +9,9 @@` | semantic | Retain both script/dependency families; reconcile differing scripts and pins from final integrated sources. |
| `public/install-manifest.json` | `52f48984` / `47df36d1` / `4ba29b08` | `@@ -1,11 +1,22 @@`; `@@ -42,7 +53,7 @@` | semantic | App release owner regenerates from final Agent/Runtime commits; preserve upstream vibecomfy/OMP additions. |
| `src/app/onboarding/WelcomeConnection.test.tsx` | `30fdfd95` / `26df345b` / `b685a480` | `@@ -18,6 +18,11 @@`; `@@ -154,7 +159,7 @@` | semantic | Preserve upstream permission mock and wording plus existing no-fetch/no-permission predicate. |
| `src/integrations/astrid/localAgents.ts` | `7cb0a23e` / `d0e540ea` / `4dd520e9` | `@@ -32,20 +32,66 @@`; `@@ -57,11 +103,18 @@` | semantic | Preserve catalog/default-agent/unknown-agent refusal and existing session identity behavior. |
| `src/integrations/paired/pairedRoutePolicy.test.ts` | `ba560ef0` / `3e920fff` / `f66fdbaf` | `@@ -21,6 +21,7 @@`; `@@ -74,6 +75,7 @@` | semantic | Preserve local-door-only refusal set and upstream selection/API-key fixtures, derived from mounted calls. |
| `src/integrations/runtime/client.ts` | `35f523c3` / `9f105079` / `126ef1d1` | `@@ -620,6 +620,10 @@` | semantic | Preserve v2 client, identity fences, and failure classification; add selectProject without changing commitTimeline authority. |
| `src/shared/components/SettingsModal/sections/ConnectionSection.tsx` | `7f36f6c1` / `d3b24fdc` / `9e7f4f34` | `@@ -1,7 +1,7 @@`; `@@ -54,8 +54,14 @@` | semantic | Preserve upstream status cases and all existing cases; normalize only trailing whitespace later. |
| `src/tools/video-editor/components/AgentChat/AgentChat.projectContract.test.tsx` | `6ccf2f86` / `3b25e68e` / `aff454f7` | `@@ -4,6 +4,7 @@`; `@@ -33,6 +34,9 @@`; `@@ -43,6 +47,7 @@`; `@@ -65,8 +70,10 @@`; `@@ -103,6 +110,7 @@`; `@@ -119,6 +127,7 @@`; `@@ -186,6 +195,121 @@` | semantic | Preserve upstream setup/HostTransport and ours owned-ACP transport families; no predicate weakening. |
| `src/tools/video-editor/components/AgentChat/AgentChat.test.tsx` | `162e6256` / `06c5ef55` / `e48139a8` | `@@ -6,7 +6,11 @@`; `@@ -175,6 +179,8 @@`; `@@ -182,6 +188,8 @@`; `@@ -265,6 +273,13 @@`; `@@ -314,7 +329,219 @@`; `@@ -452,7 +679,7 @@`; `@@ -513,6 +740,12 @@`; `@@ -1365,7 +1598,11 @@`; `@@ -1374,8 +1611,16 @@` | semantic | Preserve setup/catalog/terminal-nudge and voice/session/queue test families. |
| `src/tools/video-editor/components/AgentChat/AgentChat.tsx` | `a82ace6b` / `db6cf3f8` / `7c0fc8ef` | `@@ -3,7 +3,7 @@`; `@@ -45,7 +45,12 @@`; `@@ -315,8 +320,15 @@`; `@@ -521,9 +533,11 @@`; `@@ -534,7 +548,17 @@`; `@@ -546,11 +570,69 @@`; `@@ -657,6 +739,7 @@`; `@@ -668,11 +751,10 @@`; `@@ -683,7 +765,7 @@`; `@@ -882,6 +964,8 @@`; `@@ -906,49 +990,57 @@`; `@@ -1017,7 +1109,7 @@`; `@@ -1038,10 +1130,17 @@`; `@@ -1057,7 +1156,36 @@`; `@@ -1080,7 +1208,7 @@`; `@@ -1142,20 +1270,48 @@`; `@@ -1185,7 +1341,8 @@`; `@@ -1201,7 +1358,8 @@`; `@@ -1373,7 +1531,7 @@`; `@@ -1396,6 +1554,7 @@`; `@@ -1461,6 +1620,35 @@` | semantic | Integrate upstream setup/error/terminal with timeline-session gate, voice, and unified menu; no bypass of outbox/Runtime. |
| `src/tools/video-editor/components/AgentChat/AgentChatMenu.tsx` | `1f8ec360` / `fa386e33` / `9305a169` | `@@ -1,3 +1,4 @@`; `@@ -9,6 +10,14 @@`; `@@ -55,6 +64,8 @@`; `@@ -84,9 +95,14 @@`; `@@ -299,6 +315,7 @@`; `@@ -365,6 +382,26 @@` | semantic | Reconcile unified menu API with upstream setup/terminal actions, preserving focus and callbacks. |
| `src/tools/video-editor/components/AgentChat/AgentChatModelLine.tsx` | `bafb8fdc` / `a851a9bc` / `831f3bb0` | `@@ -6,7 +6,7 @@` | semantic | Preserve coarse-pointer sizing and model-change focus handoff. |
| `src/tools/video-editor/components/AgentChat/TourChatPanel.tsx` | `cba152e0` / `3d800101` / `d4c5e76f` | `@@ -152,8 +152,18 @@` | semantic | Keep static no-session tour and unified menu; add only upstream coarse styling after anchor review. |
| `src/tools/video-editor/hooks/useAgentSession.ts` | `33297d96` / `08bb37dd` / `2f250db1` | `@@ -1,4 +1,4 @@`; `@@ -13,7 +13,7 @@`; `@@ -71,6 +71,7 @@`; `@@ -91,7 +92,9 @@`; `@@ -352,6 +355,7 @@`; `@@ -363,7 +366,7 @@`; `@@ -388,6 +391,10 @@`; `@@ -416,7 +423,7 @@`; `@@ -430,7 +437,7 @@`; `@@ -443,7 +450,7 @@`; `@@ -464,14 +471,14 @@`; `@@ -497,18 +504,18 @@`; `@@ -536,7 +543,7 @@`; `@@ -550,7 +557,7 @@`; `@@ -589,6 +596,7 @@`; `@@ -616,7 +624,7 @@`; `@@ -651,9 +659,11 @@`; `@@ -784,7 +794,7 @@`; `@@ -1324,7 +1334,7 @@` | semantic | Preserve current identity/diagnostics/lifecycle and upstream setup-error/retry state; no second writer. |
| `src/tools/video-editor/pages/VideoEditorPage.test.tsx` | `f7546db6` / `9cb4d5da` / `7565bdcf` | `@@ -1212,9 +1212,7 @@`; `@@ -1542,6 +1540,21 @@` | semantic | Preserve publication-aware transport and deleted-URL creation test. |
| `tests/e2e/fake-runtime/server.contract.test.mjs` | `d519e743` / `62a0e80d` / `ab92ec30` | `@@ -103,7 +103,7 @@`; `@@ -335,6 +335,23 @@`; `@@ -584,8 +601,11 @@` | semantic | Preserve retired-write, auth, selection, and catalog assertions. |

All exact full-length blob IDs and the machine-readable hunk list are in `findings.json`. The owner decisions are in `conflict-classes.json`. No trivial resolution patch was prepared because no conflicting hunk was provably behavior-free.
