# App M2 producer startup health identity diagnosis — 0659

## Result

The startup4382 failure is an assertion/envelope mismatch in the probe, not a
wrong daemon, wrong realm, or failed startup. The pinned Runtime health
contract intentionally does not carry `realm_id`. Realm identity is carried by
the existing `/v1/realm` resource (and by the authenticated handshake), so the
probe's top-level `healthBody.realm_id` assertion was bound to the wrong result.

No Runtime, schema, product, daemon, or shared artifact was changed. No
central rerun, module/startup smoke, browser, build, install, producer body,
producer case, or full suite was run.

## Evidence and exact pins

The retained startup result is:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-producer-realm-physical-path-diagnosis-0538-ap2-m2-producer-startup-shell-contract-repair-0647-startup-1021065559-4382/
```

The retained log/summary records HTTP direct-health success followed by:

```text
AssertionError [ERR_ASSERTION]: Runtime health realm identity
+ actual - expected
+ undefined
- 'cd19567850a74a098273544f0fa87061'
```

The retained result has no raw response-body file; the assertion bytes above
are the complete retained response evidence. The body shape is independently
settled by the exact pinned source below, without making a new request.

Runtime exact commit/tree: `2c4ac180c2220bdad966bc01e95ad230e99ce26a` /
`7ab412cc4bcbe517efcfa806e092336390312e18`.

App/DirectHarness exact commit/tree:
`b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7` /
`fd16d32fd3487e56c9fe1ff16582dba240f63b77`.

Relevant exact source lines:

- `contract/schemas/health.json:5-13` permits only `status`, `protocol`,
  `schema_digest`, `runtime_epoch`, `runtime_session_id`, and
  `runtime_instance_id`; `realm_id` is not a health property and
  `additionalProperties` is false. Blob:
  `9af1e8122feb4ee91d5c3381be3e54ff0f779342`.
- `runtime_protocol/service.py:744-756` implements health as the cheap
  liveness query and returns no `realm_id`.
- `runtime_protocol/server.py:405-410` serves that health result and adds only
  `runtime_instance_id` from the daemon.
- `runtime_protocol/service.py:771-774` is the authoritative realm carrier:
  `realm_resource()` returns `realm_id`, `display_name`, `version: 1`, and
  lifecycle fields.
- `tests/e2e/local/support/harness.ts:394-395` stores the existing
  `runtimeInstanceId` and `realmId`; `:541-552` provides authenticated direct
  Runtime requests through `runtimeJson`; `:1122-1125` provides hosted-origin
  door requests through `doorRequest`.
- `src/integrations/runtime/RuntimeConnectionProvider.tsx:74-115` already
  defines the normal binding sequence as health, then `/v1/realm`, and binds
  `realm_id` from the latter. This is the existing normal identity read; no
  route was invented.

The generated TypeScript `Health` interfaces at both the pinned Runtime
(`packages/typescript/src/generated.ts:9`, blob
`2f614b1ca4bf950ec9ee1e543a566e2440869866`) and pinned App
(`src/integrations/runtime/generated.ts:9`, same blob) omit
`runtime_instance_id` even though the exact JSON schema requires it and the
server adds it. Existing App identity code reads that runtime field through a
deliberate structural cast. This is a separate generated-type drift; it does
not justify putting `realm_id` into health and is outside this task's scope.

## Owned correction

The immutable probe was copied byte-for-byte before editing:

```text
immutable:
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-startup-shell-contract-repair-0647/artifacts/producer-startup-only-probe.mts
sha256 4beb7c22dfa06e04d28253dbab02f76ff2a9953f0accd4b12247514e4f0608f6

owned:
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-health-identity-source-cause-0659/artifacts/producer-startup-only-probe-owned.mts
sha256 a062cab11ea3a86ef75ece5a86584d0555040336032ced515d6ac50de9481d8f
```

Bounded diff only:

```diff
     const runtimeHealth = await fetch(`${harness.runtimeUrl}/v1/health`);
     assert.equal(runtimeHealth.status, 200, 'Runtime direct health');
