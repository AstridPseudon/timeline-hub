# Runtime ordinary014 current test carry

## Result

Carried the exact `6ab3243972f8dc49105819e6d7ba7aef1a2888b8` clip-replacement
test blob into the `9cde47523803607f4dfd8d39885a9526de4ce8e7` candidate.

- Changed exactly one product-repository path:
  `tests/test_timeline_clip_replacement.py`.
- Worktree blob SHA-1 is
  `183f14dbe64466c9a8c7aec5b34850da9272f107`, exactly matching the `6ab`
  source blob. The carried blob includes
  `test_native_clip_swap_rebases_after_disjoint_intervening_edit` and its
  exact supporting assertions/helpers.
- `git diff --check` passed. No accidental product-repository design report
  exists.
- The existing retired-route strict xfail marker was preserved unchanged.

## Frozen identity and delta

- Candidate base: Runtime `9cde47523803607f4dfd8d39885a9526de4ce8e7`, tree
  `ea1ffe7e09ebf679abf409b060e753c17bdabe0d`, with exactly two parents:
  official producer `a0dca16975dfe8f5e762703b99d9791a16cf7fd7` (tree
  `4b7dd0fe44be973c344bab3de568eaf0bdd28476`) and current server
  `9f211fcdb66023a577a14111f99c87fb32ef573c` (tree
  `d22726d982ac279277c4b0210495170556e3309d`).
- Frozen Agent source: `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3`, tree
  `c5a8a3ec7e9e01c61c5ae31834da53bed4be406a`.
- Existing official artifact identity retained: version
  `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa`,
  manifest `ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815`,
  75 artifact paths, 55 definitions, and 29 operations.
- No artifact, generated contract, CAS/text/promotion/fence, clip-replacement
  product logic, audit, shell, producer, private-carrier, release, or current
  tuple file was changed. The source producer remains immutable `a0`; this
  remains a distinct candidate-server branch delta.

## Tests

Exact Agent-310 source was exported privately from the frozen commit to
`/tmp/rt-m2-ordinary014-agent-310.44KsDA` (source tree recorded above; no
shared dependency was modified). Passed:

```text
ASTRID_CHECKOUT=/tmp/rt-m2-ordinary014-agent-310.44KsDA PYTHONDONTWRITEBYTECODE=1 \
  /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  tests/test_timeline_clip_replacement.py::test_native_clip_swap_rebases_after_disjoint_intervening_edit \
  tests/test_timeline_clip_replacement.py::test_native_parent_clip_swap_route_replaces_parent_media --runxfail
2 passed in 6.29s
```

Central socket-targeted attempt (the only HTTP selector requested):

```text
request-test rt-m2-ordinary014-current-test-carry targeted \
  --files "tests/test_timeline_clip_replacement.py::test_native_clip_swap_public_http_route"
```

Result: exit 5, `1 deselected in 0.39s`. The central targeted command kept
Runtime's default `addopts` (`not integration and not darwin_native and not
live`), so the integration-marked HTTP test did not execute. HTTP success is
therefore unverified here; no broad/full suite was run and no duplicate was
submitted.

## Follow-up

Run the same single HTTP selector through an integration-enabled central lane
bound to the exact Agent `310e548…` fixture before claiming the socket result.
