# D141i validation

Reviewed and frozen source: commit `25ddf3fec4631c0e689d91dae358e68bd045309b`,
tree `e43261f85b5044f1cb90b647fc26f8fac01ae728`.

Exact targeted commands and results:

```text
TMPDIR=/tmp/w-df84da38f9/d141-matrix python3 -I -B ops-d141-farm-artifacts/test_review0253_matrix.py --archive /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/timeline-d141-schema-record-closure-c1c2a6892226f63306148f8fc570fe5b793e07c554c8acc49ec3cd89cd86097f.tgz --expected-sha256 c1c2a6892226f63306148f8fc570fe5b793e07c554c8acc49ec3cd89cd86097f
PASS: 16/16; positives 2 accepted; attacks 14 rejected; unexpected 0

TMPDIR=/tmp/w-df84da38f9/d141-controls python3 -I -B ops-d141-farm-artifacts/test_transport_security.py --archive /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/timeline-d141-schema-record-closure-c1c2a6892226f63306148f8fc570fe5b793e07c554c8acc49ec3cd89cd86097f.tgz --expected-sha256 c1c2a6892226f63306148f8fc570fe5b793e07c554c8acc49ec3cd89cd86097f --dist /home/user/work/venv-agent/lib/python3.13/site-packages/banodoco_timeline_schema-0.0.2.dist-info
PASS: 15 unittest groups, 1.023s, no extraction/import/product tests

PYTHONDONTWRITEBYTECODE=1 python3 -I -B ops-d141-farm-artifacts/package_record_closure.py --verify-archive /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/timeline-d141-schema-record-closure-c1c2a6892226f63306148f8fc570fe5b793e07c554c8acc49ec3cd89cd86097f.tgz --expected-sha256 c1c2a6892226f63306148f8fc570fe5b793e07c554c8acc49ec3cd89cd86097f
PASS_TRANSPORT_CLOSURE; rows=18; hashed=12

PYTHONDONTWRITEBYTECODE=1 python3 -I -B <independent inline reviewer harness>
PASS: 16/16; positives 2 accepted; attacks 14 rejected; unexpected 0

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -I -B -c '<ast.parse three ops-d141-farm-artifacts Python sources>'
PASS: AST 3/3

/home/user/work/venv-agent/bin/ruff check --no-cache ops-d141-farm-artifacts
PASS: All checks passed

bash -n ops-d140-farm/receive-farm.sh ops-child-custody/request-child-venv ops-child-custody/make-child-venv
PASS

git diff --check
PASS

git diff --exit-code HEAD -- . ':!ops-d141-farm-artifacts'
PASS: no outside-scope worktree changes
```

Additional read-only checks passed: helper source equals the published
digest-named helper; original archive hash/size/mode/single-link stayed
`c1c2a689…`/13285/0644/1; RECORD and direct_url remained the approved
18/12/6 and exact hashes; and only the four D141 artifact files differ from
the parent commit. The external-SHA and atomic-publication probes passed.

The supported receiver commands were reviewed but not executed:

```sh
python3 -I -B "$VERIFIER" --verify-archive "$ARCHIVE" --expected-sha256 "$MANAGER_PEER_SHA256"
env -u TAR_OPTIONS /usr/bin/tar --extract --gzip --file "$ARCHIVE" --no-same-owner --same-permissions --keep-old-files --directory "$STAGE"
D140_PHASE=pre-child ops-d140-farm/receive-farm.sh --check-only
```

The second command remains gated on the first returning
`PASS_TRANSPORT_CLOSURE`, an independent review PASS, a private empty
physical stage, and all subsequent rechecks. No full suite, localhost,
browser, live socket, product import, service, child, queue, extraction,
installation, body, network, acquisition, cleanup, delete, build, ZIP,
Store, registry, census, D130, or stopped-work operation was run.
