# AP2-M2 parent corrected custody, one original 0915

## Verdict

**REACHED ACTUAL; first retained product failure.** The changed0908 custody
gate and registration generator were independently approved. After the
selected0911 run became terminal and the local browser lock was free, exactly
one fresh integration parent actual was submitted with `--no-cache`.

Parent run ID:

`ap2-m2-parent-corrected-custody-one-original-0915-ap2-m2-parent-corrected-custody-one-original-0915-integration-actual-1021091413-25174`

Result: exit 1 after 185 seconds. The first retained product failure was:

```text
tests/e2e/local/three-products.spec.ts:1557
expected recovery attempts=1, received attempts=0
Timeout 90000ms exceeded while waiting on the predicate
```

The following assertions were not reached: `wire.posts.length === 1` and the
subsequent request/body checks. No rerun or repair was performed.

## Independent 0908 custody review

The exact 0908 artifacts were reviewed from:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-registration-and-keeper-correction-0908/record/`

The reverse diff from the 0855 gate contains exactly three hunks and six
changed lines. Only these values changed:

- protected keeper: `/home/user/work/wt/app-pin-8eb4d08e`;
- KEEP marker: `.../workers/app-pin-8eb4d08e/KEEP`;
- fresh evidence root: `.../record/evidence-final95-parent-8eb4d08e`.

The actual protected pin was independently verified as HEAD
`8eb4d08e60f434b938ea885c8cadca4bd87151b3`, tree
`ea317333400d1a342f2520556eef8ce9399666c1`, clean tracked status, active
KEEP, and `node_modules -> /home/user/work/app/node_modules`. The service
snapshot separately reported tree `ea317333...`. The selected exact pin was
also attached only to the same shared dependency symlink and remained clean.

Direct byte hashes were:

```text
gate          81676d3b04606ad0a9276008db2173cf636fce18c8aab77dd7e718e5d490fb55
helper        96969ce9ff43b676abb4616009fd1112e93020065483b2a8ae0afac7245ba109
driver        34ee03d1ea6f25ae4f68b8965f5c9b050d8892214416ec3bf551dfa81b17a2d2
source_runner 1d2ebce742bab9a20a911baedab8e7e318e82d6f1043f7f554949855acf646fd
```

`sh -n` passed for the generator, gate, and stored registration command.
The generator's controls passed: malformed 62-character digest refused before
request, valid lowercase 64-hex accepted, wrong source/pin/KEEP refused, and
stored command hash identity passed. The direct command check independently
confirmed the stored fresh integration registration contains each computed
gate/helper/driver hash exactly once.

The aggregate gate preflight passed with the real pin: source tuple, d05e
marker, locked graph, 76-artifact manifest, helper/driver guards, negative
refusals, zero-test/argv controls, and exactly one collected test
`three-products.spec.ts:1440`. The unchanged driver hash preserves its
child-status, retention, cleanup, and zero-test guards; the source runner and
helper hashes were also unchanged.

The original31285 packet was not reused or overwritten. The 0908 before/after
hash lists compare equal, and a fresh hash of the packet still matches the
before list immediately after the parent failure.

## Selected0911 prerequisite

Selected0911 reached terminal state before the parent request, with exit 1 in
one second and no browser/body execution. Its stored command failed in the
central precondition chain before the owned runner; its log was empty and no
selected evidence packet was produced. The local browser lock was then free.

## Parent durable evidence

Retained packet:

`.../record/evidence-final95-parent-8eb4d08e/run/`

It contains `bounded-browser-evidence.json`, `error-context.md`,
`playwright-trace.zip`, `runner-tail.log`, `source-identity.txt`,
`evidence-presence.json`, `result.txt`, and `retention.log`. The packet records
`runner_status=1` and `run_root_cleanup=after-evidence-copy`; source identity
matches the protected App pin and tree.

## Commands and results

- `sh -n` generator, gate, and stored command — passed.
- Independent reverse diff/hash/62-hex/packet checks — passed.
- `sh .../final-keeper-gate.sh preflight` from the protected pin — passed.
- `request-test ... ap2-m2-parent-corrected-custody-one-original-0915-integration-actual --no-cache` — exactly one request; actual reached.
- `wait-test ...25174` — failed exit 1; first retained failure at `three-products.spec.ts:1557`.
- Immediate durable evidence and original31285 hash verification — passed.

No App source files changed. Only the authorized ignored dependency symlinks
were attached to the two exact detached pins; both tracked worktrees remain
clean. No local browser/socket/full/install run was performed.
