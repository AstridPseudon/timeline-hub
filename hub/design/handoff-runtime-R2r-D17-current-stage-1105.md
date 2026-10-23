# R2r D17 current-stage authentication — bounded Runtime PASS; integrated FAIL

**Runtime normalization repaired; two remaining Agent claims are invalid.**
The exact four Agent nodes ran once on the meaningful final candidate: **2 passed,
2 failed in 38.96s**. Receipt/preview/undo/redo and retained-input reversal now pass.
Both repeated-copy variants fail the unchanged strict requirement
`provider inverse effect bindings do not cover its stage image`. Agent owns the
remaining repair; do not qualify D17 or retire writers from this result.

## Classification and exact retained evidence

Before changing the boundary, inspected the retained actual failure from
`design/agent-D17-current-auth-diagnosis-1058.json` (4,205,971 bytes). Event 191 is
the full production auth argument tuple; event 192 the stage boundary; events
193–194 retain its first sequential write and full images. These are retained
in `/tmp/w-6e26745cd8/retained-counterexample.json`, with the source artifact hash.
The original evidence and original0912 were not edited.

The first write is `occurrence:occ-copy-again`, path `[]`, present → absent.
Its authored before value is identical to the stored occurrence except that
Runtime's physical occurrence additionally contains `shot_revision_id`.
A later `shot:copy-film`, path `[]`, captures `{payload, internal_timeline}`;
it is a native aggregate of two physical roots, rather than a single payload.
The old stage checker compared the first observation directly to the physical
row, and would also resolve the shot aggregate as a timeline scope. This is a
Runtime representation mismatch, not a forged authored value.

The repair observes the same native aggregate through authenticated physical
images: strip only occurrence revision links; resolve a shot uniquely and follow
its exact internal revision; compare complete authored content, including any
supplied internal revision link. Missing native derived shot links are compared
to the authenticated physical link rather than trusting provider-supplied IDs.
Projection uses the independently authenticated stage image, preserving complete
physical payloads and shared internal roots. Native membership/order/ranges,
source history, sequential-before, final image coverage and physical effect
bindings remain required. No store change, command executor, record dropping,
new request form, history exception or binding waiver was introduced.

Captured-case source comparison in `source-causality.json` uses the exact same
production argument tuples against baseline49ce and candidate (no suite rerun):

| Actual case | Baseline49ce | Candidate | Effect bindings |
| --- | --- | --- | --- |
| receipts/preview/undo/redo | sequential-input refusal | PASS | 6 |
| repeated copy False | sequential-input refusal | missing stage-effect bindings | 0 |
| repeated copy True | sequential-input refusal | missing stage-effect bindings | 0 |
| retained inputs | sequential-input refusal | PASS | 6 |

Full request/prepared/source/base/history/effects are separately retained in
`captured-receipt.json`, `captured-repeated-false.json`,
`captured-repeated-true.json`, and `captured-retained.json` in the scratch folder.
The source history maps come from actual store validation, not invented history.

## Required owner action

Both repeated-copy undo requests contain the legacy semantic envelope with no
`label`, `steps`, `merge` or `reads`. Agent `CommitPatch.__init__`
(`astrid/sdk/timeline/_commit_patch.py:228`) therefore sets `self.v2=False`.
Its finish path (`:516`) only emits `commit.effect` bindings under `if self.v2`.
The resulting inverse still carries `inverse.stage`, three physical effects,
and complete source history, but its sole binding is `inverse.stage`:
zero parent/shot/internal before/after physical effect bindings.

C0's provider-generated-effect rule requires segment-specific physical bindings,
including both parent sides and before bindings for roots leaving the closure.
Runtime must continue refusing these incomplete claims. Agent should preserve
that complete provenance for the normal session undo/redo caller, including
synthesized legacy steps (or issue the complete v2 request through that caller).
No Agent repair was made here. The original four tests and their expectations
are unchanged. After the Agent owner repairs this, independently rerun the
requested integrated selection on the reviewed Runtime candidate; reuse the
existing 281 inverse result unless a new change requires more.

## Source and origins

- Runtime base: `49ce53289bc37d9387a7d9e6b9c9b16072162181`, tree
  `364380ae064c512c0a0d2b8903a599b7026642f4`; candidate is this base plus exactly
  the auth module and appended stage tests in this worker worktree.
- Required Agent: `ce1d1cca87379029924b0be6f98564f556597107`, tree
  `68dee9124ab8f4026ac4119f816eceec654f0bba`.
- `/home/user/work/agent` had already advanced to
  `abfa78a657b4ce1cc625104e8472fb29938e3d64`, tree
  `ffd2a6883c8703b2052daa16e6c9ee0b0c0efdae`, clean before/after.
  Its timeline product code and D17 test file are unchanged from ce1; its other
  changes include test-lane infrastructure. Never checked out or modified it.
- For exact-four and original1003, extracted immutable ce1 into
  `/tmp/w-6e26745cd8/agent-ce1`; verified **all 3403 blobs** against ce1 Git blob
  identities. Used venv-agent, candidate Runtime first on PYTHONPATH, and
  ASTRID_RUNTIME_CHECKOUT pointing to this worktree for exact-four.
- Read-only observer captured **8 origin snapshots, 4 cases, 39 Runtime modules**,
  with all origins under the candidate worktree and all module hashes unchanged.
  Actual current-history arguments are retained for each case. See
  `exact-four-origins-history.jsonl` and `observation-summary.json`.
