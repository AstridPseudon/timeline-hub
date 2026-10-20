# Runtime catalog text-binding final review

## Verdict

**REJECT** for commit `d037368d22373be92c1e4c1a821315a1130fdcff`, tree
`e5c3830af392f19842787495acf8ec7948e6ae0f`.

The bounded scope is otherwise correct, but the candidate does not satisfy the
required replay-first idempotency behavior.

## Blocking finding

For nonzero-head `set_project_shot_text_binding` retries, the implementation
resolves the mutable binding row and checks `head_seq` before calling
`_command_replay` (`runtime_protocol/service.py:3461-3475`). The same ordering
exists for `rebind_project_shot_text_binding` (`:3526-3543`). Therefore an exact
retry can be refused as stale after a later write, instead of returning its
stored receipt. This is inconsistent with the requested replay-first rule and
with the catalog-promotion precedent `4c1a1a30a6dfed4b1d0c7674fe6f8bfc23aab15f`,
whose receipt lookup precedes mutable shot/candidate reads.

Independent probe (Runtime service only, temporary realm; no product files
changed): create head 1, set head 2, create head 3, then retry the exact
head-1 request with its original idempotency key. Result:

```text
NONZERO_REPLAY_RESULT=stale-before-replay text binding head is stale
```

The fix should compute the immutable request identity from validated input,
perform `_command_replay` before resolving/checking mutable binding state, and
then retain the existing CAS/scope/write guards for new requests. Re-run the
nonzero-head set and rebind exact-retry cases after that change.

## Scope review

- Original four `tests/test_shot_text_bindings.py` assertions remain positive;
  setup privately seeds only `project_shots` in the ephemeral Runtime realm,
  so the tests do not require Agent and do not retarget to an occurrence.
- Only the two existing text-binding methods were restored. Other shot/item
  CRUD remains retired; no endpoint, DTO, table, command, or new journal was
  added.
- `_require_unplaced_project_shot` enforces same-project shot ownership and
  rejects any accepted occurrence history for that exact project/shot before
  CAS or binding/event writes. This includes current film ownership and the
  design's historical-detach case; it does not match unrelated projects or
  shots. The 4c1 promotion guard intentionally has a different policy: it
  permits exact immutable historical reuse while refusing a newer current
  global head, so the predicates should not be mechanically deduplicated
  unless the owner settles a shared policy after integration.
- UTF-8, 1 MiB size, SHA-256 identity, empty-text presence, event ordering,
  project/auth scope, historical binding invariance, and zero-write placed
  refusal are covered by the candidate and its neighbor tests. Native
  `MediaReads` strict new-selection MIME behavior and authenticated retained
  legacy reads are unchanged.

## Evidence

Central targeted cache hit for this exact source tree:

```text
request-test rt-m2-catalog-text-final-review targeted --files \
  "tests/test_shot_text_bindings.py tests/test_timeline_shot_authority.py"
=> 115 passed in 98.46s, exit 0
```

The central result was reused from the identical source tree run by the
restoration worker. Existing bounded neighbor evidence also reports:

```text
tests/test_timeline_text_selection.py
tests/test_timeline_text_binding_clear.py
tests/test_timeline_text_legacy_custody.py
=> 69 passed (one existing pytest-config warning)

tests/test_timeline_verified_media_http.py
=> 5 passed, exit 0
```

No full suite, browser/live-socket matrix, publication, merge, or pin was run.

## Scope and cost

Candidate diff: 3 files, `+326/-16` lines (`service.py +268/-2`, tests
`+58/-14`). No source edits were made during this review. Remaining work is a
small ordering correction plus focused exact-retry coverage; no scope
expansion is recommended.
