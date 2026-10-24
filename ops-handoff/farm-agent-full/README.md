# OPS-farm-agent-full candidate packet

Status: candidate only. This directory does not modify the live ORCH, farm
registry, tests, queue, bench, source checkout, installer, daemon, or hub.

## Normal first-use route

`init-bench-store.py` is the smallest new caller around the reviewed
`Store.initialize` API in the exact farm `ORCH/bin/bench_store.py`. It binds
`ORCH/tests` from the supplied ORCH root, initializes only an absent root,
then reopens it through `Store(...)` and validates the existing owner/index
projection. An existing valid store is reused read-only. Unknown, partial,
symlink, foreign, wrong-tests, and wrong-root-identity stores are refused
before any write; no owner or index is synthesized.

The authorized normal command is:

```bash
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
python3 ops-handoff/farm-agent-full/init-bench-store.py \
  --orch-root "$ORCH" \
  --store-root /home/user/work/bench-store \
  --bench-store "$ORCH/bin/bench_store.py"
```

This was not run against the live farm. The missing normal source receipt is
the Runtime checkout requested by the selected Agent lock:

```text
/home/user/work/wt/rt-pin-45c3a7f4
commit 45c3a7f476e1c5f74fafc15956a58b9871eee21f
```

It must be obtained by the normal route, not guessed or replaced:

```bash
"$ORCH/bin/request-checkout" runtime 45c3a7f476e1c5f74fafc15956a58b9871eee21f
```

The current farm has `agent full`, but no `agent full-farm` row or actual
full-farm snapshot/log. The current full row is preserved as an 86-byte
baseline (SHA-256 with LF:
`65fd24facbce3b1661aaedab1967033a2b2c7d00345a92b0bd8db7969673c184`).

## Exact approved Remotion inputs

The two `.b64` files are copied byte-for-byte from the historical approved
1835 packet. Decode without trimming or normalizing. The row is 709 bytes with
its final LF; its hash excluding that LF is
`ffdb0b13c65f106d7b818208343feb3f438dfc943f4af57c5f612ddcf73dc036`.
The env is 523 bytes with hash
`e53a69a465e05976dcf7a781f420b1c7def64a13691f7a5f387f6a0609a6da02`.
The source packet declares four env keys only: `PATH`,
`ASTRID_REMOTION_PROJECT_DIR`, `ASTRID_NODE_EXECUTABLE`, and
`ASTRID_TIMELINE_SCHEMA_PYTHONPATH`; no credentials are added.

Use the existing Remotion registration/import path. Preserve all current and
final rows and every outside byte; refuse on any baseline drift. Do not change
the maker allowlist, approved profile, toolchain, or Runtime pin.

## New full-farm registration candidate

`registration-row.txt` is the proposed new row:

```text
agent full-farm env ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-45c3a7f4 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-45c3a7f4" /home/user/work/venv-agent/bin/python -m pytest -q -n 3
```

Its test command is exactly the current farm `agent full` command. The only
added bindings are `ASTRID_RUNTIME_CHECKOUT` and the matching integration-style
`PYTHONPATH`. The Runtime commit comes only from the selected
`/home/user/work/agent/runtime.lock.json` `source_commit`; no ambient HEAD or
alternate checkout is acceptable.

If this row is generated for a managed bench, register it in the same
transaction through the existing `Store.ensure` registration API and its
existing builder/verifier. Do not hand-edit `index.json`, `owner.json`,
`suites.conf`, or an env file. The registration identity, child tuple, build
receipt, and actual checkout must come from the normal request/checkout route;
they are intentionally not invented in this candidate packet.

## Safe install/rollback instructions

An independently authorized worker should, in UTC order:

1. Capture baseline SHA-256 and byte manifests for `bench_store.py`,
   `tests/suites.conf`, the relevant env files, current/final rows, and all
   outside bytes. Refuse if any expected baseline hash or row count differs.
2. Capture a timestamped backup under its private `TMPDIR`, then decode the
   two approved attachments and run exact `cmp`, byte-count, LF, row-parse,
   and credential-key checks.
3. Run the helper above for the exact farm ORCH/tests and absent store. Let
   `Store.initialize` perform creation and let the existing store transaction
   perform any registration/projection. Use its fsync/atomic replacement and
   journal recovery; do not append or replace files by hand.
4. Recompute the complete manifest and verify that only the intended new
   registration row/env changed. On drift, refusal, or failed verification,
   stop; use the existing `Store.recover` transaction path and restore the
   UTC backup only after the same baseline checks pass.

No installer, daemon, hub-sync, provider, socket, full-suite, or live farm
operation is part of this candidate.

Full C0 v2 request/result fields, labels, steps, ordinals, patches, reads,
merge/key/dry-run behavior, and accepted/merged/conflict/invalid/preview
records remain unchanged.
