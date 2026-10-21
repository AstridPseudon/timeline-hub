# Runtime private15 Speech-compatible source

Date: 2026-10-21 UTC

## Disposition

Prepared a new private C3d descendant containing only the approved Speech WAV
fallback and the preserved audio/Speech settlement tests. This is a compatible
private source candidate, not a merge, release, consumer pin, activation, or
outer-workflow qualification.

The immutable candidate is committed as
`3e6c173128400c81842cd423d9ac90a76f54bf41`, with exact tree
`322859f268fcdcae5872aa2e3ccdcb2a288d76fb` and parent C3d
`c3d26567ff6fe4e20a959476d40aff90ad23a0ca`. The SHA is read from the
repository ref, not inferred from the tree or test-service snapshot.

## Exact identities

| Identity | Commit / tree or digest |
| --- | --- |
| Immutable C3d base | `c3d26567ff6fe4e20a959476d40aff90ad23a0ca` / `f3ae49d38454ce73a9c91a954bb530b3ce51c122` |
| Ordinary approved source | `d7597d5440d5ed5d5912235d547cb4380d226980` / `e1663a36fb6400af2a32479574fbe60d16d86443` |
| Final audio-positive restoration | `40708263d26ef39ac484cbc9f1ae7f34cfc368bc` / `6abc2f117391de8e7e35c0283f575a002199894d` |
| Final compatible private server | `3e6c173128400c81842cd423d9ac90a76f54bf41` / `322859f268fcdcae5872aa2e3ccdcb2a288d76fb` |
| Product source blob | `runtime_protocol/store.py` = `5415a62fbc4692c110017245ceda12260e25629b` |
| Settlement test blob | `tests/test_generation_publish_v1_settlement.py` = `a5317ce82f008cc4cfd8d86f73e5c95e50a567dd` |

The two candidate path blobs exactly match the final restoration source. The
product blob is unchanged from d759 and contains only the one condition that
accepts `output_port` `audio` or `speech` for the existing verified primary WAV
header fallback.

## Producer and artifact identity retained from C3d

- Private contract/client version: `0.2.15`.
- Raw command schema SHA-256: `sha256:84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc`.
- Workspace schema digest: `sha256:07c0668b2fb16226475429ec65637404c0b2e885e1b88e67f896e249089d6680`.
- Component manifest SHA-256: `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5`.
- Artifact producer: `astrid-runtime`; artifact manifest has 76 entries and
  version `sha256:2df8ebf4fb17cae1b62e78a262b2b20b393770d045d0ef8748207ac7efacbfbb`.
- The C3d generated clients, health/contract metadata, manifest, private
  materialization joins, and all other producer/source bytes remain unchanged.

## Allowlist and byte comparison

Only these two repository paths differ from C3d:

```text
M runtime_protocol/store.py                         1 insertion, 1 deletion
M tests/test_generation_publish_v1_settlement.py   43 insertions, 10 deletions
```

The test delta is the exact final restoration: the positive settlement test is
parameterized over `audio` and `speech`; the speech helper and controls use the
declared Speech port; and the exact-replay neighbor is retained. Explicit
null/value, absent duration, malformed WAV, zero-rate WAV, and authenticated
read controls remain present. No sidecar, caller duration, metadata/catalog
backfill, schema/API/client/version change, generation, consumer pin, or
canonical timeline write was added.

`git diff --quiet HEAD -- . ':(exclude)runtime_protocol/store.py' ':(exclude)tests/test_generation_publish_v1_settlement.py'`
passed. Thus every path outside the allowlist is byte-identical to C3d,
including the 0.2.15/raw84fc/all76 producer material and all source/custody,
owner, cancellation, and one-shot guards.

The committed product blob exactly matches the independently approved ordinary
Speech fix at `d7597d5440d5ed5d5912235d547cb4380d226980` and the final
audio-positive restoration at `40708263d26ef39ac484cbc9f1ae7f34cfc368bc`.
The committed settlement-test blob exactly matches the latter restoration.
An independent tree walk found 453 paths in both C3d and this candidate, with
only the two allowlisted paths changed. The candidate's 76 artifact entries
also all match their committed bytes; generated client, health, contract
metadata, release, and artifact-manifest blobs are unchanged from C3d.

## Evidence

Local focused cases on this candidate:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
  'tests/test_generation_publish_v1_settlement.py::test_speech_settlement_derives_wav_duration_for_exact_media_selection[audio]' \
  'tests/test_generation_publish_v1_settlement.py::test_speech_settlement_derives_wav_duration_for_exact_media_selection[speech]' \
  tests/test_generation_publish_v1_settlement.py::test_speech_settlement_exact_replay_returns_original_result \
  tests/test_generation_publish_v1_settlement.py::test_speech_settlement_invalid_wav_keeps_duration_unknown_and_selection_refused \
  tests/test_generation_publish_v1_settlement.py::test_speech_settlement_preserves_explicit_null_duration_and_refuses_selection \
  tests/test_generation_publish_v1_settlement.py::test_speech_settlement_zero_rate_wav_keeps_duration_unknown_and_selection_refused \
  tests/test_generation_publish_v1_settlement.py::test_speech_settlement_preserves_explicit_duration_metadata
```

Result: **7 passed in 1.10s**. `git diff --check` also passed.

Central exact-file run:

```text
request-test rt-m2-private15-speech-compatible-source-0349 targeted --files "tests/test_generation_publish_v1_settlement.py"
```

Run `rt-m2-private15-speech-compatible-source-0349-targeted-1021034850-22641`:
**17 passed in 2.31s**, exit 0. This includes the authenticated HTTP/socket
read case. No full, browser, render, model, TLS, old-root, or outer workflow
run was requested.

## Agent handoff

The exact server for the reciprocal handoff is
`3e6c173128400c81842cd423d9ac90a76f54bf41` /
`322859f268fcdcae5872aa2e3ccdcb2a288d76fb`; the C3d producer/client/health/
artifact identity remains the unchanged `c3d26567ff6fe4e20a959476d40aff90ad23a0ca`
source cohort. On this compatible server, Agent should create a fresh ephemeral fixture with
duration key absent, then retry only the previously failed selection or
prerequisite. If that succeeds, proceed to the genuine outer workflow under
the already reviewed authority and custody boundaries. Runtime unit and HTTP
coverage here must not be reported as root or outer-workflow success. Keep
explicit null/value, ledger-first retry, sidecar non-authority, and all C3d
guards unchanged.

