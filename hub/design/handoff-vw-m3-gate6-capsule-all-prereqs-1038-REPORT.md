# Gate6 capsule all-prereqs preflight — 1038

## Disposition

**HOLD / REQUEST CHANGES.** A reusable preflight-only packet is prepared from
the frozen 1002 tuple. It adds the exact normal source-closure negative and
positive checks before helper/task admission, but it did not request the
central service because independent capsule custody is REQUEST CHANGES.

## Packet

Worker packet:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-capsule-all-prereqs-1038/packet`

It contains a flat `run.sh`, the reused 1002 `preflight.sh` and validation
helpers, and `source-closure.mjs`. `run.sh` normalizes cwd, uses fd9 flock,
clears unsupported child overrides, checks canonical real paths and private
scope dirs, runs the exact four-edge negative propagation and positive d0a
closure witness, then requires an independent `APPROVE` before reaching the
normal preflight. It never invokes issuance.

Source witness passed locally: negative four exact unresolved edges; positive
exact direct-closure hashes, real regular files/no symlinks/no hardlinks, and
non-empty bundle. The packet command exits 3 as designed at the current
custody gate.

## Exact blocker

The independent review at
`handoff-vw-m3-owned-capsule-custody-review-1038-REPORT.md` confirms the
26-file capsule is source-only, not an admissible
`ASTRID_REMOTION_PROJECT_DIR`: it lacks package manifest, lockfile,
`node_modules`, and in-project CLI. The immutable d0a project has the real
graph/CLI but resolves the frozen sibling import under the absent
`/home/user/work/runtimes/astrid`. Symlinked graph/CLI escapes project
containment; a foreign validation artifact fails measured-input/context
equality. Copying/installing the immutable graph is forbidden; its read-only
census is at least 340,471,649 regular-file content bytes / 393,027,584
allocated bytes across 21,422 regular files before directory/metadata
overhead, so this is a HOLD rather than an attempted repair.

No central suite, helper/task admission, token, browser, Runtime/server,
socket, render, export, marker, physical run, or full suite was run.
