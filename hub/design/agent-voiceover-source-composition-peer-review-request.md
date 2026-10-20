# Runtime/App peer source review request: voiceover source composition

Request Runtime and App managers to independently review this bounded private
Agent source candidate before any freeze, merge, or adoption.

## Exact candidate

- Worktree: `/home/user/work/wt/agt-m2-voiceover-source-composition`
- Base source candidate: Agent `01610632816f9957de061138a146709b3a0aae6b`
  (`tl/agt-m2-voiceover-provenance-property`)
- Composition delta: only the audio slice from
  `tl/agt-m2-occurrence-audio-media-native` (`0daecba974228ad5de7a5b3f7d21fa941671a3d1`),
  applied against its common base `c0644cf1a7b63c9bcff7f70502b953a07879c9f3`.
- Current source changes are uncommitted by worker policy; inspect the worktree
  diff, not a claimed commit.

Product files in the composed candidate:

```text
astrid/sdk/timeline/_media_inputs.py
astrid/sdk/timeline/native_occurrence_media_commands.py
astrid/sdk/timeline/_shot_commands.py
```

The first two accept verified `audio/*` with finite-positive intrinsic duration
and require an explicit active raw `kind: "audio"` child track. The existing
five-field `MediaSelection`, occurrence-owned command identity, source window,
hold/speed policy, registry capture, and inverse machinery are reused. The
existing `shot.set` carrier writes only `metadata.draft_voiceover` and preserves
opaque metadata siblings.

## Exact identity floors

- Complete schema candidate: `65bb68acbfbc72dabbbc83eab66e5309fe5cf5f42c1acb4bc821c62434742a1e`
- Group floor: `27f2e3edaffdfc49665a858c5c1d6989dd89ef200932679b77367bc459329cfb`
- Private project-data floor (`392`): `39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d`
- Private carrier floor (`613`): `613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3`
- Ordinary floor (`6ba`): `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`

Product-source hashes:

```text
9bb997e5b0a675969b2e4e5eff0d4329ba9ecce1d9b4529339663a2187fcc58e  astrid/sdk/timeline/_media_inputs.py
286f6c2f3ef0b09de11bcf811c6884675b2276433247097db2df66fea4dc47a1  astrid/sdk/timeline/_shot_commands.py
09cde00d9aa6c658cfdd71da7413eb8a0480d8495f81e2de09c22f03268fb549  astrid/sdk/timeline/native_occurrence_media_commands.py
```

The sorted three-line product manifest hashes to
`a743a56f83597122a16675515fe7874b281d5fe8efd9b8871296545f6c69c98a`.

## Evidence and limits

Passed locally:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recipe_occurrence_media.py tests/editing_conformance/test_recipe_shot_set.py tests/sdk/test_timeline_materialization_schema_union.py
149 passed in 6.72s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_current_union_schema.py
34 passed in 185.23s

/home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/_media_inputs.py astrid/sdk/timeline/native_occurrence_media_commands.py tests/editing_conformance/test_recipe_occurrence_media.py tests/editing_conformance/test_recipe_shot_set.py tests/sdk/test_timeline_materialization_schema_union.py
All checks passed!
git diff --check
PASS
```

This is source/conformance evidence only. It does not qualify Runtime managed
audio admission, native HTTP, outer proposal execution, settlement, requester
outbox behavior, App consumption, generation/pin adoption, or integration.
