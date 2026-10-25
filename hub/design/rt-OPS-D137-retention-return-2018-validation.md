# OPS D137 retention return

Base: `4932c0f8e2e02ce6a203bf41fe014f9c3a7db5fa`.

The production maker now copies failed-stage stderr before `Store.ensure`
rollback, into the private maker-owned route
`/maker/tests/provision-stderr/<request>.<stage>.stderr`. The public Store
failure marker is unchanged and contains no private payload. The copy uses
O_NOFOLLOW/O_EXCL descriptor operations, requires an owned regular single-link
0600 file, refuses unsafe request/stage names and forged symlink/hardlink paths,
and does not overwrite an existing request/stage record. Payloads up to 1 MiB
are exact; larger payloads retain the first 1 MiB and write truthful byte-count,
truncation, and full SHA-256 metadata at
`/maker/tests/provision-stderr/<request>.<stage>.json`.

The focused regression exercises the actual ordinary Store cleanup boundary,
including nonzero and timeout failures after staging has been deleted, and
covers exact first stderr, mode/shape, truncation truth, forged paths, safe
allowlisting, and repeat no-clobber.

Commands and results:

- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m unittest discover -s ops-child-custody/tests -v` — 44/44 passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 -B ops-child-custody/install-prep/dry_run_controls.py` — PASS.
- `/home/user/work/venv-agent/bin/ruff check --no-cache ops-child-custody/tests ops-child-custody/install-prep/*.py` — passed.
- `bash -n ops-child-custody/make-child-venv ops-child-custody/install-prep/apply-reviewed-maker.sh` — passed.
- Embedded Python compile and exact `STORE_PY`/`STORE_VERIFY` comparison against base `4932c0f8e2e02ce6a203bf41fe014f9c3a7db5fa` — passed.
- `git diff --check` — passed.

Candidate source: `/home/user/work/wt/rt-OPS-D137-retention-return-2018/ops-child-custody/make-child-venv`, SHA-256
`4435d49953f583234e17a549b4df9896d9d45aa8aa7242ea51a61560ad1d0a36`, 75,503
bytes, mode 0755. The installer-prep pins and decision schema are updated to
this exact candidate. The source commit remains unbound until the harness
commit; no install was attempted.

The D137 fixture E2E decision remains WITHDRAWN/NOTRUN. No whole-make fixture,
package acquisition, child request, production Store, credentials, hub write,
Git mutation, or live install was performed.
