**FULLFINAL READY — harness repair only.**

Updated only P2/P3 rows in `tests/suites.conf` atomically. P2 uses `27340`; P3 uses `37340`. Each row exports its port before setup/build, checks availability with a bounded localhost bind probe, and carries it through export/eval into the original body.

| Gate | Existing target | App source / tree |
|---|---|---|
| P2 | `app-P2-bootstrap-ready-sol-2328` | `d96e45cab356e66332050aa902558789b4382dbd` / `1764a55c7e3255628fb750b1f9d22c189289765c` |
| P3 | `app-P3-bootstrap-ready-sol-2330` | `82de83a0b2be5d92e4943c18ff1cbf9aeeca753e` / `7871e4d2e3d9efaf093a7274c2b0662fa74536f6` |

Final row SHA256, including newline:

- P2: `bde3b8e1fc2998dd0a588a32a17fa2b842bb007109431bef0669574181a8aff0`
- P3: `0d73e0f6f88db6010dcdbd06b0567f6ac40539e1a1c4087ba0d26946ebe641ba`

All **245 outside rows**, including P1, remain byte-exact: **460353 bytes**, SHA256 `a6efacb0d01e1b8bceede6fa8354115a01b151c31c000d2644f4a88c0e51fcf2`.

Retained failures confirmed:

- **P2 actual7232:** native startup refused occupied `17340`; exact 893-byte stderr SHA256 `84c7e34708ca559368ad786d12b771f376fdfc25063bcab51affbcfdbf764835`.
- **P3 actual458:** exit 2/125s. Native seed/history passed; mandatory mounted leaf failed at `outbox-read`, receiving `unknown` instead of `verified`. This is a distinct unresolved failure.

Validation commands, with `TMPDIR=/tmp/w-4b506ad61f`:

- `python3 "$TMPDIR/repair.py"` — inner/outer Bash syntax and inverse-edit byte equality passed.
- `python3 "$TMPDIR/qualify.py"` — **40 checks passed**: argc2/`-c`/payload identity, real and synthetic static positives, source negatives, free-port proofs, and missing/wrong/noninteger/out-of-range/occupied refusal.
- `python3 "$TMPDIR/stages.py"` — **80 checks passed**: consistent ports through build/setup/native/list/leaf/body, carrier inheritance, and failure ordering.
- `python3 "$TMPDIR/install.py"` — atomic fresh-read replacement, outside-byte equality, final syntax passed.
- `python3 "$TMPDIR/final-controls.py"` — **40 checks passed**, including real hosted-origin configuration and unchanged original tails.
- `git diff --check` — passed; App source remains clean at required base `9abaacd9eaa55c82571a0b4eda2ff1fabc0ae5ba`.

Original pins, guards, assertions, selectors, limits, and automatic origin allocation are preserved. No unknown listener was touched. No actual build/native/list/browser/backend/service run occurred. Availability probes do not reserve ports against unrelated future listeners.

No implementation blocker. **P3 readiness remains unverified.** Manager next: one run each, in parallel, targeting the existing P2 `full-e2e-three-products` and P3 `ap2-P3-gate5-h6-0348` rows.

Commit message and `DONE` written.