# V2 timing identity repair — blocked on inherited word declarations

Task: `agt-V2-timing-identity-repair-sol-0139`. Base: `1a0ea1a40b18084c74f4e40e79b51bef9101acbf` on `tl/agt-V2-timing-identity-repair-sol-0139`. Read PLAN §3 V2, C0/C0b/C0c `design/commit-v2.md`, and independent review `31ce19421` / `agent-V2-P1-timing-review-0124.md`. Runtime source: clean `/home/user/work/wt/rt-pin-27f0306b`, HEAD `27f0306b94d136d25f237edf4b8225b5d8487be0`.

**Status: partial repair; P1 still fails four cases. Do not treat this as V2 qualification.**

## Changes

- `validation.py`: absent or explicit-null `from` means arithmetic zero for both source-window and asset-bound checks. Authored JSON stays unchanged, including explicit null. Negative/nonnumeric starts and excessive asset windows remain refused.
- `_commit_timing_validation.py`: obtain the provider's exact canonical closure through the existing pure `document_from_bundle` converter. Carry its actual child timeline/revision/digest pins into the detached timing view, indexed by each original local occurrence shot. This includes unchanged reused images and authenticated shared `doc.patch` successors; it does not infer identity from payload equality.
- `_timing_evaluators.py`: compare cut ownership by exact child image pin plus matching content digest. Distinct revisions remain ambiguous even with identical JSON. Keep shared occurrences' cut bases/ends local; otherwise merely accepting the shared identity makes later occurrences incorrectly inherit the first occurrence's start. Existing global cut graph keys and cycle diagnostics remain unchanged.
- Eight added regression parameters cover parent/child null arithmetic and asset bounds, unchanged shared images, shared patch successors, different shot revisions sharing one child, distinct child revisions with equal bytes, and independent occurrence edits (including equal resulting bytes). All original expectations remain intact.

No authored clip or declaration is filtered. No implicit occurrence fork, global ambiguity bypass, fabricated transcript binding, or `doc.patch` validation exemption was added.

## New blocking evidence

The review's two-cause diagnosis is insufficient. Once the false shared-cut ambiguity is removed, the same four params/disjoint P1 cases reach the existing word-declaration check and fail:

```text
candidate.timing: missing exact word binding for
('o', 'shot-placement-365d0383838d687737f499dfcdc96e880baaf8d4747ecf5f657993be89d8522b', 'c').on
```

Their retained child clip contains:

```json
{"astrid":{"cut":"old-cut","on":"old-anchor","until":"end"},"on":null,"opaque":{"keep":true}}
```

Main's existing intent accessor gives the nested Astrid declaration precedence. `moments.parse("old-anchor")` is a word Moment; no exact transcript/binding is present. This also reproduces after reducing the document to **one occurrence**, so it is independent of physical sharing. Preserving declaration validation while passing these cases needs an explicit inherited-legacy-declaration policy. I did not silently discard the declaration or invent authority. An asynchronous clarification was raised; no answer had arrived when this report was prepared.

There is also a census discrepancy: the unchanged requested `tests/sdk/test_p1_doc_patch_provider.py` collects **17**, not 22, cases at this base. `git diff 31ce19421 HEAD -- tests/sdk/test_p1_doc_patch_provider.py tests/sdk/fixtures/p1_feasibility/doc_patch_requests.json` is empty. The independent review commit changes only reports. The created-track-and-clip case now passes; four child/merge cases remain red.

## Exact final commands and results

Every Python/test/quality command below ran with:

```sh
export ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-27f0306b
export PYTHONPATH=.:/home/user/work/wt/rt-pin-27f0306b
export TMPDIR=/tmp/w-6b6c64e03b
export RUFF_CACHE_DIR=/tmp/w-6b6c64e03b/ruff-cache
export MYPY_CACHE_DIR=/tmp/w-6b6c64e03b/mypy-ratchet
```

The worker's supplied `tmpdir` file points to `/tmp/w-6b6c64e03b`; scratch/logs and tool caches are there.

