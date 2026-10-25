# Current Agent home source census

Captured `2026-10-25T19:43:02.373233Z` from `/home/user/peteromallet/astrid-agent`.

This is a read-only three-way source preview. The actual home integration is `a30e74e901a28b39c28facba3deb00d76f186e23` / `ece8e0887e48e45cb1fce85b1256c49a0f6126c0`; local `tl/integration` at `547e10456250c1b5bcf63b44a50c90ff0563ce1e` is stale and remains historical only.

## Summary

| Item | Result |
|---|---:|
| Ours changed paths | 928 |
| Named-upstream changed paths | 98 |
| Current changed-in-both paths | 41 |
| Current merge-tree hunk headers | 107 |
| Current ours diff hunk headers | 92 |
| Current upstream diff hunk headers | 190 |
| Old 40 exact by-byte reuse | 38 |
| Old 40 partial re-audit | 2 |
| New current conflict | 1 |

Merge-tree output: `583973` bytes, SHA-256 `641d298edc9a34bd0618b5d0f1e07d7c5fba6ee67a8e2101edc9c593ee888284`.

## Exact split for later private join workers

The old A/B scope is retained exactly; do not move old evidence into the current 41-file list.

### First20 (old A scope)

1. `astrid/chat/acpProcessHost.test.ts`
2. `astrid/chat/acpProcessHost.ts`
3. `astrid/chat/astrid-acp-bridge.ts`
4. `astrid/chat/astrid-acp-models.test.ts`
5. `astrid/chat/astrid-agent-models.test.ts`
6. `astrid/chat/astrid-agent-models.ts`
7. `astrid/chat/astrid-local-agent-host.ts`
8. `astrid/chat/astrid-local-agents.test.ts`
9. `astrid/chat/astrid-local-agents.ts`
10. `astrid/chat/astrid-project-chat.test.ts`
11. `astrid/chat/astrid-project-chat.ts`
12. `astrid/chat/astrid-shared-acp-sessions.test.ts`
13. `astrid/chat/astrid-shared-acp-sessions.ts`
14. `astrid/chat/discoveryProbe.ts`
15. `astrid/chat/localAgents.ts`
16. `astrid/chat/modelCatalog.ts`
17. `astrid/chat/service.mjs`
18. `astrid/chat/service.test.ts`
19. `astrid/chat/service.ts`
20. `astrid/core/gateway/dispatch.py`

### Last20 (old B scope)

21. `astrid/core/generation/gpu_environment.py`
22. `astrid/installer/backend.py`
23. `astrid/installer/core.py`
24. `astrid/installer/launcher.py`
25. `astrid/installer/omp/recipe.json`
26. `astrid/installer/service.py`
27. `astrid/installer/tools.py`
28. `astrid/packs/rendering/docs/SKILL.md`
29. `astrid/packs/vibecomfy/environment.windows-nvidia.json`
30. `docs/install/OMP-LANDING.md`
31. `docs/reference/services.md`
32. `docs/testing/TESTING.md`
33. `scripts/refresh_omp_recipe.py`
34. `tests/core/generation/test_gpu_environment.py`
35. `tests/test_installer_acl.py`
36. `tests/test_installer_cleanup.py`
37. `tests/test_installer_lifecycle.py`
38. `tests/test_installer_omp_source.py`
39. `tests/test_installer_platforms.py`
40. `tests/test_installer_wheel.py`

### New current tail (not in old A/B)

- `tests/test_installer_windows_tasks.py` — not covered by the old classification workers; private join owner must classify this current source.

## Conflict/blob/hunk map

