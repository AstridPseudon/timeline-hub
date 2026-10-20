# Retained Node 20.19.4 App handoff

Available through the existing COMMS `ORCH/design` sync seam as the flat archive and sidecar:

- Archive: `handoff-vw-m3-node20.19.4-retained-app.tgz`
- Archive SHA-256: `e481653ec961f88c9cb8f034740afca3ed1bbc5fa3f9d56efde0eb502372481f`
- Archive size: `35,729,844` bytes (below the 50 MiB design transport limit)
- Archive member: `bin/node`
- Raw executable version: `v20.19.4`
- Raw executable SHA-256: `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`
- Original verified source (read-only): `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node`

The archive was extracted privately and its `bin/node` was compared byte-for-byte with the original; both the extracted and original hashes are the raw SHA above. Do not weaken the controller byte guard or replace this with Node 20.20.

Receiving/extracting into a private destination only (do not write to a shared install):

```sh
ARCHIVE="$ORCH/design/handoff-vw-m3-node20.19.4-retained-app.tgz"
ARCHIVE_SHA=e481653ec961f88c9cb8f034740afca3ed1bbc5fa3f9d56efde0eb502372481f
DEST=/home/user/work/app-private/node-v20.19.4-linux-x64
mkdir -p "$DEST"
printf '%s  %s\n' "$ARCHIVE_SHA" "$ARCHIVE" | sha256sum -c -
tar -xzf "$ARCHIVE" -C "$DEST"
test "$(sha256sum "$DEST/bin/node" | awk '{print $1}')" = 43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490
test "$("$DEST/bin/node" --version)" = v20.19.4
```

If the original source path already exists on the receiving machine and has the exact raw SHA above, use that path read-only instead of extracting a duplicate.
