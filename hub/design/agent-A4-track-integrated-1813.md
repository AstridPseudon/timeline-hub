# A4 integrated track `doc.patch` qualification — bounded PASS

Date: 2026-10-23

## Verdict and scope

The current integrated Agent tree at `1962a2413095a2f82bf927e7c42c532072b5c812`
passes the requested nine-case A4 track witness. This is a bounded qualification
of the registered generic `doc.patch` / `list.move` provider path. It is not a
whole A4 or mounted-App qualification.

The plan was read first and no settled decision was changed. The witness keeps
the current production shape: App A2's `localSaveSession` persists a generic
`doc.patch`; no `track.reorder` provider was invented or revived.

## Source identity and exactness

| item | identity |
| --- | --- |
| Agent commit | `1962a2413095a2f82bf927e7c42c532072b5c812` |
| Agent tree | `fb572dec36c1a55eebf52dad71470a339207ba5d` |
| Runtime checkout | `/home/user/work/wt/rt-pin-2a9e347f` |
| Runtime commit / tree | `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d` / `f79a2355cfb39d9ada7721978bd20d5702105778` |
| Integrated witness Git blob | `ca046a721d527a1f6bf383659b8b5bbaada4d13d` |
| Integrated witness SHA-256 | `fa9aa1ce49e3acab4fda0be91f62ad6c3f98b704b3b063c4c7450d6febeff546` |
| Reviewed witness commit | `4010f98760b43e2320f6207bc1f59789bf636b21` |
| Reviewed witness blob | `ca046a721d527a1f6bf383659b8b5bbaada4d13d` (exact match) |

The reviewed source-quality result was reused because the witness blob is
identical. The scoped checks were also rerun below.

The App donor is read-only frozen commit `68594c668`. The exact relevant App
blobs remain the reviewed values:

- `documentPatchIntent.ts`: `5e1b1d1e2cd95ac7e402daf0ac9f4f4cf1ec606f`
- `localSaveSession.ts`: `83d2166d57c05980d3bd8ebc9bbd79a37c3c5e44`
- `trackReorderCapture.ts`: `81ec771ab972da61654b96e45caa9506e8a797e7`
- `commands/fixtures/recipe_m2_app_track_label.json`: `b79b69f9a95b8df417c7b157f0db92eb803535e3`

The Agent fixture has the same Git blob and content SHA-256
`5aa9aed23a9764e4a9fb0d56fd5efc47368711933adbfaa224f2f725a766ed00`.

## Exact evidence

Command, run directly from the Agent worktree:

```text
timeout 300s env PYTHONDONTWRITEBYTECODE=1 \
  ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2a9e347f \
  PYTHONPATH=.:/home/user/work/wt/rt-pin-2a9e347f \
  /home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= \
  -pno:cacheprovider --timeout=15 \
  tests/editing_conformance/test_a4_track_doc_patch_witness.py
```

Result: `9 passed in 2.43s`.

Scoped quality checks:

```text
/home/user/work/venv-agent/bin/ruff check --no-cache --isolated \
  --select E4,E7,E9,F,I,BLE \
  tests/editing_conformance/test_a4_track_doc_patch_witness.py
All checks passed!

/home/user/work/venv-agent/bin/mypy --no-incremental --follow-imports=skip \
  --ignore-missing-imports \
  tests/editing_conformance/test_a4_track_doc_patch_witness.py
Success: no issues found in 1 source file
```

Actual module origins under the test environment were checked. The witness,
its Agent helpers, and provider fixtures all resolve under this worktree;
`runtime_protocol` resolves under the pinned Runtime checkout; only `pytest`
comes from the shared venv site-packages. No borrowed Agent source was loaded.

## Covered behavior

The nine collected cases cover:

- generic `doc.patch` `list.move` with raw row preservation;
- explicit `null`, `false`, `0`, nested opaque data, and untouched neighbors;
- detached source immutability and JSON replay;
- declared collection membership/order reads;
- stale order and membership refusal, including order ABA where the final order
  returns to base;
- exact previous-value and missing-anchor refusal before mutation;
- duplicate identity and forged/occupied `created` refusal;
- dry-run preview with unchanged head and null receipt;
- accepted provider persistence of label, merge mode, step patch, reads,
  command shape, canonical output, and empty created claims; and
- a disjoint neighbor-field change merging with the reorder.

## Registry, hashes, and cleanliness

The current production operation registry has 31 entries, including
`doc.patch`, and no `track.reorder` or `transcript.associate` entry. The
`commands.py` blob is `9858390bbced10eb2ca1112dcbd16d092a12c34f5a3eebcf2ed218fe087ff6a2`
and the schema blob is
`d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`. Both
Git blobs are identical before/after the integrated merge (`commands.py`
`d349ebd4…`; schema `de301d13…`), so the production registry and schema were
preserved outside the test witness.

`git diff --check` is clean. The integrated merge diff against its first
parent is exactly one added file:
`tests/editing_conformance/test_a4_track_doc_patch_witness.py`. The worktree,
Runtime pin, and frozen App checkout were clean. No source, production test,
Git ref, App, Runtime, pin, environment, daemon, vendor, artifact, deletion,
or unrelated original was written. Bytecode and pytest cache writes were
disabled.

A credential-looking literal scan of the changed witness found no matches.
The designated worker `tmpdir` was an existing regular file, so a local test
log could not be written there; the console result above is the authoritative
run output. This did not block qualification or alter any repository.

## Explicit limits / non-claims

This report does not claim mounted HTTP/live Runtime/browser execution, full C0
request/reply coverage, history or undo coverage, whole-A4 parity, or P1/P4.
It does not claim the dormant App `track.reorder` envelope or that the App hook
executed this exact patch at runtime. Full C0 behavior remains covered by its
existing suites; this witness only asserts the relevant existing detached
provider records and replies. No full suite, browser, HTTP, native, or broad
test run was performed or requested.
