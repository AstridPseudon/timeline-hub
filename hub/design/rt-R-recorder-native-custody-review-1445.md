# R-recorder-abi-authority review

Verdicts:

- **NEW source-cause claim: PASS.** Complete native coverage cannot be inferred from remaining physical bindings, selections, reads, or effects.
- **Producer qualification: FAIL.** The current Agent producer/private carrier does not provide an independently sourced complete executor result. No implementation was made.

Evidence was authenticated directly:

| Attack omission | Accepted packets | Result |
|---|---:|---|
| `fork.source` | 2 | accepted, 9 reads / 2 selections |
| all native bindings | 2 | accepted, effects retained |
| reads | 2 | accepted, 0 reads / 2 selections |
| selections | 2 | accepted, 9 reads / 0 selections |

All eight responses were `status=accepted`; request hashes matched context and receipt hashes; receipt results equaled response data; base/source payload digests matched their declared hashes; private captures, where present, matched context and prepared digests. Packet SHA-256 values matched `boundary-facts.json`. The coverage XML hash is `184c6a01cc7606563c268a9ceed5efe7cc07208f31b257a1738c6ac38493d0c5`.

The attack is sound: `timeline_commit_auth.validate_bindings` skips bindings without `physical_ref`, and no sealed request field declares the complete native obligation set. A full `commit.effect` set therefore cannot prove reads, selections, source bindings, or dependencies were complete. The private original/landing capture is currently assembled from mutable provider records after execution; its digest authenticates those supplied bytes, not their provenance.

Trusted path identified:

- Provider registration: `RuntimeService.register_timeline_commit_provider`
- Invocation: `RuntimeService._execute_timeline_commit` → `CommitExecutionCoordinator.execute`
- Agent producer: `commands.execute`, `Recording.finish`, `CommitPatch.finish`
- Assembly: `commit.py` → `_commit_preview.prepared_records` / `capture_sequential_execution`
- Runtime consumer: `RequestCommitPort._validate_sequential_execution` → `TimelineCommitStore._validate` → `timeline_commit_auth.validate`
- Persistence: `TimelineCommitStore.accept` → `_publish`
- Replay: `history_entry` / `_verify_accepted` / `_historical_sequential`

Required smallest sound seam: the Agent executor must emit a complete immutable native execution result before `PreparedCommit`/mutable prepared-record assembly. Runtime must retain it through the existing private port boundary and compare it against the prepared candidate for every v2 invocation, including single semantic commands. A provider/caller-supplied digest alone is insufficient.

Attempt rules must preserve the original base pair `B`, and each landing/rebase pair `Hᵢ`; stale attempts are discarded, while only the accepted `(request_hash, B, Hᵢ, prepared/result digest)` is persisted. Exact retries replay the durable receipt without provider execution. Legacy records remain ABI1 only when no authenticated authority fact exists; injected `recorder_abi=2` must reject. D61’s optional history enum is approved but does not establish authority.

Evidence status:

- Retained authority run: **23 passed, 12 failed**; failures include both genuine v2 fork qualification cases, legacy-binding stripping, and all eight omission attacks.
- Supported legacy `track.create → occurrence.create` acceptance and restart replay: passed.
- `git diff --check`: passed.
- No full suite, typecheck, lint, or new code qualification claimed.