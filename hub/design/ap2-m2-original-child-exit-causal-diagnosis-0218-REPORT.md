# Historical 4657 child-exit diagnosis

## Result

I could not identify a real first status overwrite in the retained evidence.
The old `if flock ...; then ... else status=$?; fi` handoff is not, by
itself, a demonstrated loss point. A process-only reproduction of that exact
old path returned the injected nonzero child status through the original
post-steps, EXIT cleanup, and central runner envelope.

This means the historical 4657 loss cannot honestly be attributed to the old
conditional handoff or to central finalization from the available record. The
missing evidence is the actual child exit code and the wrapper's final exit
code from 4657. Its retained `runner.log` is empty and its disposable wrapper
run root, including the trace and error-context files named in the log, is no
longer available.

## Historical inputs

The retained request is:

```text
target=ap2-m2-bootstrap-current95-existing-driver-gate-0104
repo=app
suite=normal014-integration-e2e-gate5
files=''
nocache=0
requested=2026-10-21T01:10:23Z
```

The exact suite command recorded in the retained summary was:

```sh
bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-app-central.sh run "$PWD"
```

The original retained metadata was `orig-status=pass` and `orig-exit=0`.
The retained Playwright log says `1 failed` and `1 passed`; the failure was a
90-second wait for the created-project response. The result was later marked
withdrawn because of this exit/log mismatch. No historical result file was
changed by this worker.

The old wrapper body is preserved as a diff in the 0154 worker log at lines
12862-12867. Its child handoff was exactly:

```sh
if flock -w 600 /home/user/work/.app-m1-browser.lock \
  node node_modules/playwright/cli.js test --config playwright.three-products.config.ts \
  --grep "^${normal014_required_case}$"; then
  normal014_exit_status=0
else
  normal014_exit_status=$?
fi
```

There was no pipe or `eval` around this child command. The 0154 diff shows
that the later change added an unconditional invocation, immediate capture and
logging, but did not show an observed old child code of 1.

## Process-only reproduction

I ran a shell-only reproduction in a private `/tmp` directory. It used:

- `flock` with a child that writes `child-started` and exits 7;
- the old conditional handoff above;
- the original successful structured-verdict post-step shape;
- the original cleanup function, including `rm -rf ... || :` and returning its
  incoming status through `trap 'normal014_cleanup_run_root "$?"' EXIT`;
- the central runner envelope used by `bin/test-run`: subshell, `cd`,
  `timeout -k 60 90m`, `nice -n 5`, and `bash -c "$CMD"`, followed by RC-to-
  status derivation.

Observed output:

```text
trace=child-started|verdict post-step succeeded|
central_rc=7
central_status=fail
run_root_exists_after_exit=no
```

Thus the old conditional itself preserved the injected nonzero status. The
cleanup post-step also preserved it. This is causal evidence against treating
the `if/else` alone as the historical overwrite.

## Finalization comparison

The current retained `bin/test-run` path records the wrapper envelope RC at
`bin/test-run:43` and derives `ST` from that saved `RC` at `:45`; worktree
cleanup at `:44` occurs after the RC is saved. The result summary and
`status`/`exit` files are then written from those saved values at `:46-47` and
`:53`. The later exit/log mismatch guard at `:48-51` is an integrity warning
and was not present when 4657 was accepted; it is not evidence of the original
swallow point.

The common cleanup code currently uses distinct `normal014_status` and
`normal014_exit_status` variables, returns the incoming trap status, and does
not overwrite the wrapper's status. The old wrapper's explicit final
`exit "$normal014_exit_status"` was retained outside the changed handoff.

## Smallest correction recommendation

Keep the immediate child-status capture and explicit final-status return from
the 0154 wrapper change as the smallest defensible hardening/observability
correction. It makes the child RC visible before verdict and cleanup and
prevents future ambiguity. Do not describe it as a proven repair of 4657's
historical first overwrite: this reproduction shows the old conditional path
already returns a nonzero child status when the child actually exits nonzero.

For a causal attribution of 4657, the runner would need retained, per-run
values for child RC, wrapper RC immediately before EXIT cleanup, and central
RC immediately after `bash -c`; the historical retained files do not contain
those values. No browser, socket, central suite, negative3198 rerun, product
edit, bin/test-run edit, or historical result rewrite was performed.

## Checks

- Process-only old-path reproduction described above: PASS; injected child 7
  reached central RC 7 and cleanup completed.
- `sh -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-app-central.sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-source-common.sh`: PASS.
- `bash -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/test-run`: PASS.
- App worktree `git status --short --branch`: clean; no repository files were
  changed.

