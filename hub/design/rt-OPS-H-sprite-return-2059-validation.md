# OPS H packet validation

All checks were read-only and source-only. No product files were edited.

## Checks

| Check | Result |
|---|---|
| `python3 -m json.tool evidence/correction.json` | PASS |
| JSON coordinate/hash validation against exact Git blobs and retained logs | PASS |
| `ast.parse` on exact named L15 Python blobs | PASS |
| `git diff --check` | PASS |
| `git status --short` | clean; no product changes |
| pytest, renderer, browser, service request, full suite | not run, as required |
| typecheck/lint | not run; not applicable to a no-code correction |

The exact L15 blobs were read with `git show 1c3a2ce725:path`; the source-map
hashes and coordinates are reproduced in `evidence/correction.json`.

## Input hashes

These are actual read-only inputs. The author-root files below are current
post-review custody files; they are not claimed as original author preimages.

| Input | SHA256 |
|---|---|
| author `evidence/review.json` (authentic reviewer JSON) | `bbb6c75a9a1a338ab68b27c9ebc9d026afb53146b0d9aa8690a6535d972c741b` |
| author `report.md` (current overwritten file) | `53d3a69d345ab3200561eb33296daaafff0774b0baeb69b90f91ab8b5bcb1e4e` |
| author `evidence/findings.md` (current overwritten file) | `7ef0b086bc6a2e624d3182dc7a030ae68d1174977fad4274ce6f1570d9db7d83` |
| author `evidence/source-map.json` (current overwritten file) | `e5b5f003bb820fe6d4bcdb9fceba6cfc0fb18de63e589b1bfad813fbf4ee07e5` |
| author `evidence/validation.md` (current overwritten file) | `b81453e068567ef25627a293c8235b68b010477634117875727ea4f0bca70d0e` |
| author `evidence/handoff.md` (current overwritten file) | `54d8775bab0a4268f9858deb5d52340d955ab2eceaa1e8fe7f39e1a9afe852ca` |
| author raw `log.txt` | `da9775c04d0e1b56db4b5111e6d16cfce7c8c3ac4a759faee394bb3ebaa8ff70` |
| reviewer raw `log.txt` | `5bb1940de8dc6f2d8f8e509edbcf7eafc9da78ccf9a8390e45d0ceccc25fb4d2` |
| L15 `astrid/sdk/timeline_restructure.py` blob | `2cb4e8a9bd3bcc61647a2b392ad34a3954b226933322a3374a8389104c820477` |
| L15 `tests/packs/rendering/test_sprite_scene_capability.py` blob | `97fae0c73016e04ad34bc1c87a168b84baa32743298737bfb576169c6c8fd9bb` |
| L15 `tests/sdk/test_timeline_restructure_frame_boundaries.py` blob | `6f2c8f578b10bc5494beeaa4f927a603406ff6c32badfd05483e5f576bf35730` |
| retained log `22278` | `4a63b5e8ec0fdb6012c727c931377024285ba3d574b8f2f2c0608099273e1c82` |
| retained log `16353` | `150edf7c203f6565d0687306a5028021a30e1bf3c9f7149414120178fc68c0f1` |
| retained log `23676` | `b86beddcee1fea43ab1ea519e8c8b0444503179e1e1aea48630bef2ddb752c73` |

## Output hashes

Output files are the five paths requested for the packet. The hashes below are
the serialized bytes verified before this validation file was finalized; the
validation file's own final SHA256 is reported by the final file-hash check
because embedding a file's hash in itself would be circular.

| Output | SHA256 |
|---|---|
| `report.md` | `263c45dd78ec92c21a87ca92025156180ca29cd54d6f26b63333fe760d8fb36c` |
| `evidence/correction.json` | `3569fcb4cdd54d4d6403376f517b65f3e4fd82f7f2eb6c47912c86eb16e38303` |
| `evidence/findings.md` | `f00b5c9db2e6a084a5b1a5241ec838b19bfd9aa5ffb439c7bb22831e15471908` |
| `evidence/validation.md` | `see final file-hash check; self-hash is not embedded` |
| `evidence/handoff.md` | `e81b1370bb68d1d6fc000bcd07fd9a27dbed460b5ed1c095502ccf5e483aa269` |

