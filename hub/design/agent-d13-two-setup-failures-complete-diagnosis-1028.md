# D13 setup-failure diagnosis

## Result

The corrected fixture is ready for a later, separately authorized run. This
worker did not invoke the launcher, daemon, HTTP, browser, renderer, native
body, install, full suite, or central test service.

The source under review is Agent `HEAD` `89b35c9819e0c3c02a8040e0127980bc41cd1db6`
(tree `35b058912b678792d8533c63a295c12932cd859a`) plus the uncommitted
fixture-only patch SHA-256
`f0a092a6f398bd05c7cef02ddcdfbd72b2e2362ba2bcce34d55ea047834d5920`.
Only `tests/packs/video_editing/test_runtime_publication_chain.py` changed.
No product, proof-body, profile/binding, Runtime target, or authority source
changed.

## Exact classifications

1. Failure `17897` is an environment/fixture failure. The exact trace stops
   in `installed_runtime` at `path.mkdir()` for
   `/tmp/d13-JqFX4P/pytest/test_daemon_backed_host_execut0/home`; that path
   already existed. No Runtime command was launched and no product assertion
   ran. The fixture incorrectly placed controller state below pytest-owned
   `tmp_path` and used strict creation against a directory owned by the test
   environment.

2. Failure `2289` is an environment/fixture failure exposing an intended
   product contract, not a product defect. After the first repair, the exact
   trace shows the fixture created every child of its private controller root,
   including `realm`, then invoked `workspace create`. The installed Runtime
   returned `fresh realm creation requires a new root` before launcher or body
   admission. The Runtime refusal is correct: the fixture must leave the
   fresh realm root absent; it must not use `exist_ok=True` or weaken the
   fresh-root check.

Both failures are therefore fixture/environment before native admission. No
product failure is evidenced by either trace.

## Corrected setup contract

The aggregate preflight and the native fixture now use the same layout:

| Path | Before `workspace create` | Owner |
| --- | --- | --- |
| private `mkdtemp` controller root | existing, unique, outside pytest `tmp_path` | fixture |
| `runtime-support` | existing strict-created regular directory | fixture / Runtime data root |
| `home` | existing strict-created regular directory | fixture via `HOME` |
| `tmp` | existing strict-created regular directory | fixture via `TMPDIR` and `XDG_RUNTIME_DIR` |
| `realm` | **absent** | Runtime `workspace create` |

All four are direct children of the private controller root and are checked
for distinctness and symlink-free directory identity. The preflight creates
only the three controller directories and explicitly reports a pre-created
realm as a setup failure. The fixture repeats the same invariant immediately
before its unchanged CLI call.

The unchanged create argv is:

```text
astrid-runtime workspace create --profile astrid --source-manifest <profile>
  --data-root <runtime-support> --realm-root <realm> --hosted-origin off --json
```

The unchanged follow-up argv is:

```text
astrid-runtime up --profile astrid --source-manifest <profile>
  --data-root <runtime-support> --hosted-origin https://astrid.local
  --door-port 0 --wait --json
```

The fixture runs both with absolute paths and with `cwd` set to the private
controller root. It supplies the selected installed Runtime/Agent profile,
pack source, Remotion project and lock, browser, Node, Node modules, ffmpeg,
and ffprobe through the existing environment contract. It does not set
ambient `PYTHONPATH`; the existing `ASTRID_TIMELINE_SCHEMA_PYTHONPATH` value
remains the reviewed source carrier.

## Prerequisites through first native admission

The existing preflight still requires all of the following, in order:

* the four-field `astrid` profile is a regular non-symlink file;
* the seven existing manager binding values are present, with full Agent
  commit/tree IDs and SHA-256 resource digests;
* selected `source_checkout` and `runtime_checkout` resolve to the expected
  same installed tree, with the expected source digest;
* selected `runtime_environment` is an absolute non-symlink directory, its
  interpreter is regular/non-symlink, and it is the interpreter running the
  test;
* all eight required installed module origins resolve inside the selected
  tree; wheel members, RECORD rows, installed bytes, and Git source archive
  remain exact;
* Node, Remotion lock, browser, ffmpeg, and ffprobe are regular non-symlink
  files with the manager-selected bytes; the Remotion project and node_modules
  are regular directories; font provenance and non-empty font files exist;
* the pytest-owned attempt root is private and writable, the separate
  controller root is writable, and at least 5 GiB is free;
* only after `workspace create` creates the realm may `up` issue the generated
  worker/owner credential paths and endpoint; the fixture then reads the worker
  token and opens the owner client with the returned endpoint, realm ID, and
  actor ID;
* only after those lifecycle and auth steps does the unchanged test proceed to
  host discovery, capability admission, task admission, and the native target
  body. None of those stages ran here.

## Tests and limits

Passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/packs/video_editing/test_runtime_publication_chain.py \
  -k 'd13_controller or d13_explicit_bindings or d13_record_member'
10 passed, 5 deselected in 0.99s

ruff check tests/packs/video_editing/test_runtime_publication_chain.py
All checks passed

git diff --check
passed
```

The broader non-integration selection was also inspected but is not a clean
qualification result because its installed-profile test requires the manager's
external D13 environment: `11 passed, 2 deselected, 1 xfailed, 1 failed`,
with the one failure listing missing `ASTRID_D13_*`/tool/profile inputs before
any Runtime command. No retry was made.

Remaining decision/prerequisite: the orchestrator may decide whether to queue
one later D13 native run after reviewing this correction and provisioning the
already-approved installed profile/bindings and tool environment. This report
does not claim native, launcher, HTTP, browser, renderer, or proof-body
qualification.
