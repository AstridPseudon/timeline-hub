# Runtime hold-clear conversion review

**Verdict:** APPROVE the one-to-one assertion conversion source. Merge remains
blocked on a real HTTP qualification with a compatible new Agent pin; no HTTP
qualification is claimed here.

## Exact sources

- Runtime successor: `tl/rt-m2-hold-clear-conversion-qualified-successor`
  `5aee84083e7fffe4efdb46f1bb1cb5426ab16917`, tree
  `2bbb4d41e1c221d7ee34b2c252f08b65b40c5bf4`.
- Original ordinary HTTP parent: `tl/rt-m2-mainmerged014-tested-boundary-forward`
  `4dd643808e93be431f8250c0b6d34320918776ec`, tree
  `d396f8f4f2caa956a8b6689c9af09e9088fb8c27`.
- Agent boundary evidence: `tl/agt-m2-gate1-hold-clear-main-boundary`
  `b7dd64b4dc30b3b960921695ce63422e0df27690`, tree
  `93b4d762bfd7a4de62f45a54788b70f873837997`.
- The attempted current Agent pair is `06aadccd3e3b59f56cca3942695dfbe4c60e374e`,
  tree `403b89d77575d031a62f266d2859593e41bd58e1`; it advertises schema
  `ce3781c2…30d59`, while Main014 Runtime advertises `7d4afa05…31816`, so it
  cannot handshake and does not qualify the HTTP pair.

## Assertion mapping

The original `test_ordinary_http_empty_bootstrap_must_be_reachable` was split
only at the hold-clear boundary. Its setup, renderer prohibition, health and
handshake, provider identity, bootstrap/head, closed-body, origin/auth/scope,
read-only credential, database no-write, command-shape, accepted receipt,
parent readback, dependency, and history assertions remain in
`_run_ordinary_http_hold_clear_case`.

The equivalent required positive is
`test_ordinary_http_authored_source_window_hold_clear_preserves_timing`:
`from=0`, `to=4`, `hold=4`, `params`, `opaque`, clip order, track order, and
all other row data are authored before `clip.add` and carried through the same
track-create, add, hold-set, clear, commit, readback, and history path. No
accepted head is patched after the fact. The original HTTP test had no retry,
undo, or redo assertions to lose; those semantics are covered by Agent's
windowed direct test `test_literal_hold_clear_requires_main_source_extent_and_roundtrips_with_one`
and its reported 10 direct semantic passes.

The bare-row `test_ordinary_http_empty_bootstrap_must_be_reachable` now
expects the semantic `unsupported_timing` refusal mentioning
`surviving source window`. It verifies the draft still has `hold=3`, the held
accepted document is unchanged, the SQLite dump is unchanged, and the
accepted head is unchanged. Thus it does not invent duration or mutate
history. The Agent boundary also records that Main's zero duration/one-frame
floor is not authored duration, while a surviving window clears and inverts
exactly.

There is no broad `xfail`, `skip`, or new product guard. The prior invalid
strict-xfail branch is not the approved source; the final positive is a normal
required test.

## Scope checks and gate

`git diff --name-status` from the original parent to the successor reports
only `tests/test_timeline_ordinary_http.py`. Runtime raw/76 artifact paths,
including `contract/artifacts.json`, `contract/manifest.json`, and
`tests/fixtures/precut-raw-v31.tar.gz`, are untouched. No source, generated
client, schema, or artifact bytes changed.

Central evidence already records the successor's 2-test collection and Agent's
10 direct semantic passes. The central HTTP run was not a behavior result: it
used a stale snapshot that lacked the new positive node and failed at
collection. Do not merge or call this HTTP-qualified until a real compatible
Main014 Agent pin passes both mapped HTTP IDs.
