# D100/R1 review receiving recipe

Verdict: `FAIL exact finding`.

1. Correct both protected-product hash fields in the source1914 manifest to `018f174004bf9b9c275aa23ef6ceb432ce9d7294d71e3024f96353c25fa808a3`; do not change product or test source for this evidence correction.
2. Preserve final source `42040a9c05ae7105cf88459cad5f0b8b9bf56fd1`, tree `66c0215955332af8ed32ae7d4c17d4f71ccb17d4`, product hash, test hash, and one-path scope.
3. Only after ordinary free space reaches at least 5,000,000,000 bytes, run the bounded targeted Agent test:

   `/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 tests/sdk/test_d100_item_birth_boundary.py`

4. Treat the 1837/1843 candidate 24/27 result and 1858 shared-owner setup disposition as inputs, not proof. Require the direct custody cases, shared-owner case, registered provider case, and all existing refusal/no-write predicates to pass without weakening assertions.

No full suite, provider/native/live/socket/browser/collector/acquisition/Store/install run, source merge, release, pin change, fixture edit, or D130 action was performed or authorized.
