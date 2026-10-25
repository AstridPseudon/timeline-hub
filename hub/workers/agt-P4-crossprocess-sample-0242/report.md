Repaired the private observer and completed **one corrected sample**: `agent-p4-current-becfe-http-3legs-1025025625-25257`.

The unchanged original **failed at 45.557s**. Capture succeeded: **432 samples, all 10/25/40 checkpoints, zero sampler errors**. Main-thread CPU was **42.63s over 46.32s wall**, including failure reporting.

| Checkpoint | Actual elapsed | Main CPU since start | Main stack top |
|---|---:|---:|---|
| 10s | 10.050s | 8.43s | Runtime `digest` |
| 25s | 25.087s | 22.62s | stdlib JSON decoder |
| 40s | 40.002s | 36.64s | Runtime `digest` |

Runtime was the nearest product frame in **402/432 samples**; digesting and SQL execute/fetch/recheck accounted for **319 leaf observations**. Agent rules/duplicate-validation frames were absent. This establishes sampled locations, not exact function CPU attribution.

| Note | Undo wall / CPU | Redo wall / CPU |
|---|---:|---:|
| 1 | 1.426 / 1.354s | 2.514 / 2.389s |
| 2 | 5.003 / 4.711s | 3.869 / 3.641s |
| 3 | 10.286 / 9.763s | 4.839 / 4.466s |
| 4 | 12.393 / 11.723s, interrupted | Not reached |
| 5–10 | Not reached | Not reached |

The test, Agent provider, and real Runtime HTTP handler shared **PID 13309**. There were **zero Python CLI spawns** and two inline CLI calls totaling **0.202s**.

| Native child PID | Executable | Observed lifespan upper bound | Final CPU |
|---|---|---:|---|
| 13795 | git | 0.0027s | UNKNOWN |
| 13797 | git | 0.1049s | UNKNOWN; last observed 0.02s |
| 1264 | ps | 0.0134s | UNKNOWN |

Startup through collection took 1.199s. Background server polls overlapped execution; no explicit sleeps were observed. Sampler CPU was **1.365s**; other observer overhead remains unisolated.

Validation:

- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python diagnostics/test_p4_observer.py` — **4 passed**. Fake-clock checkpoints and durable serialization passed before the original; the prior writer reproduced its `TypeError`.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check --no-cache diagnostics/p4_sample_0233.py diagnostics/test_p4_observer.py` — **passed**.
- `git diff --check` — **passed**.
- `request-test integration:agent p4-current-becfe-http-3legs --no-cache`, then `wait-test agent-p4-current-becfe-http-3legs-1025025625-25257 1` — **exit 1**, original timeout.

Fixed d407/6634/4b984/635f checkouts, original hashes, profile, positive-once/17 and poison-zero controls passed. Raw artifacts are private `0600`; the service row was restored. Retained caller lines corrected inherited redo phase labels during analysis.

[Detailed results and origins](/home/user/work/wt/agt-P4-crossprocess-sample-0242/diagnostics/p4_sample_0242_results.json). No product fix or repeat body ran. Prior 30057 facts remain preserved. Commit message and `DONE` written. Manager should assign the next bounded investigation around Runtime history verification/replay-key and SQL work while preserving authority guards.