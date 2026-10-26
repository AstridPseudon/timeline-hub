# D141y validation

Verdict: **REFUSED_ALL_REPO_PREFLIGHT**. This was one real source-only invocation of the existing delivery-build CLI. No ZIP, publication, install, capture, tests, browser, service, or product authoring occurred.

## Exact invocation

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build --dry-run --source-tuple /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141y-rehearsal-0710/evidence/source-tuple.json --source-tuple-sha 6fe1b04ca64f38cc8a524bc397950df5a6bce835be614341a70e2c163d253c4d --delivery-root /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141y-rehearsal-0710/evidence/delivery --work-root /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141y-rehearsal-0710/evidence/work --template /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/delivery/README.template.md --gate-results /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/delivery/gate-results.md
```

Exit: `2`. Raw stdout, stderr, and exit are retained as `raw-command.stdout`, `raw-command.stderr`, and `raw-command.exit`.

## Actual result

The CLI reported:

```text
all-repository preflight refused:
ancestry refused for app: repo=/home/user/work/app base=fc24f84994dc36cfae9349112782ab4d91dbc73b tip=4de54db14bdc9ddc2ce2e5887258b03acbffd30d
```

Agent, Runtime, and Composition passed identity/clean/ancestor preflight. App failed the ancestor guard. Therefore all four actual build patch counts, tree checks, bundle checks, and apply checks are **NOT_REACHED**; the prospective source-only diff stats in `results.json` are not actual build results.

## Read-only controls

- All four requested source heads and trees matched the tuple and were clean before and after.
- `origin/main` was read as Agent `64197afa…`, Runtime `fa9cd546…`, App `fc24f849…`, Composition `67b8aa3d…`, with full trees recorded in `source-manifest.json`.
- Delivery script, template, and gate hashes were unchanged before/after.
- Disk trace remained above the 4,000,000,000-byte stop line; no ZIP or publication was written.
- Tests, typecheck, lint, browser, service, and full suites: **NOTRUN**.