| # | Path | Base | Ours | Upstream | Merge hunks | Ours hunks | Upstream hunks | Reuse |
|---:|---|---|---|---|---:|---:|---:|---|
| 1 | `astrid/chat/acpProcessHost.test.ts` | `c1e9602b23b1` | `8619d6ebdefd` | `4fef09d77e26` | 1 | 1 | 1 | exact-byte-identity |
| 2 | `astrid/chat/acpProcessHost.ts` | `c410008357d8` | `971388aa835a` | `4aa1d7de8c7e` | 4 | 1 | 6 | exact-byte-identity |
| 3 | `astrid/chat/astrid-acp-bridge.ts` | `6b7329a3f6d8` | `90818a91e509` | `455d13f34b4b` | 8 | 1 | 11 | exact-byte-identity |
| 4 | `astrid/chat/astrid-acp-models.test.ts` | `ab398a8f5e6b` | `63d5b69eb9b9` | `6bc1c1b8c90b` | 3 | 1 | 5 | exact-byte-identity |
| 5 | `astrid/chat/astrid-agent-models.test.ts` | `1599b6c98a1f` | `ec407f3cc851` | `21fa3c0c168a` | 5 | 1 | 7 | exact-byte-identity |
| 6 | `astrid/chat/astrid-agent-models.ts` | `82ae8f42a1cd` | `3888b90d8fae` | `6223a477ec1e` | 3 | 1 | 3 | exact-byte-identity |
| 7 | `astrid/chat/astrid-local-agent-host.ts` | `f4258dd78169` | `e223c10ac009` | `aa938dd6765c` | 2 | 1 | 2 | exact-byte-identity |
| 8 | `astrid/chat/astrid-local-agents.test.ts` | `31c8f3fe305e` | `0fcbe2999d13` | `6e614214b699` | 10 | 1 | 13 | exact-byte-identity |
| 9 | `astrid/chat/astrid-local-agents.ts` | `9fe3e410c3d9` | `e7b15de9f5ad` | `2344c0dafdf5` | 4 | 1 | 6 | exact-byte-identity |
| 10 | `astrid/chat/astrid-project-chat.test.ts` | `42c112ac990b` | `e1fe377ff8af` | `f399a7c64eb8` | 1 | 1 | 1 | exact-byte-identity |
| 11 | `astrid/chat/astrid-project-chat.ts` | `f33578bc20b2` | `13f1b6c01132` | `c8efeaf87a40` | 1 | 1 | 1 | exact-byte-identity |
| 12 | `astrid/chat/astrid-shared-acp-sessions.test.ts` | `fa469335d2bd` | `c3bc7b16d523` | `790c31642a30` | 1 | 1 | 1 | exact-byte-identity |
| 13 | `astrid/chat/astrid-shared-acp-sessions.ts` | `aacf7ffe99c4` | `f31f2fc92f79` | `8e6c944bff0f` | 1 | 1 | 1 | exact-byte-identity |
| 14 | `astrid/chat/discoveryProbe.ts` | `a328096587b3` | `09ba9f0b0070` | `ade24dfe88bc` | 2 | 1 | 3 | exact-byte-identity |
| 15 | `astrid/chat/localAgents.ts` | `adc3829fb033` | `5f3dbcb90812` | `7bd7d4d419d6` | 6 | 1 | 10 | exact-byte-identity |
| 16 | `astrid/chat/modelCatalog.ts` | `c01412c65eee` | `5de3f13200a7` | `7c650c0c4415` | 1 | 1 | 1 | exact-byte-identity |
| 17 | `astrid/chat/service.mjs` | `c04a5c992684` | `945a9bcf8d0d` | `011689ea7756` | 3 | 15 | 15 | exact-byte-identity |
| 18 | `astrid/chat/service.test.ts` | `a498d3e91243` | `f88e5e44a249` | `4cc86ad09857` | 2 | 1 | 4 | exact-byte-identity |
| 19 | `astrid/chat/service.ts` | `fc30a4eef1dc` | `3b6dfa004bcc` | `ec6b9ca21483` | 2 | 1 | 2 | exact-byte-identity |
| 20 | `astrid/core/gateway/dispatch.py` | `faee0ff3e1a1` | `239587646b1c` | `402362763963` | 2 | 2 | 2 | exact-byte-identity |
| 21 | `astrid/core/generation/gpu_environment.py` | `da1b528d46e3` | `f42e84cce1a9` | `9bccdf3fdeb5` | 2 | 1 | 2 | exact-byte-identity |
| 22 | `astrid/installer/backend.py` | `e28357d09172` | `73930778510c` | `a609940892e8` | 5 | 4 | 6 | exact-byte-identity |
| 23 | `astrid/installer/core.py` | `2db5d9f8b16f` | `15feb564a122` | `8b7c68acd646` | 3 | 1 | 7 | exact-byte-identity |
| 24 | `astrid/installer/launcher.py` | `c803aadda87f` | `2d9b58ea0758` | `6537e27183ae` | 1 | 1 | 4 | exact-byte-identity |
| 25 | `astrid/installer/omp/recipe.json` | `3a3c3290ba1f` | `e1ac1cfe00bc` | `0cbf40c60a51` | 1 | 1 | 7 | exact-byte-identity |
| 26 | `astrid/installer/service.py` | `2974b81ddc0f` | `aaa5c8cb524a` | `a3aa8e5ba45e` | 0 | 2 | 1 | partial-reuse-upstream-base-only |
| 27 | `astrid/installer/tools.py` | `868f7179bc67` | `8a456b340050` | `3efcc8dfd64b` | 3 | 1 | 3 | exact-byte-identity |
| 28 | `astrid/packs/rendering/docs/SKILL.md` | `f5c18de30093` | `7dee1d8c84af` | `715b37ce9b3d` | 1 | 28 | 1 | exact-byte-identity |
| 29 | `astrid/packs/vibecomfy/environment.windows-nvidia.json` | `e553ad26f259` | `3242b3bedb50` | `1eb15b7c4b5b` | 1 | 1 | 1 | exact-byte-identity |
| 30 | `docs/install/OMP-LANDING.md` | `726609bfa437` | `7e425adf1c8e` | `e4ade615a2b8` | 1 | 1 | 16 | exact-byte-identity |
| 31 | `docs/reference/services.md` | `99f72358b32f` | `1cd0d382bdc3` | `24ebff2bab99` | 1 | 1 | 1 | exact-byte-identity |
| 32 | `docs/testing/TESTING.md` | `c54152de6586` | `fbcfcddc4c02` | `df416ca4ed5f` | 2 | 1 | 2 | exact-byte-identity |
| 33 | `scripts/refresh_omp_recipe.py` | `b822d323bfa0` | `277031f1d06d` | `b1d630b5f487` | 4 | 1 | 14 | exact-byte-identity |
| 34 | `tests/core/generation/test_gpu_environment.py` | `bac871fb2f2f` | `f1b0783bb2ba` | `76f2ec69264e` | 1 | 1 | 2 | exact-byte-identity |
| 35 | `tests/test_installer_acl.py` | `ca328ec1ee9f` | `67bb7505c0f2` | `88dd45748db6` | 1 | 1 | 2 | exact-byte-identity |
| 36 | `tests/test_installer_cleanup.py` | `e5ea5450114e` | `c4381c314028` | `f030558f1aa4` | 1 | 1 | 1 | exact-byte-identity |
| 37 | `tests/test_installer_lifecycle.py` | `4c7c2e604b24` | `e77c7d2d29df` | `6db70490bde7` | 6 | 1 | 7 | exact-byte-identity |
| 38 | `tests/test_installer_omp_source.py` | `f8ff6760732b` | `18b560d48889` | `3ac8b3a080b2` | 8 | 1 | 12 | exact-byte-identity |
| 39 | `tests/test_installer_platforms.py` | `791311144204` | `ac69059c2b31` | `94a7e0501235` | 1 | 4 | 1 | partial-reuse-upstream-base-only |
| 40 | `tests/test_installer_wheel.py` | `a21f3238ccb2` | `cfe1729e4188` | `549e079eb4fc` | 1 | 1 | 1 | exact-byte-identity |
| 41 | `tests/test_installer_windows_tasks.py` | `be0dc5e501f2` | `6bb12bd7bc02` | `ef1b2ca9d7b9` | 1 | 3 | 4 | new-current-conflict |

