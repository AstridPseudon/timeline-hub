# F D141i Farm Group A artifact handoff

Status: `SOURCE_AUTHENTICATED / FARM_BINDING_INCOMPLETE`. This handoff makes
no Farm READY claim and does not claim a Farm request/body result.

## Ready source artifacts

| Artifact | Owner | Physical source and authentication | Supported delivery |
| --- | --- | --- | --- |
| D139a installed schema distribution | D139a schema owner | `/home/user/work/venv-agent/lib/python3.13/site-packages/banodoco_timeline_schema-0.0.2.dist-info`; directory 4096 bytes/0755; RECORD 1593 bytes/0644/SHA `844b2a2e1ee19d7a1656d57cb49c2bc8febf67295e653f93ff8f96217a0c7220`; direct_url 254 bytes/0644/SHA `b7a0a4f90218d54bc1fb118609d40a381f5762650f8e5863ec39098ec269165e` | Existing `--schema-installed-distribution` interface; bind the same physical dist-info with the standalone trusted manifest |
| Original CANONICAL_CENSUS (2149) | D139 census owner | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agt-F-D139-import-input-census-2149-input-census.json`; 10,686,270 bytes/0644/SHA `be9e8bc9c6d2411809da2d99126a9b3eef72678de2066bb6ad196d5d16ebcd30`; 1,146 unique requirements | Ordinary Farm input venue, unchanged byte-exact file; bind and rerun existing receiver hash check |
| D139a installation receipt | D139a installation/kit owner | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/rt-OPS-D139a-install-2309-installation.json`; 3,587 bytes/0644/SHA `82bdfab2c3ec483261126b3446aacf7d1ee9df6d38e1c2491b33e3927c60f5a4`; `PASS_INSTALL_COMBINED` | Supporting receipt only; bind only with the original current Farm kit summary |

## Missing or incomplete artifacts

| Artifact | Owner | Exact gap and required route |
| --- | --- | --- |
| Standalone D139a trusted source manifest | D139a schema owner | No physical file found. Required JSON is exactly `{url, commit, subdirectory, source_tree}` with canonical SHA `c9a87be9485f79878262cc9a193bfa9e4932cf0a942a62b32e272b46c7b60a2d`; publish through the existing schema-manifest route, not by treating this packet's embedded metadata as an existing carrier |
| `FARM_INSTALLED_KIT_SUMMARY` plus matching installation receipt | D139a installation/kit owner | Only the original CAS2309/installed2314 receipt evidence is present; the current `timeline.ops.d137.installed-kit/v1` summary was not found. Supply the genuine paired producer artifact and bind the existing receiver fields |
| `DEPENDENCY_SEED` original67 wheelhouse | Farm distribution/seed owner | No original67 directory is present. Supply it through the already-qualified seed producer and existing verifier route; do not unpack the bootstrap archive, use oldvenv, acquire, or create a new wheelhouse |

## Receiving boundary

The manager may place the seven packet files under the exact
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/rt-F-D141-Farm-artifacts-0229-*`
names as byte-exact evidence copies and coordinate the normal Farm venue.
This worker did not write design, hub, queue, or Farm input paths. The
production caller remains unchanged:
`ops-d140-farm/receive-farm.sh --check-only`.

After the three gaps above are supplied by their owners, the receiver may
perform its existing parser/hash/RECORD checks. No child request or Farm
result should be inferred from this handoff.
