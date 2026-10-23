# R1 current Runtime 859 qualification — HOLD

Date: 2026-10-23 UTC  
Agent source: `851439d95647820815e69b4d7163e179540f28db`  
Runtime source: `8592822fd11275540f596562f43c715676f2bc0f` at `/home/user/work/wt/rt-pin-8592822f`

## Disposition

The sequential provider candidate remains held and unmerged. Runtime 859 still rejects both moved-head positive parameter cases at its existing authenticated input boundary. This does not justify changing the Runtime guard, inventing a continuation edge, replacing the submitted physical reference, or changing the contract. The bounded provider-side source replay and the strict five refusal controls pass; the whole end-to-end qualification is red.

## Required qualification

Command:

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8592822f PYTHONPATH=.:/home/user/work/wt/rt-pin-8592822f PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_doc_patch_sequential_rebase.py
```

Result: **2 failed, 7 passed in 8.95s**.

| Case group | Result | Boundary |
| --- | --- | --- |
| Fresh-head positives (`moved=False`, declared read absent/present) | 2 passed | Provider and Runtime accept |
| Moved-head positives (`moved=True`, declared read absent/present) | 2 failed | Runtime dry-run validation rejects before write/accept |
| Strict refusal controls: field, consulted read, membership/order, changed source, forged continuation | 5 passed | Existing conflict/refusal guards remain intact |

Both failures report `invalid_records` / `provider alias is outside its authenticated boundary`. The no-read case fails at Runtime `timeline_commit_auth.py:344 → normalized → site`; the declared-read case fails at `timeline_commit_auth.py:309 → validate_read → normalized → site`. The failure is the original submitted staged physical alias at the actual replay boundary, not a provider execution failure.

The test's exact origins printed before and after each case are:

- Agent provider: `/home/user/work/wt/agt-R1-sequential-current-review-1335/astrid/sdk/timeline/_commit_patch.py`.
- Provider execution module: `/home/user/work/wt/agt-R1-sequential-current-review-1335/astrid/sdk/timeline/commands.py`.
- Runtime commit port: `/home/user/work/wt/rt-pin-8592822f/runtime_protocol/timeline_commit_port.py`.
- Runtime authentication owner of the refusal: `/home/user/work/wt/rt-pin-8592822f/runtime_protocol/timeline_commit_auth.py`.

## Provider review

`_commit_patch.py` preserves the intended source proof and guards:

- `before()` resolves a replayed physical reference only through a completed earlier step, then requires one unique materialization successor with the same owner and complete owners list. It rejects future/self sources and ambiguous successors.
- `after()` records each command before publishing the step output; `materializations()` carries exact source, successor, owner, owner-set, edge-before/edge-after, step, boundary and digest bindings.
- `rebase_patch()` separates staged predecessors from authenticated history continuations. `replay_ref()` follows only earlier command ordinals, while `continuation()` still rejects missing, cyclic, or non-unique authenticated history.
- Before/read/previous-value, collection membership/order, dependency, atomic scope, and semantic-write guards remain active. Equal final bytes do not erase historical writes, so ABA remains a conflict.
- No Runtime code, Runtime guard, wire reference, schema, pin, contract, generated client, or test expectation was changed.

The provider-side bounded source result is therefore **PASS**: replay plans contain a source-bound successor mapping and the five strict refusal controls pass. The whole provider-plus-Runtime qualification is **FAIL** because Runtime 859 has no accepted authenticated input-authority proof for the original unlanded staged physical ID. Keep G5 draft-only and P1 NO-GO.

## Durable evidence

The flat, uniquely hash-named packet and manifest are in ORCH design:

- [qualification packet](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-R1-sequential-current-runtime859-packet-23d309fb6f841fbb.json) — SHA-256 `23d309fb6f841fbba8560317c336b495ec4fcf2700a7e4c69bb7e1ea5c0f7ca7`.
- [packet manifest](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-R1-sequential-current-runtime859-manifest-23d309fb6f841fbb.json).

The packet contains the complete current Runtime-859 request, prepared records, base/source/input bundles, original and replay execution plans, continuation maps, authenticated history, tracebacks, and exact origins for both moved-head positives. It embeds `capture-001-execution.json`, `capture-002-execution.json`, and `capture-003-auth-error.json` from the prior 3b investigation as lossless UTF-8 text. No credentials, authentication headers, cookies, tokens, or secrets are included; no second export queue was created.

## Quality evidence

Current source is unchanged from the prior R1 qualification. Current checks:

- `scripts.reshape.compare_ruff_baseline`: **current 2149, baseline 2149**.
- `ruff check --no-cache tests/editing_conformance/test_doc_patch_sequential_rebase.py`: **PASS**.
- `scripts/vendor_lock.py check runtime.lock.json`: **PASS** (`ok runtime.lock.json`).
- `scripts/artifact_manifest.py --check`: **PASS** (`artifacts.json is current`).
- `git diff --check`: **PASS**.
- Private mypy exact reuse from the unchanged source qualification: **1912/1912**, zero added/removed diagnostic identities. A fresh retry with a private cache timed out after 30 seconds without output; no fresh mypy result is claimed.

No full suite, HTTP/browser/live-socket suite, native repeat, P1/P4 repeat, product edit, test edit, Runtime edit, Git write, or dependency mutation was performed.

## Next step

Runtime owner should assess the packet against existing input-authority support. Any repair must authenticate the original sequential boundary and corresponding replay boundary while preserving root identity, ownership, previous/read/membership/order/ABA checks. Until that is authorized and implemented in Runtime, this Agent candidate remains a held draft.
