## Result: PASS — exact oracle repair

Reviewed `4861a6c46` against `03d6ec851` in the permitted A4 witness test. The repair correctly matches guarded changes by ID/path and preserves:

- Subminimum values: anchor hold `0`, inserted hold `0.0667`, later position `5.0667`.
- Full payload/config mirror, null vs absent fields, opaque data, ordering, siblings, registry, and source pins.
- All four request byte lengths/hashes, base IDs, caller binding, omitted reads, and v2 assertions.
- No executor, authority fabrication, or weakened assertions.

Checks passed:

- Offline fixture/request/payload audit: 4/4.
- Pytest collection: 4 tests.
- Ruff and mypy.
- Runtime lock `34eac004`.
- Artifact manifest.
- Diff check; 3,431 outside-file identities unchanged.
- Runtime `8ea0766f` tree matches integrated `abd47e68`.

Provider bodies were not run. Prior evidence remains **4 FAIL / 16 PASS**. Authentic prepared-media authority is still missing, so App/Runtime acceptance remains blocked; no acceptance, P1 qualification, or merge approval is claimed. The denied 2017 artifact was excluded.

Created the required commit message and `DONE` marker.