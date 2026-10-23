# Runtime handoff: OPS-D21b child-packet independent custody review — 1858

## Result

**PASS — `newimmutablepacket`.** The new immutable 1855 packet is internally
consistent and preserves the independently reviewed 1852 source bytes.

All 15 new payloads are byte-for-byte and SHA256-identical to the current 1839
payloads, including maker/requester/fixture sources and the evidence logs. The
new post-copy manifest verifies **15/15**. The current Runtime worktree is
clean at base `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`.

## Custody and drift boundary

The old 1839 artifacts were not modified during this review, and the new
payloads compare equal to their current bytes. The old manifest still reports
the one known 1852 failure: `validation.log` records
`1e4293ddaeb19b21feb746110709edcab149bc7b1bdcf3f01b5890c0724da544`, while
the current old/new validation payload is
`d75c1e5ddb112320ba9b8fe60c0f154997f7b4d0ccc7ff29060c48d3d77c8551`.
The other 14 old manifest entries pass. The new manifest records the current
validation payload and passes all 15. This is accurately labeled as the sole
historical export/log drift; no historical behavior or custody evidence was
upgraded, regenerated, or treated as fresh.

The 1852 behavior/source result is inherited exactly because no source byte
changed: its 97/97 custody controls, normal and `env -i` caller flows, and
source validation remain the qualified evidence scope. This review did not
rerun those behavior checks or install an old kit.

## Exact checks

```bash
# Inline read-only assertions: all 15 old/new cmp+hash pairs; manifest set;
# new 15/15; old drift exactly validation.log.
python3 - "$OLD" "$NEW" <<'PY'
...
PY

(cd "$D" && sha256sum -c \
  handoff-runtime-OPS-D21b-child-packet-return-1855-hashmanifest.sha256)
# PASS: 15/15 OK.

(cd "$D" && sha256sum -c \
  handoff-runtime-OPS-D21b-child-reuse-bounded-sol-1839-hashmanifest.sha256)
# Expected historical result: 14 OK, validation.log FAILED, rc=1.

TMPDIR=/tmp/w-39949277c1 python3 \
  "$D/handoff-runtime-OPS-D21b-child-packet-return-1855-validate-packet.py"
# PASS: bash syntax, scoped compile, patch replay/cmp, 1826 identity,
# git diff --check, clean Runtime status, exact base diff.
```

The validator output was PASS with no product/shared infrastructure writes.
Scratch was about 216 KiB, below 1 MiB; permanent packet/report material is
below 1 MiB. No queue, bench, daemon, network, provision, host, install,
generated-file, pin, product test, or product typecheck/lint action occurred.

D21c remains settled Agent SHA + Runtime backend SHA + generated-client tuple;
there is no separate old-kit installation or new decision gate. Creator 1850
owns the bench-store adapter. Production caller route, full C0v2 schemas, and
frozen34e remain unchanged.

Recommended next step: accept the 1855 packet as the immutable source/evidence
packet, while retaining the explicit limitation that real installed-bench
qualification was not performed.
