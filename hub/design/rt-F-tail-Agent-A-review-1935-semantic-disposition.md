# Agent first-20 semantic disposition

Result: PASS. This is an independent source review of the exact BASE
`92443771676ef2bbb547d0a103d708fa8bec4c63`, OURS
`547e10456250c1b5bcf63b44a50c90ff0563ce1e`, and UPSTREAM
`886a3183bd4a4a44f0a2c08fabec4e8edcbf7b55` objects. It covers the first 20
qualified Agent conflict paths only; the disjoint last-20 worker is not
reviewed here.

## Disposition rule

`auto-compose-source-or-test-addition` means the upstream hunk changes source
or a behavior test, but the captured ours change is only one extra EOF blank
line in that file. It is therefore a real upstream behavior addition, yet no
mutual-intent choice exists between the two sides. The hunk can be retained
alongside the private EOF normalization.

`auto-compose-skills-route-addition` is the same conclusion for the two
upstream `dispatch.py` hunks: they add `_dispatch_skills` and its top-level
route, outside the ours-only doctor import relocation.

`generated-rebuild-required` applies to every `service.mjs` upstream hunk.
This is not a source-owner gate and not a hand-merge candidate. The source
changes compose at `service.ts`/its dependencies; `service.mjs` must be
regenerated after those source decisions.

There are zero genuine mutual-intent/owner-question hunks in this partition.
The earlier broad label “semantic-intent” was insufficient because it
conflated “behavioral upstream addition” with “collision requiring a choice.”
No artificial decision gate is created here.

## Ours-side exact classification

- 18 files / 18 hunks: one ours-only blank line at EOF, deletion-only in the
  private normalization patch. The affected paths are every path below except
  `astrid/chat/service.mjs` and `astrid/core/gateway/dispatch.py`.
- `astrid/chat/service.mjs`: 15 semantic generated-bundle hunks; do not hand
  merge.
- `astrid/core/gateway/dispatch.py`: 2 semantic import-relocation hunks for
  `RuntimeCLI`/`RuntimeCLIError` in `_dispatch_doctor`; preserve this source
  behavior while composing the independent upstream skills route.

## All 95 upstream hunks

