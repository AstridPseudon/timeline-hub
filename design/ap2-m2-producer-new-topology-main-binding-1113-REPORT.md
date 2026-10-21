# App2 producer new-topology MAIN binding report

## Result

Prepared the guarded source-only handoff for App source
`5863411a8c2400db719b5385002b05af0a2b3891` / tree
`31b0f77c6ef4e9fdbeff3e4f88cc4705f0891e89`, whose parent is
`b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7`; the parent’s parent is the strict
unchanged baseline `17d2518c341c47a2d8634047b400399886da3a2a`. The exact keeper
checkout and KEEP lease are `/home/user/work/wt/app-pin-5863411a` and
`.../workers/app-pin-5863411a/KEEP`.

Only data bindings changed in the private copy of the eight 0945 artifacts:
source commit/path and dependent hash values. The 0945 chain’s 51 hash guards,
20 path guards, one `0.0.13` version guard, source/custody lease, Agent
`8130a401bf44a518d5a40ae274d398b8c560be55`, Runtime
`2c4ac180c2220bdad966bc01e95ad230e99ce26a`, graph, cache, evidence, argv,
list-one, short-root, and disk prerequisites remain bound. Reverse binding to
the prior artifact bytes passed. Original 8130/2c4/C13 identities and the
19080 packet were not changed.

The rebound artifact SHA-256 manifest is:

```text
producer-physical-keeper-gate-0717-owned.sh       51326773d5c1697aba80f0d295fdd54bdd980cb86270e6446e575cc6d160d979
producer-public13-runner-0717-owned.sh             6d4055c195acce9edf1d0abf6dd6392e0a1934725d4a1ee5dc27a23c70eca120
producer-retain-failure-artifacts-0753.sh         dab4e885cedbde6273139d3b4350cacdd33020e63773f9c71e0289ab78ddea75
producer-runner-0717-owned.sh                     7bb7cbf017f62cefe2e06c5d4eed860822c0be0af8894dedd95cb75fa7f87f17
producer-startup-custody-gate-0717-owned.sh       631f3a1a20eb41aa1aaf33ff2b0164a46e4c44148639a82e341bff9249975daf
producer-startup-module-format-probe-0717-owned.mts d4eeaeb74a582fe9ccb94c1cfba7f66c41ec50eef7823db34f61ed7185e12af3
producer-startup-only-gate-0717-owned.sh          ac9b26b6d5c62154c710ca36971598f5b081e590c7ced44ac626e7bb70112b6d
producer-startup-only-probe-0717-owned.mts        a062cab11ea3a86ef75ece5a86584d0555040336032ced515d6ac50de9481d8f
```

Approved source paths and live callers:

```text
M scripts/testing/run-producer-public13-list.sh
M tests/e2e/local/producer-ownership-current-pin.spec.ts
M tests/e2e/local/support/producer-ownership-current-pin.ts
live callers: NONE
```

## Verification

Passed:

```text
python rebind-chain.py
  PASS: data-only rebinding, dependency-ordered nested hashes, reverse proof
python -m py_compile outer-controls-run.py
  PASS
sh -n artifacts/*.sh
  PASS: six shell artifacts
node --check artifacts/producer-startup-only-probe-0717-owned.mts
node --check artifacts/producer-startup-module-format-probe-0717-owned.mts
  PASS
```

The retained 0935 outer-control harness was invoked once, then stopped at its
first failure: `before`, `0/5`, before `dispatch.jsonl` existed. The copied
harness did not include its existing `launch-tool-stub.py`; system `git` ran in
the fixture and returned `fatal: not a git repository`. This means the five
controls have no pass result. No guarded preflight was run after the failure;
no browser, actual test, build, install, daemon, socket, service, or full suite
was run.

The retained control contract is five cases: `before`, `after`,
`absent-output`, `copy-failure`, and `success`; expected counts are respectively
`1 shell/0 child/0 build`, then `4 shells/1 child/1 build` for each remaining
case. None reached its assertion phase in this attempt.

## Decision and limitation

The strict two-link source ancestry is satisfied by the current commit and is
not repaired by changing `APP_SHA`; `APP_SHA` remains `17d…`. The HOLD is only
for independent review of the existing command and restoration of the missing
control-harness stub before one authorized rerun. The manager must forward the
handoff only after that review. No product/spec/helper/runner logic, guard
policy, pin authority, or graph was changed.
