# P4 ten-note operational read-only prep

## Result

READY for the existing `p4-v2-http-nodes` service as a one-test collection
selector; no HTTP test body was run in this prep.

Exact selector:

```text
tests/editing_conformance/test_p4_ten_note_v2_runtime.py::test_http_ten_note_commit_per_step_inverse_and_redo
```

The assigned checkout is exact and clean before this report:

- commit `9b658b28c3a7bc3ebda3ad5a7b5b417d78553720`
- tree `84bd8ef3429c06ced18c0639388be8b2c8ecd030`
- no product/test branch delta

The six reviewed P4 source blobs match
`hub/design/agent-P4-six-final-review-0449.md` exactly:

| Path | Blob |
| --- | --- |
| `tests/sdk/test_p4_commit_v2.py` | `85218e8e99a1c7602d2b7ee399f3847fac759186` |
| `tests/sdk/test_p4_ten_note_provider.py` | `1ed257c4604552793d2eaabfc117babe93c5b445` |
| `tests/sdk/test_p4_note_rerun.py` | `80c15e2944b5660a18077aa38f84cf3b3ced09bb` |
| `tests/sdk/test_p4_cli_sheet_v2.py` | `fd248182a0e1c120fa6440994da545c4e13219ad` |
| `tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py` | `05f7aa2bd862fc608ee17515d373c5f5b47c27eb` |
| `tests/editing_conformance/test_p4_ten_note_v2_runtime.py` | `5ee8dd5b863c164e0ea5f03257ac61849a425061` |

## Evidence

- Exact one-test collection, with the shared Runtime checkout available:
  `PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-app2-native/bin/python -m pytest -q -o addopts= -p no:cacheprovider --collect-only tests/editing_conformance/test_p4_ten_note_v2_runtime.py::test_http_ten_note_commit_per_step_inverse_and_redo`
  -> **1 test collected**. No body executed and no HTTP request was credited.
- Scoped Ruff:
  `ruff check --config pyproject.toml tests/editing_conformance/test_p4_ten_note_v2_runtime.py tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py tests/helpers/trusted_seed.py tests/sdk/test_p4_cli_sheet_v2.py tests/sdk/test_p4_commit_v2.py tests/sdk/test_p4_note_rerun.py tests/sdk/test_p4_ten_note_provider.py`
  -> **All checks passed**.
- Private mypy source scope:
  `mypy --config-file pyproject.toml --no-incremental astrid/sdk/timeline/commit.py astrid/sdk/timeline/commit_session.py astrid/sdk/timeline/emitter.py astrid/sdk/timeline/sync.py`
  -> **Success: no issues found in 4 source files**.
- `git diff --check HEAD` -> **pass** after adding only this report and the
  requested handoff document.

The locked Agent `runtime.lock.json` pins Runtime source
`34eac0041b0891e9011966b39bcbd26053fde5bc`; the test fixture calls
`use_runtime(vendored_runtime_commit())`, so actual execution will use that
locked source rather than the current sibling checkout HEAD.

## Public undo and preserved behavior

`TimelineSession.open` is the normal session entry point, and
`TimelineSession.undo` accepts the v2 `steps={publication_id: [step_id]}`
selector and emits `timeline.inverse` through the outbox. The public
`Timeline.undo` facade forwards accepted-publication undo to that session.
The existing ten-note test therefore retains the intended one commit, ten
steps, per-step inverse/redo, mirror equality, unchanged authored closure,
show/history readback, and restart assertions. No test outcome or original
fixture was changed.

## Genesis/setup finding for the manager

There is one concrete setup mismatch against the earlier first-single-HTTP
source at commit `5108aaf1438b52be17d5346e04f3dcb590a892b7`:

- the single-HTTP seed compiles `initial_bundle()` with
  `compile_authoring_candidate(...)` and adds the required canonical empty
  `registry={}` envelope;
- the ten-note seed uses `document_fixture(shared=True)`, manually adds empty
  `p4_note` objects in both mirrored clips, and does not compile the fixture
  or add `registry={}`.

This makes the ten-note genesis potentially stale for derived occurrences and
the Runtime-managed registry envelope. Genesis likely needs manager-owned
correction before body execution if the two tests are required to share the
same canonical seed contract. The ten-note commit body, commands, steps,
reads, merge mode, keys, and preservation assertions remain untouched; the
correction belongs in seed/setup coordination, not in this worker's product
or original-test files.

No full suite, review-of-review, unrelated ancestry, new launcher/marker, or
actual HTTP service execution was performed.
