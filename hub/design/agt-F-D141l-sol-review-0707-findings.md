# F D141l Sol0638 executable command review

## Verdict

**PASS_COMMAND**, with `BLOCKED_EXISTING_CONTROLLER_BINDING_MISSING` retained as
the only remaining status. The command sources and their executable controls
qualify as source/control evidence. They do not qualify the real pair, a full
body, behavior, REG0, any gate, or ship.

## Findings from 0508 FAIL9 and 0626 FAIL7

- **F-D141L-001 — closed.** The source manifest and executable source bind the
  clean current Agent `ecdc242e/tree d362fe9d`, Runtime `95d98f/tree78df31`,
  App `4de54db/tree84c3fb`, and Composition `635f4de/tree5ab519` tuple. The
  genuine Agent home receipt `agent-U4a-D141-postREG-home-0622.json` and App
  home receipt `app-D141s-postREG-source-home-0545.json` are read-only,
  SHA-bound, and checked against the tuple. The App receipt's old Agent
  observation is retained as historical observation; it is not used to restore
  the stale 8585/6a pair and no future-adoption condition is invented.

- **F-D141L-002 — closed.** The checker resolves every selector against source.
  The cut has 22 existing roots and the pristine comparator has 17 existing
  roots. The corrected v10 path is
  `tests/v10/test_timelines_create.py`. The five missing pristine own-ID roots
  are explicitly source-backed N/A; no copied test, skip, xfail, or implicit
  PASS is used.

- **F-D141L-003 — finite controller/route blocker, not a source defect.** The
  author packet correctly removed invented authenticated JSON acceptance. The
  current `suites.conf` row still invokes the old 0309 command with the fixed
  0249 receipt/brief, whose service `agent-agent-core-full-1026025151-24049`
  is a terminal refusal. The pristine row remains the old 0030-era command.
  The repaired checker authenticates the genuine old receipt/brief by exact
  path, schema, controller, service, bytes, and hash, then refuses that old
  service as current admission for both new recipes. It therefore cannot
  produce a current-pair admission from caller JSON or a scratch fixture.

  The exact permissible next action is external to this source review: the
  existing controller must bind a current pair through the established
  request-test/test-run route, including the real request/service row, current
  source tuple, command, distinct command/source manifests, owner brief and
  exact hashes. The command source may then consume those concrete bindings.
  No source-authored receipt, new authentication schema, new kit/interface, or
  second approval gate is permitted. Until that binding exists, the pair stays
  unstarted and not executable-qualified.

- **F-D141L-004 — closed.** `MANIFEST=positive.manifest` and
  `SOURCE_MANIFEST=source-manifest.json` are distinct, separately hashed
  inputs. Custody includes both and the checker rejects aliasing or equal bytes.

- **F-D141L-005 — closed for the allowed tiny control.** The actual unchanged
  production launcher and approved stub were executed through
  `tiny-controls.sh` on the current manifest: positive was exit 17 with one
  stub call; the agent-SHA-only poison was exit 1 with zero calls. These are
  launcher controls only and are not a pytest/full-pair result.

- **F-D141L-006 — closed.** The exact checker invocation executes the real
  command sources' shell syntax, current source/path and clean guards, rendered
  argv and forwarding, launcher controls, adversarial receipt/brief mutations,
  XML/raw/custody lifecycle fixtures, mutation-after-seal checks, and 5-second
  disk sampler fixtures. Its 10 admission and 36 lifecycle cases are not copied
  PASS declarations.

- **F-D141L-007 — closed for source/control evidence.** Before/after source
  witnesses, interpreter/runtime and caller/service witnesses, owned raw/XML
  outputs, protected KEEP, exact inode/owner/mode/content custody, final output
  sealing, and source equality are checked. Body, monitor, disk, evidence,
  cleanup and source failures propagate into final status and exit; the trap
  stops and reaps the owned process group before final capture. The source does
  not silently scrub changing hashes or late failures.

## Additional retained limits

The D89d calculation is independently consistent:
`X=max(4826488832-4311924736,4692029440-4311924736)=514564096`, and
`floor=max(4600000000,4000000000+X+200000000)=4714564096`. This is applied
once by the genuine controller at dispatch; preparation retains only the
continuous 5-second/4,000,000,000-byte stop. Both command paths use the same
`-n3`, cleared `addopts`, `-p no:cacheprovider`, `--timeout=45`, venv-agent,
Node/profile/plugin environment, with one heavy pair lock. No own-preparation
re-gate is added.

The whole-path 0640 report is retained only where current read-only facts agree:
the clean tuple and the absence of any body/admission execution. Its earlier
"no named row" observation is superseded by the current read-only
`suites.conf` row shown above; it is not repeated as a fact. The historic
0500 trace gap remains disclosed and is not backfilled by this review trace.
