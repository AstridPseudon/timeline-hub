# APPROVE — public managed Scene caller port

Reviewed and ported on 2026-10-20 23:46:32 UTC.

## Decision and exact delta

Approved donor `60abe2eaa0284c23a9a1ef77b1ce608602b7dd7e`, whose meta base is
`2b6e5f0e20498489e1fe0e9046c68e3248474452`. Ported its exact three-file
caller delta onto current base `2b020eaef07a2ef138291bfea357d3924d5c7956`:

- `astrid/sdk/timeline/check.py`: +41/−0
- `astrid/sdk/timeline/checkout.py`: +15/−0
- `tests/integrations/test_d09_managed_scene_only.py`: +34/−0

The resulting worktree delta is +88/−2, with no other paths changed. The
current base and donor parent are divergent (merge base
`a8a40afd37e5560a14fa5e1a09ace6018596793e`), but `check.py` was byte-identical
at both parents. The only pre-existing target-file differences were the
current checkout doc wording and the current test's import-provenance preflight;
the donor additions were applied unchanged, preserving all 312 existing test
lines and existing binding/digest assertions.

## Review

- Connected `Checkout.open()` and `Checkout.draft()` retain only the existing
  project/timeline/client binding needed for read-only diagnostics. Detached
  constructors and direct `load()` remain local; bundle clones created by
  transaction/publish/save helpers start unbound. Reload/reset preserves the
  binding on the live connected checkout. A closed/stale client or managed
  failure becomes advisory `UNAVAILABLE`, with no local fallback that could
  misrepresent managed Scene truth.
- Saved checkouts use the existing `_scene_only_request`; working copies with a
  path use `_scene_only_candidate_request`, which freezes the actual document
  through the existing candidate projection. Project/timeline scope, exact
  capture digest, timeline identity, source provenance, snapshot label, clip
  map, layer IDs, and complete frame extent remain enforced by the existing
  helpers. Mismatch or stale data refuses the managed result advisory-only.
- Formatting uses the existing `_scene_only_spans` and `_scene_problems`
  reader. Real `UNKNOWN` remains advisory; missing/stale/invalid managed data
  is reported as `scene UNAVAILABLE` rather than becoming a save failure.
- `_check_core()` is unchanged semantically and does not call the managed
  caller because the new branch is inside `diagnostics`. Save, publish,
  transactions, dry-runs, and pure structural checks therefore remain
  renderer/Node-free. No public API, DTO, source reference, certification,
  factory, or caller-authoritative metadata was added.
- The public test reuses the existing `_public13_environment` import
  preflight. It exercises ordinary zero-argument `Checkout.check()` and the
  managed Runtime/pack-host path; no private callback, Scene input tuple, or
  fabricated source is supplied.

## Evidence

Local targeted caller/save controls:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider tests/sdk/test_scene_caller_preservation.py tests/sdk/test_scene_save_core.py tests/sdk/test_timeline_checkout_publication_retry.py tests/sdk/test_timeline_checkout_facade.py
43 passed in 3.06s
git diff --check: passed
```

Candidate import-provenance smoke passed for `timeline_checkout`, SDK
filmstrip, visualization executor/Scene modules, Scene answers, Root
preparation, and verified-source; every resolved module was inside this
candidate worktree.

Central, only the new public-entry managed node:

```text
request-test agt-review-port-scene-public-caller-current targeted --files 'tests/integrations/test_d09_managed_scene_only.py::test_public_checkout_check_uses_retained_managed_scene_result'
1 passed in 113.02s (1:53), exit 0
```

No private saved/candidate integration cases were repeated. No full suite was
run. No blocking issue or material adaptation was found. The harness should
commit the three worktree files with the supplied commit message.
