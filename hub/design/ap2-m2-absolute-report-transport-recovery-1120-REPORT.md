# App2 management-artifact recovery manifest

Recovered exact management bytes on 2026-10-21 into the absolute orchestration
design directory. No App product source, repo documentation, or `.gitignore`
was changed.

| Artifact | SHA-256 | Exact source |
| --- | --- | --- |
| `ap2-m2-parent-viewport-current-main-packet-1110-recovered-REPORT.md` | `5ff954b9d475823322cec1cc6bd0792987281e47b6b3a42258492d8228e2d026` | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-viewport-current-main-packet-1110/log.txt:6412`, final successful `apply_patch` diff |
| `ap2-m2-parent-viewport-current-main-packet-1110-run-on-main.md` | `ffc367a8fc6da05cde0a0b58ff92ac9b0fe0606ef7d201ca980cbcdc84a54ccc` | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-viewport-current-main-packet-1110/log.txt:6115`, final successful `apply_patch` diff |
| `ap2-m2-transcript-derived-result-unapplied-1118-REPORT.md` | `a00802138fa37e92403fc80ff840ccf1e0d5c8eda2ef9a873ec55029b5cf409a` | `git show f881dfbc252b5ed0e1be47a46b4ee877e6da1482:design/ap2-m2-transcript-derived-result-unapplied-1118-REPORT.md` |
| `ap2-m2-element-owned-admission-handoff-unapplied-1118-REPORT.md` | `f9b3263de28e26be1dc7e7e5e7679d2f3a030e0bc01983d62a0efb7976365e0` | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-element-owned-admission-handoff-unapplied-1118/log.txt:8698`, final successful `apply_patch` diff |
| `ap2-m2-main-parent-selected-custody-review-1113-REPORT.md` | `5cfadf568777d3bf3604fb34e2f02f413f968406431f5d341039e8c374ae79df` | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-main-parent-selected-custody-review-1113/log.txt:7202`, final successful `apply_patch` diff |

The 1110 handoff is under a unique filename because
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/run-on-main-app2-parent-viewport.md` is parent-finalizer
1116's owned packet. During recovery that shared path was temporarily
collided; it was restored from the finalizer's last logged `+225`-line
patch and is excluded from this manifest and from the 1110 artifact set.

## Product-merge disposition

The four source branches are recorded below. Report-only branches are
**documentation-only / ABANDONED for product merge**:

| Source branch | Resolved tip | Disposition |
| --- | --- | --- |
| `tl/ap2-m2-parent-viewport-current-main-packet-1110` | `6707a30f14bf3a5ee19cb9e481b7dbd95b77522a` | **Excluded from abandonment list**: real parent viewport fixture product branch; parent finalizer 1116 owns its packet. |
| `tl/ap2-m2-transcript-derived-result-unapplied-1118` | `f881dfbc252b5ed0e1be47a46b4ee877e6da1482` | **Documentation-only / ABANDONED for product merge**. |
| `tl/ap2-m2-element-owned-admission-handoff-unapplied-1118` | `0cc2583aaf07e89190b9344b5ac82849d6279586` | **Documentation-only / ABANDONED for product merge**; complete peer-ready proposal recovered. |
| `tl/ap2-m2-main-parent-selected-custody-review-1113` | `0cc2583aaf07e89190b9344b5ac82849d6279586` | **Documentation-only / ABANDONED for product merge**; custody review remains valid outside the repo. |

The parent finalizer branch
`tl/ap2-m2-parent-viewport-durable-main-finalize-1116` remains the owner of
that packet and was not changed.

Peer-ready manager handoff paths:

- Result proposal: [transcript derived-result report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-transcript-derived-result-unapplied-1118-REPORT.md)
- Element proposal: [owned-admission report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-element-owned-admission-handoff-unapplied-1118-REPORT.md)

No tests, builds, browser/socket/service executions, installs, or product merge
requests were performed for this recovery task.

