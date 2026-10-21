# Occurrence trim dormant source review

Verdict: **SOURCE REQUEST CHANGES** for `f8638058aeb6195854847ec2d24f10d943bcc824` / tree `f23887964aa53444c493a5127215ffce406caccc`.

The unregistered `clip.trim@2` branch has a concrete shared-materialization data-safety defect. `_clip_trim_v2` calls `_owner` but never the existing `_exclusive` guard used by occurrence add/swap. Starting from the video occurrence-media fixture, set `bundle['placements'][1]['shot_id'] = bundle['placements'][0]['shot_id']`, then invoke the private recorder with raw selector `occurrence:occ-a/clip:clip-a`, `in_s=3`, `out_s=5`, and the fixture's verified media. The recorder accepts and writes `from=3.0`, `to=5.0`, `hold=2.0`; because both occurrences materialize the same shot, `occurrence:occ-b/clip:clip-a` also reads back as `3.0..5.0`. The required behavior is atomic refusal (`unsupported_ownership`) with unchanged input.

Hashes:

- changed operation: `clip.trim@2` (occurrence/raw-child branch; not registered or activated)
- current schema raw SHA-256: `ca55d74acbeef104be3a4a1ef57e2b4b2d7d1859d5194873a0fdf76a879ad6e3`
- current schema canonical SHA-256 (`sort_keys`, compact JSON): `b19161c0881d7496e65e3cb52dcf57b35e661b780a608bd8fabba062d7bc495f`
- frozen ordinary-floor schema raw SHA-256: `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`

The compact changed-neighbor command passed **226 tests**. No HTTP, native, full, pin, generated-artifact, registration, activation, or public qualification was run or claimed.
