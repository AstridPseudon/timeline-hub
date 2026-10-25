# D139 independent validation

## Result

The source identity, source-object hashes, 22-selector/431-Python-file coverage,
module/distribution/RECORD mapping, schema pin, and AST parsing all pass. The
review is conditional/failing for safe publication because the stored graph
edge count is 17,604 while the stored import occurrence tables contain 17,642
records. The 38 omitted records are accounted for below, but the prior packet
does not declare that filtered graph scope.

## Exact checks and results

- `python3 -m json.tool` over the prior report's four JSON evidence files: PASS.
- Read-only `git cat-file`/`git show` checks for Agent `4c4ee35d5687c4cd40a0e5395efda53aa56f939d` and Runtime `ab1e4f6141987706132916e2da16477f5a019464`: PASS; commit and tree identities match the packet and remotes.
- Read-only SHA-256 checks for every one of the 1,001 source rows against its recorded Git blob: PASS.
- Read-only AST parse of every one of the 1,001 source blobs: PASS; zero parse errors.
- Read-only expansion of the exact root selectors from the pinned command, restricted to Python files as the command inventory does: PASS; 22 selectors and 431 files.
- Read-only child `top_level.txt`, `METADATA`, `RECORD` path/size/hash verification: PASS; 68 distributions, 16,670 rows, 9,252 hashed rows, 26 import mappings.
- Read-only schema package RECORD verification: PASS; distribution `banodoco-timeline-schema==0.0.2`, 12 pinned non-RECORD entries, all hashes match the authenticated venv source.
- Read-only import arithmetic: FAIL as an equality claim. `len(graph.edges)==17604`, `sum(len(import.occurrences))==17642`; 38 occurrence records are absent from `graph.edges`.
- Read-only `git -C /home/user/work/wt/agt-F-D139-import-census-review-2210 diff --check`: PASS.
- Read-only composition worktree status: PASS; no product files changed.
- Read-only C0 schema/document inspection: PASS for the requested request/reply vocabulary and preview null receipt; no DTO or product file was changed.
- Read-only `df -B1` headroom check: PASS for the stated 5 GB source floor / 4 GB stop threshold; 5,294,874,624 bytes available.

## Graph discrepancy

The omitted records are 14 imports from the embedded D73 launcher preflight and
24 caught/conditional missing imports in:

| path | omitted records |
| --- | ---: |
| `tools/p4-d73-pinned-launch.sh` | 14 |
| `astrid/core/generation/backends/vibecomfy.py` | 10 |
| `astrid/core/timeline/banodoco_schema.py` | 7 |
| `astrid/packs/vibecomfy/production_engine.py` | 6 |
| `tests/packs/rendering/_helpers.py` | 1 |

This can be valid only if `graph.edges` is explicitly defined as a filtered
runtime/source graph rather than the complete AST import occurrence graph.

## Scope exclusions

No product imports, collection, preflight execution, provider, child, Store,
acquisition, installation, pytest, product suite, typecheck, lint, network, or
plugin execution was performed. Dynamic imports are represented only by the
existing 983 static records; data-dependent imports remain unverified.
