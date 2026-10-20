# Portable owner-film scanner v1.0.3 handoff report

## Result

Prepared one held, unpublished v1.0.3 release candidate by composing the
completed preserve-clears v1.0.2 delivery with the reviewed scanner-agent
semantic policy proposal. This is ORCH-owned delivery content only; no Agent
product files were changed. The candidate keeps the projector as the one
semantic authority, sanitizes only at the output boundary, permits a valid
optional `asset = None` clear, and does not perform whole-document reference
validation.

The semantic additions are bounded and fail closed:

- one finding per look-bearing element clip, plus half-open overlap findings
  across tracks only when at least one member has a declared look;
- `crop_*` and element `speed != 1` in the look inventory;
- media `entrance`/`exit` in `media_look_inventory`;
- canonical incoming transition declarations in
  `transition_boundaries`, without pretending to convert or render them;
- explicit `not_covered` labels for transition conversion, media look overlap,
  and renderer presence/alpha/pixel coverage;
- non-linear explicit curves only in `curve_honoured`; absent and `linear`
  curves remain covered by `continuous_audio_fade`;
- original input-list indexes for duplicate internal revision IDs and
  occurrence-prefixed projected paths;
- `projected.` prefixes for projected track/asset context paths.

Malformed scope, nested reference, source-path, and credential/caption
sentinels are never copied into output. Existing read-only input, symlink,
hardlink, same-path, and atomic replacement protections remain in place.

## Verification

Commands run in this worker worktree:

```text
/home/user/work/venv-agent/bin/python -m pytest -q delivery/tests/test_owner_film_cliplook_scan.py --agent-root /home/user/work/wt/vw-m4-scanner-final-policy-compose
23 passed

/home/user/work/venv-agent/bin/ruff check delivery/owner_film_cliplook_scan.py delivery/tests/test_owner_film_cliplook_scan.py delivery/tests/conftest.py build-release-v1.0.3.py
All checks passed

/home/user/work/venv-agent/bin/python -B -m py_compile delivery/owner_film_cliplook_scan.py delivery/tests/test_owner_film_cliplook_scan.py delivery/tests/conftest.py build-release-v1.0.3.py
passed

/home/user/work/venv-agent/bin/python build-release-v1.0.3.py
passed; deterministic ZIP/TGZ, metadata, and bare SHA files generated
```

The test suite is synthetic and includes the 19 preserve-clears base cases
with the semantic-policy cases and the explicit optional-clear regression.
It covers rational FPS, all three base categories, single-element and
cross-track overlap, crop/speed, media entrance/exit, incoming transitions,
duplicate revision positions, malformed-scope/caption redaction, relocated
CLI, and output alias protections.

The prior v1.0.0, v1.0.1, and v1.0.2 archives and metadata were preserved
byte-for-byte from the completed preserve-clears handoff. The new archives are
flat and deterministic with zeroed timestamps and ownership metadata.

## Not run / held status

No full suite, browser, live socket, network, install, database, credentials,
media, render, service, or owner-film scan was run. No owner closure was
available. The package remains unpublished pending manager review and Agent
canonical-policy review. `clean_claim` remains false in every scanner result.

## Decisions

The policy proposal targeted v1.0.1, so its semantic source/test copies were
not used as a whole-file replacement. The v1.0.2 preserve-clears behavior was
retained first, then the policy changes were composed. The old single-track
overlap expectation was replaced by the settled cross-track semantic rule;
this is an intentional policy change, not a weakened test.

