# F-final 7070 inventory successor

Prepared one private successor from the durable `rt-F-final-2252-first-return-1130`
candidate. The composition worktree remained at `tl/integration`; no product, test,
registry, installer, pin, contract, upstream, service, or installed-source files were
changed.

## Exact release source

The normal Runtime release is `7070f1378d1917fcce69857ebd33cd2b3015568b`, tree
`cd68015cb9fe85a6ecd2d15dd7e2eac69f67e2b1`. Its reviewed source is
`f0c4d6d2b66bb84e935b9008853fcb628746fe88`, which is the `PASS_SOURCE` candidate from
the security review `rt-D111b-release-security-1122` (reviewed base
`8ca89d83049affbb0bdb68a441b023225b7a731d`). The normal release receipt records the
9-case integrated smoke as 9/9 PASS and the released tree equal to the reviewed tree.

Only these released 7070 test blobs were missing from the predecessor inventory:

| path | Git blob | SHA-256 | production caller |
|---|---|---|---|
| `tests/test_timeline_commit_ancestry_reads.py` | `c30916940e7816ab1332cee271deda4352eeeef0` (introduced by `8ca89d830…`) | `316f7ca5ff1874c3f0206296ed2ef18341c8ac5a35ba1de8db803219325cd42a` | `runtime_protocol.server._timeline_commit` → `runtime_protocol.service.Service._execute_timeline_commit` → `runtime_protocol.timeline_commit_port.RequestCommitPort`; exercises `history_entry` and `history` |
| `tests/test_timeline_commit_closure_growth.py` | `9e4ebfc7c455441a41da750c41241800782e9153` (introduced by `f0c4d6d2…`) | `e64b9b587eb3540bfe58adde45191d491b40017c0cf4b2dfbbbd0ceb3ca4ae1f` | same Runtime caller; exercises `history_entry` and `revision_closure` |

The resulting inventory is 100 Python targets plus the preserved TypeScript target: all 98
predecessor targets are byte/hash-preserved, with exactly the two additions above. No
D111b, SWAP, held tag, or unmerged source is included.

## Matrix custody

The predecessor `d59-final-matrix` was copied as the durable input and not edited. A
before/after byte-hash comparison found 41 files before, 41 after, and zero changed
files. Representative unchanged hashes include:

```text
README.md                                      3fe3aa4bede266e29232a6b54eb65edab973175763e4f2d29290b5cfbb3e7970
run-final-matrix.py                            3e9c15cb535fc567768d920d2f9c4fddbdbe51800a44334486dc400e14c47f44
stubcontrols.py                                fd8f0434b78e3daae85850aa21762004a5b3f7c545b49324d5164398cfaad138
agent2236/.../sha256manifest                   c1663840d1411fb2c80edcee0cac0c3af9d5706e0a3f0a10537647d67455ec88
```

Historical P4 remains five selectors; final P4 remains the separate three-selector
pending handoff. The matrix still has ten venues, a pending tuple, D73 capture-once/four
checkout custody, positive-once/poison-zero controls, and the exact registry drift guard
that refuses before mutation.

## Checks

- In-memory compile: PASS, 18 candidate Python files.
- JSON parse: PASS, 7 candidate JSON files.
- `bash -n`: PASS, candidate shell files.
- Ruff F: PASS.
- mypy: PASS, 12 candidate-owned files.
- D73 private acceptance: PASS; one capture, four receipts before request, newer-home
  marker accepted, selected-checkout drift refused.
- D59 stub controls: PASS; positive dispatch once, poisoned dispatch zero.
- Pending matrix: PASS; refused before dispatch.
- Installer control: PASS as a refusal; live registry hash drifted
  (`fecaa66d...9156` versus preserved `b0557c...80d3`) and the guard stopped before
  mutation.

No real request-test, service body, install, registry mutation, checkout request, network,
full/browser/render/build/ZIP, or tuple selection was performed. The final tuple remains
`PENDING`.
