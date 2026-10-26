# OPS D141g-a validation

## Candidate

The immutable terminal paired source is commit `06fb2b5d16dd3c93cecf5520bb2a2da613dd1b92`,
the terminal 0418 resume. The worktree was clean before and after the review.
No product source, DTO, registry, queue, hub, service, install, or Git state was
modified.

## Exact controls

`TMPDIR=/tmp/rt-OPS-D141-pair-final-verify-0435.1Wc0oR PYTHONDONTWRITEBYTECODE=1 python3 -I ops-d141-measured-floor/controls/real-controls.py`
— **PASS**, exit 0, 68 cases. The harness explicitly returned:

- `SEC002=PASS`;
- `SEC001=NEEDS`;
- `freeze2=NEEDS`;
- `release=NOT_READY`.

The run preserved the 68-purpose assertion, exact Runtime P5 `6934`, generated
targeted15, held `8912`/`19479`, default/measured floors, cache/source/snapshot/
leases, one-heavy protection, and isolated installed→published→received direct
bin layout with no controls sibling. Matching-hash unauthorized pair attacks
refused before launch. Seven trace replacement/parent custody probes returned
bounded PASS with no redirected writes. The paired harness did not include the
donor's mounted stop-test and frozen-sampler cases, which is why SEC001 remains
NEEDS.

## Static and source checks

- `bash -n ops-d141-measured-floor/bin/test-run` — PASS.
- Python AST parse of five scoped Python files — PASS.
- `ruff check --no-cache ops-d141-measured-floor/bin/*.py ops-d141-measured-floor/controls/real-controls.py` — PASS.
- `python3 -m json.tool ops-d141-measured-floor/install-manifest.json` — PASS.
- Manifest SHA-256/mode/regular-file/one-link check for all five source files — PASS.
- Read-only exact installed predecessor check for all five live files — PASS; donor hashes, regular files, one link, mode 0755.
- `git diff --check` and `git diff --check HEAD^ HEAD` — PASS.
- Production validator source check — PASS: no `D141g-paired-control`; exact historical route remains constrained to `D141g-next-app-journey`/520d values.

## Donor and external limits

Immutable Runtime donor `56f2d56e…` / independent 0418 remains PASS49 for its
own source/control scope, including mounted stop-test, bounded frozen-sampler
failure/125, descriptor custody, and cancellation lifecycle. It is not a paired
receiver PASS and is not evidence of a release.

No full suite, live socket/browser suite, production D66 request, actual App
freeze-2 registration, receipt attachment, installation/CAS, service, body,
gate, build, ZIP, credentials, network, package/environment provisioning,
Store, cleanup/delete, or workaround was run.
