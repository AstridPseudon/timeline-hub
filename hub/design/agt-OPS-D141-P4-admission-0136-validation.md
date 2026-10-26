# D141c P4 admission validation

## Commands and results

- `bash -n ops-d141-p4-admission/test-run` — PASS.
- `bash -n ops-d141-p4-admission/admission-controls.sh` — PASS.
- `git diff --check` — PASS.
- `TMPBASE=/tmp/w-f2006d53ee/control-run-02 ops-d141-p4-admission/admission-controls.sh ops-d141-p4-admission/test-run d141c-candidate-02` — PASS; exit 0, `central_body_invoked=false`.

The control used the actual candidate, a private temporary ORCH tree, genuine request variables for the controlled suite cases, a read-only Agent integration worktree for the candidate's normal tree calculation, and only stubbed `df` and `setsid`. No production request, body, live queue mutation, or `--run` route was invoked.

Exact control output:

```text
label=d141c-candidate-02
root=/tmp/w-f2006d53ee/control-run-02/test-run-controls.l3B9fE
central_body_invoked=false
p4-at-floor rc=0 expected=0 setsid_calls=1
p4-below-floor rc=3 expected=3 setsid_calls=0
light-at-floor rc=0 expected=0 setsid_calls=1
other-heavy-at-floor rc=3 expected=3 setsid_calls=0
other-heavy-above-floor rc=0 expected=0 setsid_calls=1
core-at-floor rc=0 expected=0 setsid_calls=1
core-below-floor rc=3 expected=3 setsid_calls=0
global-guard rc=3 expected=3 setsid_calls=0
invalid-disk rc=3 expected=3 setsid_calls=0
unreadable-disk rc=3 expected=3 setsid_calls=0
p4-while-other-heavy-busy rc=3 expected=3 setsid_calls=0
other-heavy-while-p4-slot-busy rc=3 expected=3 setsid_calls=0
```

The accepted cases each recorded one stubbed launch and a `running` admission marker; refusals recorded zero launch calls and a `why` marker. Heavy accepted cases, including the named P4 row, also recorded the heavy marker. The same controls must be rerun by an independent review worker before separate CAS installation and publication.
