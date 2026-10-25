# OPS Farm installed custody review

## Result

PASS — source-only installed custody review. No composition, product, kit,
test, pin, Farm child, package, or live-maker mutation was performed.

## Exact artifact custody

| Artifact | SHA-256 | Mode | Size | Result |
|---|---|---:|---:|---|
| reviewed candidate `make-child-venv.candidate` | `e62f89eaf226897a36bd4c7f715d43a7a1d4206ff371432296c01de6bdd52dc3` | `0755` | 62091 | PASS |
| installed `orch/bin/make-child-venv` | `e62f89eaf226897a36bd4c7f715d43a7a1d4206ff371432296c01de6bdd52dc3` | `0755` | 62091 | PASS; byte-equal to candidate |
| predecessor backup `make-child-venv.20261025T143328Z.bak` | `ff8dbf0ecb615a665e346b36d9d179526a58127d09749748990ea0fa885cf8f8` | `0755` | 60881 | PASS; matches installer preimage |

The installer receipt records an atomic rename. This review independently
verified the resulting installed, candidate, and predecessor bytes/modes; the
historical rename syscall itself is not observable after completion.

## Installed verifier and controls

- `bash -n` passed for candidate, installed file, and predecessor backup.
- The installed embedded `STORE_VERIFY` block compiled successfully.
- The installed production caller reads the installed script, extracts the
  exact `STORE_VERIFY_BEGIN`/`STORE_VERIFY_END` block, and passes it as stdin to
  `python3 -I -` through the existing `subprocess.check_output` call.
- Existing bounded ownership microcontrol passed against the installed bytes.
- Existing bounded diagnostic microcontrol passed against the installed bytes,
  including control/absolute/long names, bounded printable diagnostics,
  content non-leakage, and refusal preservation.
- C0 inventory passed for request scope/base IDs, commands, label, step fields,
  merge/reads/dry-run, `Idempotency-Key`, accepted/merged/preview vocabulary,
  canonical document/receipt/head/effects/bindings/dependencies, and conflict/
  invalid code/path/hint vocabulary.

## Boundary and cleanliness

- Composition HEAD: `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`; worktree clean.
- No maker/provisioner/fullmaker process was observed in the bounded process
  check. Pending queue markers were unrelated test jobs, not installer work.
- Actual Farm root remains `INFERRED`/unobserved; no genuine refused layout was
  available. This review is not an additional Farm approval stage. The lead's
  one authorized normal reissue remains downstream of propagated hash
  verification.
- No full provider/body execution, child-venv reissue, package installation,
  metadata inventory, Git/livekit/hub/remote/upstream access, M5 work, or
  credentials were used.