- Candidate auth SHA256:
  `a8a0b00025f99ace48e0fee989fe3e11c948c3f1e2fa47a33621791e91252756`.

## Exact validation commands and results

All test temp files were placed under `/tmp/w-6e26745cd8` via TMPDIR and
`--basetemp`; no shared dependencies were changed. The following commands ran
from the Runtime worktree, with `TMPDIR=/tmp/w-6e26745cd8` additionally set:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_inverse_stage_authentication.py tests/test_timeline_commit_authentication.py tests/test_timeline_commit_read_basis.py --basetemp=/tmp/w-6e26745cd8/pytest-auth
# 137 passed in 50.27s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_source_duplicate_authority.py tests/test_timeline_commit_inputs.py tests/test_timeline_source_document_boundary.py tests/test_timeline_raw_capture.py tests/test_timeline_commit_port.py --basetemp=/tmp/w-6e26745cd8/pytest-d17
# 101 passed in 13.98s
```

The stage file now collects 52 cases (41 existing + 11 new). New main-suite
controls cover occurrence/shot before content, internal edge, after state,
forged ref/path, omitted/extra native writes, missing effect bindings, and
forged effect digests. Each refusal checks complete SQL dump, authoritative
rows, and immutable history equality. The positive checks exact undo/redo
restoration and original history immutability. Initial development runs of only
the new fixture failed (11 cases, then one diagnostic case) before its merge
mode matched the authentic atomic source-copy request; correcting that new
fixture produced 11 passed, 41 deselected in 7.23s. No existing test changed.

Exact-four command, run once from the immutable Agent extraction:

```sh
TMPDIR=/tmp/w-6e26745cd8 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/rt-R2r-D17-current-stage-sol-1105:/tmp/w-6e26745cd8/agent-ce1:/tmp/w-6e26745cd8 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-R2r-D17-current-stage-sol-1105 D17_OBSERVATION_LOG=/tmp/w-6e26745cd8/exact-four-origins-history.jsonl /home/user/work/venv-agent/bin/python -m pytest -q --tb=short -o addopts= -p no:cacheprovider -p observe_d17 --timeout=45 'tests/editing_conformance/test_commit_runtime_source_copy.py::test_source_copy_real_port_receipts_preview_undo_redo' 'tests/editing_conformance/test_commit_runtime_source_copy.py::test_repeated_source_copy_real_port_idempotency_and_guarded_inverse[False]' 'tests/editing_conformance/test_commit_runtime_source_copy.py::test_repeated_source_copy_real_port_idempotency_and_guarded_inverse[True]' 'tests/editing_conformance/test_commit_runtime_source_copy.py::test_source_copy_retained_inputs_whole_undo_redo' --basetemp=/tmp/w-6e26745cd8/pytest-four
# 2 failed, 2 passed in 38.96s; both failures are Agent missing effect provenance
```

Original corrected REALSTORE witness command, run once:

```sh
TMPDIR=/tmp/w-6e26745cd8 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/rt-R2r-D17-current-stage-sol-1105:/tmp/w-6e26745cd8/agent-ce1 /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-R2-stage-repro-1003-store-authenticated.py
# PASS: forward/inverse production accepted; forward/inverse direct AUTH pass
```

`realstore-1003.json` retains the full original output. Exact source publication
`txn-3dd966453f07405783079bca86bb90a7` was supplied via authentic store.history_entry;
inverse publication excluded, source records equal accepted forward records,
step `split`, ordinal `[0]`, created `parent/clip:music-right`. The unchanged
original diagnostic still prints stale hard-coded Agent/Runtime commit labels;
actual module paths/hashes and `verified-origins.json` identify this run.

```sh
ruff check --no-cache runtime_protocol/timeline_commit_auth.py tests/test_timeline_inverse_stage_authentication.py
# All checks passed
ruff check --no-cache --output-format=json runtime_protocol/timeline_commit_auth.py runtime_protocol/timeline_commit_store.py tests/test_timeline_inverse_stage_authentication.py
pyright --outputjson runtime_protocol/timeline_commit_auth.py runtime_protocol/timeline_commit_store.py
# Compared to exact49ce extraction, same commands: Ruff 11/11; Pyright 76/76.
# Complete diagnostic identity comparison, mapped through unchanged source lines:
# 0 added / 0 removed for both tools. Auth and new test Ruff clean.
git diff --check
# PASS
```

AST/in-memory compile PASS. Preservation: 96 frozen contract/generated/schema/
conformance files identical (superset of frozen77); 279 other existing test files
byte-identical; entire 34,547-byte existing stage test prefix and all 14 existing
definitions unchanged; original 367 lines unchanged; store byte-identical.
Original0912 SHA256 still
`47399344d70ecb35bca0f843aea5c7245cae35a623cdbbcfd777465d47810f8a`.
Full manifests and normalized diagnostics: `/tmp/w-6e26745cd8/manifest.json`,
`static-identities.json`, `preservation.json`.

## Limits and next steps

The two repeated-sharing undo/redo journeys remain unqualified because Agent
omits required provenance. This is an owner handoff, not permission to waive the
guard. The supplied v2 receipt and retained-manifest journeys pass exactly.
No full suite, native14, original20, browser, HTTP/live sockets, P4, Agent58,
281 duplicate, host daemon or git writes ran. Shared installs and integration
worktrees untouched. Review the bounded Runtime change, then give the two
missing-binding counterexamples to the Agent owner before integrated qualification.