The hunk ranges below are the exact `git diff --unified=0 BASE UPSTREAM`
ranges (the census format omits each header's trailing function/context text).
Each header has an explicit disposition; counts sum to 80 auto-composable
source/test additions plus 15 generated-rebuild hunks.

### Auto-composable source/test additions — 80 hunks

| path | upstream hunk headers | concrete upstream addition |
|---|---|---|
| `astrid/chat/acpProcessHost.test.ts` | `@@ -126,0 +127,21 @@` | Regression test for unavailable saved models and new-chat recovery. |
| `astrid/chat/acpProcessHost.ts` | `@@ -60,0 +61,3 @@`; `@@ -65,0 +69 @@`; `@@ -72,0 +77 @@`; `@@ -80,0 +86 @@`; `@@ -451,0 +458,4 @@`; `@@ -453 +463 @@` | ACP error codes, next-action data, and saved-model recovery text. |
| `astrid/chat/astrid-acp-bridge.ts` | `@@ -9,0 +10 @@`; `@@ -12,0 +14 @@`; `@@ -15 +17 @@`; `@@ -107,0 +110 @@`; `@@ -349 +352 @@`; `@@ -382,0 +386 @@`; `@@ -387,0 +392 @@`; `@@ -432,2 +437,5 @@`; `@@ -441 +449,2 @@`; `@@ -452,0 +462,13 @@`; `@@ -707,0 +730,2 @@` | Local-agent skills/key setup, sign-in/credit/terminal projections, and connection lifecycle behavior. |
| `astrid/chat/astrid-acp-models.test.ts` | `@@ -7 +7 @@`; `@@ -128,0 +129,5 @@`; `@@ -217 +222,4 @@`; `@@ -219 +227 @@`; `@@ -221 +229 @@` | Catalog assertions for sign-in, setup steps, credits, terminal metadata, and keyless/unknown states. |
| `astrid/chat/astrid-agent-models.test.ts` | `@@ -20,0 +21 @@`; `@@ -28,0 +30 @@`; `@@ -30,0 +33,4 @@`; `@@ -64,0 +71,11 @@`; `@@ -73,0 +91 @@`; `@@ -76 +94,6 @@`; `@@ -147 +170 @@` | Provider metadata and bounded model-discovery behavior tests. |
| `astrid/chat/astrid-agent-models.ts` | `@@ -14,0 +15,4 @@`; `@@ -32 +36,2 @@`; `@@ -53,0 +59,4 @@` | Provider usability/login metadata and a 10-second discovery timeout. |
| `astrid/chat/astrid-local-agent-host.ts` | `@@ -5 +5 @@`; `@@ -104,2 +104,2 @@` | Setup-specific ACP error codes and next actions for missing/sign-in/runtime states. |
| `astrid/chat/astrid-local-agents.test.ts` | `@@ -6 +6 @@`; `@@ -46 +46 @@`; `@@ -55,0 +56 @@`; `@@ -88 +89 @@`; `@@ -109 +110 @@`; `@@ -114,0 +116,2 @@`; `@@ -134 +137 @@`; `@@ -259,0 +263 @@`; `@@ -264,0 +269 @@`; `@@ -300 +305 @@`; `@@ -304 +309 @@`; `@@ -312,0 +318 @@`; `@@ -365,0 +372,57 @@` | Authentication-state, platform-shim, and setup-step behavior coverage. |
| `astrid/chat/astrid-local-agents.ts` | `@@ -6 +6,2 @@`; `@@ -232 +233 @@`; `@@ -238 +239 @@`; `@@ -263 +264 @@`; `@@ -288 +289 @@`; `@@ -290 +291 @@` | Local-agent catalog choices and setup/error behavior. |
| `astrid/chat/astrid-project-chat.test.ts` | `@@ -75,0 +76,21 @@` | Failed chat creation releases its claim for retry. |
| `astrid/chat/astrid-project-chat.ts` | `@@ -282,40 +282,47 @@` | Operation-scoped failed-claim cleanup while preserving lost-reply safety. |
| `astrid/chat/astrid-shared-acp-sessions.test.ts` | `@@ -175,0 +176,23 @@` | Failed prompt retries release request IDs. |
| `astrid/chat/astrid-shared-acp-sessions.ts` | `@@ -329 +329,7 @@` | Failed dedupe operations remove their own pending entry. |
| `astrid/chat/discoveryProbe.ts` | `@@ -5 +5 @@`; `@@ -9 +9 @@`; `@@ -46,0 +47,4 @@` | Optional stdin delivery and stdin-error cleanup for discovery probes. |
| `astrid/chat/localAgents.ts` | `@@ -1,0 +2 @@`; `@@ -9 +10,2 @@`; `@@ -18,5 +20,6 @@`; `@@ -24,5 +27,5 @@`; `@@ -30 +33,5 @@`; `@@ -40 +47 @@`; `@@ -60,0 +68,22 @@`; `@@ -83 +112 @@`; `@@ -88,0 +118,5 @@`; `@@ -93 +127 @@` | Agent sign-in/install commands, catalog metadata, setup steps, and terminal schema. |
| `astrid/chat/modelCatalog.ts` | `@@ -14,0 +15,2 @@` | Provider usability, login, and recommendation metadata in the schema. |
| `astrid/chat/service.test.ts` | `@@ -54 +54 @@`; `@@ -55,0 +56 @@`; `@@ -62 +63 @@`; `@@ -70,0 +72 @@` | Working-directory creation and actual loopback-listener coverage. |
| `astrid/chat/service.ts` | `@@ -1,0 +2 @@`; `@@ -15,0 +17 @@` | Create the configured service working directory before serving. |
| `astrid/core/gateway/dispatch.py` | `@@ -74,0 +75,5 @@`; `@@ -552,0 +558 @@` | Add `_dispatch_skills` and the `skills` top-level route; independent of the ours doctor import move. |

### Generated rebuild required — 15 hunks

| path | upstream hunk headers | disposition |
|---|---|---|
| `astrid/chat/service.mjs` | `@@ -2 +2 @@`; `@@ -4,4 +4,4 @@`; `@@ -9 +9 @@`; `@@ -14,3 +14,3 @@`; `@@ -19 +19 @@`; `@@ -22,3 +22,3 @@`; `@@ -26 +26 @@`; `@@ -30,3 +30,3 @@`; `@@ -35 +35 @@`; `@@ -38 +38 @@`; `@@ -40 +40 @@`; `@@ -42,7 +42,7 @@`; `@@ -51 +51 @@`; `@@ -54 +54 @@`; `@@ -56,3 +56,3 @@` | Do not hand-merge minified output. Regenerate from final source/dependencies; the generated artifact has no independent owner decision. |

## Owner-question check

No FAIL and no concrete owner question was found in these 95 upstream
hunks. The only follow-up is procedural: the eventual Agent owner/merge
worker must regenerate `service.mjs` after source composition. That is not a
new gate and does not authorize hand-merging generated output.
