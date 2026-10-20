# App M2 duplicate effective-graph actual gate

Date: 2026-10-20 UTC  
Worker: `ap2-m2-duplicate-effective-graph-actual-gate`  
Repo: App  
Candidate: `9caf57adbc07d046b9b10d1bed356526e88f56c3`  
Candidate tree: `0800de89eac152136380f3031c6447f538e6c145`

## Result

The requested one central duplicate gate ran with the effective private
Composition13 graph and reached the real Chromium journey, but failed on an
actual product conflict during exact retry. The duplicate gate is therefore
not qualified and no deletion/green claim is made.

Central request:

```text
ap2-m2-duplicate-effective-graph-actual-gate-e2e-m2-duplicate-effective-graph-three-products-1020201231-672
```

Result: exit 1, 106 seconds, one test failed.

## Private runner and effective graph

The worker-owned runner is:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-duplicate-effective-graph-actual-gate/run-central-m2-duplicate-effective-graph.sh
```

The registered suite is `e2e-m2-duplicate-effective-graph-three-products`.
The runner was copied from committed
`tl/ap2-m2-ordinary-enabled-fixture-final-run-source:scripts/testing/run-central-m2-ordinary.sh` and changed only for its private run-root,
worker-owned suite target, and test selector:
`M2 native occurrence duplicate`.

Before the product run it verified:

- Agent `8130a401bf44a518d5a40ae274d398b8c560be55`, tree
  `236c3e57e0265c52b81ba8085de3193026176bff`;
- Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree
  `7ab412cc4bcbe517efcfa806e092336390312e18`;
- private Composition graph version `0.0.13`;
- locked graph archive SHA-256
  `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`;
- Composition13 tarball SHA-256
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`;
- read-only shared graph and native Python availability;
- clean App source snapshot and the original App `node_modules` target.

It recreated package bins in a private per-run graph, attached that graph to
the App snapshot, and restored/removes all private paths on exit. The hosted
Vite build passed, which confirms the effective App build resolved the private
Composition13 graph instead of the failing shared 0.0.8 package; the prior
`clipOpacity` export failure did not recur. The source tuple also reported
Agent `8130...`, Runtime `2c4...`, and matching schema digests before the
journey.

## First causal failure

The browser launched and the real test reached the exact-retry phase of:

```text
tests/e2e/local/three-products.spec.ts:1204
M2 native occurrence duplicate: lost ACK, Agent label, local label, restart, exact retry and guarded undo
```

At line 1307, the retry expected an accepted commit (`200`) but received
`409`:

```json
{
  "code": "conflict",
  "details": {
    "conflicts": [{
      "kind": "dependency_changed",
      "path": ["label"],
      "ref": "parent/track:V1",
      "ours": {"state": "absent"},
      "theirs": {"state": "present", "value": "F2 Agent duplicate sibling"}
    }],
    "reason": "dependency_changed",
    "status": "conflict"
  },
  "message": "original authored guard changed"
}
```

This is an actual product/harness journey failure after browser launch, not a
Composition build failure or a provider-neighbor baseline. The later retry,
undo, opaque-preservation, and final zero-legacy assertions were not reached.
The three unrelated provider tests remain unclassified; no baseline was
asserted from this result.

The central log is:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-duplicate-effective-graph-actual-gate-e2e-m2-duplicate-effective-graph-three-products-1020201231-672/log.txt
```

## Local/static validation

Passed:

```text
sh -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-duplicate-effective-graph-actual-gate/run-central-m2-duplicate-effective-graph.sh
private Composition13 graph/archive/tarball guard checks
clean predecessor commit/tree guard checks
```

No local browser, socket, Runtime-door, full suite, or direct runner execution
was performed. No App product code, dependency, public pin, shared install,
or test guard was changed. One central request was made; no rerun was made.

## Recommended next step

The App/Agent/Runtime owners should inspect the duplicate journey’s intended
dependent-edit semantics at the exact retry conflict for
`parent/track:V1`. Preserve the existing causal, retry, undo, opaque-data,
and zero-legacy assertions; do not reclassify this failed gate as a baseline
or mark the duplicate deletion qualified until a separately authorized run
passes on a reviewed candidate.
