# D127c protected review — FAIL

## D127C-F1 — repeated and non-element-only profiling selection

`_is_element_request()` returns true when *any* command has `op ==
clip.set-element` (helper lines 472-476). It neither requires the request to
contain exactly one command nor records a first matching request. Every
eligible handler entry calls `_start_profile()` (lines 1207-1209), so a second
element POST or an element command mixed with another command is profiled too.
An offline two-dispatch probe produced two captured cProfile summaries. This
does not satisfy the required one element-only first-POST and deterministic
first/retry selection rule.

## D127C-F2 — raw-pstats parent is not safely private

`_raw_profile_path()` resolves the parent and then accepts any parent inside
`TMPDIR`, including the TMPDIR itself or a symlinked directory that resolves
inside it. It calls `mkdir(..., exist_ok=True)` and `chmod(parent, 0700)` on
that existing parent (lines 572-576). The final file uses `O_EXCL`, but the
parent is not required to be a newly created dedicated private directory.
This fails the no-symlink/unsafe-path and private-parent requirement.

## D127C-F3 — partial enable can leak the profile binding

`_start_profile()` catches an `enable()` exception and marks the profile
failed, but does not restore `profile_previous` or disable a profiler that was
partially installed (lines 487-493). A focused injected-profile probe whose
`enable()` installs a profile and then raises left `sys.getprofile()` set.
The normal return/exception path has cleanup, but the required try/finally
binding guarantee is absent for observer failure.

## D127C-F4 — required negative controls are incomplete

The new tests cover one matching request, a non-element command, dry-run, a
handler exception, projection row shapes, and file modes. They do not cover
wrong suite/request/path/method, an unselected handler, symlink/overwrite
rejection, profile byte bounds, or exact caller-edge counts as required by the
brief.

## D127C-F5 — requested scoped type checks are not qualified

Ruff, compile, and diff checks pass. Pyright reports two new
`Stats.stats` attribute errors at helper lines 606 and 639. The direct mypy
run also reports those two errors, along with the repository's existing broad
baseline errors and missing test/dependency stubs. The author evidence reports
no mypy or Pyright run.
