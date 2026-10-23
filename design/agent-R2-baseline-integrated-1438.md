# R2 integrated narrow compiler proof

Result: **PASS**, scoped to the retained R2 redo compiler repair on the actual
integrated Agent tree `58316fd6e0ce8a1fb3b2b3826ec71906d29080de` (tree
`00c04a48841d95f5bf95dc604758767d2b065227`). This is evidence-only; it does
not claim public redo, whole R2, G5, or P1 completion.

## Identity and reviewed scope

- Actual `583` is a merge of base `8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe`
  and reviewed repair `80523b472cc817c2da01bf89c177d5d7dc4c2e10`.
- `git diff 80523b472 583` is empty: the actual tree is byte-identical to the
  independently reviewed tree.
- `8c..583` changes exactly four intended paths:
  `astrid/core/timeline/authoring_bundle.py`,
  `astrid/sdk/timeline/_commit_patch.py`, the focused captured-redo test, and
  its fixture.
- Actual source/fixture SHA-256 values match the immutable review packet:
  - `authoring_bundle.py`:
    `99c5f1231246f317957a0900eff49c48a4135afe56fa8270f2a0958981c15ff2`
  - `_commit_patch.py`:
    `c41946a5efe138039cac06d58e5e46fb253390000cf2fc565a7b10333954c1a`
  - focused test:
    `0717cc3826339abadf2a485592f166957d92c3760b5aeb9ebfd03bba81e13834`
  - fixture:
    `a20636115ffb6e986ad7731d57bc90dd7ed98a2330b65d3dc71b83a3707ddb37`
- Immutable packet:
  `design/agent-R2-redo-media-1404-a29df82beb548306.json`, SHA-256
  `a29df82beb548306683ab64d738eb776a519587fdb30cad3e997e91468621ef8`;
  source packet hash `9603ca432b1c9d1c1b16908f00547d26da6d04df3ad681308cbae5f3e57635d1`.

## Preservation and origins

The registration/reservation and private-capture/R1 paths were not modified.
The following 8c and current blobs are identical: `commit.py`
`61a39df539ee74b68a5fe00f981677d5300dc874`, `capture.py`
`aaea8424fa6bbacf01df708aed4f53ede658fbee`, `_doc_patch.py`
`e780e7abf3baf7aca1315fbc8a54c3a9e13feef2`, `inverse.py`
`6385c8c3caa9761059d766b6487c967463736fb9`, `_root_inverse.py`
`5d2a1165c96e140482b427da0f3e26f06071f080`, `runtime.lock.json`
`924834f795b81c0716e8bf40ab3f08de71d819fa`, and `artifacts.json`
`d68a3884c65c5684634c22ebb03def35ba277992`.

The normal Runtime producer remains `34eac0041b0891e9011966b39bcbd26053fde5bc`;
the vendor lock check passed against that checkout. The frozen schema digest
`d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d` and
Composition identity `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`
were not changed by this four-path Agent merge. No home checkout move was
performed: current and home both started and ended at Agent `583` / tree
`00c04a48841d95f5bf95dc604758767d2b065227`.

The focused proof imported these exact origins both before and after tests:

```text
Agent:   /home/user/work/wt/agt-R2-baseline-integrated-1438/astrid/core/timeline/authoring_bundle.py
         /home/user/work/wt/agt-R2-baseline-integrated-1438/astrid/sdk/timeline/_commit_patch.py
         /home/user/work/wt/agt-R2-baseline-integrated-1438/astrid/sdk/timeline/commit.py
Runtime: /home/user/work/wt/rt-pin-cfa0af0d/runtime_protocol/timeline_commit_auth.py
```

## Commands and results

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-cfa0af0d \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-cfa0af0d timeout 20 \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
tests/editing_conformance/test_captured_redo_media_closure.py \
tests/timeline/test_authoring_bundle.py::test_timing_is_admitted_but_competing_selected_media_fails_before_publish
# 10 passed in 2.57s

/root/.local/bin/ruff check --no-cache \
astrid/core/timeline/authoring_bundle.py astrid/sdk/timeline/_commit_patch.py \
tests/editing_conformance/test_captured_redo_media_closure.py
# All checks passed

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python \
scripts/vendor_lock.py check runtime.lock.json \
--producer /home/user/work/wt/rt-pin-34eac004
# ok runtime.lock.json (matches producer manifest)

git diff --check
# exit 0
```

The literal `--producer /home/user/work/wt/rt-pin-34eac004/artifact_manifest.py`
form was also checked and correctly failed CLI preflight because this script's
`--producer` argument is a checkout directory. No files were changed; the
documented checkout-directory invocation above is the passing result.

## Boundary

The retained strict boundary remains: the Agent-native inverse source/effect
orientation mismatch (`shot-placement-*` alias before versus canonical
`document-diff-*` physical input) is still refused by Runtime. No public redo
body was retried, no Runtime patch or guard waiver was made, and no whole-redo
PASS is claimed. The reviewed repair only proves the narrow historical-child
baseline compiler path and its preservation/negative guards.
