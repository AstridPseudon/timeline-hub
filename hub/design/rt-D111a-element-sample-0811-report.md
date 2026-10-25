## D111a report

Implemented private diagnostic-only files:

- [native launcher](.../diagnostics/measure_d111a_native_element.mjs)
- [passive sampler](.../diagnostics/sitecustomize_d111a.py)
- [targeted test](.../diagnostics/test_d111a_native_sample.py)

Evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D111a-element-sample-0811/evidence/` — 216 KB, raw files mode 0600.

Final central test:

```text
request-test ... targeted --files "diagnostics/test_d111a_native_sample.py" --no-cache
wait-test ...-1025081301-2078
PASS: 1 passed in 33.15s
```

Source fidelity:

- Runtime `1daca2a33f6d7b10053e07c539a54843e3984e19`
- Agent `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2`
- Genuine provider seed and native request path
- Refusal control: HTTP 401
- Element request: HTTP 200 with receipt
- PID 12503, `python3.13`, birth ticks `14688060`
- Request wall: 4522.7 ms; Runtime stderr SHA256: `e3b0c442…2b855`

Profile:

- 135 samples, 20 ms interval
- 260 lost samples
- Observer CPU: 421.0 ms
- Inclusive top Runtime frames included `service.py:438`, `timeline_commit_store.py:173`, `server.py:1208`, `server.py:528`, and `server.py:313`
- Inclusive overlap is explicit; shares are not additive or self CPU.
- Evidence points to Runtime store/port read/history evaluation as the next source-owner area. No optimization was made.

Checks passed: Python compile, Node syntax check, Ruff, `git diff --check`, central targeted test. No product, protected test, schema, cache, pin, or generated files changed. Full suites were not run.