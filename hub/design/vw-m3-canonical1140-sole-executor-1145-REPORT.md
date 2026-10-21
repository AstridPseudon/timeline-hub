# Canonical1140 execution result

## Outcome

One central preflight under the 2026-10-21 11:45 manager grant passed. The
single conditional physical request failed during packet readiness before any
of the five Playwright bodies ran. No retry, alternate tuple, packet edit,
or requalification was performed.

Physical setup failure:

```text
AssertionError at packet/packet-ready.mjs:19
expected /^Total: 5 tests in 1 file$/m
actual   discovered exactly 5 current native-codec-chrome155 parity cases
```

The preflight captured and passed the full `normalDiscovery` listing with
`Total: 5 tests in 1 file`; the physical packet-ready discovery assertion
observed the summary string instead. This is the exact actual result and is
not repaired or relabeled here.

## IDs and counts

Preflight:

`vw-m3-canonical1140-sole-executor-1145-e2e-viewing-canonical1140-preflight-1145-1021114524-6250`

- command: `bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-canonical-stage-sort-packet-1140/packet/run.sh --preflight`
- PASS, exit 0, 48s
- no token, browser, Runtime, or helper launched

Physical:

`vw-m3-canonical1140-sole-executor-1145-full-e2e-viewing-canonical1140-physical-1145-1021114631-32323`

- command: `bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-canonical-stage-sort-packet-1140/packet/run.sh`
- FAIL, exit 1, 77s
- 5 discovered; 0 executed; 0 passed; 0 failed; 5 not executed

Case bodies at `cases.ts:229`, `246`, `267`, `277`, and `317` were all not
executed. Consequently there are no actual frame or PCM positives and no
picture-only or half-gain control results. No parity is inferred from setup.

## Frozen source and limits

- packet manifest: `341d40cf87d379ff2257ad9710752a0c65d2b1ce5680dc962ebde1dd816c9f53`
- App: `0d4323913b92c4e0e3830bf14ec7f35d981475ca` /
  `5a1e0e85d0f336f642426b91ccf3b3f1984ebd14`
- Agent: `d0a5072bbe7b7ce9489f43aa0a81027ec400343b`
- Runtime server: `8f105c26e3b62f9c2683f717a9773a12bc775a8e`
- Runtime producer: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, 75 artifacts
- Composition: `5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8`
- source/stage graph: `4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c` / 21455
- stage manifests: `b349c5344ec607bc32b0e4711adf317aacd984ce98d3e5a316ba726079bb37ac`, `0d9da325991bfed2fda247284adb37885d118a08f5f4fc655128f6b7481c04de`
- public13: `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738` / 77
- storage floor: `10737418240`; known threshold: `11320247244`

Central logs show the source/graph/77+75/inode/CLI/validation/build GET 200/
ancestry/list5/environment/short socket/disk/lock/cleanup guards passing
before packet-ready failed. The physical namespace contains only grant,
source tuple, and one-shot marker; no Playwright output or raw media was
created.

## Next step

Disposition the discover/list assertion mismatch and obtain a new explicit
grant and fresh immutable packet before another physical request. The consumed
1140 marker must not be reused.
