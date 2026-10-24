## Review result: FAIL for final custody; module-only controls PASS

Reviewed `bea3081a84822c524ed1d259e9b57caaa2bbd529`:

- Tree: `4b1025b5c03016354d1e608f397b23b7b1e8c6e1`
- Parent: `c5525bffa62fc36adcb21c93adb401e0fb28b827`
- Worktree unchanged; no self-fix performed.

Positive controls passed:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile working-service-binding.py working-service-binding-control.py
python3 working-service-binding-control.py
python3 -O working-service-binding-control.py
git diff --check
```

Both normal and `-O` controls reported `PASS`.

Exact adapted hashes:

| Stage | Source | Body | Env region | Protected prefix | Protected suffix |
|---|---|---|---|---|---|
| P2 | `f6042b33d35229f47fe74cbd2a575b5984422d2209ed664b996fe1b590656d43` | `7f2f68f1eefec5cf124b2efc1912919c1bd9906f604bfcc896a0d775ac802c24` | `9ac45d405e0cb2581241e3909d45190bd77ea87ab6b1d5fc42aab785c94f63ff` | `3b530ab9bd3dcf74354913fbb7b22f12f723a71d5c00d152bb2cbacd6effe92c` | `2e7d6e669d5dd6a9825aa4b3a2e99f3989ab96038d1c199addcc9f6a7e7a462c` |
| P3 | `6366048bf89533fa450a4575288ac2de004696bab49db6d32f1869783ae493f3` | `07327c899cc7e122caa65b2c936a0cf1e3d9bac45873067c15b3e75179120327` | `ea50daf13b5d8bb1b5e88f18c42f22aabaf4b3a00e123e1c3a0bd2b145aee6eb` | `3d4e7a9478dc6ad4ad75c52121617f7d7f5829b25a95ac3a935f7388f5f1ca4c` | `accaafd0928a5a18c29d3a952306112886262a41dda785b768e527f739a4260d` |

Both regions are 2122 bytes. In-memory wrapper checks passed: `argv=1`, export present, failure guards present, `bash -n=0`.

Readonly imports passed for both real interpreters:

- Agent venv: Agent/client/schema origins resolved correctly.
- Runtime venv: Runtime/protocol origins resolved correctly.

Blocking findings:

- `_region()` accepts an injected earlier `P2FAIL`/`P3FAIL` marker, so the old-child boundary is not unique.
- Protected prefix/suffix mutations are accepted; hashes are calculated dynamically rather than checked against approved constants.
- A stale source parent or `ref` is accepted.
- Arbitrary valid client file and runtime-artifact digests are accepted.
- The adapted block assigns `RCPY`, but retained P2/P3 launch code sets `ASTRID_RUNTIME_PYTHON="$CPY"` and uses `CPY`; the Runtime interpreter is not actually used.
- `caller-publication.py` does not yet import or call the adapter. Import check: `PASS; adapter seam: NOT INTEGRATED`.

Recipe/current tuple mismatch:

- Recipe `ed81088e…`, tree `a75cebb9…`, parent `0971c645…`, records App `bbed290d…`.
- Current App is `6ab5938d34d75fe9f90f4c21f2518dfd1b6e847d`, tree `d39d5ece2e004f2af7505f9b452894192cd6dec7`, parents `1da6cbd… d5e9de…`.
- Current Agent: `9b055a93ff15fce0a2e80f2647d47743b1fc4c33`, tree `ed0043…`, parents `cba425… 156f2…`.
- Current Runtime: `becfe6db88b2cc034dba3fafa6c050117cdf2b06`, tree `7edc08…`, parents `46eb068… c021f1…`.

The stale recipe passes the module-only control but must not produce final `READY`.

Next mechanical join: regenerate/authenticate the final tuple after App merges, then in `caller-publication.py::rebind()` call `adapt_environment_block()` on the already source-rebound decoded body, retain its returned hashes, and update the retained launch environment so Agent uses `CPY` while Runtime uses `RCPY`. No live service, browser, HTTP, backend, native, or full-suite execution was performed.