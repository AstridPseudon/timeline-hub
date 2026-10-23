# G5 lossless capture repair — agt-G5-redo-capture-return-1552

Status: harness-only repair complete; no meaningful diagnostic invocation was run by this worker.

The new uniquely hashed observer is [agent-G5-redo-capture-1552-lossless.py](./agent-G5-redo-capture-1552-lossless.py), SHA-256 `2188e04aeafd32e088f59438bac8efd56ff4a7cd67d80c8b8635a6c7010fb3d3`. It loads the preserved 1534 reproducer without changing its source, target test, product code, tests, schema, clients, pins, or runtime. The old source SHA-256 remains `153be3ff0db9e473bde9289e9964ea7900e8666713073677a8d4251c42c91740`; the prior failure artifact remains `88662e...b554be`.

The observer clone keeps ordinary JSON values exact and uses explicit finite-JSON tags for callables (`module`, `qualname`, `sourcefile_sha256`), cycles, dataclasses, types, bytes, non-finite floats, mappings with non-string keys, exceptions, tuples, sets, and opaque objects. It never uses `repr`, source text, environment dumps, or credential fields. Critical request/history/prepared/native/effects values are retained as complete encoded payloads. Every transport, provider, port, guard, preview, and accept observation writes a canonical finite-JSON JSONL precall packet and flushes/fsyncs before invoking the wrapped call. Payloads carry SHA-256 content hashes; the first occurrence contains the full payload and duplicates reference it. The packet store is bounded at 4096 lines and fails closed rather than silently dropping a packet.

## Locked preflight

- Agent HEAD: `91ac58a9fc6f1f752be16c0e4b8a1bf17095acee`
- Runtime HEAD: `9ce4242bc01f100bab9efc51032a73985cefb2b2`
- Original target body: SHA-256 `c2711a2d10765828694ee1906d75bdf62a91ed6ac0bbef8e4cb0d823e48ec30d`, 6798 bytes
- Original target file: SHA-256 `d7dc8942c49b4c464535280b8849520adfba4b67d4dc0560a5b68203abf7983b`
- Both assigned/runtime worktrees were clean at inspection.

## Evidence

`PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-G5-redo-capture-1552-lossless.py --offline-smoke`

PASS (`checks=5`). This offline-only smoke verifies exact finite-JSON critical roundtrip, function-valued exception locals, nested dataclass/type metadata, readable durable precall data, and serializable final output after a synthetic exception. No service, fixture, original body, pytest lane, or live socket was used.

`PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m py_compile /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-G5-redo-capture-1552-lossless.py`

PASS.

## Live diagnostic disposition

The actual redo result, guard `ref/path/base/theirs`, provider stack, history/stage records, and SQL no-write outcome are **not claimed here**: the manager owns the one fresh invocation after this repair. The new output is designed to retain those exact fields in `g5-redo-events.jsonl` before wrapped calls and in the final `g5-redo-diagnostic.json`. If that authorized invocation has a new failure, stop, retain the partial capture, and do not retry or modify the guard. Any behavioral/authentication cause belongs to the precise implementation owner selected by the manager; this worker owns only observer cloning, serialization, and durable capture.
