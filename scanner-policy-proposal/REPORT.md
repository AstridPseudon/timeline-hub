# Agent scanner semantic-policy proposal

Status: **UNAPPLIED; review handoff only**.

Agent integration base: `33b0a8385f2cd184f0e79544f78678bc0dbee0d7`.

This proposal is based on the completed ORCH-owned bounded-reference scanner
v1.0.1 copy. It keeps the existing Agent projector, clip-field codec,
registry, rational-FPS helper, and half-open timing helpers as the only
semantic authorities. It always leaves `clean_claim` false and reports only
bounded IDs/pins, property names, source paths, frame ranges, and inventory
labels.

Implemented policy changes:

- `curve_honoured` is emitted only for an explicitly present non-linear curve;
  absent and explicit `linear` curves remain represented by
  `continuous_audio_fade`, while invalid explicit curves are `unknown`.
- Element look findings use declared codec fields, including `crop_*` and
  `speed`; singleton look-bearing elements are listed; half-open overlaps are
  checked across tracks and pairs with no look fields are omitted.
- Media `entrance`/`exit` declarations are retained in a bounded
  `media_look_inventory`.
- Canonical transition declarations are retained in a bounded
  `transition_boundaries` inventory with incoming semantics; conversion and
  renderer presence/alpha/pixel coverage remain in `not_covered`.
- Projected track/asset context paths are explicitly prefixed with
  `projected.`.
- Internal revision source positions use the original input-list indexes while
  occurrence-prefixed clip keys retain occurrence identity.

The ambiguous `not_covered` portion was held until the exact Agent second-pass
review was located on
`refs/remotes/hub/timeline/agent/tl/agt-reviews-audio-mouth-scanner`,
`design/agent-review-viewing-20261020b.md`. The proposal follows that review's
bounded inventory requirement and does not invent conversion or pixel
semantics.

## Evidence

Targeted synthetic proposal tests:

```text
/home/user/work/venv-agent/bin/python -m pytest -q scanner-policy-proposal/test_owner_film_cliplook_scan.py --agent-root "$PWD"
22 passed
```

Static checks:

```text
/home/user/work/venv-agent/bin/ruff check scanner-policy-proposal/owner_film_cliplook_scan.py scanner-policy-proposal/test_owner_film_cliplook_scan.py scanner-policy-proposal/conftest.py
All checks passed

/home/user/work/venv-agent/bin/python -B -m py_compile scanner-policy-proposal/owner_film_cliplook_scan.py scanner-policy-proposal/test_owner_film_cliplook_scan.py scanner-policy-proposal/conftest.py
passed
```

No full, browser, render, network, install, database, credentials, media,
socket, service, or owner-film run was performed. No Agent product files or
published archives were modified.
