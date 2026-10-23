# Runtime handoff: OPS-retire-process review

## FAIL — missing diagnostic evidence

The independent review confirms the installed source diagnosis and all nine
private fixture branches, but the required read-only HOST diagnostic cannot be
qualified. The author’s final report does not contain the command it claims to
contain, and the author log retains no verbatim command bytes. Consequently no
exact command or hash can be exported; no replacement is invented.

The local source result is limited to this: for a present non-empty-cmdline
process, any failed `/proc/<pid>/exe` readlink collapses to
`process executable is unreadable`; verified empty cmdline continues on exe
failure; an entry disappearing during the read continues as an exit race;
hidden proc root refuses; absent glob entries are unobserved; readable target
references refuse. The author summary’s “fail-closed/unknown” exit-race phrase
is inaccurate; the source and fixture say “continue,” with the process
disappearance limitation. Handler hash is
`954d5d87fe2e6fcf42b34953ec0edc519a2eb97ade8f66f0f2f96f523516b791`; request
hash is `21f61833a6718794ab2a06a3a96d34ca58c050ccd0151622e16866ac78758139`.

Fresh fixture exit 0; handler/request `bash -n` exits 0; Runtime
`git diff --check` exits 0 and status is clean. No production or host state
changed. The nine App2 refusals remain remote-cause-unknown and do not qualify
retirement.

Minimum remote need: one retained, bounded, read-only HOST observation of the
first failing PID with proc namespace/mount visibility, exe-read errno,
post-attempt existence/race, and cmdline empty boolean/length only. It must
disclose no cmdline contents, executable paths/contents, arguments,
credentials, or credential files; stop on permission denial; and perform no
removal, retry, chmod, or alternate cleanup.