### Exact hunk headers

1. `astrid/chat/acpProcessHost.test.ts`
   - merge-tree: @@ -124,6 +124,27 @@
   - ours: @@ -341,0 +342 @@ describe('AcpProcessHost', () => {
   - upstream: @@ -126,0 +127,21 @@ describe('AcpProcessHost', () => {
2. `astrid/chat/acpProcessHost.ts`
   - merge-tree: @@ -58,11 +58,15 @@; @@ -70,6 +74,7 @@; @@ -78,6 +83,7 @@; @@ -449,8 +455,12 @@
   - ours: @@ -512,0 +513 @@ export class AcpProcessHost {
   - upstream: @@ -60,0 +61,3 @@ export class AcpProcessHostError extends Error {; @@ -65,0 +69 @@ export class AcpProcessHostError extends Error {; @@ -72,0 +77 @@ export class AcpProcessHostError extends Error {; @@ -80,0 +86 @@ export class AcpProcessHostError extends Error {; @@ -451,0 +458,4 @@ export class AcpProcessHost {; @@ -453 +463 @@ export class AcpProcessHost {
3. `astrid/chat/astrid-acp-bridge.ts`
   - merge-tree: @@ -7,12 +7,14 @@; @@ -105,6 +107,7 @@; @@ -346,7 +349,7 @@; @@ -380,11 +383,13 @@; @@ -429,8 +434,11 @@; @@ -438,7 +446,8 @@; @@ -450,6 +459,19 @@; @@ -705,6 +727,8 @@
   - ours: @@ -1032,0 +1033 @@ export function startAcpBridge(config: AstridAcpBridgeConfig): ReturnType<typeof
   - upstream: @@ -9,0 +10 @@ import { getAstridAgentModelCatalog } from './astrid-agent-models.ts';; @@ -12,0 +14 @@ import { discoverLocalAgents } from './astrid-local-agents.ts';; @@ -15 +17 @@ import { SharedAcpSessions, sharedSessionModels } from './astrid-shared-acp-sess; @@ -107,0 +110 @@ type BridgeOptions = {; @@ -349 +352 @@ function hostError(error: unknown): { status: number; body: JsonRecord } {; @@ -382,0 +386 @@ export class AstridAcpBridge {; @@ -387,0 +392 @@ export class AstridAcpBridge {; @@ -432,2 +437,5 @@ export class AstridAcpBridge {; @@ -441 +449,2 @@ export class AstridAcpBridge {; @@ -452,0 +462,13 @@ export class AstridAcpBridge {; @@ -707,0 +730,2 @@ export class AstridAcpBridge {
4. `astrid/chat/astrid-acp-models.test.ts`
   - merge-tree: @@ -4,7 +4,7 @@; @@ -126,6 +126,11 @@; @@ -214,11 +219,14 @@
   - ours: @@ -299,0 +300 @@ test('catalog levels belong only to the model that advertised them and stale sup
   - upstream: @@ -7 +7 @@ import { bridgeTestClient } from './bridge-test-client.ts';; @@ -128,0 +129,5 @@ test('agents lazily share one bootstrap per ready agent, hide native sessions, a; @@ -217 +222,4 @@ test('Astrid sign-in preserves keyless model access; unknown auth remains ready'; @@ -219 +227 @@ test('Astrid sign-in preserves keyless model access; unknown auth remains ready'; @@ -221 +229 @@ test('Astrid sign-in preserves keyless model access; unknown auth remains ready'
5. `astrid/chat/astrid-agent-models.test.ts`
   - merge-tree: @@ -18,6 +18,7 @@; @@ -26,8 +27,13 @@; @@ -62,6 +68,17 @@; @@ -71,9 +88,15 @@; @@ -144,7 +167,7 @@
   - ours: @@ -288,0 +289 @@ if (args[0] === '--agent-profile-file') {
   - upstream: @@ -20,0 +21 @@ const catalog = {; @@ -28,0 +30 @@ const catalog = {; @@ -30,0 +33,4 @@ const catalog = {; @@ -64,0 +71,11 @@ function readCalls(path: string): unknown[] {; @@ -73,0 +91 @@ test('agent model catalog maps the CLI response to the safe ACP projection and p; @@ -76 +94,6 @@ test('agent model catalog maps the CLI response to the safe ACP projection and p; @@ -147 +170 @@ setInterval(() => {}, 1000);
6. `astrid/chat/astrid-agent-models.ts`
   - merge-tree: @@ -12,6 +12,10 @@; @@ -29,7 +33,8 @@; @@ -51,6 +56,10 @@
   - ours: @@ -74,0 +75 @@ export async function getAstridAgentModelCatalog(options: AstridModelOptions): P
   - upstream: @@ -14,0 +15,4 @@ type AstridModelSnapshot = {; @@ -32 +36,2 @@ async function runAstrid(options: AstridModelOptions, args: string[]): Promise<s; @@ -53,0 +59,4 @@ function modelCatalog(output: string): AcpModelCatalog {
7. `astrid/chat/astrid-local-agent-host.ts`
   - merge-tree: @@ -2,7 +2,7 @@; @@ -101,8 +101,8 @@
   - ours: @@ -121,0 +122 @@ export async function createLocalAgentAcpProcessHost(agent: ExternalAgent, optio
   - upstream: @@ -5 +5 @@ import { ASTRID_ACP_COMMAND, ASTRID_ACP_CONTEXT_SYSTEM_PROMPT, resolveAstridAcpS; @@ -104,2 +104,2 @@ export async function createLocalAgentAcpProcessHost(agent: ExternalAgent, optio
8. `astrid/chat/astrid-local-agents.test.ts`
   - merge-tree: @@ -3,7 +3,7 @@; @@ -43,7 +43,7 @@; @@ -53,6 +53,7 @@; @@ -85,7 +86,7 @@; @@ -106,12 +107,14 @@; @@ -131,7 +134,7 @@; @@ -257,11 +260,13 @@; @@ -297,11 +302,11 @@; @@ -310,6 +315,7 @@; @@ -364,3 +370,62 @@
   - ours: @@ -365,0 +366 @@ test('mixed external-agent authentication states stay associated with their agen
   - upstream: @@ -6 +6 @@ import { join } from 'node:path';; @@ -46 +46 @@ test('reports Not installed when external CLIs are absent and has no adapter fie; @@ -55,0 +56 @@ test('reports Not installed when external CLIs are absent and has no adapter fie; @@ -88 +89 @@ test('Windows discovery finds a user CLI .cmd shim from the registry PATH', asyn; @@ -109 +110 @@ test('Windows Claude npm shims resolve to the JavaScript entrypoint used by auth; @@ -114,0 +116,2 @@ test('Windows Claude npm shims resolve to the JavaScript entrypoint used by auth; @@ -134 +137 @@ test('Windows Codex npm shims run the package entrypoint for auth status and ret; @@ -259,0 +263 @@ test('reads Claude JSON login status and falls back to text only when JSON is in; @@ -264,0 +269 @@ test('reads Claude JSON login status and falls back to text only when JSON is in; @@ -300 +305 @@ if (${JSON.stringify(probe)} === 'claude-text' && args.length === 2) {; @@ -304 +309 @@ if (${JSON.stringify(probe)} === 'claude-text' && args.length === 2) {; @@ -312,0 +318 @@ if (${JSON.stringify(probe)} === 'claude-text' && args.length === 2) {; @@ -365,0 +372,57 @@ test('mixed external-agent authentication states stay associated with their agen
9. `astrid/chat/astrid-local-agents.ts`
   - merge-tree: @@ -3,7 +3,8 @@; @@ -229,13 +230,13 @@; @@ -260,7 +261,7 @@; @@ -285,9 +286,9 @@
   - ours: @@ -297,0 +298 @@ export async function localAgentLaunch(agentId: ExternalAgent, env: NodeJS.Proce
   - upstream: @@ -6 +6,2 @@ import { delimiter, dirname, join, win32 as win32Path } from 'node:path';; @@ -232 +233 @@ async function claudeStatus(command: string | null, env: NodeJS.ProcessEnv, cwd?; @@ -238 +239 @@ function choice(id: LocalAgentId, state: LocalAgentChoice['state'], platform: No; @@ -263 +264 @@ export async function discoverLocalAgents(options: Options = {}): Promise<LocalA; @@ -288 +289 @@ export async function localAgentLaunch(agentId: ExternalAgent, env: NodeJS.Proce; @@ -290 +291 @@ export async function localAgentLaunch(agentId: ExternalAgent, env: NodeJS.Proce
10. `astrid/chat/astrid-project-chat.test.ts`
   - merge-tree: @@ -73,6 +73,27 @@
   - ours: @@ -262,0 +263 @@ test('parallel identical drafts survive project version retries without advancin
   - upstream: @@ -75,0 +76,21 @@ test('New assigns Main when the project has no previous Main chat', async () =>
11. `astrid/chat/astrid-project-chat.ts`
   - merge-tree: @@ -279,46 +279,53 @@
   - ours: @@ -323,0 +324 @@ export class ProjectChatRegistry {
   - upstream: @@ -282,40 +282,47 @@ export class ProjectChatRegistry {
12. `astrid/chat/astrid-shared-acp-sessions.test.ts`
   - merge-tree: @@ -175,6 +175,29 @@
   - ours: @@ -345,0 +346 @@ test('queued validation receives metadata accepted by the previous setter', asyn
   - upstream: @@ -175,0 +176,23 @@ test('writer takeover is atomic around turns, retries dedupe, and detach retains
13. `astrid/chat/astrid-shared-acp-sessions.ts`
   - merge-tree: @@ -326,7 +326,13 @@
   - ours: @@ -427,0 +428 @@ export class SharedAcpSessions {
   - upstream: @@ -329 +329,7 @@ export class SharedAcpSessions {
14. `astrid/chat/discoveryProbe.ts`
   - merge-tree: @@ -2,11 +2,11 @@; @@ -44,6 +44,10 @@
   - ours: @@ -58,0 +59 @@ export function discoveryProbe(command: string, args: string[], options: ExecFil
   - upstream: @@ -5 +5 @@ import { join } from 'node:path';; @@ -9 +9 @@ export function discoveryProbe(command: string, args: string[], options: ExecFil; @@ -46,0 +47,4 @@ export function discoveryProbe(command: string, args: string[], options: ExecFil
15. `astrid/chat/localAgents.ts`
   - merge-tree: @@ -1,4 +1,5 @@; @@ -6,7 +7,8 @@; @@ -15,19 +17,24 @@; @@ -37,7 +44,7 @@; @@ -58,6 +65,28 @@; @@ -80,17 +109,22 @@
   - ours: @@ -114,0 +115 @@ export function isExternalAgentSession(sessionId: string, agent?: typeof EXTERNA
   - upstream: @@ -1,0 +2 @@ import { z } from 'zod';; @@ -9 +10,2 @@ export const EXTERNAL_AGENT_IDS = LOCAL_AGENT_IDS.filter((id): id is Exclude<Loc; @@ -18,5 +20,6 @@ export function formatAstridSignInLine(root: string, platform = process.platform; @@ -24,5 +27,5 @@ function astridSignInLine(): string {; @@ -30 +33,5 @@ function astridSignInLine(): string {; @@ -40 +47 @@ export const LOCAL_AGENT_TABLE: Record<LocalAgentId, {; @@ -60,0 +68,22 @@ export const LOCAL_AGENT_TABLE: Record<LocalAgentId, {; @@ -83 +112 @@ export const localAgentCatalogSchema = z.object({; @@ -88,0 +118,5 @@ export const localAgentCatalogSchema = z.object({; @@ -93 +127 @@ export const localAgentCatalogSchema = z.object({
16. `astrid/chat/modelCatalog.ts`
   - merge-tree: @@ -12,6 +12,8 @@
   - ours: @@ -20,0 +21 @@ export type AcpModelCatalog = z.infer<typeof modelCatalogSchema>;
   - upstream: @@ -14,0 +15,2 @@ export const modelCatalogSchema = z.strictObject({
17. `astrid/chat/service.mjs`
   - merge-tree: @@ -1,4 +1,5 @@; @@ -7,10 +8,21 @@; @@ -81,3 +93,50 @@
   - ours: @@ -2 +2 @@; @@ -4,4 +4,4 @@ import{randomBytes as ed}from"crypto";import{dirname as td,isAbsolute as nd,join; @@ -9 +9 @@ import{randomBytes as ed}from"crypto";import{dirname as td,isAbsolute as nd,join; @@ -14,3 +14,3 @@ import{randomBytes as ed}from"crypto";import{dirname as td,isAbsolute as nd,join; @@ -19 +19 @@ import{randomBytes as ed}from"crypto";import{dirname as td,isAbsolute as nd,join; @@ -22,3 +22,4 @@ import{randomBytes as ed}from"crypto";import{dirname as td,isAbsolute as nd,join; @@ -26 +27,25 @@ import{randomBytes as ed}from"crypto";import{dirname as td,isAbsolute as nd,join; @@ -30,3 +55,3 @@ import{randomBytes as ed}from"crypto";import{dirname as td,isAbsolute as nd,join; @@ -35 +60 @@ import{randomBytes as ed}from"crypto";import{dirname as td,isAbsolute as nd,join; @@ -38 +63 @@ import{randomBytes as ed}from"crypto";import{dirname as td,isAbsolute as nd,join; @@ -40 +65 @@ import{randomBytes as ed}from"crypto";import{dirname as td,isAbsolute as nd,join; @@ -42,7 +67,7 @@ Set the \`cycles\` parameter to \`"ref"\` to resolve cyclical schemas with defs.; @@ -51 +76 @@ ${c}`;if(/Not logged in|Run `?claude auth login/i.test(a))return"signed-out";if(; @@ -54 +79 @@ ${this.context}; @@ -56,3 +81,3 @@ ${this.context}
   - upstream: @@ -2 +2 @@; @@ -4,4 +4,4 @@ import{randomBytes as ed}from"crypto";import{dirname as td,isAbsolute as nd,join; @@ -9 +9 @@ import{randomBytes as ed}from"crypto";import{dirname as td,isAbsolute as nd,join; @@ -14,3 +14,3 @@ import{randomBytes as ed}from"crypto";import{dirname as td,isAbsolute as nd,join; @@ -19 +19 @@ import{randomBytes as ed}from"crypto";import{dirname as td,isAbsolute as nd,join; @@ -22,3 +22,3 @@ import{randomBytes as ed}from"crypto";import{dirname as td,isAbsolute as nd,join; @@ -26 +26 @@ import{randomBytes as ed}from"crypto";import{dirname as td,isAbsolute as nd,join; @@ -30,3 +30,3 @@ import{randomBytes as ed}from"crypto";import{dirname as td,isAbsolute as nd,join; @@ -35 +35 @@ import{randomBytes as ed}from"crypto";import{dirname as td,isAbsolute as nd,join; @@ -38 +38 @@ import{randomBytes as ed}from"crypto";import{dirname as td,isAbsolute as nd,join; @@ -40 +40 @@ import{randomBytes as ed}from"crypto";import{dirname as td,isAbsolute as nd,join; @@ -42,7 +42,7 @@ Set the \`cycles\` parameter to \`"ref"\` to resolve cyclical schemas with defs.; @@ -51 +51 @@ ${c}`;if(/Not logged in|Run `?claude auth login/i.test(a))return"signed-out";if(; @@ -54 +54 @@ ${this.context}; @@ -56,3 +56,3 @@ ${this.context}
18. `astrid/chat/service.test.ts`
   - merge-tree: @@ -51,15 +51,16 @@; @@ -68,6 +69,7 @@
   - ours: @@ -143,0 +144 @@ for (const alreadyEnded of [false, true]) {
   - upstream: @@ -54 +54 @@ for (const bindFails of [false, true]) {; @@ -55,0 +56 @@ test('chat defaults to an ephemeral port and registers the actual loopback liste; @@ -62 +63 @@ test('chat defaults to an ephemeral port and registers the actual loopback liste; @@ -70,0 +72 @@ test('chat defaults to an ephemeral port and registers the actual loopback liste
19. `astrid/chat/service.ts`
   - merge-tree: @@ -1,4 +1,5 @@; @@ -13,6 +14,7 @@
   - ours: @@ -68,0 +69 @@ if (import.meta.main) await runChatService();
   - upstream: @@ -1,0 +2 @@ import { randomBytes } from 'node:crypto';; @@ -15,0 +17 @@ export async function runChatService(env = process.env, createServer = createAst
20. `astrid/core/gateway/dispatch.py`
   - merge-tree: @@ -72,6 +72,11 @@; @@ -551,6 +556,7 @@
   - ours: @@ -189,0 +190,2 @@ def _dispatch_doctor(args: list[str]) -> int:; @@ -192 +193,0 @@ def _dispatch_doctor(args: list[str]) -> int:
   - upstream: @@ -74,0 +75,5 @@ def _dispatch_media(args: list[str]) -> int:; @@ -552,0 +558 @@ _TOP_LEVEL_HANDLERS = {
21. `astrid/core/generation/gpu_environment.py`
   - merge-tree: @@ -18,6 +18,8 @@; @@ -104,7 +106,10 @@
   - ours: @@ -279,0 +280 @@ if __name__ == "__main__":
   - upstream: @@ -20,0 +21,2 @@ from typing import Any; @@ -107 +109,4 @@ def _description(pack: str) -> tuple[Path, dict[str, Any]]:
22. `astrid/installer/backend.py`
   - merge-tree: @@ -30,6 +30,7 @@; @@ -510,6 +511,26 @@; @@ -591,6 +612,7 @@; @@ -599,6 +621,9 @@; @@ -640,8 +665,26 @@
   - ours: @@ -171,0 +172,17 @@ class Backend:; @@ -382,0 +400 @@ class Backend:; @@ -399,6 +416,0 @@ class Backend:; @@ -634,0 +647 @@ class Backend:
   - upstream: @@ -32,0 +33 @@ from .core import (; @@ -500,0 +502,20 @@ class Backend:; @@ -581,0 +603 @@ class Backend:; @@ -589,0 +612,3 @@ class Backend:; @@ -630,0 +656,13 @@ class Backend:; @@ -634,0 +673,2 @@ class Backend:
23. `astrid/installer/core.py`
   - merge-tree: @@ -204,16 +204,16 @@; @@ -271,6 +271,10 @@; @@ -300,8 +304,8 @@
   - ours: @@ -309,0 +310 @@ def new_version_id(manifest: dict) -> str:
   - upstream: @@ -207 +206,0 @@ class Installer:; @@ -208,0 +208 @@ class Installer:; @@ -215 +214,0 @@ class Installer:; @@ -216,0 +216 @@ class Installer:; @@ -273,0 +274,4 @@ class Installer:; @@ -303 +306,0 @@ class Installer:; @@ -304,0 +308 @@ class Installer:
24. `astrid/installer/launcher.py`
   - merge-tree: @@ -2,11 +2,121 @@
   - ours: @@ -63,0 +64 @@ def install(root: Path) -> tuple[Path, ...]:
   - upstream: @@ -4,0 +5,2 @@ from __future__ import annotations; @@ -5,0 +8 @@ import os; @@ -6,0 +10 @@ from pathlib import Path; @@ -9,0 +14,106 @@ from ..core.util import process as _process
25. `astrid/installer/omp/recipe.json`
   - merge-tree: @@ -1,46 +1,46 @@
   - ours: @@ -49,0 +50 @@
   - upstream: @@ -3 +3 @@; @@ -5 +5 @@; @@ -8,3 +8,3 @@; @@ -17,3 +17,3 @@; @@ -25,3 +25,3 @@; @@ -33,3 +33,3 @@; @@ -41,3 +41,3 @@
26. `astrid/installer/service.py`
   - merge-tree: (no textual overlap emitted)
   - ours: @@ -113,2 +113,4 @@ def render(system: str, version: Version, data: Path, log: Path, *, user: str =; @@ -299,0 +302 @@ class Service:
   - upstream: @@ -113,2 +113,4 @@ def render(system: str, version: Version, data: Path, log: Path, *, user: str =
27. `astrid/installer/tools.py`
   - merge-tree: @@ -20,7 +20,7 @@; @@ -317,7 +317,7 @@; @@ -388,7 +388,7 @@
   - ours: @@ -517,0 +518 @@ def install_tools(manifest: dict, root: Path, target: str, run) -> dict[str, str
   - upstream: @@ -23 +23 @@ FILTERS = {"ebur128", "silencedetect", "astats", "signalstats", "blackdetect",; @@ -320 +320 @@ def load_omp_recipe() -> dict:; @@ -391 +391 @@ def _install_omp_source(selected: dict, recipe: dict, root: Path, target: str, r
28. `astrid/packs/rendering/docs/SKILL.md`
   - merge-tree: @@ -535,8 +535,8 @@
   - ours: @@ -176,27 +176,28 @@ lane.; @@ -212,2 +213 @@ Use `timelines log <timeline> --project <project> --verify --json` to verify the; @@ -216,7 +216,16 @@ SDK checkout operations:; @@ -225,9 +234,47 @@ python3 -m astrid timelines publish <timeline> --project <project> -m "<what cha; @@ -287,11 +334,16 @@ Use this loop for every inspection or edit:; @@ -307,4 +359,6 @@ The short agent preamble is:; @@ -345,2 +399,2 @@ unregistered top-level `config.structure` is invalid. These maps are retained; @@ -353,4 +407,4 @@ shared shot metadata.; @@ -359 +413,3 @@ coordinator-issued target as a detached bundle. The target's; @@ -361,24 +417,2 @@ assert shown.ok; @@ -387,6 +421,5 @@ receipt = bound.publish(work, idempotency_key=frozen["candidate_digest"]); @@ -396,2 +429,2 @@ report = []; @@ -407,5 +440 @@ for placement in work["placements"]:; @@ -414,3 +443,3 @@ bound.validate(work); @@ -654 +683 @@ that import/runtime capability as unavailable rather than inventing it.; @@ -657,5 +686,2 @@ Use the same pinned parent composition for direct edits and code-driven batch; @@ -664,5 +690 @@ supported edits, use ordinary Python against the detached same-schema bundle:; @@ -670,3 +692,5 @@ from astrid.sdk.authoring_bundle import (; @@ -674,6 +697,0 @@ candidate = open_authoring_bundle(; @@ -682,21 +700,21 @@ publication = publish_authoring_candidate(candidate, writer, idempotency_key=run; @@ -714,5 +732,5 @@ Do not reconstruct or save a legacy whole-document `config`/`registry` payload; @@ -736,2 +754,6 @@ project-level shot records. They do not rewrite a timeline document or replace; @@ -764,3 +786,4 @@ Inspect its detached plan and diff before deciding whether to apply it. It does; @@ -779 +802,2 @@ reconciliation, never substitution of the latest text.; @@ -786 +810 @@ python3 scripts/timeline_document.py check --file /tmp/edit.json; @@ -788 +812 @@ python3 -m astrid timelines script <timeline> --project <project> --json; @@ -791,0 +816,5 @@ python3 -m astrid timelines script <timeline> --project <project> --revision <pa; @@ -920,4 +949,4 @@ composition without requiring a video render; use `rendering.render` when an
   - upstream: @@ -509,2 +509,2 @@ crop, effects, or appearance in the composition. Use the installed Astrid
29. `astrid/packs/vibecomfy/environment.windows-nvidia.json`
   - merge-tree: @@ -12,8 +12,7 @@
   - ours: @@ -30,0 +31 @@
   - upstream: @@ -15,2 +15 @@
30. `docs/install/OMP-LANDING.md`
   - merge-tree: @@ -1,67 +1,161 @@
   - ours: @@ -66,0 +67 @@ The live installer qualification also used this exact producer commit locally. I
   - upstream: @@ -3,3 +3,18 @@; @@ -9 +24 @@ The fixed commit is `9e282751c0059e37d2f6fbc14ffa0b450710bd23`, based on `9962a4; @@ -12,3 +27,5 @@ Use a clean clone of `peteromallet/oh-my-pi` that contains base commit `9962a46d; @@ -17 +34,3 @@ git show -s --format='%H%n%T' 9e282751c0059e37d2f6fbc14ffa0b450710bd23; @@ -20 +39 @@ The first command must show `9e282751c0059e37d2f6fbc14ffa0b450710bd23 refs/heads; @@ -23 +42,3 @@ git push origin 9e282751c0059e37d2f6fbc14ffa0b450710bd23:refs/heads/astrid-acp-s; @@ -27 +48,3 @@ Verify the commit is available from GitHub before changing or deploying the app.; @@ -30,4 +53,8 @@ Verify the commit is available from GitHub before changing or deploying the app.; @@ -38 +65,11 @@ Verify the commit is available from GitHub before changing or deploying the app.; @@ -42 +79,5 @@ Keep the app deployment gate closed until GitHub serves that commit and the app; @@ -45 +86 @@ Use Bun **1.3.14**. The reviewed fork uses the unchanged frozen Bun lock with SH; @@ -50 +91,3 @@ sha256sum bun.lock; @@ -54,2 +97,2 @@ native_scratch="$(mktemp -d)"; @@ -60 +103,2 @@ rm -rf "$native_scratch"; @@ -64 +108,11 @@ sha256sum bun.lock; @@ -66 +120,37 @@ The latest run passed **67 tests, 0 failed, 316 assertions across two files in 1
31. `docs/reference/services.md`
   - merge-tree: @@ -25,8 +25,10 @@
   - ours: @@ -71,0 +72 @@ The app launcher no longer owns a chat process or its credential.
   - upstream: @@ -28,2 +28,4 @@ manifest field. It names either an exact npm package and version or a fork
32. `docs/testing/TESTING.md`
   - merge-tree: @@ -396,7 +396,7 @@; @@ -585,15 +585,18 @@
   - ours: @@ -649,0 +650 @@ These are known. Report what you see, but don't stop testing for them.
   - upstream: @@ -399 +399 @@ Record its title and a sentence you can find again.; @@ -588,9 +588,12 @@ These are known. Report what you see, but don't stop testing for them.
33. `scripts/refresh_omp_recipe.py`
   - merge-tree: @@ -1,38 +1,24 @@; @@ -45,6 +31,8 @@; @@ -56,40 +44,19 @@; @@ -109,10 +76,8 @@
   - ours: @@ -119,0 +120 @@ if __name__ == "__main__":
   - upstream: @@ -2 +2 @@; @@ -5 +5 @@ python scripts/refresh_omp_recipe.py --producer-repo /path/to/oh-my-pi \; @@ -7,2 +7,2 @@ python scripts/refresh_omp_recipe.py --producer-repo /path/to/oh-my-pi \; @@ -15 +14,0 @@ import base64; @@ -19 +17,0 @@ import subprocess; @@ -21 +18,0 @@ import tarfile; @@ -25,11 +21,0 @@ from pathlib import Path; @@ -47,0 +34,2 @@ def main() -> None:; @@ -59,26 +47,5 @@ def main() -> None:; @@ -87 +54 @@ def main() -> None:; @@ -90 +57 @@ def main() -> None:; @@ -92 +59 @@ def main() -> None:; @@ -112 +78,0 @@ def main() -> None:; @@ -114,2 +80 @@ def main() -> None:
34. `tests/core/generation/test_gpu_environment.py`
   - merge-tree: @@ -52,11 +52,9 @@
   - ours: @@ -289,0 +290 @@ def test_solver_version_must_match_before_environment_creation(tmp_path, monkeyp
   - upstream: @@ -55 +54,0 @@ def test_environment_source_pins_match_existing_admission():; @@ -59 +57,0 @@ def test_environment_source_pins_match_existing_admission():
35. `tests/test_installer_acl.py`
   - merge-tree: @@ -128,8 +128,9 @@
   - ours: @@ -217,0 +218 @@ def test_unix_installer_retains_original_per_user_lock(tmp_path, monkeypatch, sy
   - upstream: @@ -131 +131 @@ def test_windows_uninstall_deletes_default_workspace_while_lock_is_held(tmp_path; @@ -132,0 +133 @@ def test_windows_uninstall_deletes_default_workspace_while_lock_is_held(tmp_path
36. `tests/test_installer_cleanup.py`
   - merge-tree: @@ -25,6 +25,7 @@
   - ours: @@ -307,0 +308 @@ def test_windows_program_cleanup_includes_retained_ownership_marker(tmp_path, mo
   - upstream: @@ -27,0 +28 @@ def installation(tmp_path, monkeypatch, system=None):
37. `tests/test_installer_lifecycle.py`
   - merge-tree: @@ -39,6 +39,7 @@; @@ -65,6 +66,16 @@; @@ -78,6 +89,11 @@; @@ -98,10 +114,6 @@; @@ -116,13 +128,81 @@; @@ -164,7 +244,7 @@
   - ours: @@ -565,0 +566 @@ def test_cli_rejects_removed_repair_flag():
   - upstream: @@ -41,0 +42 @@ class LifecycleBackend:; @@ -67,0 +69,10 @@ class LifecycleBackend:; @@ -80,0 +92,5 @@ class LifecycleBackend:; @@ -101,4 +116,0 @@ class LifecycleBackend:; @@ -119 +131 @@ def test_reinstall_attaches_kept_realm_without_creating_another(tmp_path):; @@ -125,0 +138,68 @@ def test_reinstall_attaches_kept_realm_without_creating_another(tmp_path):; @@ -167 +247 @@ def test_reinstall_ignores_current_pointer_to_removed_interpreter(tmp_path):
38. `tests/test_installer_omp_source.py`
   - merge-tree: @@ -38,11 +38,11 @@; @@ -90,13 +90,13 @@; @@ -104,9 +104,9 @@; @@ -185,7 +185,7 @@; @@ -199,7 +199,7 @@; @@ -252,12 +252,12 @@; @@ -268,7 +268,7 @@; @@ -384,3 +384,60 @@
   - ours: @@ -385,0 +386 @@ def test_hostile_bun_settings_and_registration_paths_are_build_only(tmp_path, mo
   - upstream: @@ -41 +41 @@ def fixture(tmp_path, monkeypatch):; @@ -45 +45 @@ def fixture(tmp_path, monkeypatch):; @@ -93 +93 @@ def test_selected_fork_freezes_graph_generates_only_views_and_does_not_patch(tmp; @@ -99 +99 @@ def test_selected_fork_freezes_graph_generates_only_views_and_does_not_patch(tmp; @@ -107 +107 @@ def test_selected_fork_freezes_graph_generates_only_views_and_does_not_patch(tmp; @@ -109 +109 @@ def test_selected_fork_freezes_graph_generates_only_views_and_does_not_patch(tmp; @@ -188 +188 @@ def test_bundled_recipe_pins_build_closure_without_selecting_or_patching_source(; @@ -202 +202 @@ def test_local_fork_uses_selected_commit_and_records_actual_tree(tmp_path, monke; @@ -255 +255 @@ def test_default_and_comment_select_published_exact_release():; @@ -259,2 +259,2 @@ def test_default_and_comment_select_published_exact_release():; @@ -271 +271 @@ def test_invalid_or_unpinned_source_is_refused(value):; @@ -385,0 +386,55 @@ def test_hostile_bun_settings_and_registration_paths_are_build_only(tmp_path, mo
39. `tests/test_installer_platforms.py`
   - merge-tree: @@ -137,7 +137,11 @@
   - ours: @@ -136,0 +137,3 @@ def test_windows_task_settings_and_no_console_executable():; @@ -303,0 +307,10 @@ def test_stage_profile_points_to_candidate_service_declaration(tmp_path, monkeyp; @@ -305 +317,0 @@ def test_stage_profile_points_to_candidate_service_declaration(tmp_path, monkeyp; @@ -596,0 +609 @@ def test_chat_declaration_failure_can_retry_without_claiming_fresh_workspace(tmp
   - upstream: @@ -137 +137,4 @@ def test_windows_task_settings_and_no_console_executable():
40. `tests/test_installer_wheel.py`
   - merge-tree: @@ -65,7 +65,7 @@
   - ours: @@ -72,0 +73 @@ print(json.dumps({'module':astrid.services.__file__,'declaration':declaration,
   - upstream: @@ -68 +68 @@ print(json.dumps({'module':astrid.services.__file__,'declaration':declaration,
41. `tests/test_installer_windows_tasks.py`
   - merge-tree: @@ -1,4 +1,4 @@
   - ours: @@ -4,0 +5 @@ import subprocess; @@ -7,0 +9,2 @@ import pytest; @@ -56,0 +60,37 @@ def test_task_cleanup_preserves_powershell_success_and_failure(tmp_path, operati
   - upstream: @@ -1 +1 @@; @@ -4,0 +5 @@ import subprocess; @@ -7,0 +9,2 @@ import pytest; @@ -56,0 +60,37 @@ def test_task_cleanup_preserves_powershell_success_and_failure(tmp_path, operati

## Source-fact seam recommendation

- Automatically composable: `astrid/installer/service.py` (current ours body is byte-identical to upstream; only an extra EOF blank line remains), `tests/test_installer_windows_tasks.py` (new current conflict shares the full added test body; only the module docstring differs), and `astrid/packs/rendering/docs/SKILL.md` (historical B classification marked the interpreter wording textual/context-only).
- Genuine intent seams: the remaining 38 current paths. Their old exact classifications remain reusable for the 38 byte-identical paths; `tests/test_installer_platforms.py` is the material re-audit because current ours adds fixture-source materialization while upstream adds the same XML assertions. Preserve both predicates/fixtures and let the Agent owner choose the semantic join.
- No hunk was resolved or applied. These recommendations are source facts for later private join workers, not merge authorization.

## Already-upstream and whitespace map

- `git cherry -v 886a3183bd4a4a44f0a2c08fabec4e8edcbf7b55 a30e74e901a28b39c28facba3deb00d76f186e23`: 0 already-upstream (`-`) and 725 not-already-upstream (`+`) patch identities; no normalized patch-equivalent local commits were found.
- `git diff --check 92443771676ef2bbb547d0a103d708fa8bec4c63 a30e74e901a28b39c28facba3deb00d76f186e23`: exit 2, 162 findings across 162 paths, all committed current-home whitespace findings.
- `git diff --check 92443771676ef2bbb547d0a103d708fa8bec4c63 886a3183bd4a4a44f0a2c08fabec4e8edcbf7b55`: exit 0, 0 findings.
- No whitespace or source bytes were changed by this task.
