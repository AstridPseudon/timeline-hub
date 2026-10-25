# F-D86 D107 exact baseline read handoff

Status: `SOURCE COMPLETE / STATIC ONLY`.

Added exactly one file:

`tests/editing_conformance/test_m1_legacy_archive_read.py`

The original M1 source and existing pair-reader tests are unchanged.  The new
selector is:

`tests/editing_conformance/test_m1_legacy_archive_read.py::test_explicit_held_baseline_then_current_word_bound_read_is_closure_exact`

It depends on the existing `reader` fixture through normal pytest plugin
registration from `test_current_pair_reader.py`; it does not invoke a fixture
wrapper directly.  Therefore the protected behavioral run uses the same
genuine archive and verification path, whose exact archive SHA-256 is
`2915bd4ac0d46954d19c30f87a517b82074218699978e650fab03fcba81b72d3`.

The selector first uses `store.fetch_bundle` with the explicit held source
pair:

```text
project       7b6f2bae8ffe42bf925216c38249ed79
timeline      film
revision      film-parent-v1
publication   txn-55c0651b2cd64255ae06e73f9708220a
```

It asserts the returned base identity and full `_runtime_document` equality to
Runtime's authenticated `revision_closure`, then checks the retained baseline
parent digest, original three-occurrence graph, `music-bed` timing/effects,
CAS/media manifest pins, transcript document/word anchor, and exact text
binding pin.  No current-head read substitutes for this historical baseline.

The same selector then separately reads the authenticated advanced pair:

```text
revision      a3e671256f1c42b8837d3e118c97b21b
publication   txn-11c90075be6c4c8bb9e2627366f0fe4f
```

It checks full closure equality again and asserts the current word-bound
`music-bed` declaration, opaque value, timing, and `music-other` addition.
The test body performs no commits or other writes.

Static evidence is in:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D107-read-return-0639/evidence/`

No pytest, import/collection, fixture/helper execution, service, probe,
archive acquisition, or full suite was run in this source-only return.
