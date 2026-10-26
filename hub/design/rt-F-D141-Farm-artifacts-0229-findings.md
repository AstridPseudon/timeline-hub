# F D141i Farm artifact publication findings

## Result

This is one authenticated Group A source packet, not a Farm READY claim. The
physical source venue contains the exact D139a installed schema distribution,
its 18-row/12-hashed-row RECORD closure, private direct_url binding, and the
unchanged 2149 canonical census. The Farm receiver cannot be READY from these
observations because the standalone trusted manifest, current Farm kit summary
pair, and original67 wheelhouse are not present at a Farm-bound venue.

## Qualified existing producers

1. The physical schema directory is
   `/home/user/work/venv-agent/lib/python3.13/site-packages/banodoco_timeline_schema-0.0.2.dist-info`.
   Its RECORD is 1,593 bytes, mode 0644, SHA256
   `844b2a2e1ee19d7a1656d57cb49c2bc8febf67295e653f93ff8f96217a0c7220`.
   All 18 RECORD paths are regular, non-symlink files and all 12 hashed rows
   match. Its private direct_url is 254 bytes, mode 0644, SHA256
   `b7a0a4f90218d54bc1fb118609d40a381f5762650f8e5863ec39098ec269165e`, and
   names the approved ArtAgents commit/subdirectory. The child-s2 schema
   candidates were excluded because their RECORD SHA is
   `8e4e8da1e8d10897c4096087601dd40eddc382edc60933fe419cc56cd4acf041`.

2. The unchanged original CANONICAL_CENSUS is physically present at the 2149
   source path, 10,686,270 bytes, mode 0644, SHA256
   `be9e8bc9c6d2411809da2d99126a9b3eef72678de2066bb6ad196d5d16ebcd30`.
   It parses as `timeline.d139.input-census/v1` and reports 1,146 unique
   requirements. The independent 2216 result is retained only as finite
   reconciliation provenance; it is not substituted for this file.

3. The original D139a installation receipt is physically present at
   `rt-OPS-D139a-install-2309-installation.json`, 3,587 bytes, mode 0644,
   SHA256 `82bdfab2c3ec483261126b3446aacf7d1ee9df6d38e1c2491b33e3927c60f5a4`.
   It records `PASS_INSTALL_COMBINED`, source commit/tree, and the approved
   maker identity. It is supporting evidence only: the current
   `FARM_INSTALLED_KIT_SUMMARY` in the required form was not found, so this
   receipt is not promoted as a complete Farm kit pair. The historical D137
   installed-kit JSON remains immutable and is not retargeted.

4. The original67 wheelhouse was not found. The physical bootstrap archive is
   3,002,878 bytes, mode 0644, SHA256
   `443977b004381bf3dd23cdcc7558335913256dc438198ed6478259d2f98cb548`, but
   it is explicitly excluded: it is not the original67 wheelhouse and must not
   be unpacked into a new dependency producer. The existing verifier source is
   not itself a wheelhouse.

## Provenance boundary

The schema install is an authenticated installed-distribution input, not a
portable ArtAgents source carrier. The source tree tie remains unavailable;
no acquisition or source repackaging was performed. The trusted manifest's
four-key content and canonical SHA are recorded from the settled D139a
decision, but no standalone file was fabricated. Raw direct_url content stays
private; the safe receipt provides the path, mode, bytes, hash, and pinned
identity.

No output claims Farm READY, no request/body/census/import/collection/control/
child/service/bootstrap/package-install/network behavior changed, and no
hub or design path was written by this worker.
