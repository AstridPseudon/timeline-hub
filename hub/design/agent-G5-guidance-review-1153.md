# Independent Luna G5 guidance review

## Result

**FAIL — draft-only; do not integrate until the original P1 GO.**

Reviewed `tl/agt-G5-guidance-return-1145/e1dbde787937792b1270e1d2444f068f9fc0ca41`
against `086db31e4c2b565dd891740c1c599ad6abb3dc34`, using the settled PLAN
G3/G5 scope and C0 §§1–5. The candidate is a bounded one-file diff in
`astrid/packs/timeline/cli.py` (8 additions, 7 removals), and it does not add
control flow, providers, writers, tests, generated files, pins, or contract
changes. The guidance replacement is not merge-ready because two of the new
routes are not valid end-to-end `apply` continuations and stale executable
`publish` guidance remains in the same file.

## Findings

### F1 — the navigation `apply` command uses a JSON checkout as a sheet

`_editing_navigation()` continues to issue:

```text
python3 -m astrid.packs.rendering.docs.scripts.timeline_document checkout ... --file /tmp/timeline-edit.json
```

That checkout writes a JSON authoring bundle (`timeline_document.py:checkout`
calls `dump(args.file, candidate)`). The changed continuation then issues:

```text
python3 -m astrid timelines apply <timeline> --project <project> /tmp/timeline-edit.json
```

The real `timelines apply` handler reads `sheet_file` and calls
`astrid.sdk.timeline_sheet.parse_sheet(text)`, which accepts the human cut-sheet
grammar, not the JSON checkout document. The command therefore parses at the
argparse level but is not a supported working command after the preceding
checkout/edit/check steps. The guidance's `workflow` value (`checkout, edit,
check, apply`) describes a path that cannot consume its own file.

Relevant candidate lines: `cli.py:1209`, `cli.py:1221–1234`.
Relevant implementation: `cli.py:3496–3505` and
`astrid/sdk/timeline_sheet.py:310`.

### F2 — the local-file edit continuation misuses and does not quote `target`

In the `parsed.file` branch, `target` is the local draft path. The changed
message renders it as the positional `ref` of `timelines apply`:

```text
timelines apply {target} --project {project} <sheet-file>
```

The real parser accepts a positional ref and a sheet path, but it does not have
a `--file` mode for this command; `_cmd_apply` consequently treats the draft
path as a timeline ref and then looks for a working copy under that ref. A
draft path is not a timeline ref. In addition, the interpolated target is not
shell-quoted. A parser smoke with `/tmp/draft with space.json` exits 2 because
`space.json` becomes an extra argument. This fails the requested source
context/path-quoting check even though the no-space form is syntactically
accepted.

Relevant candidate lines: `cli.py:3228–3241`; the source assignment is
`target = parsed.file` at `cli.py:3187`.

### F3 — stale executable `publish` guidance remains in `cli.py`

The candidate removes the three `publish` strings in its diff, but two
executable workflow epilogs in the same owned file still say:

- `cli.py:2311`: `checkout → edit → check → publish`
- `cli.py:2490`: `checkout → edit → check → publish`

They are emitted by the `show`/`visualize` help paths and violate the explicit
“no stale executable publish guidance” requirement. This is within the allowed
guidance-only file scope, not an unrelated product route.

### F4 — an existing behavior test fails on the intentional guidance change

The neighboring targeted test
`tests/v10/test_domain_cli_projects_timelines.py::test_timeline_navigation_preserves_resolved_scope_and_editing_resources`
fails at line 1132 because it still expects the established workflow list to
end in `publish`, while the candidate returns `apply`. The exact requested
author suite passes, but this existing behavior test is not preserved. No test
edit was made (and test edits are out of scope); the candidate needs an
orchestrator decision about the required expectation/xfail treatment before
integration. The repository rule forbids silently encoding the changed
behavior by weakening or deleting this test.

## Verification

### Passed

- Exact author suite (16 cases):

  ```text
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTEST_ADDOPTS= /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/agt-G5-guidance-review-1153-testtmp tests/sdk/test_scene_save_core.py
  ```

  Result: `16 passed in 4.01s`.

- Real parser smoke using `cli.build_parser(None)` and `shlex.split`:
  quoted project/ref values in the navigation helper preserve
  `project 17`, `timeline main`, and `/tmp/timeline-edit.json`; the supported
  ref/project/sheet form parses successfully; the target-none edit follow-up
  parses successfully.
- `git diff --check` against the requested base: passed.
- Candidate diff file scope: exactly `astrid/packs/timeline/cli.py`; the diff
  contains only the guidance literals described above, with no control-flow or
  unrelated delta.

### Baselines / failures recorded

- Scoped Ruff:

  ```text
  RUFF_CACHE_DIR=/tmp/agt-G5-guidance-review-1153-ruff /home/user/work/venv-agent/bin/python -m ruff check astrid/packs/timeline/cli.py
  ```

  Exit 1 with 15 diagnostics. Comparing the candidate output with Ruff on the
  base file via stdin gives the same 15 diagnostic identities; none is on a
  changed guidance line. This is the inherited Ruff15 baseline, not a new
  candidate lint error.
- Private scoped mypy:

  ```text
  MYPY_CACHE_DIR=/tmp/agt-G5-guidance-review-1153-mypy /home/user/work/venv-agent/bin/python -m mypy --cache-dir=/tmp/agt-G5-guidance-review-1153-mypy --no-incremental astrid/packs/timeline/cli.py
  ```

  Exit 1 with 81 existing errors in this module; none is at a changed guidance
  expression. No type-relevant code changed.
- Neighboring targeted test:

  ```text
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTEST_ADDOPTS= /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/agt-G5-guidance-review-1153-v10tmp tests/v10/test_domain_cli_projects_timelines.py -k timeline_navigation_preserves_resolved_scope_and_editing_resources
  ```

  Exit 1: `1 failed, 96 deselected`; failure is the `publish` versus `apply`
  workflow assertion at line 1132.

No full, browser, HTTP/socket, native14, P1/P4, original58, D17, dependency
install, or host-daemon suite was run or requested. No Git mutation was made.

## C0 / G3 / G5 impact

The diff does not touch request/reply fields, command payloads, labels, steps,
reads, merge modes, dry-run behavior, source/rationale/group IDs, or accepted /
merged / conflict / invalid / preview result structures. Thus the C0 §§1–5
wire and persistence requirements are unchanged. The failure is entirely in
the user-facing continuation strings that the production CLI caller emits.

## Recommended next steps

1. Decide whether this navigation is meant to be a JSON checkout workflow or
   a cut-sheet workflow. If it is JSON, do not advertise that JSON file as the
   `apply` sheet. If it is a sheet workflow, source the file from
   `timelines show <ref> --as sheet` and keep the `apply <ref> --project P
   <sheet>` command tied to that sheet.
2. Do not put a local draft path in the `apply` ref slot. Emit a real timeline
   ref, or state that the detached file mode has no direct `apply` continuation;
   quote any actual path/ref values that are inserted into shell commands.
3. Remove/refresh the two remaining `publish` epilogs in `cli.py` and resolve
   the neighboring test expectation under the repository's expected-to-fail
   rule before requesting another review.

