# D141 transport security correction

Status: isolated transport controls pass; independent corrected review is
pending. **Every actual receiver step below remains gated on that review PASS.**
No extraction, installation, Farm check-only, request, or body was run here.

The immutable original payload remains the 13,285-byte archive with SHA-256
`c1c2a6892226f63306148f8fc570fe5b793e07c554c8acc49ec3cd89cd86097f`.
Its embedded `safe_receiver` text is historical advice and is superseded by
this correction and the corrected verifier's `safe_receiver` output. Do not
execute its old preflight or `--no-same-permissions` extraction command. The
payload archive and its sidecar must not be rewritten to update that text.

The receiving manager must obtain the corrected helper source/hash and the
expected payload SHA-256 separately from the existing trusted manager peer.
The evidence `publication.json` identifies the immutable helper carrier and
its source hash. A filename, a sidecar, or a digest computed from received
bytes cannot supply authority for `--expected-sha256`. There is no fallback
to any of those inputs and no new signer or trust authority. Sidecars check
consistency only. The receiver cannot authenticate against a malicious
trusted manager or privileged owner.

After independent corrected review PASS, the receiving owner must retain the
received helper and archive in private, physical, safely owned ancestry with
no concurrent writers. Authenticate the helper against the manager's supplied
source hash before running it. Bind `ARCHIVE`, `VERIFIER`, and
`MANAGER_PEER_SHA256` from that handoff, then run:

```sh
python3 -I -B "$VERIFIER" --verify-archive "$ARCHIVE" \
  --expected-sha256 "$MANAGER_PEER_SHA256"
```

Stop unless the corrected verifier returns `PASS_TRANSPORT_CLOSURE`. It checks
the exact 25 members (18 payload files, two metadata files, five directories),
18 RECORD rows / 12 hashed / six named unhashed entries, pinned RECORD and
direct URL, four-key source identity, file bytes, entry manifest, modes and
uid/gid. Unhashed files are authenticated by the external whole-archive hash;
an attacker refreshing closure metadata or a sidecar cannot authorize them.
Both compressed and expanded input are limited to 20 MiB. Only regular files
and the exact directory closure are accepted; links and unsupported extensions
are refused before any filesystem extraction.

Only after that success, and while the same authenticated archive remains
protected from replacement, may the receiving owner prepare a new empty
physical `STAGE` directory owned by the receiving user, mode 0700, beneath
private safe ancestry. The owner must verify that it is empty, contains no
links, and has no other writers. Clear `TAR_OPTIONS` and use the fixed system
GNU tar, without additional options:

```sh
env -u TAR_OPTIONS /usr/bin/tar --extract --gzip --file "$ARCHIVE" \
  --no-same-owner --same-permissions --keep-old-files --directory "$STAGE"
```

`--same-permissions` preserves the checked 0644 file and 0755 directory modes;
the verifier rejects writable or special modes first. `--no-same-owner` keeps
the receiving user's custody; no recursive ownership or permission changes
are authorized. The receiver's identity must already satisfy the existing
production custody checks. Do not follow links, overwrite an existing stage,
use `--absolute-names`, `--overwrite`, or `--ignore-zeros`, or repair a failed
ownership/mode check with a broad `chown`/`chmod`. Recheck the extracted files
against the authenticated entry manifest, including regularity, single links,
bytes, modes, allowed receiving ownership and exact directory/file closure.
Stop on any difference before admission.

Bind the actual extracted installed distribution as
`SCHEMA_INSTALLED_DISTRIBUTION=$STAGE/timeline-d141-schema-record-closure-c9a87be9485f79878262cc9a193bfa9e4932cf0a942a62b32e272b46c7b60a2d/site-packages/banodoco_timeline_schema-0.0.2.dist-info`
and `SCHEMA_SOURCE_MANIFEST` to the extracted `trusted-schema-manifest.json`.
Bind `SCHEMA_RECORD_CLOSURE` and `SCHEMA_DIRECT_URL` to the corresponding
RECORD/direct_url files. The manifest is the newly produced approved
four-key object, SHA-256
`c9a87be9485f79878262cc9a193bfa9e4932cf0a942a62b32e272b46c7b60a2d`,
and is not recovered historical evidence or an ArtAgents source-tree carrier.

The production caller remains unchanged:
`D140_PHASE=pre-child ops-d140-farm/receive-farm.sh --check-only` with all
genuine approved installed-distribution/manifest inputs. Verifier, D131 and
ownership gates are unchanged. The current installed-kit summary plus separate
matching `PASS_INSTALL` pair and the original67 wheelhouse remain missing.
The 2309 `PASS_INSTALL_COMBINED` receipt remains supporting only. No bootstrap
substitution, new dependency producer, generic availability reader, or Farm
READY claim follows from this transport correction.

C0v2 is unchanged: revision/publication base pair, commands, label, steps with
patch and reads, `merge`, request `reads`, dry run and idempotency remain the
existing contract. Accepted/merged, conflict, invalid and preview replies and
Runtime authority are unchanged. This correction neither sends a request nor
changes any product semantics.
