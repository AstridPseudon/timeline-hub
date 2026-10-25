# F-D86 protected source review

## A — opaque9

**PASS_SOURCE**

- Commit: `9f88f8cd0808f56530c9a297b22c0862f13e9529`
- Tree: `ca5cf5289c97eb90165b33e1da72e99d884c6e3b`
- Changed blob: `67691003702da64b03a3ebb66aa2972920f90787`
- Create/fork blobs unchanged: `0178b098…`, `e17b6c46…`
- Only permitted file changed.

The candidate preserves bundle provenance, uses genuine semantic shared allocation, then guarded `doc.patch` restoration for occurrence fields/order. Original opaque values, identities, topology, assertions, guards, and six emitter cases remain conserved.

Remaining outside owner:

- IDs 78–79: create assertions, `test_commit_runtime_occurrence_create.py:70`.
- ID 80: fork inverse native-write coverage, `runtime_protocol/service.py:2518`.
- IDs 81–86: behavioral confirmation remains pending; source seam is corrected.

## B — ordinary-script4

**PASS_SOURCE**

- Commit: `a2c71eeceb407607d4d66630aa6af08e1974123f`
- Tree: `faf97ab445916a4e7e83cdca01fd970989cc2ff3`
- Blobs:
  - S3: `b6c0224200543ed30af96361c0d6bddf3caeca9f`
  - Union: `52d62549652d089268bcf6b59d96ff43e68a62ca`
  - Script: `729445cd499dd2f975b7374cce95ed8a44b97e5d`
- Only the three permitted files changed.

The candidate uses `capture_clip_add`, separates genuine occurrence birth before text binding, and performs a genuine text rebind from the prior accepted revision. Original four scenarios, inputs, assertions, branches, retries, grouped inverse, shared identity, and canonical digest expectations remain conserved.

No remaining source finding outside the assigned files; behavioral confirmation remains pending.

## Evidence

- In-memory AST parse/compile: passed.
- AST assertion/raise/control-flow conservation: passed.
- Baseline and candidate Ruff: passed.
- Baseline and candidate mypy: passed with `venv-agent`, `--python-version 3.13`, and shadow files. Default invocation exposed only the environment’s incompatible NumPy stub.
- `git diff --check`: passed.
- Worktree clean.
- No pytest, collection, fixture/helper execution, service, browser, build, or behavioral suite run.

No product, Runtime, generated, schema, pin, ledger, or dependency files were changed. Git metadata records both candidate commits as authored by `Claude`; the brief labels the originating author Luna, so provenance should be reconciled if that metadata is a hard gate.

Commit message written and `DONE` created.