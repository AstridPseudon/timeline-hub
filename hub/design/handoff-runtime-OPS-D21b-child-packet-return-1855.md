# Runtime handoff: OPS-D21b child-reuse packet return — 1855

## Result

Created a new immutable 1855 packet under the unique prefix
`handoff-runtime-OPS-D21b-child-packet-return-1855-*`. The 15 payload files
are byte-for-byte copies of the current 1839 final export; the completed
15-entry manifest was written after all payload copies and checks. The old
1839 files and its manifest were not modified.

The settled D21c option A is recorded: the reusable bench identity is keyed
by Agent SHA + Runtime backend SHA + generated-client tuple. This is a
source/evidence packet, not an installation or full-D21b
qualification.

## Drift causality and limits

The 1839 manifest still records the prior `validation.log` SHA256
`1e4293ddaeb19b21feb746110709edcab149bc7b1bdcf3f01b5890c0724da544`, while
the current captured flat log is
`d75c1e5ddb112320ba9b8fe60c0f154997f7b4d0ccc7ff29060c48d3d77c8551`.
The 1852 independent review reported exactly this one-entry mismatch and
explicitly did not rewrite either old evidence file. The 1839 assembly trace
shows the validator output being redirected to the flat validation-log path;
the 1852 review command used the validator without a flat-log redirect. Thus
this is export/log drift, not a custody-control or source-script change. The
exact later write event cannot be reconstructed beyond that trace, so this
packet preserves the current captured bytes and records the drift rather than
regenerating the old log or changing the old manifest.

Independent 1852 evidence is reused because the scripts are unchanged:
97/97 custody controls, normal and `env -i` caller flows, source validation,
and the independent scoped checks all passed there. Those behavior controls
and installs were not rerun for this packaging-only return.

## New packet identity

Manifest: `handoff-runtime-OPS-D21b-child-packet-return-1855-hashmanifest.sha256`

Key script hashes:

```text
fcfe7736fa9067e8f76eb2240d2c6fee3791ac2a7447b08025fcf961f40b0d7d  make-child-venv.sh
dfb377aaa988d4a4e01c01bda470049b0b3acc8da7275180641a490aa8661443  request-child-venv.sh
b318e1f1a0915b58d96861c3f8ab20356b5c16117630acc5b2fa5395f0e9f40a  validate-packet.py
```

Captured-log hashes:

```text
87e62c1860e0bc283e007aac89e78b2a9a4f28b96690bef077643dba57d8b713  security.log
13878dfed6f284f271798d01d8cdb9defe82a5e28dadc36d5ea17a7e5080e76a  dispatcher.log
d75c1e5ddb112320ba9b8fe60c0f154997f7b4d0ccc7ff29060c48d3d77c8551  validation.log
1adfe5010b72f93bb0742a4b15d87c9ba6a18d013da7388498184ec0ce0fa4d0  cmp.txt
```

The manifest contains all 15 payload hashes and excludes itself; no manifest-
mutating script is included in the manifest set. Payload size is 134,692
bytes; payload plus manifest is below 1 MiB.

## Exact checks

All commands below completed with exit 0 unless stated otherwise:

```bash
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
D="$ORCH/design"
OLD="$D/handoff-runtime-OPS-D21b-child-reuse-bounded-sol-1839"
NEW="$D/handoff-runtime-OPS-D21b-child-packet-return-1855"
for suffix in -make-child-venv.sh -request-child-venv.sh -fixture-python.sh \
  -fixture-sources.py -test-child-reuse.py -test-dispatcher.py \
  -validate-packet.py -make-child-venv.patch -request-child-venv.patch \
  -make-child-venv.from-1811.patch -request-child-venv.from-1811.patch \
  -security.log -dispatcher.log -validation.log -cmp.txt; do
  cmp -- "$OLD$suffix" "$NEW$suffix"
  sha256sum "$OLD$suffix" "$NEW$suffix"
done

bash -n "$NEW-make-child-venv.sh"
bash -n "$NEW-request-child-venv.sh"
bash -n "$NEW-fixture-python.sh"

TMPDIR=/tmp/w-de657a8476 python3 "$NEW-validate-packet.py" \
  > /tmp/w-de657a8476/packet-validation-1855.log 2>&1

git diff --check
git diff --exit-code HEAD --

(cd /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design \
  && sha256sum -c handoff-runtime-OPS-D21b-child-packet-return-1855-hashmanifest.sha256)
```

The new-prefix validator passed Python/scoped Runtime compilation, four exact
patch replays, Runtime clean/diff checks, and the captured 1826 script identity
checks. New packet `sha256sum -c` passed **15/15**. Scratch was 3,740 bytes
(under the 1 MiB limit); the permanent packet plus this report remains under
1 MiB. No queue, bench, network, provisioner, daemon, HOST/product test,
generated file, pin, install, or Git write was performed.

Next: independent package-custody review of the 1855 packet. No repeated
behavior review is needed unless a source byte changes.
