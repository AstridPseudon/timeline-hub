# Agent short-attempt current-port review

## Verdict: APPROVE

Reviewed the exact committed `tl/agt-m3-short-attempt-current-port` at
`21e84b7d0d39f9d0b0cf97eaeac62aa7cebb37f8` against base `f82da322`.
This is the requested three-file delta only:

- `astrid/core/execution/generic_host.py`
- `astrid/packs/rendering/rendering/renderers/remotion/root_preparation.py`
- `tests/packs/rendering/test_remotion_attempt_temp.py`

No executable defect was found in the requested process/storage-custody
scope.

## Scope findings

- Ephemeral roots retain the `astrid-attempt-` reclaim prefix while removing
  task/attempt identity from the basename; `mkdtemp` plus explicit `chmod`
  keeps the host-created root mode `0700`.
- Explicit `attempt_base` allocation remains collision-refusing and now also
  creates each child mode `0700`. The existing child-name identity is not
  changed.
- Managed Remotion scratch uses `.r-*` only after the internal invocation,
  exact progress-marker name, owner-only attempt directory, symlink-free
  ancestry, direct staging-child, and output-under-`attempt/outputs` checks
  all pass. Foreign progress/staging paths fall back to the existing longer
  workspace path.
- `.r-*` files remain inside the attempt tree, so existing live/final storage
  walks and evidence accounting charge their bytes. The diagnostic classifier
  labels them as renderer workspace.
- `TemporaryDirectory`/`ExitStack` removes the `.r-*` directory; the existing
  attempt cleanup either deletes the owned root and verifies absence or
  retains/latches uncertainty. Symlinked roots are refused by the existing
  cleanup behavior rather than recursively followed.
- The strict `RenderRequest.verified_source` implementation and source tests
  are byte-identical to `f82da322`; no source-custody regression was repeated
  from the cumulative `973c082e` endpoint.

## Evidence

Commands run in the review worktree:

```text
git diff --name-status f82da322..HEAD
  M astrid/core/execution/generic_host.py
  M astrid/packs/rendering/rendering/renderers/remotion/root_preparation.py
  A tests/packs/rendering/test_remotion_attempt_temp.py

git diff --check f82da322..HEAD
  pass

for p in astrid/core/rendering/contracts.py astrid/core/rendering/service.py \
  tests/packs/rendering/test_verified_source.py tests/sdk/test_capture_source_runtime.py; do
  git diff --quiet f82da322 HEAD -- "$p" && echo "UNCHANGED $p"
done
  all four reported UNCHANGED

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python \
  -m pytest -q -p no:cacheprovider \
  tests/core/test_generic_host_attempt_isolation.py::test_attempt_base_rejects_reused_child
  1 passed in 0.63s
```

The task supplied the completed focused evidence of `71+6` targeted tests;
those suites were not rerun here per the instruction to run at most one
precise counterexample. No browser, MP4, full suite, pin, DTO, or product
qualification was run.

## Decision and next step

Approve this exact port for integration. Retain the separate limitation that
the pathname checks are not an atomic defense against a concurrent same-UID
rename/symlink race; no such race is introduced by this delta or required by
the reviewed admitted-host path. Browser/MP4 qualification remains a separate
gate.
