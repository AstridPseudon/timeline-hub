# R1 private sequential capture — source ready, joined qualification held

Agent base: `851439d95647820815e69b4d7163e179540f28db`.
Runtime tested: `8592822fd11275540f596562f43c715676f2bc0f`,
`/home/user/work/wt/rt-pin-8592822f`.
Current Agent comparison: `8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe`.

## Delivered

Published the exact private interface during the first five minutes:
`design/agent-R1-private-sequential-interface-1403.md`.
The existing provider now calls
`port.capture_sequential_execution(capture: dict) -> None` immediately before
the existing preview/accept, for each head attempt when the method is supported.

Three product files changed: `_commit_patch.py` captures actual command input/output
closures and evaluation boundaries; `_commit_preview.py` carries full original and
landing records, the actual recursively serialized replay map, exact context and
digest of the complete prepared candidate; `commit.py` invokes that channel and
resets the replay map on every retry. No caller/public request, PreparedCommit,
schema, generated client, accepted-history map, dependency or toolchain changed.

Each execution retains original physical refs, exact revisions/digests, base and
evaluated-head pairs, step/command/change ordinals, ownership and complete owner
sets, materialization managed edges, exact reads/patch-before, dependencies and
effects. Input/output documents retain successor pins and intermediate states.
The original unlanded alias remains an original execution fact, never an accepted
history successor. Runtime must independently authenticate the supplied facts.

An absent/noncallable private method refuses only a moved-head sequential staged
input requiring this proof, with `sequential_proof_unavailable`. Fresh-head and
ordinary ABI paths remain usable. A private port refusal propagates without
falling through to preview/accept. CAS retry tests prove the original execution
stays fixed while each candidate gets a new landing/map/prepared digest.

## Evidence

Final packet: `design/agent-R1-private-sequential-packet-59e329b65a9b83c3.json`.
SHA-256: `59e329b65a9b83c38f257ae5b87157072e30d71e63e0506b8b6908aa89231619`.
Size: 998519 bytes. Matching flat manifest:
`design/agent-R1-private-sequential-manifest-59e329b65a9b83c3.json`.
The earlier `9e3d0d52d1b3fb77` transport-only packet remains retained; use the final
packet above, which also binds exact source bytes/hashes and the current-only patch.

The final packet includes four real-provider captures (declared reads absent/present,
preview/accept dispatch), full requests, prepared candidates, original/landing
command images and records, replay maps, source/head closures, authenticated
history, exact before/after module origins, and the final scoped log. Those four
cases deliberately stop at the receiving private port with `capture_complete`,
before independent verification or persistence. Complete database dumps, document
and history remain unchanged. They prove transport, not accepted merged edits.

Worker `evidence/` retains the four raw captures, logs, exact diagnostic identity
comparison, full source packet and manifest, and clean current-only patch.

## Tests and checks

All commands ran from this assigned worktree unless a baseline directory is named.
No full, HTTP/browser/socket suite, original-nine joined repeat, native14/58,
P1/P4, D17 or V4/54 suite was requested.

Final scoped command (exact):

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-8592822f ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8592822f R1_EVIDENCE_DIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R1-private-sequential-proof-sol-1403/evidence /home/user/work/venv-agent/bin/python -m pytest -q -s -o addopts= -p no:cacheprovider --basetemp=/tmp/w-cca99996de/final tests/editing_conformance/test_private_sequential_capture.py tests/editing_conformance/test_private_sequential_capture_runtime.py tests/editing_conformance/test_doc_patch_sequential_rebase.py tests/editing_conformance/test_doc_patch_v2.py -k 'private or test_sequential_refusal_has_no_writes or test_rebase_requires_source_bound_materialization_and_exact_managed_edges'
```

**30 passed, 97 deselected in 16.82s**. This comprises 11 private-provider tests,
5 actual Runtime/provider capture tests, the original 5 no-write sequential
refusal controls, and 9 strict source-materialization controls. The four original
sequential positive cases were not executed. New tests cover recursive lineage,
CAS recapture, unsupported ports, rejection propagation, caller-supplied private
claims, complete metadata/custody, original vs landing physical identities and
reads/patch-before at each sequential input.

Earlier focused neighbouring run (before the final duplicate-lineage fail-closed
detection improvement), exact:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-8592822f ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8592822f /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/w-cca99996de/guards tests/editing_conformance/test_doc_patch_v2.py tests/editing_conformance/test_doc_patch_mirrors.py tests/sdk/test_timeline_commit_provider.py tests/editing_conformance/test_doc_patch_sequential_rebase.py -k 'not test_sequential_physical_inputs_land_at_actual_step_boundaries'
```

