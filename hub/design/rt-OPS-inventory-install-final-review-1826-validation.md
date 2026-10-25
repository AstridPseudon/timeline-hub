# OPS inventory installer independent first-return review

Result: `PASS_SOURCE_SECURITY_FIRST_RETURN`.

The prior `a5c39e412b8974932bb20a726ef08f8853c594a4` review remains retained as
`FAIL_SOURCE_SECURITY`. The return commit `a3e707dbcb80a200dbb5d8f60a8f0d63fd807da4`
addresses all seven findings in the private `ops-child-custody/install-prep/`
scope. No remaining source-security finding was identified under the approved
same-user manager-only receiving boundary.

## Exact checks

```text
TMPDIR=/tmp/w-94a6e4694e PYTHONDONTWRITEBYTECODE=1 python3 -B ops-child-custody/install-prep/dry_run_controls.py
PASS: private candidate, preimage, no-clobber, descriptor race, identity CAS, helper, symlink, and hardlink controls

bash -n ops-child-custody/install-prep/apply-reviewed-maker.sh
PASS

bash -n ops-child-custody/make-child-venv
PASS

/home/user/work/venv-agent/bin/ruff check --no-cache ops-child-custody/install-prep/*.py
PASS (All checks passed!)

/home/user/work/venv-runtime/bin/python -B <in-memory ast.parse of install-prep and tests Python>
PASS: AST parse 7 Python files

git diff --check
PASS
```

Exact source and boundary checks passed:

```text
candidate source commit 09ed4999741b822fba7e8b3033ca28db6bcf8fa1
candidate tree 32dbfb3e6ec08b032db2c9f75c6fae29e5e4abcc
candidate c3226b93d08e035f662ff57a7512522eb13f354acf2f13123999d71772e7142e / 69516 bytes / 0755
preimage parent 9428f515fcd8dccaef26193438b3ac89f903f5aa
preimage tree 7952f3e9e15532072066474ea9d151fe79114bd6
preimage 0857a5e0d9faeceb585b371f1f82cbf4b574ff20350974fd3c95f852e57b6d39 / 68351 bytes / 0755
bench_store.py 123bb93c1f2e3d6bd23c21e50cc8445afc8853e5e659759cd30dcaa53b7adfe2 / 43403 bytes / 0755 / links1
verify_dependency_seed.py 116b4e6bcb791d08e6c3c548f7fb52c52e9225b9428d7e201c09b02160d7bfe2 / 52731 bytes / 0755 / links1
```

## Private installer route

The installer was run once against disposable physical ORCH and TMPDIR roots
under `/tmp/w-94a6e4694e`, the clean current Composition checkout as a read-only
source of the exact archived candidate commit, and synthetic gate JSON. The
protected live-kit helpers were read-only inputs; the route copied them only to
the disposable private ORCH replica. Output:

```text
PASS: exact E2E and independent review gates accepted
PASS: candidate installed with CAS preimage, no-clobber backup, atomic replacement, and helper readback
PASS: private installer replica target/backup/helper readback and lock cleanup
```

The private route verified target candidate hash, one preimage backup, both
helper hashes, and lock cleanup. Synthetic gates do not qualify D125b or Agent
E2E1800/1810.

## Gate and installation limits

The future real gate format is usable: `e2e_inventory.py` writes the required
E2E fields, and a separate independent review binds its exact path and
SHA-256 to the candidate and source commit before the installer reaches any
receiving-tree write. The actual approved historical installation target is
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/make-child-venv`;
the 1656/1659 evidence remains limited to installed-source proof, with actual
child acceptance `UNVERIFIED / EXACTMISSING`.

No live target, backup, temporary installation, Store, package acquisition,
provider, socket, Git mutation, permission write, production child, or D130
SWAP/WAL path was used. No full40 suite was requested or rerun, and no Agent
E2E was duplicated. D125b remains `HOLD` until the genuine same-WIP E2E and
independent result are received and accepted.
