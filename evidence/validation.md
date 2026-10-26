# Validation

Static/source-only checks completed:

- `bash -n evidence/command-cut.sh evidence/command-pristine.sh evidence/positive-stub.sh` — PASS.
- Python stdlib JSON parse of `controls.json`, `admission-derivation.json`, `source-manifest.json`, and `readiness.json` — PASS.
- SHA-256 of `positive-stub.sh` — PASS: `38afc8a5b177801f86f33b0166c8ecd4489ee997629e91b336b9c248ca360ad0` was checked against the required value `38afc8a5b177801f86f33b0166c8ecd4489ee997629e91b336b9c248ca360ad0`.
- Positive/poison manifest comparison after removing `agent_sha` — PASS; the only difference is the zeroed poison `agent_sha`.
- Cut selector extraction — PASS: two identical 22-root invocations; `-n3`, cleared `addopts`, disabled cache provider, and `--timeout=45` are present.
- Pristine selector extraction — PASS: 17 unique upstream-present roots and the same four pytest flags.
- Read-only source tuple checks — PASS for integrated Agent `8585ed9c.../92a3ffdb...`, Runtime `6a011d58.../ac5b8627...`, and Composition `635f4de0.../5ab5191a...`; all inspected worktrees were clean.
- D89d arithmetic — PASS: `X=max(4826488832-4311924736,4692029440-4311924736)=514564096`; floor `max(4600000000,4000000000+X+200000000)=4714564096`.
- Pristine SHA history — PASS: `64197afa...d33e303a` exists with tree `6c0488...3e26e`; the `...d33e303e` object is absent.
- Worktree `git diff --check` — PASS.
- Predecessor comparison — reviewed the genuine D141i 0309 cut and 0318 final review, D141b `0710897c`/`0030` plain-pristine recipe/review, and 1848 controls. The current cut retains the corrected terminal checks, but the current pristine script drops the predecessor source/exit/raw/XML/disk custody pattern.

Not run by scope and policy: pytest, collection, product/provider imports, typecheck/lint, request-test, service/live sockets, full rerun pair, P4 body, launcher positive/poison body, or any production test body. The missing genuine App receipt means the launcher controls were not runnable against a genuine complete tuple.

The source worker’s genuine trace was read without backfill: 44 samples at exact five-second intervals from `05:00:57Z` to `05:04:32Z`, minimum `4693712896` bytes. The gap before that trace is disclosed in `disk-trace.txt` and the findings.
