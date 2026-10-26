# OPS D141s validation

## Candidate and control run

- Exact immutable candidate: `b168dbb05d469941ee57c63190198bb4df852cd7` / tree `aa70f43234e26aa2cdb23031ca0683c3e81da0bd`.
- Author precommit retained as parent identity: `06fb2b5d16dd3c93cecf5520bb2a2da613dd1b92`.
- Independent command: `TMPDIR=/tmp/rt-OPS-D141s-pair-independent-0503.ZUMwzW PYTHONDONTWRITEBYTECODE=1 python3 -I ops-d141-measured-floor/controls/real-controls.py` — PASS, exit 0, 73 cases.
- Harness result: `SEC001=PASS`, `SEC002=PASS`, `freeze2=NEEDS`, `release=NOT_READY`.
- The first attempted `mkdir -p` used the assigned worker `tmpdir`, which is a pre-existing regular marker file; Python did not start. The required run then used a fresh private `/tmp` directory with the same effective command and completed PASS.

## Static and custody checks

- `bash -n ops-d141-measured-floor/bin/test-run` — PASS.
- Python AST parse of four scoped `bin/*.py` files plus `controls/real-controls.py` — PASS, 5 files.
- `ruff check --no-cache ops-d141-measured-floor/bin/*.py ops-d141-measured-floor/controls/real-controls.py` — PASS.
- `python3 -m json.tool ops-d141-measured-floor/install-manifest.json` — PASS.
- Manifest SHA-256/mode/regular-file/one-link/direct-bin/private-controls check — PASS, all five candidate files.
- Installed donor check against live `/tmp/.../orch/bin` and donor `56f2d56e` `privateops-d141-measured-floor` blobs — PASS, all five hashes, mode 0755, regular files, one link.
- `git diff --check` and `git diff --check HEAD^ HEAD` — PASS.
- `git status --short` — clean before evidence; no candidate source was modified.

## Layout and production boundary

The author script's isolated installed → published → received layout contains
only direct `bin/` files; the controls directory is absent from the received
bin. The normal request path generated a full ID, retained `TEST <FULLID>` in
pending, and ran from the received direct bin. This was an isolated fixture
only; no live dispatcher, queue, service, install, CAS, or hub was touched.

The validator has no `D141g-paired-control` production authority. Matching-hash
wrong-suite/source/twin/command/replay cases refused before launch and
artifacts. It does still contain literal historical 520d route values; that is
the current `D141S-APP-001` freeze-2 source finding.

Read-only source inspection confirms the paired runner performs one controller
admission/floor decision before background dispatch, runs preflight then body
inside one admission unit, performs one post-unit 4 GB stop check, and owns one
continuous trace/finalization path. The current controls intentionally refuse
synthetic paired production decisions before launch because no current App
builder binding is available; they do not claim an authorized App pair body.

## C0 and prohibited scope

Read-only inspection of `/home/user/work/runtime/contract/commit-v2.md` confirms
the settled request and reply fields: scope/base pair, ordered commands, label,
steps/per-step patches, declared reads, `fields|atomic`, idempotency, dry-run,
source/rationale/group; accepted/merged canonical authenticated receipts with
bindings/effects/dependencies/history/guarded undo; conflict reason/head;
invalid code/path/hint/suggested command; preview without mutation. No DTO,
product, test fixture/assertion, generated, pin, registry, queue, service,
receipt, body, full-suite, import/collection/preflight, network, package,
environment, Store, cleanup/delete, hub/Git or alternate route was used.
