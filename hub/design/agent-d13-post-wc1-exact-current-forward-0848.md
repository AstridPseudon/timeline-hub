# Agent D13 post-WC1 exact current-forward source

Prepared source handoff for the harness. The worktree is based on reviewed
D13 `5be2918c45909abcf0c91b79b53a2ce73eed83b1` / tree
`218da96139901ced0a059cdce37146cb7fc314db`; true merge parent is current
`566307478f43672db23f84fda2a478bb6116a008` / tree
`c6ecc87ab4b5c7500de07715ab4f4a5803f1e1de`; common
ancestor is `a9f4cfdaee40f3382b51d6cdb291d7012be96b8c`.

Final tree recipe: current `56630747` everywhere outside the exact nine-path
D13 allowlist, with the nine final blobs copied byte-for-byte from `5be2918c`.
The full matrix and evidence are in the worker report. The only genuine
outside-allowlist current delta since `a9f4cfda` is preserved exactly from
`56630747` in:

```text
astrid/sdk/timeline_media_replacement.py
tests/stage1/test_runtime_client_cutover.py
tests/test_timeline_clip_replacement.py
```

Mechanical result: every outside-allowlist tracked blob equals `56630747`;
all nine feature blobs equal `5be2918c`; `runtime.lock.json`, `artifacts.json`,
and `cli-surface.json` remain current-exact. Current document b476, core-types
a9, transcript/size, RK02 afe, and WC1 outbox 566 content is retained. No
semantic reconciliation or assertion removal was performed.

Evidence: `git diff --check` passed; focused preserved media/assembly/sync
tests passed **81 in 8.61s**. No build, install, wheel, native, HTTP, render,
browser, private-body, or full suite was run. The harness must create the
two-parent commit; this is the source input for downstream wheel/profile work.
