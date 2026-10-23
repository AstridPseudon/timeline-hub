# Agent U4a-v2 merged-reply review

**Verdict: FAIL — exact source pin is product-incompatible.** Agent adoption
`92c37ba46` is byte/hash exact against Runtime producer
`21482a416d1f0f976ec563b9e1bf96a765f80e56` (tree
`7a182a69fa7ec893987dbbd3ac34eb3ba577ec6f0`): all 15 lock mappings and the
producer manifest pass, `generate.py --check` passes, and the exact adoption
delta is only `runtime.lock.json` plus the three generated client files and
contract metadata. Current R3/R1/V1/V3/P1/V4 source is preserved.

The offline official-client/public-Agent-WorkspaceClient probe passes accepted
and preview (`would_status: "merged"`) complete envelopes, preserving full v2
request serialization and receipt/data/source/steps/dependency guards. It
rejects the valid merged success at adopted
`astrid_runtime_client/generated.py:948` because the canonical producer
template `generators/python_client_template.py:948` only allows
`("accepted", "rebased")`. Runtime store source already emits `merged` at
`runtime_protocol/timeline_commit_store.py:1066`, and the schema already types
it. The minimal producer correction is to add `"merged"` to that template
allowlist, regenerate normally, refresh/check the artifact manifest, publish a
new producer tuple, and re-vendor. No Agent fallback or hand-edited output is
appropriate.

Requested targeted tests: **46 passed, 39 deselected**. Normal ratchets:
Ruff **2151/2151**, private mypy **1915/1915**. Scoped generated/facade Ruff
and mypy findings are inherited baseline issues. No product edits were made.
