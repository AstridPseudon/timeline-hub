# P5 D141 immutable Agent-tree correction validation

## Disposition

This is a finite metadata fact correction only. The original applicability
record remains immutable and is not retargeted. The separately named derivative
corrects exactly one JSON pointer:

`/actual_integrated_heads/agent/tree`

Original value:

`92a3ffdb5a8bf476f10bfa1bbda3e2856fb9938c`

Correct value:

`92a3ffdb5a8bf476e10bfa1bbda3e2856fb9938c`

The corrected value is authenticated from Agent Git object
`8585ed9c0404d0187b2ce70242d25114a32747c2^{tree}`; it is not guessed.

## Immutable bytes and hashes

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| Original `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/rt-F-D141-postREG-custody-review-0513-p5-applicability.json` | 8585 | `a46bcb2d7e566b01c54da297968a2236eb81d6598f5ac85bf18c55e70d096389` |
| Derivative `p5-applicability-corrected.json` | 8585 | `688d08bc899c3c1583fb2010d0f8ff2251e2c593b24d62d2a703856d90a26ce6` |

The original hash was read back after derivative creation and is unchanged.
The derivative parses as JSON. A recursive readback comparison found exactly
one differing path, the pointer above; all other keys, key order, arrays,
values, 38-case IDs, XML/case-set paths and hashes, module paths, and source
paths are unchanged.

## Git and controlling-source proof

Commands and results:

```text
git -C /home/user/work/agent rev-parse --verify 8585ed9c0404d0187b2ce70242d25114a32747c2
8585ed9c0404d0187b2ce70242d25114a32747c2

git -C /home/user/work/agent rev-parse --verify 8585ed9c0404d0187b2ce70242d25114a32747c2^{tree}
92a3ffdb5a8bf476e10bfa1bbda3e2856fb9938c

git -C /home/user/work/agent cat-file -t 8585ed9c0404d0187b2ce70242d25114a32747c2^{tree}
tree
```

The corrected tree agrees with the Agent entry in the source-independent 0513
handoff (SHA-256
`53604c56e3d3083960de700c79160b22e186401732edad734ae1083b320e67cb`) and the
local Git object. The separately named 0513 source manifest (SHA-256
`9eb45d29e3c51ea639835b7aec3526fb4b5532b68e6cd618de37c967a424e5f2`) still
records the stale copied Agent tree
`92a3ffdb5a8bf476f10bfa1bbda3e2856fb9938c`; this is a finite unrelated
metadata discrepancy, left unmodified and not expanded. The controlling C0
contract is `/home/user/timeline-hub/hub/design/commit-v2.md`,
SHA-256
`4581ea85aada0af405b1b1b9284e9938a6dba3ca4f6980b7c3c0be8f135f9bb7`.

All checked commit, tree, and parent identities are full 40-digit lowercase
hex values.

## Identity and scope boundary

The original event/metadata identity remains:

- request `runtime-d141-p5-cut-1026013331-6934`, status `pass`, summary
  `38 passed in 31.02s`;
- original proof pair Runtime `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d` /
  Agent `28e56cacb42d3da85b02e5b3543895b44f3d0f70`;
- XML path, XML SHA-256, case-set SHA-256, counts, and retained source/module
  paths are unchanged.

This is distinct from final integrated-head applicability: Runtime
`95d98f038320d5d46bd679ac000ab3e15825c935` and Agent
`8585ed9c0404d0187b2ce70242d25114a32747c2`, where the Agent tree is the
corrected Git value above. The source-independent 0513 PASS remains controlling;
there is no new P5 receipt, no rerun, no new body, no collection/import/provider
review, and no contract or production-caller change. The production caller
continues to use the original P5 path.

No product, test, fixture, input, generated file, pin, source, service, queue,
request, admission, environment, package, or repository file was changed.
