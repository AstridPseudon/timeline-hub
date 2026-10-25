Completed the private OPS child custody candidate from held WIP. Maker SHA-256: `0857a5e0d9faeceb585b371f1f82cbf4b574ff20350974fd3c95f852e57b6d39`.

The narrow correction reuses authenticated archive installs for unseeded builds, keeping generated packaging output outside retained source snapshots. Verifier, Store caller, retention lifecycle and reserves remain unchanged.

Validation passed:

- `bash -n ops-child-custody/make-child-venv`
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m unittest discover -s ops-child-custody/tests -v` — **29 passed**, including seven embedded Python compilations, parent RED/candidate GREEN and adversarial ownership controls.
- `/home/user/work/venv-agent/bin/ruff check --no-cache ops-child-custody/tests`
- `git diff --check`

No configured Python mypy/pyright baseline applies.

**Actual layout remains UNVERIFIED.** Main lacks `/home/user/work/bench-store`; at 16:48Z, disk was 3,368,525,824 bytes below the diagnostic reserve. No live build, acquisition, registration or body ran. All 10 generated fixture paths were enumerated; they are explicitly distinguished from actual observations.

Required evidence is under the worker’s `evidence/`. See [validation](/home/user/work/wt/rt-OPS-child-custody-resume-sol-1643/ops-child-custody/validation.md). Commit message and `DONE` were written. Per D30, no `design/` or `report.md` files were written.

Next: independent Luna custody review, then separate exact installer. Agent alone issues one new request after publication.