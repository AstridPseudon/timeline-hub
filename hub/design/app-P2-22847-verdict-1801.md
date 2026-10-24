## P2 verdict correction: FAIL

> **Hub headline — corrected original-gesture result:** The SAME-ID run `app-pin-587316e3-d73-p2-current-1747-1024175319-22847` selected 8 original cases, executed 3, and produced **0 PASS / 3 FAIL / 5 NOTRUN**. **Readiness is separate: 1 PASS**, and is not an original gesture result. Element apply **failed** after `14.506s` because dialog status `"applied"` was absent after `5000ms` and retained UIApply evidence ended `pending`; popup ADD **failed** after `35.080s` with HTTP `422`, `validation_error`, `invalid_records` because the provider reported authenticated-occurrence ownership mismatch; parent move **failed** after `115.403s` because the expected `Committed ...` revision label was missing at lines `631/689`. RegisterAsset save, automatic child placement, popup SWAP, transition None single, and transition None bulk were **NOTRUN**. The verdict is **FAIL**.

### Correction provenance

This is a finite accounting and wording correction, not a new run. The immutable original worker report was preserved untouched; its flat `8 selected / 4 executed / 1 PASS / 3 FAIL / 5 NOTRUN` line incorrectly counted the separate readiness PASS as an original case. The independent first-return worker `app-P2-22847-verdict-count-return-1809/report.md` establishes the corrected `8 selected / 3 executed / 0 PASS / 3 FAIL / 5 NOTRUN` result and confirms that the original worker report and producer report were not modified.

| Input | SHA-256 |
|---|---|
| Immutable original worker report `app-P2-22847-verdict-1801.md` | `44af867779c4c59bbc93aaf469260433e882e7246b18bc3ffd3b2d0da360f10f` |
| Independent correction `app-P2-22847-verdict-count-return-1809/report.md` | `a654e727d6785999105552b8705442c84510f304f6519230a60cbe2c76669a99` |

### SAME-ID run

`app-pin-587316e3-d73-p2-current-1747-1024175319-22847`

- Exit `1`, terminal duration `402s`.
- Original cases: **8 selected / 3 executed / 0 PASS / 3 FAIL / 5 NOTRUN**.
- Direct JUnit: `tests=8 failures=3 skipped=5 errors=0`.
- Separate readiness XML: **1 PASS**; this PASS is excluded from the original-case totals above.

Case boundaries:

1. Element apply — **FAIL**, `14.506s`. Dialog status `"applied"` was absent after `5000ms`; retained UIApply evidence ended `pending` at teardown. No accepted response was proven.
2. Popup ADD — **FAIL**, `35.080s`. HTTP `422`, `validation_error`, `invalid_records`: `provider created shot owner differs from its authenticated occurrence`. This is the observed provider validation result; no additional source cause is inferred.
3. Parent move — **FAIL**, `115.403s`. The accepted path reached reload, but the expected `Committed ...` revision label was missing at lines `631/689`. Guarded undo was unproven.

Explicit NOTRUN cases:

- registerAsset save
- automatic child placement
- popup SWAP
- transition None single
- transition None bulk

Compared with `25943`: the element failure is unchanged; popup’s message differs and the old physical-observation cause is not reused; parent advanced beyond the old history-reads assertion and failed later during reload. All eight remain CORE.

### Tuple, snapshot, and original-hash verification

| Repo | SHA | Tree |
|---|---|---|
| App | `587316e37891f1b474c2c3734e19044246b62285` | `84886c6b1915ca9748d04bb36c0fe8b6861efca6` |
| Agent | `f4d6c72ce336da66813fc39828187bccbaf80a5b` | `5d328a24dd64fb216ae527b6c05f51d99d7c564e` |
| Runtime | `327da207ed30880fe2ae0cd0b116722bb2c6f7a6` | `0140a9ab2bf8582c4712dbf84498a6d5dcb132cf` |
| Composition | `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` | `5ab5191a296980a0a6bcd1178ab6902d6478a148` |

Actual service snapshot verified after completion: head `3a56e7a70b2c04d2c1acfbe3ca7f9b62a75ff2f1`, sole parent App SHA `587316e37891f1b474c2c3734e19044246b62285`, exact App tree, zero content diff.

Versions: Node `v20.19.4`, npm `10.8.2`, `AstridRuntime/0.1 Python/3.13.16`, protocol `workspace.v1`, schema `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`, provider `astrid-v1`, compiler `authoring-bundle-1`.

No-weakening evidence: the six protected source hashes matched:

`2b9723db262978ebbb410d5925163fe61c4a83f05f3b44fbbd524bc9df301593`, `50960dd2efadc8350b8647a1f7e88a6cad2b44907bf36a7108832ee0ea9ebf17`, `4292d0b5928e1390c48d0e33876621a2e9b6c7e0616607a72f1b3fa3873d1de9`, `07fe3d84831e2e5977405811ceaa7a592614871e15ec108d812eb024ebed2f3c`, `c0624a04200c40acaf6866d270d9b9b9665b33173565ee709df384ddcdc0e797`, `a6468188ff21c4fd8bd397ff242b0260ee92ab6f2f90ac94786973eaf3c1e99a`.

Runtime safe-phase output: **`UNAVAILABLE`**. No daemon/direct-private custody is inferred.

### Checks from the existing evidence

- SAME-ID `bin/wait-test`: exit `1`, `402s`.
- Preflight `6282`: PASS, exit `0`.
- Missing-runtime-SHA control `10754`: expected refusal, exit `1`.
- `git diff --check`: PASS.
- Assigned worktree at the source run: clean.

The retained D73 qualification is **14 passed**; Node checks passed, scoped ESLint passed, and strict-islands exited with the same known **15 baseline diagnostics**. It is not `9/9`, and the evidence does not say missing generated modules.

No retest, source edit, browser/service rerun, collector, producer, or new cause analysis was made for this correction. The production caller uses this corrected report. Full C0v2 request/replies, authenticated/canonical history, and guarded-undo behavior remain unchanged.
