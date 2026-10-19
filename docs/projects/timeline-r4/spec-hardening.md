# spec-hardening.md: data safety and safe exposure (MIG-0, COMPAT-1, MIG-GOLDEN, routes, SEC gate)

**Workstream:** HARDEN · **Brief:** [briefs/WS-HARDEN.md](briefs/WS-HARDEN.md) · **Evidence:** [reviews/astra-high-migration.md](reviews/astra-high-migration.md), [reviews/astra-high-security.md](reviews/astra-high-security.md), [reviews/astra-xhigh-app-deep-dive.md](reviews/astra-xhigh-app-deep-dive.md) §2.6 · **Rulings:** DECISIONS-deep-dives-1 (Security, Migration), DECISIONS-app-deep-dive #11

## 1. Compatibility rules (every task)
- **Wire formats are additive.** `TimelineConfig` 0.0.3 ⊇ 0.0.2; `TimelinePatch` `scope` is optional; intent is dual-read (A1).
- **Published revisions are never rewritten.** Migrations run in drafts on checkout; they are lossless, idempotent, journaled `migrate`, and never an undo step.
- **The live film** changes only by a user-approved publish, after its duplicate passes MIG-GOLDEN.

## 2. MIG-0: A1's lossless bug
- **The bugs:**
  - `_strip_derived()` strips underscore keys at any depth (`sdk/timeline/doc.py:160`, used by save and publish), so the `app.astrid._legacy` collision values (`core/timeline/astrid_ns.py:91-94`) vanish;
  - `migrate_bundle()` skips parent clips (`:175`);
  - non-dict values are replaced (`:102,121,158`).
- **The fix:** strip only the owned derived paths (`_index`, `_timeline`); preserve malformed and colliding values; walk the parent clips.
- **The proof:** load → save → publish → reopen → merge → undo with collisions, parent clips and opaque underscore keys. Migrating twice gives no change.

## 3. COMPAT-1: semantic keys behind declared capabilities

> **14 Oct:** one integer `app.astrid.v` versions Astrid semantics and replaces the per-feature `requires {intent, edit[], render[]}` arrays, because every writer goes through the commit path (H-DATA). Extensions use their own admitted `app.<stable-owner-id>.v`; neither version substitutes for the other.
- **The problem:** `music`, `link` and `pinned` change meaning (an old retime moves a pinned member, ignores links, and defaults to keep-end), and nothing checks a version.
- **Historical declaration (superseded):** `parent.config.app.astrid.requires = {"intent": N, "edit": [features], "render": [features]}`. Do not reintroduce these per-feature arrays.
- **Current declarations:** `app.astrid.v` protects Astrid semantic keys; each admitted extension declares and owns its distinct versioned `app.<stable-owner-id>.v` namespace. A missing or unsupported owner version refuses that owner's write; it never implies support. Runtime remains generic storage/acceptance and does not interpret the namespace.
- **The rollout order:** readers ship first, then writers; a writer and reader understand the declared owner version before emitting or consuming that namespace. Rollback is restoring a revision.

## 4. MIG-GOLDEN: the v8 identity gate

> **14 Oct:** compiled-document bytes (+ cut rows and intent reads) gate the compiler; decoded frames and audio samples are compared once, for R-EVAL.
1. **Freeze the source identity:** every revision digest, the media digests, the narration pins, fps, the frame counts. The exact baseline is set by SPEC-0: the release figure 2:30.2 and the audit CSV's 150.133 s disagree.
2. **Raw, semantic and evaluator comparisons:** keep `app.astrid_render_clock`; never strip all of `app`.
3. **The 45 cut rows, exact.**
4. **Every decoded frame and audio sample** (after proving that repeated renders are deterministic). Cut-start frames are diagnostics only.
5. **Intent reads,** every key; other namespaces byte-for-byte.

**When it runs:** it gates any migration, RS-1, and the live-film publish.

## 5. Routes and transport (H-ROUTES = LOCAL-1 + SEC-5)
- **The route and header allowlists are generated from their consumers:** the App's generated client, the commit routes, project chat, inspect, history/restore, `X-Astrid-Session`. Explicit denials for everything else.
  - Today the paired relay omits the editing routes and strips `X-Astrid-Session` (`APP/config/vite/pairedRoutePolicy.ts:25,79,93-108`).
