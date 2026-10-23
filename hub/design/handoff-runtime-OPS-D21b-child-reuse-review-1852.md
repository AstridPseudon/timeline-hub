# Runtime handoff: OPS-D21b child-reuse independent source review — 1852

**Verdict: FAIL.** The 1839 packet's private behavior checks pass, but its
exported hash manifest fails exact verification: 14/15 entries pass and
`handoff-runtime-OPS-D21b-child-reuse-bounded-sol-1839-validation.log` fails.
The manifest expects SHA256
`1e4293ddaeb19b21feb746110709edcab149bc7b1bdcf3f01b5890c0724da544`;
the current flat export is
`d75c1e5ddb112320ba9b8fe60c0f154997f7b4d0ccc7ff29060c48d3d77c8551`.
I did not rewrite either evidence file.

Fresh private behavior reruns all exit 0; the separate hash check exits 1:

```bash
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
P="$ORCH/design/handoff-runtime-OPS-D21b-child-reuse-bounded-sol-1839"
TMPDIR=/tmp/w-c12e5734ef python3 "$P-test-child-reuse.py"
TMPDIR=/tmp/w-c12e5734ef python3 "$P-test-dispatcher.py"
TMPDIR=/tmp/w-c12e5734ef python3 "$P-validate-packet.py"
(cd "$ORCH/design" && sha256sum -c "$P-hashmanifest.sha256")  # exit 1: one stale hash
```

- `test-child-reuse.py`: **97/97 custody controls passed**, including Agent
  full-source/metadata/direct-url/all-RECORD ownership, Runtime backend/client
  source custody, read-only/integrity, changed-key/new-build refusals,
  malformed/partial/ambiguous/symlink/race/wrong-source cases, and no
  existence-only acceptance.
- `test-dispatcher.py`: normal and `env -i` exact request-writer → extracted
  dispatcher branch → private mock-maker payloads passed; private roots were
  asserted before every execution.
- `validate-packet.py`: shell syntax, scoped Runtime compile, installed and
  1811 patch replay/cmp, 1826 byte identity, clean Runtime status and exact
  base `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d` passed.

Private peak was 990,815 logical / 2,109,440 allocated bytes; the flat packet
is 136,793 bytes. No shared requester/daemon/queue/bench/provision/network,
product/test/generated/pin change or install was performed. D21c option A is
preserved: Agent SHA + Runtime backend SHA + generated client tuple. The
qualified 1839 custody input remains input to unique creator 1850, not a
separate installation.

Next step: reconcile/re-export the changed validation log and manifest, then
repeat this independent review. Real installed-bench qualification remains
unverified by design.
