## D42 whole-path review: FAIL

No product changes; worktree remains clean at `a6843aa9322d354a8db2576a43dd202244608d65`.

Production path:

`server.py:545` GET → `service.py:2520` → SQLite mutex → `_read_history` → `history_entry` → `_verify_accepted` → `_verify_replay`. Page entries repeat authenticated `history_entry` reads under the same mutex.

Freshly authenticated inputs include:

- actor, realm, project/timeline membership and archive authority;
- idempotency/result/history rows and exact JSON bytes;
- event prefix, IDs, sequence, hashes and accepted-event payload;
- revision closure, manifests, digests, ownership and CAS media;
- continuation graph and inverse-stage history;
- captured sequential execution, request, prepared result and semantic events.

The memo key also includes these inputs, realm, archive mode and validator version.

Findings:

1. The known closure-cell bypass remains valid. Function identity/code/defaults are fingerprinted, but `__closure__` contents are not. This matches cumulative review 0357’s finite attack.

2. New gap: cached validator `_resolver` state is not fingerprinted. The fingerprint records `validator._registry`, but validation actually resolves `$ref` through `validator._resolver`. Private probe:

```text
first_auth_validate_calls=2
warm_auth_validate_calls=2
warm_skipped=True
cold_after_memo_clear=ProtocolError
```

Replacing only `CommitContext._resolver` with an empty `Registry` left the warm read accepted; clearing the memo made the cold read refuse as corrupt.

Recommended smallest seam: do not add another dependency whitelist. Memoize only through a sealed, immutable validation capsule with a cheap version token. Capture closures, defaults, validator resolver/registry state and schema state in that capsule; any mutable or unversionable dependency must force full verification and must not be cached. Preserve the existing SQLite mutex and fresh database/input checks.

Evidence:

- Prior cumulative report: 145 authentication/HTTP selectors passed; 184 replay/input/dependency selectors passed, but the closure attack failed.
- Private resolver attack: passed as described above.
- `git diff --check`: passed.
- No full, browser, HTTP, duplicate adversarial suites, or product tests rerun.