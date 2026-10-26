# D141 transport security validation

PASS for isolated correction controls; corrected independent review PENDING.
Base: `59ab7b78b09dc077f7c9c6f60ede1c77d178ab12`. Final verifier source SHA-256: `729e8a08def9ffb845b3181fa85ccf083ed3ef7982852aff74b022947abac528`.

Exact targeted commands (run directly, no full suite or central service):

```sh
python3 -I -B ops-d141-farm-artifacts/test_review0253_matrix.py --archive /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/timeline-d141-schema-record-closure-c1c2a6892226f63306148f8fc570fe5b793e07c554c8acc49ec3cd89cd86097f.tgz --expected-sha256 c1c2a6892226f63306148f8fc570fe5b793e07c554c8acc49ec3cd89cd86097f
```
PASS, exit 0: 16/16; two positives accepted, all 14 attacks rejected with Refusal.
This replays the independent reviewer's final recorded matrix from its log,
with the required API/path/scratch adaptations recorded in controls.json.

```sh
python3 -I -B ops-d141-farm-artifacts/test_transport_security.py --archive /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/timeline-d141-schema-record-closure-c1c2a6892226f63306148f8fc570fe5b793e07c554c8acc49ec3cd89cd86097f.tgz --expected-sha256 c1c2a6892226f63306148f8fc570fe5b793e07c554c8acc49ec3cd89cd86097f --dist /home/user/work/venv-agent/lib/python3.13/site-packages/banodoco_timeline_schema-0.0.2.dist-info
```
PASS, exit 0: 15 unittest groups with adversarial subcases. Exact source
conservation compares all 18 original archive files, bytes, modes, uid/gid
and entry metadata to the read-only approved installed distribution. No
product imports or product tests run.

```sh
python3 -I -B ops-d141-farm-artifacts/package_record_closure.py --verify-archive /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/timeline-d141-schema-record-closure-c1c2a6892226f63306148f8fc570fe5b793e07c554c8acc49ec3cd89cd86097f.tgz --expected-sha256 c1c2a6892226f63306148f8fc570fe5b793e07c554c8acc49ec3cd89cd86097f
```
PASS, exit 0: PASS_TRANSPORT_CLOSURE. Omission of --expected-sha256 is also
exercised by the own-controls command and returns exit 2 as required.

Static checks:

- `/home/user/work/venv-agent/bin/ruff check --no-cache ops-d141-farm-artifacts` — PASS, exit 0.
- `bash -n ops-d140-farm/receive-farm.sh ops-child-custody/request-child-venv ops-child-custody/make-child-venv` — PASS, exit 0.
- `git diff --check` — PASS, exit 0.
- `git diff --exit-code HEAD -- . ':!ops-d141-farm-artifacts'` — PASS, exit 0.
- `ast.parse` of each `ops-d141-farm-artifacts/*.py` source in this finalization probe — PASS.

The initial added-control run exposed a fixture PAX-path override and the
producer directory-kind check; both were corrected without changing any
passing behavior expectations. Final direct runs above pass. Nothing was
skipped, disabled, or weakened. Receiving extraction is statically reviewed
only, deliberately unexecuted; a corrected independent PASS is still required.

The original payload remains 13,285 bytes, SHA c1c2a6892226f63306148f8fc570fe5b793e07c554c8acc49ec3cd89cd86097f,
with the original digest-only sidecar and c9a87 four-key manifest. The corrected
helper is a new digest-named byte-exact source copy in ORCH/artifacts. No old
name, prior evidence, hub, production caller, D131, product code or C0 schema
changed. The missing current kit/PASS_INSTALL pair and original67 remain
unresolved. No Farm READY, full suite, extraction/install, request/child,
product import/collection, body/service/socket/network/package/acquisition,
403 retry, availability census, Store/registry/retirement/cleanup/delete,
D130/stopped-work/build/ZIP action occurred.

Actual immutable published helper smoke (after byte-publication):

```sh
python3 -I -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/timeline-d141-transport-verifier-729e8a08def9ffb845b3181fa85ccf083ed3ef7982852aff74b022947abac528.py --verify-archive /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/timeline-d141-schema-record-closure-c1c2a6892226f63306148f8fc570fe5b793e07c554c8acc49ec3cd89cd86097f.tgz --expected-sha256 c1c2a6892226f63306148f8fc570fe5b793e07c554c8acc49ec3cd89cd86097f
```
PASS, exit 0; PASS_TRANSPORT_CLOSURE, 18 rows / 12 hashes, corrected receiving advice.
