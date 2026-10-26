# F-final validation

## Actual evidence read

- Actual result: `runtime-delivery-v2-final-1026171722-10589` exit 1,
  `builder_invoked=false`, `zip_written=false`.
- Actual traceback: `run-final-delivery.py:23` /
  `ModuleNotFoundError: No module named 'delivery_lifecycle'`.
- Actual registry row was compared byte-for-byte with the installed
  `suites.conf` row; it is the concrete marker-substituted row selected by the
  service. Candidate-row difference is expected marker substitution.
- Existing actual disk trace was preserved as source evidence. A new harmless
  two-sample REAL `df -B1` sampler also ran at five-second cadence: 5,143,875,584
  and 5,143,855,104 available bytes, both above the 4,000,000,000 stop line;
  PID 4 exited 0, wait status 0, and was reaped.

## Harmless controls run

- Exact hashchecked row wrapper with caller `--help`, from a non-candidate cwd:
  exit 1 with the same `ModuleNotFoundError`; no builder or service path.
- In-process `importlib.util.spec_from_file_location` loader with candidate
  directory inserted into `sys.path`, caller `--help`: import PASS and argparse
  help exit 0. This models `check_jj`/`installer.load_runner`, not production.
- `PYTHONDONTWRITEBYTECODE=1` compile checks for caller, lifecycle, D68 wrapper,
  and installer: PASS.
- `bash -n evidence/candidate/check.sh`: PASS.

## Not run

No source-positive clone harness, full suite, service retry, dry-run, builder,
clone, install, registry write, or package/body execution was performed.
