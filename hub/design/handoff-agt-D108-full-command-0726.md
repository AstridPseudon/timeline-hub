# Handoff: agt-F-D108-full-command-0726

Published the sole source-only `agent-core-full` command at
`design/agent-core-full-command.md` for MAIN. No pytest collection, import,
body execution, registry write, checkout, install, or product change was made.

Fixed guards are Agent
`070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2` (tree
`6056414359ae9fce08d999d54cbecf719fda33c3`) and Runtime
`1daca2a33f6d7b10053e07c539a54843e3984e19` (tree
`a522511414947e48e317a5e5c2103483b121a750`). App and Composition remain normal
MAIN request-checkout bindings, as required by the source evidence.

The exact row-181 command is unfiltered, uses the existing D73 pinned launcher,
`/home/user/work/venv-agent/bin/python`, Runtime schema/provider paths, timeout
45, `-n 3`, `-o addopts=`, `-p no:cacheprovider`, and a MAIN-owned real JUnit
path. Agent `070dfc`'s D110 test is covered by the existing `tests/sdk` root.

Source evidence has a count mismatch: metadata says 23 roots, but row 181,
`-core-roots.txt`, and the inventory contain 22 actual selector roots. The
published document preserves those exact roots and records the discrepancy; no
missing root was invented. MAIN must reconcile any central row count metadata
against the byte inventory before installing the row.

Baseline facts carried forward: pre-fix collection `9268` tests / 409 source
files, inventory SHA256
`7ac5cdd0bfa2b811f9a0a4fb719d9a28ef6080d2bb879ed29fe54fc1a6882b69`; upstream
924 XML SHA256
`2941565205663912985f766210bfead7db42264976fabee7dc899d03d4f4657f` at the
path recorded in the full command document. Final counts are MAIN-owned.

The existing parsed preflight is positive-once(body17) and poison-zero; MAIN
owns registry installation, CAS, both proofs, and the full submission. The
worker's static acceptance checks were limited to document syntax, source facts,
root byte identity, and diff hygiene; no body was run.
