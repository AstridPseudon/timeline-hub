# Runtime private 613 / 952 pair tuple

**Status: PRIVATE HANDOFF ONLY.** This is the independently approved Runtime
candidate for Agent peer review/private qualification. It is not a public pin,
adoption, release, integration pin, or native-pair qualification.
This document records final handoff execution, not a review-of-review.

## Exact tuple

| Field | Value |
| --- | --- |
| Runtime commit / tree | `95202c2b09e83aaae028287d6c59b773410141f3` / `d438d3e28a29ad80fa6b7c19c55e1b7a4485eae2` |
| Contract version | `INTERNAL0.2.14` (package version `0.2.14`, unpublished) |
| Raw Agent/Runtime command schema | `contract/schemas/edit-command.json`, SHA-256 `613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3`; Agent357 source is byte-identical |
| Canonical Agent source | commit `357230816c86da65d5f8cc92b10a3a90d29874e0`, tree `94692ec85167d5c606626c4ec678fe2a63ee0aa6` |
| Schema inventory | 55 definitions / 29 operation clauses / 12 explicit v2 branches |
| Health/contract metadata | `SCHEMA_DIGEST = sha256:ddf6396dc32bd54bfeed549a99034693eaed76478b45ad0b7242117f6b734d36`, from `packages/python/astrid_runtime_client/contract_metadata.py` |
| Raw bundle | `runtime_protocol/schemas/timeline-commit-bundle.json`, SHA-256 `4a0779db14b9bbd827e964a495367b465bab5c00ee0b5717b8ff27777010a858` |
| Artifact manifest version | `sha256:b397e5fdb9fc25502bbda9ad5011e82dd2d63330d5af373834d31e6761276e20` |
| `contract/artifacts.json` file SHA-256 | `35aa9d247979760b5570f804f30688fb6eaa179d57f5bbca0a41fd6e645deb9d` |

The `4a0779…` value is the raw bundle-file hash; it is not a wire or health
digest. The health/contract digest is the `ddf6396d…` metadata value above.
The raw command-schema, raw bundle, metadata/health, and artifact-manifest
identities are separate and must not be relabeled or substituted.

Public 0.2.13 remains unchanged at producer `2c4ac180c2220bdad966bc01e95ad230e99ce26a`.
The ordinary 0.2.14 candidate remains unchanged at Runtime `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`,
tree `4b7dd0fe44be973c344bab3de568eaf0bdd28476`, artifact
`sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0`.

## Evidence and next gates

- [Original independent 952 review](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/runtime-private613-952-review.md>): APPROVE for private Agent peer review only; its `4a0779…` label is corrected above.
- [Agent357 source review](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/runtime-review-full-union357-source.md>) and [generator/source guard](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/runtime-union613-generator-readiness.md>) preserve the 55/29 source and compatibility floors.
- [Normal private generation evidence](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/runtime-union613-normal-private-gen.md>) records the exact 218-pass and 645-pass lanes; the source-guard review records 131 passed.
- [Closed-intent fix evidence](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-closed-empty-intent-generator/report.md>) records 147 focused and 94 adjacent passes. These are prior evidence, not a broad rerun here.

The exact producer checkout requested by the manager is
`/home/user/work/wt/rt-pin-95202c2b` at Runtime 952/tree d438. The corrected
scratch consumer was copied from `fe59f6a3`, retargeted only to this checkout,
and its `@ts-expect-error` was moved directly before the forbidden nested
`intent.unexpected` property. The exact one-time check passed:

```text
tsc --noEmit --strict --module NodeNext --moduleResolution NodeNext --target ES2022 \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-private952-handoff-finalize/probes/typescript_consumer_probe.mts
exit 0
```

Still required: a new normal Agent PRIVATE vendor pin, peer review of this
Runtime counterpart, and one actual native 357/613 pair. No public pin,
adoption, or integration is authorized by this handoff.
