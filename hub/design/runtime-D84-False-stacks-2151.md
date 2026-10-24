Completed the single authorized run. No product or test sources changed.

Agent: `197d780dca51949605c02352e7d1089a087aaa11`, tree `9deb9f157f5af433a884d5153c06e3a5223af7ef`. Runtime: exact `bc04caa23f4b503fc55e49769ead20677904702a`, tree `fa696b342468ae191735409822fa3c7c66f8a590`.

| Dump UTC | Elapsed | Test stage | Main-thread observation | Cumulative CPU |
|---|---:|---|---|---:|
| 21:52:59.115613Z | 30.0085s | Redo, test line 550 | `timeline_commit_validation.py:120 reuse` | 23.7803s |
| 21:53:13.117770Z | 44.0107s | Final ABA-refusal request, line 557 | `jsonschema/validators.py:396 descend` | 35.9295s |

Both stacks traverse `_capture_records → validate_sequential_capture → _historical_sequential → _verify_accepted`. Both show computation inside `RequestCommitPort._read:215`, after its mutex acquisition. Neither samples a main-thread lock, condition, socket or outbox wait. The waiting thread at 30s belongs to the pending diagnostic timer.

Main-thread CPU increased **12.1491s over 14.0022s wall time**, with progress from redo to the final refusal check. This demonstrates sampled computation, but cannot quantify individual costs, exclude intervening waits or establish daemon contention. **Causal lock attribution remains UNKNOWN.** Request ordinals were not instrumented.

Exactly one pytest case ran:

```bash
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --junitxml=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D84-False-stacks-sol-2151/evidence/original.xml 'tests/core/test_timeline_element_publication_runtime.py::test_public_helper_restart_exact_retry_later_head_inverse_redo[False-None]'
```

Result: **exit 1**, pytest-timeout at **45.008s** in JUnit; CLI reports **1 failed in 46.56s**. `git diff --check` passed. Test-file, body and AST hashes match before/after; both checkouts remain clean. Timers were cancelled and the raw dump closed. Raw stacks, stdout and JUnit retain mode `0600`.

Handback for owners **2145/2147**: [safe observations and limits](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D84-False-stacks-sol-2151/evidence/safe-summary.json). Exact environment, origin hashes and intact outputs are alongside it. Use these observations in the existing investigations; no further original was run.

Service6749’s terminal summary was unavailable locally. No capture blocker remains. Conventional `R2D84` commit message and `DONE` were written.