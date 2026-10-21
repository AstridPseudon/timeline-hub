# Agent complete source/current-main forward

## Result

Prepared a private source-only successor in the worker worktree. The harness
must commit the resolved tree with two parents:

- approved source parent: `5672d2b7deee2bfe2ab375fd6db5fc35a192591d`
  (tree `6dd13b552c4f07fff5586b1fa772bdbdf64accba`)
- frozen current published014/Main497 integration parent:
  `7ab6cbae273f133b3adf2a7bae9f2439f02ce71e` (tree
  `075339b2c6d5e57c1b0e76754457d053b51edf2c`)
- merge base: `6efc81500a0e0688c2bb41e736503f0fc3e04abb`

The live `tl/integration` ref advanced after dispatch; those later changes are
intentionally excluded. The worker merge-parent file is pinned to the frozen
`7ab6...` SHA.

## Exact allowlist and boundaries

The resolved tree is exactly:

1. The 27 non-manifest paths from:
   `git diff --name-only 6efc81500a0e0688c2bb41e736503f0fc3e04abb 7ab6cbae273f133b3adf2a7bae9f2439f02ce71e -- . ':(exclude)artifacts.json'`.
   These preserve the current Scene, AM-footage, CLI, visualize/cache, and
   related public controls byte-for-byte.
2. The 93 non-manifest paths from:
   `git diff --name-only 6efc81500a0e0688c2bb41e736503f0fc3e04abb 5672d2b7deee2bfe2ab375fd6db5fc35a192591d -- . ':(exclude)artifacts.json'`.
   These are the independently approved bounded source union and private
   C3d voiceover source. No callers were activated.
3. Speech prerequisite source/regression paths only:
   `astrid/packs/generation/pack.yaml` (the four-line automatic
   `generation_publication` declaration from `4048bec6b`),
   `tests/sdk/test_generation_variant_publication.py`, and
   `tests/integrations/test_speech_publication_prerequisite.py` from
   `ca62c71f3`. The ca62 regression removes caller-owned duration metadata;
   the withdrawn `29399` metadata workaround is absent.
4. `artifacts.json`, composed to retain the approved private voiceover
   entries and the frozen integration's current public artifact entries.
   `scripts/artifact_manifest.py --check` passes.

The allowlist audit reports 27/27 current-integration blobs, 93/93 approved
source blobs, and 3/3 speech blobs exact, with zero unexpected blob drift.
No package version bump, generated-client regeneration, freeze, new Runtime
pin, public caller activation, or `sourceRoot` authority was added. Raw OLD,
producer-leaf, group-inverse, and security-fix cohorts remain excluded.

## Identity and client boundary

- Edit schema raw SHA-256: `daec2964bb589d2087409446f99b84cfe9d6fb62b0b3af25e37363a78b170514`.
- Canonical formatted schema SHA-256: `9c05ec496e957548fe4656ca655a67a7b936ff4f220bdedae474a680e6d32eb9`.
- Schema inventory: 62 definitions, 36 closed operation clauses.
- Private C3d `runtime.lock.json` SHA-256:
  `07c7be425e8b5595006db280541c97d6e3dd174ae92f54b8550340e21167ec32`;
  its producer source is `c3d26567ff6fe4e20a959476d40aff90ad23a0ca`.
- Private generated client bytes are retained exactly: `__init__.py`
  `4069c15e93b72d504cc882b18dbae119fcd9e7a5186f3c06238bad304276a206`,
  `contract_metadata.py`
  `40d329430bf40c36876b12adc08c6c59f2a4b7e980da8b963305b6b375a43aea`,
  `generated.py`
  `61b55a2e14127a9cc360054a67f6c0b6259ff7eb75bcf58e9c788da344c234ca`,
  and `timeline_commit_types.py`
  `f33a509da59352fed877d2c0ccc5e2e150d17494a0a28e4de811d2c268382644`.

The private C3d client/lock is the only Runtime client boundary carried by
this source candidate. The public 0.2.14/95bd generated replacement was not
used as the private bytes, and no public Runtime/App/Composition consumer was
changed.

## Evidence

Passed:

- Source/floor/conformance command covering the bounded movement, parent
  media/reference, track order, timing, schema union, and speech tests:
  327 passed before the declaration-source correction; the eight speech
  declaration cases failed because the required pack declaration was not yet
  present. This diagnostic failure was corrected without weakening tests.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider tests/sdk/test_generation_variant_publication.py`
  — 32 passed in 85.16s after the declaration source was added.
- Current non-render scene/cache subset (scene roles, public summary,
  projection, visualize cache, visualize IDs) — 70 passed in 1.09s.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B scripts/artifact_manifest.py --check` — passed.
- `git diff --check` — passed.
- Frozen-source blob audit — passed with zero unexpected drift.

Not run: the speech integration test requiring a live C3d Runtime, native,
full, browser, renderer, render, and broad duplicate matrices. The attempted
current scene check had 70 passing tests and one unrun-by-policy environment
error: the real-scene node requires provisioned renderer peers (`esbuild`),
which were not installed or mutated.

The harness-assigned final merge commit/tree SHA is not available until worker
exit; its required second parent is recorded as `7ab6cbae...`.
