# P4 D141l independent source review

Verdict is deliberately split:

- `SOURCE_QUALIFIED`: the review worktree is the exact Agent `ecdc242ed9b673f641759ecf029f95e89a2c6f92` base, all four advertised source tuples/tree/parents are clean and match, the approved selector is present with its predicates unchanged, and launcher/installer bytes match the packet.
- `FAIL`: the required same exact author checker exited 1 before its checks because `/home/user/work/wt/app-P4-D141l-cli-source-host-0825` no longer exists. This is a source-packet reproducibility failure, not a product behavior failure.
- `PRODUCTION_INPUT_MISSING`: the production registry state, historical profile, production body-evidence directory, and production JUnit output are absent. The source packet records these gaps honestly; no profile was provisioned and no body was run.

Checks and results:

- Exact author checker command: exit `1`, traceback at `git -C /home/user/work/wt/app-P4-D141l-cli-source-host-0825 branch --show-current`.
- Review source identity: Agent `ecdc242ed9b673f641759ecf029f95e89a2c6f92`, tree `d362fe9d`, clean; Runtime `95d98f03`, App `82e9e13d`, Composition `635f4de0`, all clean and matching the packet.
- `python3 -P` AST checks for `check-source.py`, `tools/install_p4_launcher.py`, and the approved test: PASS. `bash -n` for launcher and positive stub: PASS. Git diff/diff-check: PASS/clean.
- The generated production input manifest exists with mode `0600` and required source, environment, profile, interpreter, timeout/JUnit, and service fields. Its profile registry field is explicitly `MISSING`; the future runmanifest and production JUnit do not exist.
- Candidate row has one approved selector, `run -- -m pytest`, `-m integration`, `--timeout=45`, `-p no:cacheprovider`, the restricted environment, and the same durable JUnit path as the production input manifest and argv. The actual future runmanifest cannot be checked because no production preflight/body occurred.
- Author positive/poison claims were inspected as tiny controls only: positive stub is the recorded SHA and exits 17 with one call; poison differs only in Agent SHA. The positive runmanifest exists; its advertised control JUnit file does not, consistent with the stub not producing JUnit. No pytest collection, product import, service request, request-test, wait-test, install, CAS, registry, queue, or source-pin operation was run by this review.
- Product typecheck/lint are not applicable because this is operational-only source review with no product edit.

Trace lifecycle is in `sampler-lifecycle.json`; the primary trace validated with 21 samples, minimum 4,789,325,824 bytes free against the 4,000,000,000-byte stop. A separate controlled probe recorded SIGTERM, wait, reap, and validation exit 0. The primary sampler observed its review shell's premature exit after a command error; that lifecycle gap is disclosed rather than claimed away.
