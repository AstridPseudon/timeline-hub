# ORCHREPORT — vw-m3-frame12-current-ready

Status: READY-only contract/controller prepared; no grant and no actual run.

The current evidence is sufficient to carry forward the existing four-case
normal-profile native1920/Chrome155 test path, including the approved
`1ba0800af` dialog/backdrop capture fix and the `eeddb47c` resolved-theme
landing. The gate remains deliberately closed until the coordinated 0.0.12
consumer pair and official Runtime/client tuple are published.

The flat handoff contains:

- `handoff-vw-m3-frame12-current-ready-contract.json`
- `handoff-vw-m3-frame12-current-ready-controller.mjs`

The controller is read-only and `--check-ready` only. It refuses to launch
anything, refuses to create a grant or run marker, and reports missing tuple
inputs. It requires the real App and Agent 0.0.12 artifacts with the approved
`sha256:0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`
identity and exactly 77 archive files; the final source tuple must supply
both consumers' actual commits/trees, official matching Runtime/client pins,
and six peer hashes per consumer. The final source freeze must also assert
Node 20.19.4, Chrome 155, the pinned export browser, the existing four cases,
real managed input/full native MP4 download, same Player seek path, strict
RGB 2/255 and 0.001 limits, unmodified PNGs, and the original640 baseline.

No old `7989` ancestry was merged. No fixture resize, color/theme override,
codec conversion, threshold change, or baseline waiver was introduced. The
controller names the current render staging `320784f82`, capture fix
`1ba0800af`, theme landing `eeddb47c`, and Composition source `5e06f401` as
review inputs only; it does not treat any of those names as a substitute for
the final consumer SHA/tree.

Pending owner inputs:

1. App owner: committed 0.0.12 pin/tree and six-file peer graph.
2. Agent owner: committed 0.0.12 consumer/tree and six-file peer graph.
3. Runtime owner: official matching Runtime source and generated-client pins.
4. Manager: final source freeze and explicit grant after the above are
   published.

No browser, renderer, socket, full suite, install, network, or central test
request was run. The local check below is syntax-only and intentionally does
not attempt the gate.
