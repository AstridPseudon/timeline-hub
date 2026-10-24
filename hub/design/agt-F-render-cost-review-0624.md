# Review report

Verdict: diagnostic custody **PASS**; causal qualification **FAIL/UNPROVED**.

- Qualified identity: Agent child `3b5c`, installed source `ba8f`, Runtime `f320`, Node `v20.19.4`, profile `819acf`.
- Harness SHA matched durable pre-execution copy: `7bc25e...c6302`.
- Actual child argv/cwd, declared environment, PID, result-file digest, empty stdout/stderr, return code `0`, and result identity were consistent.
- Result: 563-byte `SupportReport`, SHA `619949...ff03`, exact refusal: `clip[0] transitions are not supported in v1`.
- `ASTRID_RENDER_BACKEND` explains the expected full-environment mismatch after transport injection; declared preflight fields matched.

Original AST review:

- Function AST hash: `ca54f2...ded82`; 9 assertions.
- Ten production support executions: four loop probes, then effects, transition, opacity, params, audio-track, volume.
- Transition is execution 6, not “secondprobe”; raw `_support_reasons` calls do not invoke production support.
- Sol0603 executed only the transition call; original body did not run.

Timing:

- Caller total: `15.838s` (`15.839s` diagnostic result).
- Registry build: `11.497s`.
- Discovery scans: `5.633s` + `5.813s`.
- Transport/child: `4.334s`.
- This is 35.2% of the original 45-second global watchdog, but tracing overhead is uncalibrated and child internals were not traced. The original ten-probe `45.65s` failure remains unexplained.

Source cause boundary:

- One rendering registry build calls `discover_pack_metadata()`.
- The duplicate work is `astrid/core/pack/discovery.py:399-407`: source `scan()` followed by `scan(project_pack_root)` to locate authored `local`.
- `astrid/sdk/rendering.py:437-516` is the production caller; `astrid/core/rendering/registry.py:461-473` constructs the registry.
- Existing `2802d61c40` concerns timeline element-registry reuse in `_type_resolve.py`; the support diagnostic never enters that validator path, so it does not explain this timing.

No implementation is authorized. Existing interfaces do not prove that `scan()` and `scan(project_pack_root)` have identical authority for all callers; tests intentionally distinguish those arguments. The exact missing fact is a guaranteed per-call source-root/authority equivalence.

Checks:

- Read-only finite custody/hash/AST/timing validator — **PASS**.
- `git status --short --branch` — clean.
- No product/test changes, original body rerun, full suite, browser, render, or additional probe.

Next author must prove one-call discovery preserves complete registry contents/order, source kind and priority, collision behavior, installed/source eligibility, aliases, and all validation guards; retain separate project-local semantics for differing scanner roots; and add production-caller evidence showing the exact transition refusal. No cross-call cache, trust-surface change, broad environment allowlist, or caller-profile authority is justified.