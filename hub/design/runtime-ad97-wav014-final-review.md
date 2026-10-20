# Runtime ad97 WAV829 + raw014 final review

Date: 2026-10-20 UTC

## Decision

**APPROVE private candidate only:** `ad97e16effc53fa13f91c43f076f6edb3c38985f`
(tree `5c81a9445bd4d6db11b3de11a93940f13c539a28`). This is not a public pin,
release, integration adoption, or actual voiceover-workflow qualification.

The candidate is the exact two-parent composition of raw014 `7d1cfa6b1da0c50bb8a9d3430dcaa6272b20b55e`
(tree `ac693097189637d3bd0fc3a39299d9b166758853`) and approved WAV829
`8292b94dc463e28808cd57e20a6aa372d474837b` (tree
`de34d64765611dd2baa09ff3533c448f11cab702e`) over base
`e2db1e8cc7c176fafa1e4e651da3639b6e3a89dd`.

## Exact scope and preservation

The first-parent delta is exactly:

- `runtime_protocol/cas.py`
- `runtime_protocol/store.py`
- `runtime_protocol/service.py`
- `tests/test_generation_publish_v1_settlement.py`

The raw014 base and declared-pin/single-FD/acceptance-recheck/ledger-first
behavior are unchanged. In particular, the candidate has byte-identical
protected blobs for `runtime_protocol/timeline_commit_port.py`,
`tests/test_timeline_raw_audio_port.py`, `contract/artifacts.json`,
`contract/manifest.json`, and `contract/component-manifest.json` relative to
raw014. The 75-entry artifact manifest remains unchanged and carries the
ordinary014 identities: artifact `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0`,
raw schema `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`,
wire schema `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`,
and 55 definitions / 29 operations.

The WAV delta is limited to the existing settlement path. Explicit output
`duration_seconds` presence, including explicit `null`, is carried only in a
transient map. It is not a wire result field, receipt, event, catalog field,
or new stored presence flag. A missing speech WAV duration is derived from
one verified CAS descriptor; invalid or zero-rate WAVs remain unknown and the
existing media-selection refusal remains in force. Existing generation-level
explicit metadata is not rewritten.

Accepted settlement replay is checked before lease validation, staging, CAS
access, and enrichment. The independent replay probe below made both CAS open
and settlement enrichment fail on the second identical request; the stored
accepted result still returned unchanged.

The existing 014 parent-ownership pre-adoption transition remains explicitly
open and named, not quietly removed: `tests/test_timeline_clip_replacement.py::test_native_parent_clip_swap_route_replaces_parent_media`
still carries its public-schema pre-0.2.14 xfail marker. This review does not
claim that transition or the outer voiceover action is qualified.

## Evidence

Exact candidate snapshot checks:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$CAND" /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider tests/test_generation_publish_v1_settlement.py tests/test_timeline_raw_audio_port.py
22 passed in 13.97s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$CAND" /home/user/work/venv-runtime/bin/python generators/generate.py --check
passed

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$CAND" /home/user/work/venv-runtime/bin/python scripts/artifact_manifest.py --check
contract/artifacts.json is current

git diff --check 7d1cfa6b1da0c50bb8a9d3430dcaa6272b20b55e ad97e16effc53fa13f91c43f076f6edb3c38985f
passed
```

Independent candidate-only replay probe:

```text
accepted replay returned before CAS/enrichment: PASS
```

The inherited central targeted settlement run on candidate tree
`5c81a9445bd4d6db11b3de11a93940f13c539a28` reported **14 passed**. The
approved WAV829 central HTTP/security neighbor run reported **29 passed**;
the candidate does not change that HTTP implementation surface. The separate
current HTTP/CLI wrapper was not usable because it references the absent
`/home/user/work/wt/rt-m2-init3c4f-server7d1-pair` checkout. No full, broad,
speech-model, renderer, or live outer-voiceover workflow suite was run.

## Agent handoff

The exact private cohort metadata was sent to the Agent manager inbox for a
future outer-voiceover qualification only:

- Runtime candidate: `ad97e16effc53fa13f91c43f076f6edb3c38985f`, tree
  `5c81a9445bd4d6db11b3de11a93940f13c539a28`.
- Immutable ordinary014 artifact/client producer: `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`,
  tree `4b7dd0fe44be973c344bab3de568eaf0bdd28476`.
- Frozen Agent source: `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3`.
- Raw schema: `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.
- Runtime wire: `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`.
- Artifact: `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0`;
  75 artifacts / 55 definitions / 29 operations.

This handoff is metadata for a future outer `video_editing.sync_draft_voiceover`
qualification. It is not a claim that the actual outer workflow has been
submitted, settled, or qualified. No public pin, release, or integration
adoption is authorized by this review.
