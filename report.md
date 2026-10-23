# P4 ten-note seed correction

## Result

Prepared the ten-note Runtime genesis seed from the exact base
`9b658b28c3a7bc3ebda3ad5a7b5b417d78553720` / tree
`84bd8ef3429c06ced18c0639388be8b2c8ecd030`.

The only product/test source delta is
`tests/editing_conformance/test_p4_ten_note_v2_runtime.py`:

- import `compile_authoring_candidate`;
- convert the untouched `document_fixture(shared=True)` plus the empty
  `p4_note` containers with `bundle_from_document`;
- compile the candidate through the normal publication constructor;
- seed the compiled parent/shot/internal closure and add only the normal
  Runtime `registry` default.

The ten-note case data, commit body, commands, steps, inverse/redo assertions,
accepted/merged/refused coverage, private-cache behavior, and all readback,
history, attribution, mirror, opaque/null/absence/order assertions are
unchanged. No product, schema, pin, lock, launcher, helper, or suite files
changed.

## Evidence

- `python -m pytest -q -o addopts= -p no:cacheprovider --collect-only tests/editing_conformance/test_p4_ten_note_v2_runtime.py::test_http_ten_note_commit_per_step_inverse_and_redo`
  — **PASS**, 1 test collected. The environment emitted its existing unknown
  `timeout` config warning.
- `ruff check --config pyproject.toml tests/editing_conformance/test_p4_ten_note_v2_runtime.py`
  — **PASS**.
- `mypy --config-file pyproject.toml --no-incremental astrid/sdk/timeline/commit.py astrid/sdk/timeline/commit_session.py astrid/sdk/timeline/emitter.py astrid/sdk/timeline/sync.py`
  — **PASS**, no issues found.
- `git diff --check` — **PASS**.
- Offline compiler/trusted-seed-shape witness — **PASS**: exact authored parent
  fields, timing, opaque/null values, note setup, order, and compiled child
  closure validate through `bundle_from_document`; no HTTP/service/socket was
  used.

## Known seam and exclusions

The normal authoring adapter intentionally virtualizes repeated physical shots
into independent per-placement authoring identities. The unchanged original
positive assertion still checks the shared placement behavior; this seed task
does not rewrite that assertion or invent a binding to force it. Actual HTTP
execution, inverse/redo body execution, Runtime readback, and service/full
suites remain unverified and belong to the manager's next body run.

Source blob: `5ee8dd5b863c164e0ea5f03257ac61849a425061` →
`8a93768271fc1ca4f48db927c25d70cbbe97a3d9`.
