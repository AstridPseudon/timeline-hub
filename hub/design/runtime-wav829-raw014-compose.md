# Runtime WAV829 + raw014 composition

Date: 2026-10-20 UTC

## Result

Prepared a private Runtime candidate from `7d1cfa6b1da0c50bb8a9d3430dcaa6272b20b55e`
(`ac693097189637d3bd0fc3a39299d9b166758853`) with the approved cumulative
WAV829 settlement delta. The candidate remains uncommitted in the worker
worktree; the harness will assign the commit SHA after exit. Central snapshot
tree: `5c81a9445bd4d6db11b3de11a93940f13c539a28`.

The source delta is limited to:

- `runtime_protocol/cas.py`: descriptor-stable WAV header inspection, including
  non-positive-rate and invalid-duration refusal.
- `runtime_protocol/store.py`: existing `generation.publish_v1` variant
  metadata enrichment, with explicit output duration presence carried only
  transiently and fallback derivation only when duration is absent.
- `runtime_protocol/service.py`: transient explicit-null presence map passed to
  the existing settlement path; no result, receipt, event, catalog, DTO, or
  private wire carrier mutation.
- `tests/test_generation_publish_v1_settlement.py`: valid, invalid, explicit,
  explicit-null, and zero-rate WAV boundary coverage.

The current raw014 base remains exact: `runtime_protocol/timeline_commit_port.py`
and `tests/test_timeline_raw_audio_port.py` are unchanged. Generated contract
files and `contract/artifacts.json` are unchanged; the artifact check reports
75 entries and retains the approved `f021e771` artifact and `6ba7b51e` schema
identity. No API/schema/version/table/client metadata, canonical timeline write,
variant-append, regeneration, renderer, model, or voiceover activation was
added.

## Evidence

Local focused lane:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider tests/test_generation_publish_v1_settlement.py tests/test_timeline_raw_audio_port.py
22 passed in 7.77s
```

Local checks:

```text
git diff --check
/home/user/work/venv-runtime/bin/python generators/generate.py --check
/home/user/work/venv-runtime/bin/python scripts/artifact_manifest.py --check
```

All passed. The central targeted snapshot run was:

```text
request-test rt-m2-wav829-raw014-compose targeted --files "tests/test_generation_publish_v1_settlement.py"
/home/user/work/venv-runtime/bin/python -m pytest -q tests/test_generation_publish_v1_settlement.py
14 passed in 3.42s
```

This includes the authenticated HTTP selected-media path. The separate named
`current-http-cli-durability` request was not usable because its wrapper failed
before test collection on a missing `/home/user/work/wt/rt-m2-init3c4f-server7d1-pair`
checkout; it was not resubmitted.

No broad/full/speech-model suite was run. The latest strict parent tests remain
open and were not altered; no dropped assertion claim is made.

## Handoff

WAV829 final review approved `8292b94dc463e28808cd57e20a6aa372d474837b` in its
original lineage. This composition is a private candidate only, not a merge or
voiceover activation. After harness commit, send the assigned candidate SHA and
the central snapshot identity to the Agent INBOX with status **reviewed WAV829
delta; HTTP/boundary qualified; adoption pending**. No SHA is invented here
because the harness has not committed the worktree yet.
