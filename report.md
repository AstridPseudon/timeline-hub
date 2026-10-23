# OPS-retire-process independent review

## Disposition: FAIL

The source diagnosis is locally supported, but the required diagnostic
deliverable is not reviewable. The author’s final `report.md` contains only a
short summary and says that a minimum read-only HOST command exists; it does
not contain that command. The author log likewise contains the requirement and
the claim, but no command bytes. Therefore there is no exact command to
recover, hash, or export. I do not invent a replacement.

This is an evidence-custody failure, not a finding that the installed guard is
wrong. Remote App2 errno, PID, proc namespace, mount visibility, and race state
remain unknown. The nine refusal receipts prove only the common refusal text
and zero retirement, not their remote process cause.

## Independently verified source diagnosis

Installed files were read-only inspected at these hashes:

- handler `retire-child-venv`: `954d5d87fe2e6fcf42b34953ec0edc519a2eb97ade8f66f0f2f96f523516b791`
- request `request-retire-venv`: `21f61833a6718794ab2a06a3a96d34ca58c050ccd0151622e16866ac78758139`

In `scan_processes` (handler lines 280–315):

- A present process with non-empty cmdline and failed `/proc/<pid>/exe`
  `readlink` is refused as `process executable is unreadable`. The shell code
  collapses ENOENT, EACCES, EPERM, and other readlink failures; it does not
  preserve errno.
- A verified empty cmdline with failed exe `readlink` continues. This is the
  approved empty-cmdline rule; PID/zombie status is not guessed.
- If the proc entry disappears during the read, the handler continues that
  entry as an exit race. This is the precise behavior; it is not a refusal or
  proof of safety for a still-live process. The author summary’s
  “fail-closed/unknown” wording is inconsistent with its fixture and source;
  the handoff’s “continues” wording is the accurate description, with the
  limitation that the process was observed to disappear.
- An unavailable proc root is refused. A PID absent from the proc glob is
  unobserved, not a refusal.
- A readable executable/reference to a candidate is refused. The handler also
  checks cwd and open-file links; no target reference is permitted through
  those paths.

## Nine private cases

Command:

`PYTHONDONTWRITEBYTECODE=1 python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-retire-process-diagnosis-1824/private/proc_fixture_diagnosis.py`

Exit: **0**. The nine cases all emitted metadata only: non-empty ENOENT,
EACCES, EPERM; exit race; empty-cmdline deleted-exe and zombie-like cases;
hidden proc root; invisible PID; and readable target reference. No command
arguments, actual cmdline contents, executable paths, or credentials were
printed. The fixture has no removal/retry operation and its branch outcomes
match the installed source above; it is not evidence of the remote host.

## Checks

- `bash -n .../bin/retire-child-venv`: exit **0**
- `bash -n .../bin/request-retire-venv`: exit **0**
- `git diff --check`: exit **0**
- `git status --porcelain`: empty, exit **0**

No production state, guard, queue, target, retry, provision, host tool,
daemon, product test, generated file, pin, or branch/ref was changed. No live
`/proc` probe or retirement request was run. The existing
`request-retire-venv -> RETIREVENV -> handler` caller and C0 v2 shapes remain
untouched.

## Minimum remote HOST need

An authorized remote HOST execution must provide one bounded, read-only,
failure-only observation of the first failing PID: proc namespace and mount
visibility, errno from the exe-read attempt, whether the PID exists after the
attempt (race), and cmdline empty boolean/length only. It must not print
cmdline contents, executable paths/contents, arguments, credentials, or
credential-file data; it must stop on permission denial and never remove,
retry, chmod, or continue around a denial. Until that exact command and its
safe output are retained, the remote cause and cleanup qualification are
unproven.

