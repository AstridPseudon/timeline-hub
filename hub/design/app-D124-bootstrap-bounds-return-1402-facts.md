# D124 facts

- Worktree base: `4b4e0558ef3853bc999dd65c0df4580ad5704eff`; parent `af5fe0a2748ce6df65fb36ce9cd435fc1df0502a`.
- Final product diff is limited to `tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts`.
- The candidate’s approved two-line fake-runtime POST/write-fixture delta remains byte-for-byte unchanged.
- Normal helper SHA: `a17a92115661fcef13b49169504ad8726e6f6c0cdce66b195128b14477fa76a4`.
- Reviewed helper SHA: `6c9daef27884c30b8faf234349078310af7ebe016bf0c4339960d5baae5a0760`.
- Validator repairs enforce finite nonnegative values, source constants (8 requests, 128 events, 64 KiB, 32 phase count, 20 ms sampling), retention/output accounting, phase status/count/timestamp consistency, duration relationships, sample-share arithmetic and safe identifier/path forms.
- A prior protected reviewed-helper capture passed the final validator. A fresh live reviewed-helper launch exited before endpoint readiness; no Runtime/helper source was changed.
- No `*.spec.ts` files changed.
