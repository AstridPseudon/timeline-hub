# D141 transport correction handoff

Status: PASS_LOCAL_TRANSPORT_SECURITY / INDEPENDENT_REVIEW_PENDING /
FARM_NOT_READY. Every actual receiver step is held until corrected independent
review PASS. All original evidence and the original payload remain preserved.

Final immutable verifier helper: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/timeline-d141-transport-verifier-729e8a08def9ffb845b3181fa85ccf083ed3ef7982852aff74b022947abac528.py`
SHA-256: `729e8a08def9ffb845b3181fa85ccf083ed3ef7982852aff74b022947abac528` (26956 bytes).
Source: `/home/user/work/wt/rt-F-D141-Farm-transport-security-sol-0300/ops-d141-farm-artifacts/package_record_closure.py`, at base `59ab7b78b09dc077f7c9c6f60ede1c77d178ab12` plus the reported bounded diff.
The conventional commit is left for the harness; no commit/ref operation ran.

Original immutable payload: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/timeline-d141-schema-record-closure-c1c2a6892226f63306148f8fc570fe5b793e07c554c8acc49ec3cd89cd86097f.tgz`
SHA-256: `c1c2a6892226f63306148f8fc570fe5b793e07c554c8acc49ec3cd89cd86097f` (13,285 bytes). Its adjacent original sidecar is unchanged.
Its embedded old receiving advice is superseded; do not follow it.

The receiving manager must supply this helper's expected SHA and the expected
payload SHA through the existing trusted manager-peer handoff independently
of received sidecars or metadata. Authenticate helper bytes first. No new
signer, signature, or authority is introduced. Never pass a SHA calculated
from an untrusted received archive as the expected value. The test fixtures
supply fixture SHA deliberately only to exercise structural defenses.

After review PASS, follow `/home/user/work/wt/rt-F-D141-Farm-transport-security-sol-0300/ops-d141-farm-artifacts/RECEIVING.md`.
It specifies private safe custody and an empty physical mode-0700 stage;
corrected preflight with --expected-sha256; fixed GNU tar with cleared
TAR_OPTIONS, --no-same-owner --same-permissions --keep-old-files; exact
post-extraction file/entry/mode/allowed-owner recheck; and the unchanged
production installed-distribution/manifest/RECORD/direct-URL bindings.
No broad ownership or permission changes are permitted. No actual receiving,
extraction, package install or Farm check-only ran here.

Exact source conservation PASS: the 18-file/12-hash/six named unhashed closure
is byte-exact against the approved read-only venv-agent source, with exact
modes/uid/gid and no extras. The four-key manifest remains canonical c9a87;
RECORD remains 844b2a2e; direct URL remains b7a0a4f9 and exact pinned 242f
URL/subdirectory/source-tree identity. This is not a newly recovered source
tree or a historical attestation. Raw direct_url remains in the payload only,
not evidence JSON.

Manager: commission independent corrected review of actual helper/carrier,
original payload, the 16-subtest reviewer replay and 15 own-control groups.
Farm receiving/integration owner: only after that PASS and all genuine
bindings, run unchanged receive-farm.sh --check-only with exact approved
installed-distribution/manifest inputs; keep verifier/D131/ownership strict.
D139a installation/kit owner: current genuine kit summary plus separate
matching original PASS_INSTALL remains MISSING; 2309 PASS_INSTALL_COMBINED
stays supporting only. Farm distribution/seed and original67 owners: physical
authenticated original67 wheelhouse and genuine manifest remain MISSING;
no bootstrap substitution or new dependency producer.

C0v2 is unchanged in full: base revision/publication pair, commands, label,
steps with patches and reads, merge mode, declared reads, dry run,
idempotency, accepted/merged, conflict, invalid and preview shapes. No child,
request, registry, Farm action, availability reader or product change.
