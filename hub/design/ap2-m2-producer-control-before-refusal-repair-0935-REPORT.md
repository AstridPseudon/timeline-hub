# AP2 M2 producer outer-control refusal repair — 0935

## Result

The copied 0917 harness was repaired only for the diagnosed `before` case:

- `before` now expects one outer custody-shell dispatch, zero child dispatches,
  and zero build-stub dispatches.
- `after`, `absent-output` (missing), `copy-failure`, and `success` retain the
  four-shell dispatch order, one child, and one build-stub assertions.
- Temporary `set -x` / `sh -x` debug noise was removed.
- The eight final chain artifacts and product source were not changed.

The final cheap preflight then stopped before the five controls. It exposed a
separate, real binding-chain mismatch, so I stopped as instructed: no chain
repair, no second preflight, and no control retry.

## Corrected harness diff

```diff
@@ -107,8 +107,7 @@
   config=t/'config.json';config.write_text(json.dumps(cfg))
   env=dict(os.environ,PATH=str(binpath)+':'+os.environ['PATH'],CONTROL_CONFIG=str(config),TMPDIR=str(t/'tmp'))
-  debug_cmd=cmd.replace(' sh '+str(chain/'producer-startup-custody-gate-0717-owned.sh'), ' sh -x '+str(chain/'producer-startup-custody-gate-0717-owned.sh'))
-  result=subprocess.run(['/bin/bash','-c','set -x\n'+debug_cmd],cwd=app,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=30)
+  result=subprocess.run(['/bin/bash','-c',cmd],cwd=app,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=30)
@@ -117,13 +116,20 @@
   events=[json.loads(l) for l in (case/'dispatch.jsonl').read_text().splitlines()]
   shells=[e for e in events if e['tool']=='sh' and e['args'] and e['args'][0]!='-c']
   executed=[Path(e['args'][0]).name for e in shells]
-  assert executed[:4]==[ORDER[-1],ORDER[3],ORDER[2],ORDER[1]],executed
+  if label=='before':
+   assert executed==[ORDER[-1]],executed
+  else:
+   assert executed[:4]==[ORDER[-1],ORDER[3],ORDER[2],ORDER[1]],executed
   # npm forwarder must really dispatch build + test; fake npm only handles
   # build, while the real wrapper executes the fake Playwright executable.
   children=[e for e in events if e['tool']=='playwright']
-  assert len(children)==1,children
-  assert children[0]['args']==['test','--config','playwright.producer-ownership-current-pin.config.ts','tests/e2e/local/producer-ownership-current-pin.spec.ts']
-  assert sum(e['tool']=='build-stub' for e in events)==1
+  if label=='before':
+   assert not children,children
+   assert sum(e['tool']=='build-stub' for e in events)==0
+  else:
+   assert len(children)==1,children
+   assert children[0]['args']==['test','--config','playwright.producer-ownership-current-pin.config.ts','tests/e2e/local/producer-ownership-current-pin.spec.ts']
+   assert sum(e['tool']=='build-stub' for e in events)==1
```

The complete copied record is at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-control-before-refusal-repair-0935`

## Verification

Passed:

```text
outer-controls.py: syntax PASS
artifact shell scripts: syntax PASS (6)
register-final-chain.py: PASS; chain=8; status=preflight-bound-no-actual
literal next command syntax: PASS
```

The generator initially referenced the deleted 0917 service worktree. In the
copied generator only, `SERVICE_ROOT` was bound to the existing exact keeper
`/home/user/work/wt/app-pin-09171792`, as permitted by the brief's final
preflight-on-pin instruction. This does not alter the chain or product source.

Attempted once, stopped:

```text
cd /home/user/work/wt/app-pin-09171792 && sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-control-before-refusal-repair-0935/artifacts/producer-startup-custody-gate-0717-owned.sh preflight
```

`preflight.log` is empty and the command stopped before the five-control
marker. Controls completed: `0/5`. No browser, build, daemon, socket, actual,
install, service, or full-suite run occurred.

## First mismatch

The first failing product guard is
`producer-startup-custody-gate-0717-owned.sh:68`:

```text
expected OWN_WRAPPER_SHA = 0f57d4885999f265ee43a14acb14a9abe58014dc773edc9edb3423687f8add39
actual producer-runner-0717-owned.sh = def88cbff626291b52ce7ab695366da131ea753824d940a9342f8a896cb38cd3
```

The original 0917 chain contains the same stale expected value; the 0822
runner itself hashes to `0f57d488…`. This contradicts the settled statement
that the final chain is fully rebound. I did not silently repair it because the
run rule says to stop at the first new failure. The likely next repair is to
rebind the transitive runner hash in the chain, then rerun the full preflight
and five controls once under orchestration authority.

## Final manifest and registration readback

Manifest:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-control-before-refusal-repair-0935/manifest.json`

```text
status: preflight-bound-no-actual
App HEAD: 09171792bd626f5eabd421d1f1c2b497a4fc9786
App tree: 31b0f77c6ef4e9fdbeff3e4f88cc4705f0891e89
spec SHA-256: 6666c0365d13f302725788e6fbfcce9e0fb283e4b30c40661886522a67f270e6
helper SHA-256: df1faac404b69efa8a5fb06297814e6ca3b5d52b4a5856633706c7ac2e3ae949
wrapper SHA-256: 329cfca7ff6fcc6764e5eaa6cb53ba77a40e6aa842361d0ed6795ca5b4398352
registration.sh SHA-256: 49a05eae563e3b1d1b9412a53b55c934fef20fd34871de3494b6ce858b1bbe5d
```

The manifest registration digest was checked against the actual
`registration.sh` bytes and matched exactly. The literal next command was
syntax-checked but not executed:

```sh
cd /home/user/work/wt/app-pin-09171792 && PLAYWRIGHT_PORT=24117 PLAYWRIGHT_BASE_URL=http://127.0.0.1:24117 sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-control-before-refusal-repair-0935/artifacts/producer-startup-custody-gate-0717-owned.sh list
```

## Blocker

Blocked by the pre-existing final-chain transitive `OWN_WRAPPER_SHA` mismatch
above. No `DONE` marker was created.
