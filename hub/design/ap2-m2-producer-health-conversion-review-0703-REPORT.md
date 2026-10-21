# App M2 producer health/realm conversion review — 0703

## Verdict

**APPROVE.** The retained failure was a fixture assertion mismatch, not a Runtime or product defect. `/v1/health` remains the pinned liveness resource and excludes `realm_id`; the existing `/v1/realm` resource is the authoritative realm carrier. The corrected existing startup smoke passed once centrally.

Exact target: `ap2-m2-producer-realm-physical-path-diagnosis-0538`.

## Owned artifacts and custody

Original 0647 artifacts were not modified. Immutable hashes remain:

```text
producer-physical-keeper-gate.sh         c365641bdeca10b9d740d5968c9a1161db7b18f8bf49e9d8bd46f14aae60cfab
producer-startup-custody-gate.sh         4af8fa42b218645be2aaa1f24caace9b83533722bc1842178cbfef55c7ab349f
producer-startup-only-gate.sh            46cf870be41d5db7f109b05f11b0c1fcd2c38f5975dbeb0db1bee78907a51d62
producer-startup-only-probe.mts          4beb7c22dfa06e04d28253dbab02f76ff2a9953f0accd4b12247514e4f0608f6
producer-startup-module-format-probe.mts d4eeaeb74a582fe9ccb94c1cfba7f66c41ec50eef7823db34f61ed7185e12af3
```

Owned artifact hashes:

```text
producer-startup-only-probe-owned.mts    a062cab11ea3a86ef75ece5a86584d0555040336032ced515d6ac50de9481d8f
producer-startup-only-gate-owned.sh      4963a1eb47f84c58ed51f271a581604339eda61547a817019e0e273eee668e41
producer-startup-custody-gate-owned.sh   ffeaa34c944b931a0e2f393156dd3dc78cb39318bf24c64bb4073e2b6b3d5a20
producer-health-realm-offline-review.mjs a681e0a4ff618a103195c4cd6704556f9f3d13f841cf687b99b6f810faee2561
```

The owned startup gate changes only the probe path. The owned custody gate changes only the owned probe/startup paths and their transitive hashes; all other pins and guards are copied unchanged. The unique preflight/startup entries were registered in `scratchpad/orch/tests/suites.conf`.

App source remained unchanged at commit/tree `b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7` / `fd16d32fd3487e56c9fe1ff16582dba240f63b77`.

## Assertion and source review

The owned offline review passed 22 checks. It verified:

- exact pinned Runtime schema/source: health has no `realm_id`; server adds `runtime_instance_id`; `realm_resource()` carries `realm_id` and `version: 1`;
- direct health status/instance, direct realm status/realm/version;
- door health status/instance and door realm status/realm/version;
- existing bearer credential, hosted origin, `doorRequest` path, and synchronous `RawResponse.json()` behavior;
- normal App probe order: health, then `/v1/realm`;
- matching identity/version acceptance and wrong instance, realm, and version refusal probes;
- all retained physical-root, optional audit-leaf, planted realm symlink, teardown, and no-producer-body guards.

The health schema and Runtime source were read from commit `2c4ac180c2220bdad966bc01e95ad230e99ce26a` (tree `7ab412cc4bcbe517efcfa806e092336390312e18`). Agent and Composition pins were unchanged from the reviewed custody scripts.

## Exact checks and results

```text
node producer-health-realm-offline-review.mjs ... <(git show pinned health.json) <(git show pinned service.py) <(git show pinned server.py)
  PASS — 22 offline source/result/guard checks
for f in artifacts/*.sh; do sh -n "$f"; done
  PASS — all owned shell gates
```

Central preflight, exact test ID:

```text
ap2-m2-producer-realm-physical-path-diagnosis-0538-ap2-m2-producer-health-conversion-review-0703-preflight-1021070615-7825
```

Exact command:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-producer-realm-physical-path-diagnosis-0538 ap2-m2-producer-health-conversion-review-0703-preflight --no-cache)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test ap2-m2-producer-realm-physical-path-diagnosis-0538-ap2-m2-producer-health-conversion-review-0703-preflight-1021070615-7825
```

Result: **PASS**, exit 0 in 8s. The central log reports public13 resolver success, 10/10 source preflight checks, and ESM module-format success.

The one and only corrected startup smoke, exact test ID:

```text
ap2-m2-producer-realm-physical-path-diagnosis-0538-ap2-m2-producer-health-conversion-review-0703-startup-1021070652-30920
```

Exact command:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-producer-realm-physical-path-diagnosis-0538 ap2-m2-producer-health-conversion-review-0703-startup --no-cache)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test ap2-m2-producer-realm-physical-path-diagnosis-0538-ap2-m2-producer-health-conversion-review-0703-startup-1021070652-30920
```

Result: **PASS**, exit 0 in 11s. It reported:

```text
startup negative PASS: planted realm-root symlink refused by Runtime
startup positive PASS: physical root healthy realm=c58c8e8314d1435d93999250d99c3cc0 runtime=4f900bec56fa407ca9b7b5baaf99d456
startup-only smoke PASS: no browser, Vite, build, producer body, or producer case invoked
```

Keeper postflight command:

```sh
find -P /home/user/work/wt/ap2-m2-producer-physical-keeper-startup-preflight-0545 -type f | wc -l
find -P /home/user/work/wt/ap2-m2-producer-physical-keeper-startup-preflight-0545 -type l | wc -l
git -C /home/user/work/wt/ap2-m2-producer-physical-keeper-startup-preflight-0545 status --short
```

Result: 5,912 files, 2 symlinks, clean status. The retained 0647/0655 full byte-manifest postflight was unchanged at 5,912 regular files and 2 symlinks. After this smoke, the protected keeper is still clean at `b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7` / `fd16d32fd3487e56c9fe1ff16582dba240f63b77`, with `node_modules -> /home/user/work/app/node_modules`.

## Executed and unreached

Executed: offline source/result review; shell syntax; central cheap preflight; one central corrected startup smoke; read-only keeper postflight checks.

Unreached by design: full App suite, browser, Vite, build, install, producer body/case, and any local worker socket run. No Runtime, Agent, Composition, or App product source/pin was changed.

## Decision and next step

Keep the Runtime health schema and product code unchanged. Use the owned probe and custody artifacts for this qualification result; the orchestrator can now consume the passing startup evidence. No retry or additional producer case is needed.

