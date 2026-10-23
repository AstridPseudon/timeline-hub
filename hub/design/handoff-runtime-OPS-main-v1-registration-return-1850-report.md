# Runtime handoff: OPS-main-v1-registration return 1850

## Result

Corrected finite proposal only. The earlier author1840 result was a no-op and
the independent1848 review was **FAIL** because it treated hidden `.why`
refusal explanations as active pending records. They are not executable
records; the matching c13 creation entry is completed history. This return
does not make that unsupported active-use claim.

The superseding 18:46 directive replaces further `retire-*` patching with
OPS-bench-store. Accordingly, the nine-row removal exists only as an in-memory
proposal in TMPDIR. No live `suites.conf`, env, bench, target, runtime, or
worker state was edited.

## Exact proposal

The archived source and current ORCH source compare byte-for-byte. The source
has 106 rows and 106 unique `(repo, suite)` keys, SHA-256
`f64e1f4be56cb6045058494db95fd10878946fefdf50f4563af532887a89c1d0`.

The proposal removes exactly these executable rows and no other bytes:

| source line | suite | before line SHA-256 | proposed state |
|---:|---|---|---|
| 5 | `registered7d-current-integration` | `8a6d36d5d483c8c5669d122496e70a115dec300ec28f7921936b853aca4820f3` | absent |
| 85 | `registered-native-render-integration` | `ca865986221775bb6db7abe0ffbde85be755857f5cc54f6fb52827294d476fe2` | absent |
| 92 | `registered014-render-integration` | `6c27e4d676e6c219e4b97bb721701334cfeb65246d354e2b3bf9caa0527f6353` | absent |
| 105 | `custody-root-cause-exact7d-trace` | `de4ac0a0092e21121abd26ccedc54ac04229ed5836dd13d8252e41f39b6fba1e` | absent |
| 109 | `custody-root-cause-exact7d-trace-clean` | `7e24566761c38fee5a222ae80ae1d7e2970fa967ff0778b9e5356fa0d1693eca` | absent |
| 111 | `custody-root-cause-exact7d-original-order` | `fc1f0c3ef28312326716247cdbd12b1601bbb4e056d2631688c23297de26c2e4` | absent |
| 113 | `custody-root-cause-exact7d-guard-context` | `c7ae7baacd735f94acbf52e93b7dc4f05b6a64eef080a9edf9491b773f77d013` | absent |
| 114 | `venv-agent-child-s2-c13-c13-full` | `e53d5bb0c12234f5cda78252070fbcaab78ac937ee1572194216ef4db77aae4e` | absent |
| 120 | `full-remotion13-s2-integration` | `da81f16c1b179fa7b57fb255beb5dc620641c100f6f79f995c522250c98b1ffe` | absent |

The proposed config is 97 rows, 97 unique keys, SHA-256
`570680d5a9941c87a9cb566471aeab91b95fabaac94f2036c8f0a48194bec70d`.
Old s2/c13 references are absent from executable rows; the historical comment
at source line 81 is intentionally retained. Row 56 remains exactly
`ffdb0b13c65f106d7b818208343feb3f438dfc943f4af57c5f612ddcf73dc036` after
LF stripping. All five direct env hashes remain exact, including approved
`agent-remotion.env` `e53a69a465e05976dcf7a781f420b1c7def64a13691f7a5f387f6a0609a6da02`.

## Lifecycle boundary

The supported queue directories contained zero non-hidden pending, running, or
leased records. The `.why` files are refusal explanations only. The c13
creation record is completed history. OPS-bench-store is staged only: its core
must pass independent review and installation before a production caller uses
the new store. No eviction, retirement, cleanup, target request, retry,
provisioning, chmod, daemon action, `/proc`/host probe, ledger, or new
registration was performed. Frozen C0v2/34e request-reply shapes are unchanged.

## Validation

All commands ran against the private proposal/TMPDIR, not the live config:

```text
python -m py_compile /tmp/w-ae24216c2e/validate_proposal.py
PASS
python /tmp/w-ae24216c2e/validate_proposal.py
PASS: originalcmp; 106 -> 97 rows; 106 -> 97 unique keys; old refs absent from executable rows; only nine rows changed; row 56 and five env hashes protected
git status --porcelain=v1
PASS: empty
git diff --check
PASS
```

No Runtime product tests, typecheck, or lint were applicable to this metadata
proposal. No full or live-socket suite was requested. The worktree remains at
Runtime `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d` with no source diff.

Artifacts:

- `handoff-runtime-OPS-main-v1-registration-return-1850-proposal.patch` — exact proposal only; not applied.
- `handoff-runtime-OPS-main-v1-registration-return-1850-manifest.json` — hashes, scope, and lifecycle facts.

Next step: independent review of this proposal and the newstore core; only
after that review/install may the approved lifecycle route be considered.
