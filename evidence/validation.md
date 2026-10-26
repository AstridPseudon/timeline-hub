# D141l independent validation

Verdicts are separate: Node DATA **PASS**; pristine attachment **PASS**; operational compression **FAIL** because one manifest-listed KEEP was absent at the independent read. No product tests, typecheck, lint, browser journey, full suite, or body inspection was run.

## Node DATA

- Composition HEAD/tree matched `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` / `5ab5191a296980a0a6bcd1178ab6902d6478a148`; worktree was clean.
- Independently hashed the five retained Node source files, the controller-admission receipt, and the trace. The 19 trace rows, header, offsets, job ID, PID `18109`, five-second labels, MAX `4798197760`, and MIN `4625068032` all matched the prepared records.
- Controller admission `4814028800` was authenticated from the original 0606 receipt at byte range `[104,137)`. It is a conservative admission bound, not the actual Node-first sample. The actual Node-first comparison is `4798197760`.
- Growths are `188960768` and `173129728`; the unchanged formula selects `4600000000` bytes. Gaps between samples remain explicitly unobserved; no continuous peak is claimed.
- Repeated the unchanged validator from a worker-owned scratch fixture using the same nine-argument signature:

```text
python3 -I /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/d141-validate-receipt.py /tmp/w-99449a541b/node-validator-control/tests/app-full-d141-node-phase-1026063009-19156/recorded-measured-floor.json /tmp/w-99449a541b/node-validator-control app-full-d141-node-phase-1026063009-19156 app full-d141-node-phase /home/user/work/app 4de54db14bdc9ddc2ce2e5887258b03acbffd30d 84c3fb7f73f08c22220f8e808962fe3f24aaa0aa 'npm run test:node'
```

Exit `0`, stdout `4600000000`; validator SHA-256 is `2987adbcd888400a41afbbd60e22ea2e4afe6c4580b084a4d63dcced6943a7f6`. The fixture used genuine original Node19156 identities but was not attached to the historical receipt or any real test ID.

## Pristine attachment

The original read-only validator returned exit `0`, stdout `4793895424`, for the unchanged request/receipt pair. The request hash is `26f6a8d0dfded2d7c96eba9cf2577862da0a841c91e84a26debe7a933a304321`; the receipt hash is `4c01fb145865378a8405f8cdca5e263c9a9a44eac30046113b780e274aa52fbc`; source HEAD/tree are `d822d2f5d2bd05187b4ff5b6071c3e13945d4747` / `2af40a015057779ceb4e4b37cad62e1469aa7e36`. The source worktree was clean and the request had no body.

The same-ID request was observed as `running` at `2026-10-26T07:05:42.116Z`; it was not intervened in. This is not a pre-admission claim, and no duplicate request, body, queue edit, or floor bypass was made.

## Operational compression

The independent read decoded and matched all `161/161` manifest preimages by SHA-256, byte count, mode, and mtime; checked all `111/111` pre-existing `.gz` records unchanged; and confirmed all 12 current `20261026` logs were excluded and had no `.gz` companion. The author result also records `PASS`, manifest unchanged, and recorded KEEP pre/post checks passing.

At the independent read, `37/38` manifest-listed KEEP markers still matched. `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-pin-867cb273/KEEP` was absent. This is finite missingness in the current custody view; no deletion or recompression of a log is inferred, and no original was corrected.