```sh
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider --tb=short tests/sdk/test_p1_doc_patch_provider.py
# exit 1: 4 failed, 13 passed in 2.72s
# Log: /tmp/w-6b6c64e03b/p1-final.log

/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider --collect-only tests/sdk/test_p1_doc_patch_provider.py
# exit 0: 17 tests collected
# Log: /tmp/w-6b6c64e03b/p1-collection.log

/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider --tb=short tests/editing_conformance/test_commit_timing_validation.py tests/editing_conformance/test_commit_v2_validation.py tests/sdk/test_timing_compiler.py tests/sdk/test_timing_cycles.py tests/sdk/test_timeline_commit_v2_errors.py tests/editing_conformance/test_doc_patch_v2.py tests/timeline/test_meta_validator.py
# exit 0: 203 passed in 30.26s
# Log: /tmp/w-6b6c64e03b/targeted-final.log

/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider --tb=short tests/sdk/test_timeline_commit_provider.py tests/sdk/test_timeline_commit_provider_document.py
# exit 0: 139 passed in 29.55s
# Log: /tmp/w-6b6c64e03b/provider-neighbors.log

/home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/validation.py astrid/sdk/timeline/_commit_timing_validation.py astrid/sdk/timeline/_timing_evaluators.py tests/editing_conformance/test_commit_timing_validation.py tests/editing_conformance/test_commit_v2_validation.py
# exit 0: All checks passed!

/tmp/astrid-u2-typecheck/bin/python -m mypy --cache-dir /tmp/w-6b6c64e03b/mypy-scoped astrid/sdk/timeline/validation.py astrid/sdk/timeline/_commit_timing_validation.py astrid/sdk/timeline/_timing_evaluators.py
# exit 0: Success: no issues found in 3 source files

make ruff PY=/home/user/work/venv-agent/bin/python
# exit 0: current=2151 baseline=2151

make mypy PY=/tmp/astrid-u2-typecheck/bin/python
# exit 0: current=1915 baseline=1915

make structure cycles PY=/home/user/work/venv-agent/bin/python
# exit 0: structure current=13 new=0; no new cross-package cycles

git diff --check
# exit 0
```

Single-occurrence reproduction, with the same exports:

```sh
/home/user/work/venv-agent/bin/python - <<'PY'
from astrid.sdk.timeline.commit import _digest, bundle_from_document, document_from_bundle
from astrid.sdk.timeline._commit_timing_validation import validate_candidate_timing
from tests.sdk.test_p1_doc_patch_provider import _bundle
single = document_from_bundle(_bundle('params-absent-to-explicit-values'))
parent = single['parent_revision']
parent['payload']['occurrences'] = parent['payload']['occurrences'][:1]
parent['content_digest'] = _digest(parent['payload'])
value = bundle_from_document(single)
print('one pinned occurrence, no shared-cut ambiguity')
print(next(iter(value['shots'].values()))['internal_timeline']['clips'][0]['app'])
try:
    validate_candidate_timing(value)
except Exception as exc:
    print(type(exc).__name__ + ': ' + str(exc))
PY
# TimingCompileError: missing exact word binding for ('o', 's', 'c').on
# Log: /tmp/w-6b6c64e03b/p1-single-occurrence-probe.log
```

## Frozen wire and scope limits

Request scope/project/timeline/base revision/publication/key, commands, label, steps (patch and reads), merge, optional request reads, and dry_run are unchanged. Accepted/merged canonical data and receipts, authoritative effects/dependencies, conflict/invalid replies and preview shapes are unchanged. The production caller still invokes final validation for all commands. Neighboring provider tests cover accepted/merged/conflict, dry_run, inverse/restore, dependencies and canonical closure reuse, but the four original P1 child outcomes remain unverified because they refuse before acceptance.

Only the three owned product modules and two regression files changed. No `commit.py`, R1 `_commit_patch.py`, `commands.py`, schema, metadata contract, locks, generated files, Runtime, G3 or G4 edits. No original P1 test edits or weakened/skipped/xfail expectations. No full suite, browser/socket suite, shared dependency mutation, git mutation, cleanup or push.

## Source fingerprints

```text
b6ff7eada9e36e8b858a0e65be82c4fcdea906167bd35b8f8f5ca1891db65c05  astrid/sdk/timeline/validation.py
57aaaa608a6367acebdf7873fd04b422d6f9b1c46cbd5a6e3a7cf8b880eb4626  astrid/sdk/timeline/_commit_timing_validation.py
2b2e63515a6c3bb36f226eef22ef8b33175d3525f5824a5c4ba06cf9792fec44  astrid/sdk/timeline/_timing_evaluators.py
dc9da649c7b03000a6724103514669ee28efea2cc74f2fe76abb9ffc4249fcd9  tests/editing_conformance/test_commit_timing_validation.py
5aacc545d5e3d825e0132112515a408c7c823a185d66a8d3d445ab33ec6f21b7  tests/editing_conformance/test_commit_v2_validation.py
```

Next: orchestrator resolves the inherited unresolved timing-declaration policy and reconciles the original P1 census, then assigns the remaining repair and repeats the original assertions. Independently review this bounded identity/null repair before integration. BLOCKED marker is written; DONE is deliberately absent.

