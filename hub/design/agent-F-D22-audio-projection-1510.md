# F-D22 audio projection diagnosis

Status: **FAIL / existing owner-scope question; no source fix**.

Base Agent: `58316fd6e0ce8a1fb3b2b3826ec71906d29080de`  
Runtime: `3b926efab2eed122d374540baee297d4cdcec62a`  
Node: `v20.19.4`  
Composition archive SHA-256: `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`

## Causal finding

The two retained failures in
`tests/editing_conformance/test_compile_contracts.py` assert
`audio.render_source` on the result of the pure graph projection. The
projection at `astrid/core/timeline/shot_composition_projection.py:314-389`
has only graph/occurrence input. It preserves the exact authored fade params,
source window, labels, occurrence/media identity, opaque fields, and absent
`render_source`; it has no verified source bytes, materialized registry,
attempt directory, asset server, or public envelope result from which to name a
prepared file.

The existing trusted producer is already wired in
`astrid/packs/rendering/rendering/renderers/remotion/root_preparation.py:236-249`.
It calls `prepare_normal_audio_sources()` only after managed materialization
and server setup. That producer checks the resolved registry and source digest,
uses public Composition trim/rate and envelope helpers, writes an
attempt-owned WAV, then attaches the server URL plus exact
`envelope_key/source_from/playback_rate`. The locked Composition test admits
one exact tuple and rejects four forged variants. Therefore adding a
`render_source` in projection would be an invented unauthenticated source and
would violate existing guards.

## Evidence

- Retained profile qualification: **34 pass, 6 fail** across the exact 40
  nodes; only these two audio vectors are the compile failures. The fixture's
  `xfail` prose is not a pytest marker.
- Retained exact two-vector trace: **2 failed, 27 deselected** at the boolean
  `audio.render_source` lookup.
- Bounded existing source controls under the requested profile, after removing
  inherited forbidden `NODE_OPTIONS`/`NODE_PATH`: **3 passed in 1.15s**.
- Public Composition admission/forgery control: **1 passed, 1 warning in
  0.52s**.
- `git diff --check`: pass; no worktree changes.

Relevant source hashes: `shot_composition_projection.py`
`6f2cd27d9cdfb16ffd6d1c351c204dfd750d3182001c52333d92a91118c17115`,
`normal_audio.py`
`00e46437f1199488260fa6b3409297eddbb2b827ec7a1d0be1b6fff3fbf2b74a`, and
`root_preparation.py`
`71e38ad87d9dd52a9f18a58b2c6122fa87a49d5b2fcc1b07e575f8400c61a61b`.

## Required decision / owner

This is not an Agent projection repair. The fixture/contract owner must decide
whether these expectations are to be moved into an authenticated host
preparation integration fixture, or whether a separately funded cross-layer
fixture seam should connect this logical graph to the existing trusted
producer. The present fixture has no verified media bytes or attempt URL, so no
legitimate bounded fixture correction is available. No code, fixture, xfail,
skip, or positive assertion was changed.
