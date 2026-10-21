# AP2 M2 selected real-output retention — independent first review 0941

## Decision

**HOLD the exact `ff79ff6f` bytes for merge until copy-failure refusal is
repaired.** The retention correction itself is minimal and correctly retains
the real 13522-shaped partial packet, but the claimed copy-failure guard is
not effective on this shell path. No runner, App source, helper, selected
actual, registration, or test was changed by this review.

The prior 0911 overall hold remains relevant to any actual submission: the
next registration must accept the synthetic service **tree** while retaining
the exact protected keeper **HEAD/tree**. This review does not authorize
another original case; the HOME selected phase-order fixture correction is
still pending.

## Exact bytes and minimal diff

Reviewed artifacts:

```text
new0927 runner:
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-real-output-retention-correction-0927/artifacts/run-owned-selected-final95.sh
  SHA-256 ff79ff6f32d248989b6227790cebbe34c1ffd4711b8b3dc90c0708fe6e7a8c8e

immutable old0903 source:
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-real-output-retention-correction-0927/artifacts/source-0903-run-owned-selected-final95.sh
  SHA-256 4459f2c9acd7ce411f92beab33c216e549c98fe1fad996706998e6c5aaab85a3

0858 reverse/source proof: b3fb1336b36bd3703e3fc460ca9fe0932e9601b39c721215e07c5ca35bf535e5
```

`diff -u old0903 new0927` has only two changed regions: the identity adds
`*_present` plus explicit `*_retained` flags, and retention changes from
all-three-required to independent detection/copy of DOM, error-context, and
trace. All 29 changed lines are in those regions; the remaining 701 source
lines are byte-identical. The original child status and EXIT cleanup are
unchanged.

The new path correctly does the following:

- records presence separately from retention;
- treats no output as `PREBODY`, retaining child log, identity, and sums;
- treats any available artifact as partial output and copies each available
  artifact independently;
- keeps the bounded allowlist to `child.log`, `browser-output/{dom.html,
  error-context.md,trace.zip}`, `identity.txt`, and `SHA256SUMS`;
- refuses a non-absolute, pre-existing, symlink-resolved, or RUN_ROOT-inside
  durable destination before writing it.

No credential, environment dump, source checkout, cache, summary, or browser
profile is copied. The unique disposable durable destination used for my
proof was outside the runner root and was removed after inspection.

## Independent bounded proof

Command (existing MODE=run launch-stub seam; no direct helper call):

```sh
NORMAL014_USE_BASE_PYTHON=1 \
APP_KEEPER_ROOT=/home/user/work/wt/app-pin-a50ca4a0 \
SELECTED_FINAL95_MODE=run \
SELECTED_FINAL95_LAUNCH_STUB=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-real-output-retention-correction-0927/artifacts/fixture-failure-trace-context-only.sh \
SELECTED_FINAL95_DURABLE_ROOT=/tmp/ap2-m2-review.Sq2mQu/evidence \
sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-real-output-retention-correction-0927/artifacts/run-owned-selected-final95.sh \
/home/user/work/wt/ap2-m2-selected-real-output-first-review-0941
```

Result: exit **17** as expected; child and outer status were both 17.
`sha256sum -c SHA256SUMS` passed for all retained files. The packet contained:

```text
browser-output/error-context.md  d27b851969fe1e1e39c93c8a5da46095f747c1a6a934562d50619caa0e83d0c0
browser-output/trace.zip         0efb3d7a43af40edf8d47cefe23876939ea22b0bbde9c847819562e98f9eafd2
child.log                        356db59611b56b8da4226db632ad14922a6b58409bf9d42f06b019407445c724
identity.txt                     f0c8126dd9057fa7be9de5ab9ed133710649fd2369b647012dbd33088c0cab64
```

Identity was truthful for the fixture: `phase=BODY`, `child_status=17`,
`child_started=1`, `body_started=1`, `dom_present=false`,
`dom_retained=false`, `error_context_present=true`,
`error_context_retained=true`, `trace_present=true`, and
`trace_retained=true`. No standalone DOM was claimed. The temporary
`ap2-m2-selected-final95-owned.*` root was absent after EXIT cleanup.

This proves retention of a setup/fixture failure packet only. It proves no
P1/P2 admission, page/DOM setup, selected behavior, browser, build, daemon,
socket, service registration, or original case.

## HOLD finding: copy failure is masked

The report's claim that copy failures return a nonzero retention result is not
supported by the shell control flow. `cleanup` invokes
`retain_failure_evidence` in an `if` condition. Under `set -e`, commands in a
function called as an `if` condition are exempt from errexit. In the new
independent blocks:

```sh
copy_bounded "$context" "$durable_root/browser-output/error-context.md" 1048576
context_retained=true
```

if `copy_bounded` fails (for example its size check or `cp`), execution can
continue, the retained flag is set true, identity and `SHA256SUMS` can still
be written, and retention can report success. The same masking applies to the
child-log copy and the other artifact copies. The pre-existing durable-root
refusal itself still returns visibly because it explicitly `return 1`s.

Exact minimal correction for the owner (not applied here): make every
`copy_bounded` and newly-created artifact-directory operation fail the
retention function explicitly, e.g. `copy_bounded ... || return 1` before
setting its `*_retained=true` flag. Preserve the independent-copy behavior;
do not restore the DOM requirement.

## Marker semantics and unchanged custody

`BODY` and `body_started` are runner markers, not behavior evidence.
`body_started=1` is set before the launch stub (line 690) or before the real
test command (line 705), and `phase=BODY` is derived from any output file.
The exact minimal reporting correction is to describe these as “launch/output
phase entered” and “output present,” never as proof that P1, P2, page/DOM
setup, or even the test body executed. The 13522-shaped fixture is explicitly
setup failure before selected assertions.

The byte diff confirms the following remain unchanged from old0903: source
and protected-keeper checks; synthetic service-tree versus exact keeper
HEAD/tree separation; Agent/Runtime/producer pins and artifact graph;
selected title/spec, argv, list-one/zero-test refusal; locked Node/Vite/
Vitest/Playwright graph; short physical paths; origin/credential checks; and
single-root cleanup/original-RC handling. The next registration must preserve
that tree-versus-keeper split; no registration was submitted here.

## Commands and scope

```text
sh -n <new0927 runner>                         PASS
diff -u <old0903> <new0927>                    two retention-only regions
bounded MODE=run fixture proof                 PASS; expected exit 17
(cd <packet> && sha256sum -c SHA256SUMS)       PASS
git status --short --untracked-files=all       clean
```

No broad repeat, historical/browser test, selected actual, full suite,
central service submission, install, build, daemon, socket, or shared
dependency write was performed. Existing 0903 controls and the 0927 report
were reused for the unchanged guard set; this review did not claim those
historical controls as newly re-run.
