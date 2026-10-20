# Runtime historical PCM scope fixture repair

## Change

Updated only `tests/historical_audio_fixture.py`. The fixture now builds a
valid sibling-owned immutable child closure before the authored publication:

- The original `film` closure remains untouched and is still checked against
  its captured baseline.
- Each copied internal timeline and shot receives a deterministic legal owner
  identity under `historical-audio-pcm`; occurrence IDs, ordering, authored
  payloads, opaque fields, transcript text, and audio metadata are preserved.
- Text bindings are registered through the existing Runtime API for the new
  shot owners before publication. The semantic mapping from each original
  binding to its new binding/event-stream identity is asserted.
- A genuine six-second mono 8 kHz 16-bit PCM WAV is stored in CAS. Duration is
  absent, and no generation, variant, or adoption fields are introduced.
- Existing closure persistence is used only for the temporary unplaced child
  bootstrap. The temporary parent has no occurrences or dependency history;
  normal publication then records the complete closure. The sibling timeline
  is published through the normal API twice, preserving the journey's existing
  history and receipt expectations.
- Before returning the fixture, ordinary Runtime GETs for the parent, shots,
  and internal timelines plus `revision_closure` are exercised and compared
  with the expected canonical document. CAS bytes and the original film
  baseline are also checked.

No Runtime/Agent read-scope, schema, authority, journey, observer, or
expectation changes were made. No SQL or fabricated history was used.

## Validation

Passed locally:

```text
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m py_compile tests/historical_audio_fixture.py
git diff --check
```

Passed the direct fixture smoke test using the exact Agent path
`/home/user/work/wt/agt-pin-27e823a5`: it created the captured realm, prepared
both source and duplicate fixtures, reopened the sibling through ordinary
Runtime reads, checked the canonical closure and CAS bytes, and completed
without assertion failures.

The required single central run was submitted once with the exact requested
Agent/Runtime pins and `--runxfail`:

```text
rt-m2-historical-pcm-scope-setup-fix-original-raw27-two-node-pair-integration-1020183610-24878
```

At handoff it remained queued because two other named runs occupied the test
service slots. No central result or new failure was available. No full suite,
browser suite, or additional historical retry was run.
