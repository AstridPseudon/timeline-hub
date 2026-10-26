# F-final launcher whole-path findings

Status: finite independent investigation complete. No product source, registry,
candidate, installer, test body, generated file, pin, or canonical install was
changed.

## Definite findings

### F1 — actual normal launch loses the caller's sibling module path (BLOCKER)

The registered `delivery-v2-final` row launches a fresh `python3 -c` process.
Its hash-checked code verifies the regular file and SHA256, rewrites `sys.argv`,
and executes the caller with globals containing `__name__` and `__file__`.
It does not insert `Path(p).parent` into `sys.path`.

`test-run` then runs the row under `bash -c` after `cd` to the detached Runtime
snapshot and sets `PYTHONPATH=$SNAP`. The caller lives in the private candidate
directory, not in that snapshot. Python imports do not infer a module search
path from an arbitrary `__file__` global supplied to `exec`.

The caller's first non-stdlib import is `run-final-delivery.py:23`:
`from delivery_lifecycle import run_delivery`. The exact service traceback is
`ModuleNotFoundError: No module named 'delivery_lifecycle'`, exit 1, before
`main`, before lifecycle setup, before D68, and before builder entry.

Harmless private control reproduced the same boundary with the exact hash
wrapper and `--help`: exit 1 with the same import error. No builder or service
was invoked by this control.

Minimal reusable seam: preserve the hash check, argv rewrite, source/gate
guards, and caller bytes while making the production hash-checked launch add
the caller's parent directory to the import search path before `exec` (or use
an equivalent reviewed loader seam). The existing `installer.load_runner`
and protected source harness already demonstrate the needed `sys.path.insert`
behavior, but that behavior is absent from the production row.

### F2 — protected positive harness does not exercise the normal row

`check_jj.load_caller` inserts the candidate directory into `sys.path` before
loading the caller and calls `caller.main(...)` in-process. `candidate/check.sh`
both exports `PYTHONPATH=$ROOT` and inserts the same root. The positive path is
therefore importable by construction and is not the actual registered
`python3 -c`/`bash -c`/snapshot path.

`installer.load_runner` likewise hash-checks the caller/helper, inserts
`RUNNER.parent` temporarily, executes the caller in-process, then removes the
path. Its passing result proves the candidate source can be imported through
that loader; it does not prove the installed row can import its sibling.

This explains why the existing positive missed actual normal launch. It is an
isolation mismatch, not a safety denial or a product guard refusal.

### F3 — pre-install row validation is not exact installed-row execution

The candidate row file contains `FINAL_TUPLE_SHA256_PENDING` and
`GATE_TUPLE_SHA256_PENDING` markers. `install-final-services.py` validates the
candidate bytes and their reviewed row hashes, then substitutes concrete tuple
hashes into the registry. The installed row is consequently a different byte
string. The installer verifies the resulting registry/predecessor digests but
does not shell-parse or execute the substituted row.

Observed exact values: current registry SHA256 is
`0495919f9ab694d034ca53d77877c90d5553560ac3bbcbf7e90e8b268e227e15`; the
candidate row artifact is
`251dc22826a7b42314c77b51e49b5e7cc3f44a9a17246eb3c92e40c370ecad81`; the
installed `delivery-v2-final` row itself hashes to
`95714eb061e7a1c7093be48046ea01e8d0eb4af47c35d76d3e36656a2994d050`.
The concrete substitution is expected, not itself a defect, but it is the
boundary where the missing import-path check escaped coverage.

## Audited paths with no additional finding

- Request/queue: service `runtime-delivery-v2-final-1026171722-10589`,
  `integration:runtime`, `delivery-v2-final`, `--no-cache` was the intended
  route and the exact row was selected.
- Hash/argument construction: the row's wrapper checks regular non-symlink
  file plus SHA256, then `sys.argv=[str(p), *sys.argv[3:]]`; the caller's
  `argparse.REMAINDER` receives the intended builder arguments after `--`.
  No argument-order or quoting defect was found.
- Source guards: caller and D68 statically retain source/gate tuple hashes,
  root binding, clean worktrees, ref/tree identity, App-base, overlap, private
  staging, and source-identity-after checks. No guard was bypassed by 10589.
- Lifecycle/D68: `run_delivery` uses absolute sampler and finalizer paths,
  parent-death/cancel handling, trace binding, disk floor, process-group
  termination, wait/reap, and then launches the D68 wrapper. None of this was
  reached in 10589; the static path has no second import-path mismatch.
- Builder: D68 uses an absolute `SourceFileLoader` path and was not reached.
  No builder, dry-run, clone, body, or delivery result exists for 10589.
- Ownership: the accepted source/gate/stage checks are present and were not
  the failure. The exact production entry remains the required acceptance
  point; source-positive ownership controls are not runtime acceptance.
- Cache: the observed request had `--no-cache`, so no cached result was used.
  This report makes no cache-pass claim.

## Acceptance recommendation

After the author repairs only the production loader seam, the orchestrator
should accept the change only on a fresh exact installed-row request:

`request-test integration:runtime delivery-v2-final --no-cache`

The result must show no sibling-import error, a durable lifecycle record with
trace validation and reap status, D68 wrapper receipt/staging reached, and the
builder entry reached without source/gate identity drift. `check_jj`,
`installer.load_runner`, a generic import-availability reader, or worker exit 0
are not substitutes for this real-production-entry proof.
