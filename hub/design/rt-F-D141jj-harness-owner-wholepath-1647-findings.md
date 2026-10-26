# D141jj finite owner-fixture continuation — NOT READY

## Verdict

The complete Sol-1637 derivative remains unqualified. Its one complete command
passed the real caller → D68 → bounded-stub positive, poisoned-manifest and
root-binding controls, and the corrected stale non-App upstream refusal. It
then stopped at fixture setup:

```text
os.chown(wrong_owner_root, 65534, -1)
OSError: [Errno 22] Invalid argument
```

This is before `source_identity`; it is not a source-owner PASS, a stage-owner
PASS, a production defect, or a safety/classifier refusal. The namespace maps
only UID/GID 0 (`/proc/self/{uid,gid}_map: 0 0 1`). No chown or privilege
experiment was attempted here.

## Acceptable finite fixture strategy

Use a private, allowlisted per-path stat fixture or an isolated module proxy.
The proxy must leave the candidate guard source bytes and control flow intact,
keep the real `os.geteuid()` at 0, and alter only `lstat()` metadata for the
named fixture path. Every other path and every non-owner field must delegate to
the real implementation. The proxy must be installed only in the isolated
caller module for source/service preflight and only in the isolated D68 module
for the direct stage entrypoint. If the actual caller launches D68 in a child
process, the child must receive an equally narrow D68-module/path fixture; a
parent-only proxy cannot establish the child guard and must be reported
unverified.

The source-owner case may use a fake `st_uid != 0` for exactly the private
source root. The stage-owner cases must use a real UID-0 source root first and
fake `st_uid != 0` only for the stage parent/service TMPDIR. This proves the
source guard passes before the intended stage-owner guard. Mode cases may use a
real private directory with mode 0775; no owner spoof is needed. No global
`os.geteuid` patch, broad `os.stat`/`Path.lstat` patch, production edit, or
exception sentinel is acceptable.

## Remaining finite defects and boundaries

1. The UID65534 ownership fixture is impossible in this root-only sandbox.
   Adapt only the private fixture mechanism as above. Do not count setup
   `EINVAL` as any guard result.
2. Eight caller negative cases and both direct stage controls were not reached
   after the setup stop. They remain required evidence, not presumed passes.
3. The stale-upstream observation must remain exactly the corrected contract:
   recorded `upstream_base != current origin/main`; caller returns code 2;
   caller writes a `FAIL` receipt; D68 records the exact reason; repos and
   stage are empty; the builder marker is unchanged. Do not convert this to an
   exception-only assertion or a no-receipt result.
4. The wrong-stage-owner actual-caller case may legitimately stop in the
   caller's `run_wrapper` stage-parent guard; the separate direct D68 case must
   reach D68 `require_directory(stage parent)`. Neither may stop first in
   caller `source_identity`.
5. The wrong-stage-mode cases have the same two intended entrypoints: caller
   `run_wrapper` and direct D68 `require_directory(stage parent)`. The source
   identity must be real and successful before either stage-mode refusal.
6. The wrong-App-tree case has two distinct controls: direct
   `require_app_base` (authorized tree reason) and caller `gate_identity`
   (frozen tuple tree drift). A caller tree refusal is not evidence for the
   direct authorized-tree branch.

The prior positive and historical same33 PASS remain retained evidence. No
qualification, installation, or product merge follows from this report.
