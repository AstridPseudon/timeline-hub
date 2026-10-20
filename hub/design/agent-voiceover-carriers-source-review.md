# WC5 voiceover carrier source review

Date: 2026-10-20 UTC. Reviewed only the deltas from Agent base
`c0644cf1a7b63c9bcff7f70502b953a07879c9f3`; no composition, freeze, generation,
pinning, or HTTP work was performed.

## Decisions

### `tl/agt-m2-occurrence-audio-media-native` — APPROVE

Approved as a bounded future WC5 carrier source. The delta is limited to
verified `audio/*` admission in `_media_inputs.py`, audio-vs-visual raw-track
selection in `native_occurrence_media_commands.py`, and conformance coverage.

- The command wire remains the closed five-field `MediaSelection`; the
  candidate schema is unchanged at 58 definitions / 32 operation conditions,
  with raw schema SHA-256
  `27f2e3edaffdfc49665a858c5c1d6989dd89ef200932679b77367bc459329cfb`.
- Audio requires the existing exact Runtime-verified selection, positive size,
  and finite-positive server-carried `duration_seconds`. Source `from`/`to`,
  `hold`, `speed`, and occurrence bounds remain in seconds; no caller duration,
  probe, clamp, or audio-as-visual fallback is introduced.
- Audio requires an already-existing active raw child track with `kind: audio`.
  The operation does not create/adopt a raw track. Existing create-or-require
  registry binding behavior remains exact, and the media kind is preserved on
  swap.
- The existing operation names, occurrence ownership/isolation, raw child
  identity, dependency recording, and guarded inverse remain unchanged. The
  real-WAV case records the exact five-field selection and strictly restores;
  malformed duration and wrong-track refusals leave the bundle unchanged.

No counterexample was found in the requested delta. This approval does not
qualify Runtime managed-object admission, native HTTP, CAS custody, historical
unregistered audio, automatic track birth, placement/ripple retiming, or the
outer producer/requester settlement. Those remain separate future gates.

### `tl/agt-m2-voiceover-provenance-property` — APPROVE

Approved as a bounded informational metadata carrier source. The delta adds
only the closed `shot.set` leaf `payload.metadata.draft_voiceover` (object or
explicit `null`) and its explicit clear spelling. It does not add a producer,
Runtime authority, task/run/media authorization, endpoint, DTO, or legacy
writer.

- `shot.set` still requires explicit occurrence ownership and writes only the
  leaf. Existing metadata siblings, unknown/namespaced fields, settings,
  source/root identity, and sibling occurrences are preserved; no whole-shot,
  root, or metadata replacement occurs.
- Set, explicit `null`, and explicit clear remain distinct. The recorder keeps
  exact leaf before/after state, including absent/null metadata-container
  presence; inverse restores absent and null containers exactly.
- Disjoint leaf rebase succeeds, same-leaf ABA/intervening writes block
  inverse, and shared-occurrence sibling isolation holds. The original
  voiceover fixture is consumed as data; its text/digest/settings/audio/run/task
  and base fields are not rewritten by this carrier.
- The complete schema candidate hashes to the documented
  `65bb68acbfbc72dabbbc83eab66e5309fe5cf5f42c1acb4bc821c62434742a1e`, while
  removing only this leaf reconstructs the prior group candidate hash
  `27f2e3edaffdfc49665a858c5c1d6989dd89ef200932679b77367bc459329cfb`.

No counterexample was found in the requested delta. The leaf intentionally
does not authenticate or authorize any value inside the provenance object;
future Runtime/producer authority must continue to use the existing guard,
receipt, and settled-artifact path.

## Evidence

Candidate trees were tested from the two branch refs in private temporary
directories using the shared Agent venv (no shared dependency was modified).

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$TREE /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recipe_occurrence_media.py tests/editing_conformance/test_recipe_m2_parent_media.py tests/editing_conformance/test_recipe_m2_placement.py tests/editing_conformance/test_recipe_m2_shot_pool.py tests/sdk/test_timeline_current_union_schema.py tests/sdk/test_timeline_materialization_schema_union.py
295 passed in 173.07s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$TREE /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recipe_shot_set.py tests/sdk/test_timeline_materialization_schema_union.py
85 passed in 3.00s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$TREE /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/packs/video_editing/test_draft_voiceover.py
22 passed in 0.27s

/home/user/work/venv-agent/bin/python -m ruff check --no-cache [all changed Agent Python files in each candidate]
All checks passed (both candidates).

git diff --check c0644cf1a7b63c9bcff7f70502b953a07879c9f3 <audio-ref>
PASS
git diff --check c0644cf1a7b63c9bcff7f70502b953a07879c9f3 <provenance-ref>
PASS
```

Additional focused probes passed: setting from absent/null metadata roots and
exact inverse, clearing an absent leaf, and updating one shared occurrence
while preserving its sibling. No full suite, live socket, Runtime HTTP,
composition, release, or pin was run/requested.

## Follow-up boundary

The future tuple remains separate from current `392`. Before any adoption,
qualify the Runtime-managed audio admission and the normal outer
`video_editing.sync_draft_voiceover` requester/settlement path independently;
do not treat this informational leaf as Runtime authority or as proof of a
completed audio placement/timing carrier.