-    const healthBody = await runtimeHealth.json() as { realm_id?: string; runtime_instance_id?: string };
-    assert.equal(healthBody.realm_id, harness.realmId, 'Runtime health realm identity');
    const healthBody = await runtimeHealth.json() as { runtime_instance_id?: string };
     assert.ok(healthBody.runtime_instance_id, 'Runtime health instance identity');
+
+    const runtimeRealm = await harness.runtimeJson<{ realm_id?: string; version?: number }>('GET', '/v1/realm');
+    assert.equal(runtimeRealm.status, 200, 'Runtime direct realm');
+    assert.equal(runtimeRealm.body.realm_id, harness.realmId, 'Runtime direct realm identity');
+    assert.equal(runtimeRealm.body.version, 1, 'Runtime direct realm version');

     const doorHealth = await harness.doorRequest('/v1/health');
     assert.equal(doorHealth.status, 200, 'Runtime door health');
+    const doorHealthBody = doorHealth.json() as { runtime_instance_id?: string };
+    assert.equal(doorHealthBody.runtime_instance_id, harness.runtimeInstanceId, 'Runtime door health instance identity');
+    const doorRealm = await harness.doorRequest('/v1/realm');
+    assert.equal(doorRealm.status, 200, 'Runtime door realm');
+    const doorRealmBody = doorRealm.json() as { realm_id?: string; version?: number };
+    assert.equal(doorRealmBody.realm_id, harness.realmId, 'Runtime door realm identity');
+    assert.equal(doorRealmBody.version, 1, 'Runtime door realm version');
```

The correction keeps the strict direct health HTTP status and instance
identity checks, adds the authoritative direct realm status/identity/version,
keeps the door health status, adds door instance identity, and adds the
authoritative door realm status/identity/version. The original physical-chain,
negative symlink, source, module-format, version, pin, and custody guards are
untouched in the owned probe/gate record. The immutable 0647 artifact itself
was not modified.

## Remaining prerequisites before another smoke

Both transport sides must satisfy this complete assertion set:

1. Direct `GET <runtime>/v1/health`: HTTP 200; schema/protocol/epoch/session
   fields valid; `runtime_instance_id` present and non-empty.
2. Direct authenticated `GET <runtime>/v1/realm`: HTTP 200; `realm_id` equals
   `harness.realmId`; `version === 1`.
3. Door `GET /api/runtime/v1/health` with the hosted origin: HTTP 200;
   `runtime_instance_id` equals `harness.runtimeInstanceId`; no credential or
   session path is leaked in the body, as retained door checks require.
4. Door `GET /api/runtime/v1/realm` with the hosted origin: HTTP 200;
   `realm_id` equals `harness.realmId`; `version === 1`; the existing origin,
   credential, source, and version guards remain active.
5. The module/source preflight, planted Runtime symlink refusal, physical
   custody/keeper postflight, and all exact Runtime/Agent/Composition pins
   remain unchanged and must be independently reviewed against the new owned
   probe before execution.

The next smoke must use a newly reviewed custody wrapper that points to the
owned probe above. Literal central-suite recipe, intentionally not executed
here:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-producer-realm-physical-path-diagnosis-0538 ap2-m2-producer-health-identity-source-cause-0659-startup --no-cache)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Do not register or run that recipe until the new wrapper's hash, physical
source/keeper graph, literal probe argv, and early teardown have received the
same independent custody review as 0647. No producer body/case should be
added to this startup qualification.

## Checks run

- `sha256sum` of immutable and owned probes: PASS; hashes above.
- `diff -u --label immutable-0647-probe --label owned-0659-probe ...`: PASS
  as a bounded, expected 11-line change; no other bytes differ.
- `git -C /home/user/work/wt/ap2-m2-producer-health-identity-source-cause-0659 diff --check`: PASS.
- App worktree `git status --short`: clean; no App source files changed.
- No test suite or central service rerun was requested, per task scope.

## Decision / handoff

Decision: the fixture/probe was wrong. Keep Runtime health and schema
unchanged; carry realm identity through the existing `/v1/realm` result on
both direct and door paths. The owned probe is ready for independent custody
review and a later fresh suite registration. No blocker remains for this
diagnosis; the next action belongs to the orchestrator/central test service.
