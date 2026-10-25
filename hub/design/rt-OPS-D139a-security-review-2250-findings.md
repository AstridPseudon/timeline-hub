# D139a independent security review

Verdict: **PASS_SOURCE**.

No source findings. The candidate’s installed-distribution route requires the
exact pinned PEP 610 VCS URL, commit, subdirectory, package and version; checks
all 18 RECORD rows and 12 hashes; accepts only the six named unhashed rows;
rejects unhashed code/JSON/pyi and unlisted files; snapshots exactly the RECORD
closure; checks ownership, regular-file shape, link count, symlink/path safety,
traversal and source replacement; and binds the immutable snapshot identity into
the existing Store, report, inventory and receipt paths. The production caller
uses `--schema-installed-distribution` through the existing
`Store.ensure(build, verify, registration)` route.

The pinned source-tree tie is explicitly `UNAVAILABLE`, matching the resolved
D139a decision. No acquisition was attempted. The real child/install/Store
acceptance was not run because the task forbids it; synthetic controls are not
credited as that acceptance.

Protected evidence:

- Candidate maker: `fd83c9e2017f75fb0d76a2d633d4a63aed090df37c4d7417b03152e7a4fc22b5`, 111171 bytes, mode 0755.
- Original/base maker: `5b6bfa01a74e7760e2cefe6713c0557cca695abb61074b3f01c9391949cfb064`, 93300 bytes.
- Shared installed preimage: `f07b80937dde807d9aa5dad1deed278d831e7f56fb3810708e955926b45b969f`, 75541 bytes.
- Protected Store/dependency helpers: `123bb93c1f2e3d6bd23c21e50cc8445afc8853e5e659759cd30dcaa53b7adfe2` and `116b4e6bcb791d08e6c3c548f7fb52c52e9225b9428d7e201c09b02160d7bfe2`.

The original 2214/2218 provenance and the current genuine installed input both
show the required 18 RECORD rows, 12 hashed rows, pinned ArtAgents direct URL,
and the same six standard unhashed names; the current exact closure is recorded
in `record-closure.json`.
