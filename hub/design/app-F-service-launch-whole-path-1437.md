## Report

- Read PLAN §3 and audited the installed caller at `3d86494f48` (author1419/security1424 PASS/installer1429). No product files changed; worktree remains clean.
- Current authenticated tuple:
  - App `be98aac54e...`, tree `2839c7e...`, both parents retained.
  - Agent `5492fc8041...`, tree `9fce413c...`, both parents retained.
  - Runtime `e68cf23164...`, tree `a2cbedd...`, both parents retained.
- Preserved custody metadata includes 14 App / 15 Agent mappings, 51 request fields, 133 reply/history fields, import origins, CPY/RCPY interpreters, Remotion/Node/Composition graph, target snapshot, registry/outside rows, body/native/encoded stages, and P2/P3 stage/read/wait/history/undo guards. Full request/response contract fields remain unchanged.

### Finding

The exact missing boundary is the generated `CUSTODY_PREFIX` in `caller-publication.py:104-109`. It requires inherited:

`TIMELINE_AGENT_CHECKOUT`, `TIMELINE_RUNTIME_CHECKOUT`, `TIMELINE_CHILD_NAME`, and `TIMELINE_REMOTION_NAME`

before entering the generated row.

The normal P2/P3 outer rows do not export those variables before invoking `bash -c`; they only construct normal `ASTRID_*`, `CPY`, `RCPY`, import, client, graph, and source-admission bindings later inside the body. Therefore both current runs terminate before any original body, import, client, graph, or source admission.

Cached primary failures:

- P2 `12541`: `full-e2e-three-products`, exit 2 in 1s.
- P3 `1689`: `ap2-P3-gate5-h6-0348`, exit 2 in 1s.
- Both emitted: `current caller environment inputs are required; original-body-NOTRUN following-stages-NOTRUN`.

The passing historical P1 route used a different contract: it populated its shell environment before launching the body, with explicit `ASTRID_CHECKOUT`, `ASTRID_RUNTIME_CHECKOUT`, interpreter, `PYTHONPATH`, and client setup. Its historical values must not be adopted for the current tuple.

Offline normal, `-O`, the plan’s 22+37 controls, and wrapper checks only authenticated source construction, serialization, syntax, argv, and manually injected export statements. They did not execute the generated outer row under the central runner’s inherited environment, so they could not detect this boundary mismatch.

### Minimal safe principle

Source-mode launch must bind every variable required by its first custody prefix at the same outer launch boundary, from the current authenticated recipe. Missing values must remain a hard pre-body failure; they must not default to historical paths, child names, or receipts.

No live service or full suite was rerun. The specified R4/prior-report paths were unavailable at their exact locations; current source and primary failure artifacts were available.

Commit message written to the required path; `DONE` created.