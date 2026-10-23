## Report

- Review: G5/R2 independent retained-input and causal-ownership review of
  `f527261833dd1467a0180b9c179ad4029ca66a58`.
- Verdict: **PASS** retained-input fidelity; **PASS** causal-ownership
  attribution to the Runtime physical/native observation boundary.
- Product acceptance: **not claimed**. G5 remains P1-gated; no merge or product
  patch was made.
- Evidence: fixture is 377,565 bytes and exactly reproduces packet events
  115/117/119/129/158. Accepted source is split `caa332...` (3 occurrences,
  `e6d3...` config); predecessor/output is flat `a58d...` (1 occurrence,
  `3261...` config). Agent reconstruction matches the prepared writes and
  steps; the fourth native write fails only because Runtime observes physical
  `shot_revision_id` pins absent from authored native rows.
- Ownership: Runtime `_inverse_stage_state` (734–738) exposes physical rows and
  `_inverse_stage_boundaries` (970–972) compares them directly. Agent’s
  `_command_state` contract (282–286, 290–292, 369–379) rejects pins and
  preserves authored rows. Source orientation is consistent. This requires
  Runtime/contract coordination, not an Agent recorder pin injection.
- The original test body remains byte-identical from `91ac58a9`, body hash
  `c2711a2d10765828694ee1906d75bdf62a91ed6ac0bbef8e4cb0d823e48ec30d`.
  Both new tests are unskipped; the authentication-positive remains RED in the
  retained evidence and was not replayed.

### Commands and results

- `PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-cfa0af0d PYTHONPATH=.:/home/user/work/wt/rt-pin-cfa0af0d /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --collect-only tests/sdk/test_timeline_restructure_inverse_retained.py` — **2 collected**; requested node name is absent in this SHA.
- Same environment, adapted to the available lossless node
  `::test_retained_inverse_orientation_matches_actual_accepted_input` — **1 passed** in 0.47s.
- `python -m ruff check --no-cache tests/sdk/test_timeline_restructure_inverse_retained.py` — **passed**.
- `python -m mypy --cache-dir=<private tmpdir> tests/sdk/test_timeline_restructure_inverse_retained.py` — **passed**.
- `python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004` — **passed**.
- `python scripts/artifact_manifest.py --check` — **passed**.
- `git diff --check` — **passed**.
- Product/inverse/original-body comparison against `91ac58a9` — **clean**; only
  the retained fixture and new diagnostic test are added.

### Scope and next step

No auth-positive replay, public/original journey, full suite, HTTP/socket/browser
run, pin/dependency/env change, daemon operation, generated file, or product
code change was made. Next step is Runtime-owner contract coordination for an
authenticated physical/native observation representation, followed by one new
original-body qualification; do not count the pin-lift control as acceptance.
