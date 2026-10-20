# Runtime final producer checkout

This is the stable, read-only Runtime producer checkout for the final composed
release source:

- Path: `/home/user/work/wt/rt-m2-pin-2c4ac180`
- HEAD: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`
- Tree: `7ab412cc4bcbe517efcfa806e092336390312e18`
- Branch: `tl/rt-m2-pin-2c4ac180`
- Worktree state: clean at handoff

The final S2 review approves the composed release tree
`7ab412cc4bcbe517efcfa806e092336390312e18`; this checkout provides that exact
tree at the stable producer commit above.

## Release identity

The values below are the exact identities recorded in
`design/runtime-release-s2-final-review.md` and verified against this checkout:

- Client release: `0.2.13`
- Schema digest: `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`
- Raw command schema digest: `sha256:a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef` (48 definitions, 22 operations)
- Artifacts: `75`, including `operation-handle.ts`
- Artifact manifest version: `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`
- Raw `contract/artifacts.json` SHA256: `129abdbbf1f877643618b5290b39a5dd9225ba95b4c8fe8f2bb005ea4cf85497`
- `contract/component-manifest.json` SHA256: `1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5`

The package metadata agrees on `0.2.13`: `generators/release.json`,
`packages/python/pyproject.toml` (`astrid-runtime-client`), and the TypeScript
package and lockfile (`@astrid/runtime-client`). The root service package
`astrid-runtime` remains separately versioned `0.1.0`.

## Consumer vendor-lock commands

From a consumer checkout containing `runtime.lock.json` and
`scripts/vendor_lock.py`, first set that lock's `source_commit` to the full
producer SHA shown above. Then run:

```sh
PYTHONDONTWRITEBYTECODE=1 python scripts/vendor_lock.py update runtime.lock.json --producer /home/user/work/wt/rt-m2-pin-2c4ac180
PYTHONDONTWRITEBYTECODE=1 python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-m2-pin-2c4ac180
```

`update` copies the locked Runtime client artifacts and records the producer
manifest version; `check` verifies the consumer bytes, producer HEAD, committed
manifest, and producer artifact hashes. The producer checkout itself is not
modified by either command.

## Qualification boundary

The approved release source is the merged Runtime source represented by
`2c4ac180c2220bdad966bc01e95ad230e99ce26a` and tree
`7ab412cc4bcbe517efcfa806e092336390312e18`. Consumer qualifications remain
separate work: Agent/App caller pairing, their local pins, and their own
qualification evidence must be performed by their owners. This handoff does
not publish, activate, or mark the release as published.
