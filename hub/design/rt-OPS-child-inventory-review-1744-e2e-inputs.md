# Prepared E2E input review

Status: **NOTRUN**. The runner is source-reviewed and prepared, not qualified.

Minimum legitimate fixture setup for `tests/e2e_inventory.py`:

- A manager-admitted private venue entirely under the run's `$TMPDIR`, with the
  protected `bench_store.py` and a supported Python executable.
- Two already initialized, empty, disposable fixture Stores (parent and
  candidate) with the existing owner/index custody; this reviewer must not
  initialize them.
- Clean Git-committed tiny Agent and Runtime source checkouts whose exact file
  sets and bytes equal `fixture_sources()`, including the Runtime client and
  CLI entry points.
- Already available local no-index wheels for pip 26.2.1, setuptools 80.9.0,
  wheel 0.46.3, and the two tiny private dependencies. No acquisition or
  network fallback is allowed.
- Unchanged disk admission: at least 5,905,580,032 free bytes for the normal
  child path, with the existing 4,000,000,000 stop line and no heavy body.

These are execution inputs, not invented product approval prerequisites. The
runner's `approved_private_fixture=true` is a manager admission assertion; it
must be supplied by the authorized fixture venue, never manufactured by this
review. The Store owner/index and clean source commits are legitimate custody
inputs because the runner uses the real whole shell caller and Store path.

The runner itself refuses missing venue inputs, removes ambient index/PYTHONPATH
redirectors, uses the exact parent 0857 source and unchanged verifier, records
only safe stage/exit metadata, and reports `NOTRUN` on missing admission. It
does not initialize Stores, write Git, change reserves, substitute a venv, mock
the verifier, or acquire packages.

The prior attempted run was blocked with:

```text
EXACTMISSING: approved private fixture venue manifest, Store custody,
committed tiny sources and local wheels
```

The actual Farm child production report/inventory remains EXACTMISSING and
must be censused in place by the Farm lead; reconstruction is not a valid E2E
input.