**234 passed, 4 deselected in 66.29s**. No passing behaviour test was modified.

Quality commands:

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/_commit_preview.py tests/editing_conformance/test_private_sequential_capture.py tests/editing_conformance/test_private_sequential_capture_runtime.py --output-format concise
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check --no-cache . --output-format json
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-cca99996de/mypy-final /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy astrid scripts/reshape --hide-error-context --no-color-output --no-pretty --show-error-codes
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
```

Scoped Ruff **PASS**. Whole normal Ruff **2149/2149**, private Mypy
**1912/1912**, with **zero added and zero removed path/message/code identities**.
Raw normal linters exit 1 for the unchanged baseline backlog; their comparison
passes. Mypy checked 958 source files, 252 with existing errors. The exact HEAD
baseline was read with `git archive HEAD astrid scripts pyproject.toml` into
`/tmp/w-cca99996de/baseline`; the same Ruff/Mypy commands ran there with its own
`MYPY_CACHE_DIR=/tmp/w-cca99996de/mypy-base`. Vendor lock, artifact manifest and
diff whitespace checks all **PASS**. No baseline file changed.

Initial harness invocations first lacked the Runtime import path, then used
`.../worker/tmpdir` as a directory although it is a harness pointer file. Those
invocations failed during fixture setup and did not exercise product behaviour.
Reading that file provided `/tmp/w-cca99996de`; only invocation/temp paths were
corrected. Two initial test assertions were corrected: replay source is the
authenticated landing root, and the public service wraps arbitrary exceptions.
Final tests use explicit Runtime refusal to stop at capture. No old test was
weakened, skipped or deleted.

## Cumulative scope and current-only port

This worker adds 70 product lines and replaces one import line across three
product files, plus two focused test files. The reviewed 851 sequential mapping
patch and original nine-case test remain inherited.

The entire inherited branch also lacks current 8c355's D20 shared-occurrence
implementation: `commands.py` loses 7 lines, `commit.py` loses its unrelated
4-line shared-source reservation hook, and `native_occurrence_shared.py` plus
`test_occurrence_shared_d20.py` are absent. These are inherited ancestry
differences, not edits made here. **Do not merge this branch wholesale.**

`design/agent-R1-private-sequential-current-only-1403.patch` is a cumulative R1-only
patch against exact 8c355. It includes the reviewed sequential mapping change,
this private carrier and the three relevant test files; it retains all current
D20 source/registration/reservation behaviour. Patch SHA-256:
`a5a40e633a169af373c589799f8a98071d56491d7fd6b1935db14c14c75cb8cd`.
All resulting Python files were parsed, but this patch has not been applied or
qualified on a current-only worktree. The requested subsequent current-only port
and review remain separate work. No Git write, merge request or push occurred.

## Decisions, limits and next owner

There was no reusable original/replay execution carrier in Runtime 859, so the
small request-scoped private method is necessary. Carrying complete generated
records and exact command closures avoids a second public schema or hand-built
partial claims. Runtime retains authentication and persistence ownership.

Runtime 859 has no verifier/capture method. Therefore independent rejection of
forged capture/context/step/ordinal/owner/digest/map data is **not qualified** by
these Agent transport tests. Existing strict history/materialization refusals do
pass. No guard was waived and no fake verifier was added to Agent or Runtime.

Runtime owner should implement the published method and independently authenticate
both sequences against captured base/head/history, then bind to the exact
prepared candidate and verify unique lineage/owners/edges/reads/effects at each
boundary. Missing/forged/different-request/step/ordinal/owner/digest/map,
future/self/ambiguous/cycle/foreign/stale/ABA/order/selection controls remain
required for that verifier. After its author publishes an exact ready pin, run
the original nine cases once with both meaningful sources. Until then this is
source-ready partial work, joined qualification held; G5 remains draft and P1
NO-GO. No settled C0/PLAN decision was contradicted.
