# OPS Farm metadata finite-input return

Disposition: SOURCE_ONLY successor; no Composition, product, LiveKit, Git, or
Farm installation/retry was performed.

## Evidence boundary

The Farm reply at `peer-farm-to-runtime-20261025T1412-h14-refusal-retained-evidence.md`
confirms that the failed entry was cleaned and staging is empty. The actual
RECORD row is therefore unavailable and is not claimed as observed. The
generated `licenses/LICENSE` layout remains an independently validated source
backed inference only. This successor does not add an install gate, retain a
child, or attempt to reconstruct the missing inventory.

## Successor delta

Base: reviewed 1417 candidate `d2da4aecd759999fe1d7c929b82403533746df746c50b9928f97d083605b2a3a`.

The only new behavior is in the existing embedded `STORE_VERIFY` refusal path:

- `metadata_diagnostic_ref()` emits at most 96 printable ASCII characters;
  normal safe names are `distribution:relative/metadata/name`.
- Newline/control, absolute-looking, unsafe, and long names use a sanitized
  bounded prefix and a 12-hex SHA-256 suffix. The path is still rejected; the
  diagnostic formatter never changes verifier path handling.
- `fail_unowned_metadata()` retains the fixed reason
  `unowned local distribution metadata: ` and adds only the distribution and
  relative metadata row. No file content, host path, credentials, request
  body, or raw exception is included.
- The existing `python3 -I` caller captures only verifier stdout for the
  inventory. `SystemExit` writes this fixed reason to inherited stderr, which
  is the existing refusal/error-log stream and survives the normal staging
  cleanup without copying or preserving a child.

The reviewed ownership rule is unchanged: the only extra accepted row remains
`licenses/LICENSE` when its bytes equal authenticated committed source
`LICENSE`; all other unowned metadata remains refused. RECORD integrity,
immutable source, source identity, symlink, extra-file, and registration guards
are unchanged.

## Private installation plan

After independent final delta review, the Runtime lead may atomically install
the exact successor as `make-child-venv.new`, preserve the installed
`ff8dbf0ecb615a665e346b36d9d179526a58127d09749748990ea0fa885cf8f8` predecessor
backup, verify the successor hash, and then authorize one normal Farm re-issue
on the owner-approved tuple. This worker did not install, retry, register, or
touch the live kit.

## Checks

- `python3 evidence/test_metadata_ownership-1417.py`: PASS.
- `python3 evidence/test_metadata_diagnostics.py`: PASS, including bounded
  output, newline/control and long names, absolute-looking names, content
  non-leakage, and refusal preservation.
- `bash -n evidence/make-child-venv.candidate`: PASS.
- Embedded verifier `compile(..., "<STORE_VERIFY>", "exec")`: PASS.
- Ruff candidate versus baseline: both retain the same 2 baseline findings
  (`I001`, `SIM102`); no new finding.
- mypy candidate versus baseline: both retain the same 7 baseline findings;
  no new finding.

The complete command outputs and the minimal diff are in this evidence
directory. C0 request/reply shapes were not changed.
