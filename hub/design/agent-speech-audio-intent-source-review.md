# Agent speech audio intent source review

Date: 2026-10-20 23:28:51 UTC

## Verdict

**SOURCE-ONLY APPROVE** for candidate `74925baff74aec14517820ba31da319631fb74d4`,
against meta base `4d4535882f1e028805c3da178bf9a7fa53696da8`.

This is a bounded source approval of the normal exact
`generation.generate_speech` admission change. It is not a live Runtime
qualification or a public release claim.

## Source findings

- `runtime_synthesizer` declares only the existing v1 audio intent: one
  `main` group, `speech` selector, ordinal `0`, `original` variant, and
  required output. Exact text/settings remain ordinary executor inputs;
  metadata carries only audio content type, voice, and the text digest.
- `invoke` recognizes speech as audio only when that explicit intent is
  present. The normal no-intent speech route remains outside automatic
  publication. The existing validator then removes the intent from executor
  inputs, and `_kernel_invoke` adds only the existing matching
  `generation.publish_v1` effect with the capability as `generation_type`, the
  resolved project as target, and the existing output-port/group/ordinal/
  variant shape.
- Project resolution remains the authoritative Runtime current-project read;
  an absent selection is not synthesized. Explicit project identity is carried
  to admission. The terminal task/result context is retained without
  rewriting: task and attempt IDs, the managed output row/association, and the
  terminal `generation_publish_v1` publication (including Runtime-created
  generation/variant identity) are carried for the matched Runtime selection
  read.
- The Agent does not create a catalog selection, generation, variant, producer
  identity, duration, or public DTO. It does not use latest/gallery/raw CAS
  adoption or client-duration fallback. The inner
  `generation.generate_speech` capability remains distinct from the outer
  `video_editing.sync_draft_voiceover` producer.
- The existing readable managed WAV/provenance path remains in place. Missing
  managed speech/provenance rows and absent/invalid audio or text hashes refuse
  before authoring. The existing preserve/RIPPLE and timing/lowering code is
  outside the product diff and its existing positive behavior remains tested.

The exact five-field project catalog selection and verified intrinsic duration
remain Runtime-counterpart authority. The matched counterpart must obtain that
selection from terminal Runtime association/generation/variant/catalog
context and refuse invalid or absent metadata; this Agent source does not
invent or adopt a substitute.

## Evidence

Focused targeted tests:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/sdk/test_generation_publication_consumer.py \
  tests/sdk/test_projectless_admission.py \
  tests/packs/video_editing/test_draft_voiceover.py
61 passed in 1.16s
```

The integration file collected five speech/publication cases (one unrelated
integration case was deselected):

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  --collect-only tests/packs/video_editing/test_runtime_publication_chain.py \
  -m integration
5/6 tests collected (1 deselected)
```

Per the handoff, the actual integration run stopped at the HEALTH digest
mismatch (`ce378` server versus `ddf639` Agent). I did not bypass, repin, or
rerun it. Therefore no live Runtime qualification is claimed.

Additional read-only checks: `git diff --check` passed; the candidate changes
only the speech adapter, SDK admission hook, and their tests. No timing schema,
lowering, child-delegation, renderer, public DTO, or legacy audio/RIPPLE
source was changed in this candidate.

## Blockers / next steps

No source change is requested. A normally matched Runtime counterpart must
qualify terminal selection and verified duration, including refusal for absent
or invalid catalog metadata, before any combined/native qualification claim.

