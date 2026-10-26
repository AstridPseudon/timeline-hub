# F/D141i command review — FAIL

## Verdict

`FAIL_COMMAND`. The command is not safe to admit to the one authorized local
measurement in its current form. This review did not run the command, pytest,
collection, provider/product imports, or the recorded dry controls.

## Blocking findings

1. `D141I-COMMAND-001` — `measurement-command.sh:47-50` defines:
   `exit "\${2:-78}"`. The escaped expression is literal rather than a
   numeric shell expansion. Every `die` call omits a second argument, so
   refusal paths do not deliver the intended bounded default status.

2. `D141I-COMMAND-002` — `positive.manifest:37` declares
   `.../private/measurement-runs/agent-core-full.xml`. The command sets
   `RUN_ROOT` to `.../private/measurement-runs/agent-core-full` and passes
   `--junitxml="$2"` with `$2` equal to
   `.../private/measurement-runs/agent-core-full/agent-core-full.xml`.
   Manifest declaration and actual argv destination do not match.

3. `D141I-COMMAND-003` — line 306 runs `record_disk after_body >/dev/null
   || :`. A terminal disk trace read/write failure is therefore ignored, and
   `record_disk` does not set `evidence_rc`; a zero body and monitor exit can
   still reach PASS despite missing terminal disk custody.

4. `D141I-SOURCE-004` — the positive manifest and source manifest bind the
   profile lock hash ending in `...be18e`, while the actual existing
   `runtimes/agent-remotion-v3-819acf-1110/package-lock.json` hashes to the
   value ending in `...be18d`. The current environment receipt does not match
   the launcher manifest. The retained prep dry-preflight claim does not cure
   this current static mismatch.

## Passing finite checks

- Candidate hash matches `command-diff.json`:
  `0486505ae868d24b871c32575be95341887cfaf8bcae0877e8ac1c41791c1abf`.
- `bash -n` passed for the candidate and the pinned launcher.
- All five prep JSON files parsed with Python standard-library `json`.
- Positive/poison manifest hashes match `manifest-diff.json`, and the only
  changed field is `agent_sha`; poison uses exactly 40 zeroes.
- All four exact source tuples were read-only verified at the requested
  commit/tree, clean status, exact path, and official origin.
- Interpreter, Node, profile archive/registry, runtime lock, and both 4d74…
  schema-copy receipts matched; the profile lock receipt is the exception
  above.
- The candidate retains the exact D134 1848 22-root selector order and
  `-q -n3 -o addopts= -p no:cacheprovider --timeout=45`; all 22 roots are
  present in the exact Agent tree.
- Launcher `run` mode and `-m pytest` are retained. The launcher source writes
  request and run manifests, while the candidate structurally retains source
  before/after, raw streams, runner/JUnit/exit, caller argv, disk trace, and
  KEEP paths. None were executed here.
- Admission/stop thresholds are 4,700,000,000 and 4,000,000,000 bytes, with
  one nonblocking heavy lock and no D134 clock gate or additional gate file.

## Boundary

This is a command/source qualification result only. I did not fix author
artifacts, rerun unchanged controls, submit a service request, inspect a test
body, or grant any behavior/REG/ship credit. No alternative route is proposed.
