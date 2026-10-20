# Runtime catalog text corrected review

## Verdict

**APPROVE** for replay-fix commit `63e761e29e7e51fc5fa71cc01cd1fe0cf5952125`,
tree `7e1b71ac53312ddbbceefa32b40a919d467b5002`.

This approval is for the bounded text-binding replay correction, subject to the
integration condition below. The candidate is not a replacement for the
current Runtime integration source.

## Review findings

- `set_project_shot_text_binding` and
  `rebind_project_shot_text_binding` validate immutable request input, derive
  the project-scoped binding identity and request hash, and call
  `_command_replay` before mutable binding resolution, head checks, placement
  checks, or object-integrity checks.
- Project lookup/authentication remains before replay, so project scope and
  current authorization behavior are preserved.
- A changed payload under an existing idempotency key still reaches the
  request-hash refusal. New requests retain the existing CAS, event, MIME,
  placement, and compare-and-set guards.
- The four original positive assertions remain positive. UTF-8 byte sizing,
  SHA-256 identity, empty text presence, event ordering, and no accepted-film
  write behavior remain covered by the candidate and its neighbor tests.
- Only `runtime_protocol/service.py` and
  `tests/test_shot_text_bindings.py` changed in the candidate (`56` insertions,
  `25` deletions; `62` test insertions). No endpoint, DTO, schema, table,
  command kind, or new journal was added.

## Integration condition

`81f8c7e0b22c34804015c054762af3d737e4698a` (tree
`0e3a5b938d9ca489fc760b09d34b02d4ac9aad51`) is **not** an ancestor of the
candidate; their merge base is `16acbb6ef94a6d8e226ccdc351ba0d96e0b09ea5`.
The candidate therefore must be applied to `81f8c7e` with the known conflicts
in `runtime_protocol/service.py` and `tests/test_timeline_shot_authority.py`
resolved by retaining the integration-side behavior.

The resulting merged source must retain the promotion helpers from
`4c1a1a30a6dfed4b1d0c7674fe6f8bfc23aab15f` (including
`promote_project_shot_candidate` and `_shot_revision_payload`) and the
current-global-head/destination-occupancy fence in the publication path. In
particular, the merge must not replace the integration service with the
candidate's older service.py; it should carry only the replay-first text
binding hunks plus their focused regression coverage. No merged SHA is claimed
here because this worker did not merge or pin refs.

## Evidence

Independent direct RuntimeService probe, using a temporary realm and no product
files: `DIRECT_ORIGINAL4_AND_RESTART_REGRESSION=PASS`. It covered the original
four positive behaviors, then set A -> rebind B -> restart -> exact A retry,
fenced `_resolve_text_binding`, and verified identical receipt/result,
unchanged binding bytes, unchanged event hashes, unchanged CAS bytes, and zero
SQLite changes. This is service-functional evidence only, not HTTP
authentication evidence.

Central targeted test on the exact candidate tree:

```text
/home/user/work/venv-runtime/bin/python -m pytest -q tests/test_shot_text_bindings.py
=> 5 passed in 6.07s
```

Previously reported central targeted evidence for the exact replay-fix tree:

```text
tests/test_shot_text_bindings.py tests/test_timeline_shot_authority.py
tests/test_timeline_text_selection.py tests/test_timeline_text_binding_clear.py
tests/test_timeline_text_legacy_custody.py tests/test_timeline_verified_media_http.py
=> 190 passed in 134.41s
```

Local static checks:

```text
git diff --check HEAD^ HEAD                         => passed
python -m py_compile runtime_protocol/service.py tests/test_shot_text_bindings.py
                                                     => passed
```

No full suite, browser/live-socket matrix, merge, publication, or pin was run.

## Limits and next step

The exact set replay and the source ordering were independently verified. A
separate exact rebind-after-later-write restart probe was not repeated here;
the candidate's same replay-first implementation covers that path and the
reported central targeted result includes its neighbor coverage. The next
step is the orchestrator's conflict-resolved merge onto `81f8c7e`, followed by
the merged-tree focused suite; preserve the promotion helpers and fence as an
explicit merge invariant.