- **The commit service is mounted** in Astrid's local host on both transports, with the scoped product credential.
- **One versioned credential format and parser;** the granted scopes are returned; expiry is enforced.
- **Explicit size handling:** the relay's limit is 128 KiB, the loopback's 1 MiB. Measure v8's save payloads, then raise the cap, chunk, or upload as an object.
- **One primary transport for astrid.haus** (the user's decision, Q-T). The other is tested separately.

## 6. The SEC gate (built in Release 1; no real data on astrid.haus before it passes)
| Task | Minimal fix | Canaries that must fail |
|---|---|---|
| **H-GRANT** (SEC-1) | A local grant {realm, browser session, projects, operations, expiry}; structured capability decisions (no title-based approval); the agent and its descendants confined (filesystem/network) with a sanitized env; caller MCP config can't widen the grant | reading outside files or credentials, writing outside, unapproved egress, a deceptive tool title, an MCP expansion, a forged actor or session, a cross-project claim |
| **H-TRANSPORT** (SEC-2 + SEC-4) | Authenticated internal helper calls with exact endpoint identity; loopback-bind assertions; WSS enforced; frames bound to (connector, generation, request); bounded concurrency; active content (HTML/SVG) on a sandboxed origin | unauthenticated or hostile-Origin calls through any helper port; a second LAN machine; cross-connector response injection; an HTML/SVG canary |
| **H-REVOKE** (SEC-3) | Separate "disconnect", "revoke the grant" and "stop delegated work"; new actions and commits fenced; reconnect authority invalidated without relying on the close-reason string; running renders follow Q-S4 | a revoke during an upload, a prompt or a render; a reconnect or restart reviving the grant |

**The E-4 verification matrix** (before the film test, on the chosen transport): deployment identity, credential boundary, project boundary, hostile browser traffic, content isolation, agent boundary, session lifecycle, attribution, transport correctness, product acceptance. **Run the adversarial checks on a disposable fixture first.**

## Astra098: additive operation compatibility and declared data access

The target combined contract retains exact `schema_digest` for source/evidence identity and generates `operation_versions` finite sets for runtime compatibility (for example, `listEvents: [1, 2]`); this is not a claim that current source already emits the metadata. A client profile names each operation and the exact semantic version used by the feature being run. A legacy scalar descriptor is a singleton set. A required version passes only when that exact value is advertised; a higher number alone never establishes compatibility. Version covers request, response, errors, and behavior. Advertise both old and new versions only when the old contract remains supported and tested. A breaking implementation advertises only its new version. This wire-operation metadata is distinct from `app.astrid.v` timeline semantics and extension owner-namespace versions.

Profiles are feature-scoped. Check baseline connection/edit-safety requirements before realm load or mutation. Check optional rename and `from=latest` semantics only when used; their absence disables or refuses that feature while unrelated baseline App flows remain available. Do not turn an optional feature miss into a whole-App lockout. A legacy Runtime without metadata uses only a verified mapping for an exact contract digest; otherwise refuse the unsupported feature, and deny a baseline flow before load or mutation when its safety requirements are not met. Health and handshake must agree on exact Runtime identity and digest. Generated inventory is compatibility metadata, not authorization: inventory membership alone does not make an operation callable or writable, and generated wrapper admission plus the authenticated route/owner/grant checks still apply. Preserve bearer authentication, endpoint/origin, project/actor grants, runtime identity/restart, write scope, explicit denials, and request/response checks. Do not add a general schema-subtyping engine.

The pack-v3 manifest declares exact document kinds and schema versions plus the owner namespace/schema version, implementation identity/digest, and existing effects/resources. Runtime and project/actor grants and subject scope remain the authority. `documents.write` refuses timeline/edit-timeline kinds; timeline changes use declared owner data and existing EditCommands. Foreign/malformed/unknown namespaces and explicit clears remain losslessly preserved. No general schema-subtyping engine, per-feature `requires` arrays, Runtime semantic interpreter, or route/service is added. Details and focused negative cases are in [the Astra098 amendment](amendments/20261016-upstream-transcript-extension-integration.md).

For transcript data, preserve the existing hash-bound `config.app.transcript` managed-input declaration and use its `.references` member for media associations/defaults. Store each immutable occurrence reference at `clip.app.transcript.binding`; the default association index cannot retarget a bound clip. Only the validated semantic import command writes provenance/snapshot fields or derived timing inputs. Generic owner-property writes cannot forge them. Compare legacy top-level `transcriptReferences` only with canonical `.references` during explicit migration; conflicts preserve both originals and refuse. The existing declaration may coexist with `.references`. Caption Foundry uses the admitted transcript host's validated binding operation or owns only separately declared data.
