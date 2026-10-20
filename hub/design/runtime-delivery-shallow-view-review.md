# Runtime delivery shallow-view review

## Verdict

**APPROVE for installation** of the worker copy
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m4-delivery-shallow-view-script-fix/delivery-build`
over the shared `ORCH/bin/delivery-build`, with the temporary Git configuration guard below
retained for every production run. This review does not approve ZIP creation, publication, a
hard-stop claim, or a changed source tuple/script.

Worker-copy SHA256: `a3e7ab2ba9cd051cc64d5fd3806b4b49b2eb1909f5063968282970ccc91fa34e`.
Shared pre-install SHA256: `cee29952d65b306414c9c5492b6be594a5b47d8a091f307bbb525bc42a4db81e`.
The shared script was not changed by this review.

## Code review

The diff from the shared script is limited to `private_source_view` (lines 71–111) and passing
its returned source into App ancestry/statistics, squash, and bundle creation (lines 217–239).

- The helper is active only for `app` when the source is shallow. It creates a fresh private Git
  repository under the per-run temp directory, writes one `objects/info/alternates` file pointing
  at the source object store, and installs only the pinned `origin/main` and `tl/integration`
  object IDs as local refs.
- It refuses a shallow private view, a private shallow file, any `rev-list --missing=print`
  reachable-object result, a changed tip, or a changed tip tree before squash/bundle generation.
  The missing-object refusal is fail-closed; the synthetic probe from the worker reported
  `private App source view has 1 missing reachable object(s)`.
- The source `.git` and shared object store are read-only inputs. All helper files are beneath
  `tmp/<repo>/source-view`, and the normal per-repo `finally` removes that directory; the outer
  `finally` removes the remaining `tmp-verify/<stamp>` tree. Dry-run staging is intentionally
  retained for inspection; successful non-dry builds remove staging after writing the ZIP, while
  failed builds retain staging for diagnosis.
- The generic path returns the original source repository unchanged when the repo is not the
  shallow App case. The existing ranged, merged-history, unrelated/full-bundle, binary,
  rename/delete, patch-corruption, and source-metadata tests therefore preserve the generic
  four-repo behavior.
- No fetch uses a remote name or URL: squash/verification fetch from the local source path,
  private view, or generated bundle only. No source ref, shallow file, index, replace ref, or
  graft is written.

The App source tuple inspected read-only is:

| identity | value |
|---|---|
| `origin/main` | `860d43b331fb4422b16bc0dbd7b08666a0c766a0` |
| `tl/integration` | `0fa436c7847a2cdb1c2b565dbf7749e1d3ca605b` |
| `tl/integration^{tree}` | `1e3f95a5051e9c2a8871c84d17c65d0af71d189d` |
| shallow boundary | `3f05489e8c5f66870a5401f0aaa5ce6913eb8e11` |

The source is shallow, and its real tip is a merge with parents
`4553d4b8c7a7fdf226b25634660c63da9f0c947a` and
`76be83b1a572360838c5ab0cb925a157ae103b34`. The actual parent object is present. The worker's
private view check found zero missing reachable objects. The prior authorized App-only run
already proved the complete bundle advertised the exact tip and that empty-repository bundle
fetch plus `git am` produced tree `1e3f95a5051e9c2a8871c84d17c65d0af71d189d`; that run was not
repeated here per the brief.

## Tests and configuration review

Ran directly against the worker copy:

```text
PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null \
  DELIVERY_TEST_SCRIPT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m4-delivery-shallow-view-script-fix/delivery-build \
  python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m4-delivery-ref-fix-final-review/test_delivery_final.py
```

Result: **11 passed** in 2.682 seconds. No four-repo or full suite was run. The test fixture's
signing/hooks settings are private to its temporary Git repositories.

The production script itself does not force `commit.gpgsign=false`; `GIT_ENV` inherits ambient
Git configuration. I confirmed that a private generic fixture fails `git am` under
`commit.gpgsign=true` with a signing error, so the approved production invocation must include
`GIT_CONFIG_GLOBAL=/dev/null` (as the prior App-only run did), or an equivalent temporary config
that disables signing and hooks. This is an invocation guard, not a source-repository mutation.
Without that guard, installation is not reproducibly safe in an environment with mandatory
global signing; the exact correction would be to add equivalent per-process temporary config in
`GIT_ENV` and a regression test before using the script without the guard.

Post-test status: assigned Runtime worktree clean; shared script still has SHA256
`cee29952d65b306414c9c5492b6be594a5b47d8a091f307bbb525bc42a4db81e`; no shared install,
source change, external fetch, ZIP, publication, or hard-stop claim was made.

Recommended next step: install the worker copy only after preserving the exact launch guard and
then use the central service for the separately authorized delivery run. Re-qualify if the
script, source heads, or launch environment changes.
