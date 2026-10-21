# full5664 public-registry assertion review

Decision: **APPROVE**.

Candidate: `76ba53c15f54a2dc49e75159d19a921585d26440`, tree
`8384f60a582c1cb582a0cfcedd082d1feaf96e38` (base `acc08c2cd2`).

Evidence:

- Classification identifies the old failure as a stale negative expectation,
  while approved repair `52437515d9b82263a88634e776e11fca29d759a8` (tree
  `4e96542af42e6e3fa65400931ed20eb1ad842754`) intentionally retains the
  public Composition-owned `text-card` and routes it through the public API.
- Immutable public13 (`@banodoco/timeline-composition` 0.0.13) resolves an
  effects entry `text-card`; its resolved function name is `TextCard`.
- Old -> new in `tests/packs/test_composition_elements.py`:
  `assertNotIn("'text-card'", effects)` ->
  `assertIn("'text-card': selectOwnedEffect('text-card', TextCard, "
  "{'rendering': TextCard}),", effects)`.
- This is a structural ownership assertion, not a substring-presence check.
  The retired local import guard remains, as do the fade-up/cross-fade wrapper
  guards and the audio-reactive/custom-owner coverage in the adjacent tests.

Actual replacement test: `CompositionElementTest::test_bundled_element_registries_generate_together`.

Evidence command (worker report):
`ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-0013 ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider tests/packs/test_composition_elements.py tests/packs/rendering/test_remotion_element_generation.py` -> **19 passed**.

No product/test changes were made by this review; no full or replay19 suite was run.
