# Independent final gate — currentRoot three-stills preparation

## Decision

**APPROVE the frozen preparation for exactly one manager-granted central capture window.** This is approval of the controller/source/manifest handoff only; it is not a pixel, MP4, Player, audio, Runtime-admission, or Gate 6 claim. No capture grant was created.

Approved frozen inputs:

- Agent revision `4ef1391c2c104d5d11b3a27265035c51be296045`, tree `afb2ed8506a99a088d7be3dbadaf593338d2fb5a`.
- Controller SHA256 `079fa981108214b0dac2d7f1453ae95fc716e2444ae4d6457d3cec538178dc97`.
- Manifest SHA256 `4127d7e25aba66d57862af09a46368004fcda0a95c5c531ae80c0b0ae490dff9`.
- Public12 package, source, generated outputs, replay outputs, dependency graph, six peer files, Node, Chrome tree, fixture, and MAIN reference inputs are bound by the frozen manifest.

The literal central suite command is:

```sh
R=$($ORCH/bin/request-test $WORKER e2e-viewing-current-root-cap-three-stills) && $ORCH/bin/wait-test "$R"
```

Before that command, the manager must create the exact three-line grant in the frozen `COMMAND.md`; this report does not create it.

## Independent checks

Run from the clean Composition worktree `/home/user/work/wt/vw-m3-current-root-cap-independent-gate`:

- Python AST parse of `controller.py`, `replay.py`, and `offline-checks.py`: **PASS**.
- `/tmp/.../workers/vw-m3-current-root-cap-three-stills-prep/node --check render.mjs`: **PASS**.
- Same Node `--check resolve.mjs`: **PASS**.
- `/home/user/work/venv-agent/bin/python -B ...controller.py preflight`: **PASS**, `capture_run=false`, status `OFFLINE_PASS_NOT_CAPTURE_GRANTED`.
- `/home/user/work/venv-agent/bin/python -B ...offline-checks.py`: **PASS** — missing-grant refusal, exact retained three-PNG positive, single-channel +2 accepted, single-channel +3 rejected, and wrong dimensions rejected.

Fresh preflight reported 1,427 source files, 77 public12 members, 21,488 graph entries, unchanged graph/six peers/Node/Chrome hashes, and valid postflight cleanup. Free space was `13,246,996,480` bytes against `12,986,365,667` required; the 10 GiB floor and staging budget passed. The frozen manifest hash was unchanged after rerun.

No browser, renderer, localhost/socket, central test, grant, or full suite was run. No product files, integration worktrees, shared dependencies/caches, or Git refs were modified. Capture-state files (`CAPTURE-GRANT.txt`, `CAPTURE-STARTED`, metadata, comparison, and capture log) remain absent.

## Recommendation

The viewing manager may perform the one central capture procedure in the frozen `COMMAND.md`, after checking the quiet window and exact grant text. Treat any metadata/pixel mismatch as a visible failure; no intended pixel differences are approved.
