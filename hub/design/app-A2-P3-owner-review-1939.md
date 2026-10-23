# A2/P3 owner-cause independent review

## Verdict

- **PASS — exact source facts.** The reviewed cause report accurately identifies the production readiness boundary and preserves its lifecycle caveats.
- **PASS — conditional source counterexample.** The `assetResolver` dependency schedule is a source-level conditional counterexample only; it does not attribute the actual 15659 failure.
- **UNKNOWN — actual 15659 cause.** No existing safe Farm projection was published at this review cutoff, so the report correctly does not choose basis-read, identity, session, IndexedDB/outbox, cancellation, Agent, or Runtime as the actual cause.
- **UNKNOWN — missing evidence.** The missing owner input is the already-requested safe, stage-only projection of the retained 15659 trace, with case/time/source-member provenance and the mounted basis/identity/session/owner fields. No new run or probe is authorized.

## Review basis

The App worktree is unchanged at `2107e1870e51c650d59315f4cc1ab6af338f198c` with tree `a3ff3584e9b559bbb3c3a82b77be7516ed8e761c`. The submitted report's cited source hashes match this tree:

- `useTimelineSave.ts` `0f888f7c843ce7f8179c70b34b373a030c00d22a`
- `timelineLocalSaveHandoff.ts` `1c6176d2abc3d06f5b27b7c391a2c22c292ea4d1`
- `localSaveSession.ts` `83d2166d57c05980d3bd8ebc9bbd79a37c3c5e44`
- `commitOutbox.ts` `8f6c157b910b12b900b61d45354442e3474c2975`
- `runtime/client.ts` `6e9a894d09959ed9fa8f1c0c6f01b9423441c59b`
- `runtime/dataProvider.ts` `fea25c9f28fa617eb3cf252a0a86818ef1218be2`

The source audit was read-only and checked PLAN §3 A2/P3, contract §§1–5, `handoff-ap2-P3-15659-owner-boundary-review-1918.md`, and `design/app-A2-P3-owner-cause-sol-1934.md`.

## Exact source findings

The production caller binds local saves through `useTimelineSave.ts:145–235`: it reads the verified original basis (`:156–179`), awaits recoverable identity (`:181–184`), then constructs `createLocalSaveSession` with the scoped project/timeline and identity (`:186–191`). Cancellation, closed-owner, edit-sequence, and generation checks can reject or retire that path (`:163–184`, `:214–241`). A changed `assetResolver` changes `resolveAssetUrl` and therefore the effect dependency (`:43–49`, `:242`), while `localOwner` remains memo-stable for unchanged provider/timeline (`:78–82`).

The report's conditional schedule is therefore valid and bounded: if the original verified read remains pending and that dependency changes, the old effect cleanup sets `cancelled`; the replacement sees the same head and returns at `:133–135`; the old continuation rejects at `:178–180`, before identity and session creation. This proves only the conditional schedule. The audited source does not prove that 15659 had that dependency transition, pending read, or cancellation state.

The handoff enforces the stable authoring boundary and source identity (`timelineLocalSaveHandoff.ts:59–112`, `:205–235`), while `localSaveSession.ts:208–245` performs scoped claim/recovery and durable-owner readiness. `commitOutbox.ts:205–248` exposes the IndexedDB open/list boundary; `:252–303` increments and persists the owner generation before invoking the hold callback; `localSaveSession.ts:213–239` reads the claimed record before resolving its mounted promise. These facts do not identify which stage failed in 15659.

The report also correctly retains the contract's request/reply, idempotency, dependency, and guarded-replay obligations (contract §§1–5, especially `commit-v2.md:60–80`, `:254–274`, `:595–661`, `:703–744`, `:1563–1618`) without using them as evidence of an unobserved mounted state.

## Actual-run boundary and missing input

Proof1918 says the real run failed at `openCommandTimeline`, before the first gesture and Gate5 body (`handoff-ap2-P3-15659-owner-boundary-review-1918.md:3–15`). It records the selected App/Agent/Runtime and the 90-second owner-readiness failure, but not the mounted basis read, identity presence, cancellation/generation, IndexedDB transaction, owner record, or safe error stage. `ready:false`, event/head aggregates, and absence of a newly listed owner cannot distinguish those cases.

At the cutoff there was no published flat safe projection of the retained trace. The next owner input is only the existing trace's sanitized stage projection: actual case and time, artifact/member provenance, mounted project/timeline/basis pair, identity/realm presence booleans, lifecycle and generation state, storage/lock/session outcomes, scoped owner creation/put/settled state, recoverable counts, and sanitized error code/class/stage. Do not provide raw trace archives, credentials, principals, tokens, cookies, request bodies, or full trace copies.

The original Gate5 file remains `37caf28577d42fbe98afd2320dffa3c72e6e74b1` in both `HEAD:` and the worktree. The two P1 segment hashes remain `4b04ad7ef74b8106244d87c23d12c7a18da251dd8f5a746f42d3221a72ea8b7f` and `2f7501184477c8aec38d3cd289dd13c0d011fa8f69ecd43378f24f6c3100a2f7`. No source, test, collector, configuration, dependency, environment, or Git mutation was made.

## Verification disposition

Read-only commands only: source/diff/hash audit and preservation checks. Targeted tests, typecheck, lint, browser/HTTP/service runs, and fresh experiments are **N/A** for this unchanged-code review; no fresh PASS is claimed. No plan decision was shown wrong. The report should remain UNKNOWN pending the existing safe Farm projection or an explicit owner statement that the needed trace fields were not captured/lost.
