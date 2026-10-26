# P2 D141cc single-transition custody review

Verdict: **FAIL_CUSTODY**. Execution outcome: **NOTRUN**. This is a custody verdict, not a product verdict.

The authorized selector was `p2-transition-none-single@original`. The native `--submit` invocation occurred exactly once and returned exit 1 before request creation, row registration, artifact persistence, or service-body execution. The exact stderr was:

`D66 source selection: D66 agent source does not match its submit-time pin: selected ecdc242ed9b673f641759ecf029f95e89c2a6f92/d362fe9dfdbd0c1fc8e0739c193ed2b74a7d2735, pinned ecdc242ed9b673f641759ecf029f95e89a2c6f92/d362fe9dfdbd0c1fc8e0739c193ed2b74a7d2735`

This is an ordinary source-guard mismatch, not a safety denial. The manually entered agent SHA differs at zero-based character 33 (`c` versus accepted `a`). The controller receipt also records the four integration checkout paths, while dispatch recipe index 2 requires the four exact detached paths. The worker log's rendered shell command shows detached paths, creating an unresolved representation conflict; custody therefore cannot pass.

Separate guard and execution findings:

- The first corrected wrapper exited 2 before reaching native `--submit` because it addressed `evidence/evidence/candidate/controller.py`. This is a controller guard failure, not a second native invocation and not a test result.
- The later native invocation was the only native invocation. There was no retry, second submit, direct request-test, wait-test, stop-test, alternate selector, body, or cleaner outcome.
- Read-only namespace checks found no exact suite registry row, no actual request directory, no submit artifact, no lock, and no request ID. The assigned output directory contains no service artifact; the native stdout is empty and stderr is the exact 256-byte guard error.
- The current four source pins and trees are exact and clean in the detached pin worktrees, and the builder SHA/blob match the accepted recipe. This does not convert the guard failure into a source or product PASS, and no product-registry inference is made.
- The controller's initial sampler was output-only and reaped. Retained session 44814 wrote the direct trace, was polled at 5-second intervals, stopped with SIGINT, waited, and reaped. `first_tool_direct_trace` remains false. The reviewer trace is supplemental and also does not claim first-tool coverage.
- The worker's final validation command raised `KeyError: 'native_invocation_count'` against `controller-receipt.json` and still created `DONE`; the report's earlier JSON validation PASS is not treated as validation of that failed final command.

Therefore this selector is finitely closed as custody failure with execution NOTRUN. It is not a valid journey GO and must not be retried by this controller. D141ff popup known-gap notes and other selector outcomes remain outside this single-selector verdict.
