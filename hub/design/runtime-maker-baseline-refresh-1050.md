## Result

Refreshed `candidate/make-child-venv.baseline` from the exact reviewed Git object and updated its existing manifest hashes.

- Source commit: `ab6d49bfb15f971788283f65f303a86dc0b53de2`
- Source tree: `a494ab2f1f8b623069a6633f0048c06b06ada362`
- Source blob: `05b17676eef4932180d6aa2eefb485ae106f1193`
- SHA256: `c1197e1a3407e970c02ff50519f800296905b89ad113ad32b9a41516a50fa3b6`
- Live and normal-hub copies matched byte-for-byte.
- Strict test file hash unchanged.

Tests/checks:

- Targeted pytest: `1 passed`
- `bash -n` baseline: passed
- `git diff --check`: passed
- Manifest JSON validation: passed
- Old baseline/live comparison: expected RED (`e4c0a9…` vs `c1197e1…`)

Only the permitted baseline and manifest entries changed. No real-child credit or production behavior is claimed. Completion marker and commit message were created.