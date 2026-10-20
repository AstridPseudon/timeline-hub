# Independent Agent review: native parent media swap

**APPROVE bounded source delta `7afcd2dabfe5015ef1bbc9c9fa4e399f2107f90d` (`tl/agt-m2-parent-media-swap-native`) on current Agent `cf7448ed6c1298b172d004914cfe2bb8c99048e7`. HOLD official SDK/App cutover, standalone schema publication and legacy deletion.** No blocking defect found in this slice. No source fixes, git mutations, integration/ledger edits or shared-dependency writes.

The distinct closed `clip.swap-media` v1 correctly targets `parent/clip:<raw-id>` with parent ownership and exact `{old_media,media}` selections. Existing occurrence swap semantics remain occurrence-only. The shared helper writes only selected clip.asset and a scoped new registry entry when needed; it does not publish a whole document. Same clip identity, old aliases, unrelated rows/closures, registry locations, order, opaque values and supported raw source window/speed/incoming transition survive exact inverse. New alias is created or required exactly. Explicit clear remains presence removal through clip.set; null/empty/false are not clear. Known time_map/timeMap and declared dynamic relations refuse in the bounded recipe.

Both selections are read through real Runtime selected_media and revalidated at acceptance. Actual stale/foreign/fingerprint and old/new lifecycle-race refusals pass without commit writes. Captured full-row/membership/track guards remain. No equal/State.matches or ID-remap weakening occurred. The inverse now scans authoritative raw parent clips while the derived mirror is stale, retains all other parent/occurrence/shot dependency scans and refuses surviving dependents. Same-value asset/physical-registry ABA blocks undo; disjoint sibling edits rebase and survive undo; equal-state ordinary rebase remains the PLAN policy. Original occurrence goldens and all original WC3 positives remain. Digest-only legacy replacement is intentionally held, not deleted.

**Complete schema must be composed before freeze.** Candidate Agent schema SHA256 `de7af1ef9f5846eb2ec03f1c49d14c16692a6c228b84a1260408d2dd49da9a3f` preserves current integration, but omits frozen S2 `26ef2bbb`'s producer.guard, five producer definitions and optional element schema_source. This is the older-base omission already disclosed by the implementer. The private Runtime schema SHA256 `7ebd71146c5f5bdd1811d0f0530f7ca95e9e2120a59f5496bbcacd1335731621` contains all candidate semantics and these newer features; its normal compatibility/generator and 75-artifact checks pass. Do not copy the entire older Agent schema over S2 or interpret source approval as publication approval.

Private provenance independently checked: retained runtime-s2 tracked files match Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a` except schema and expected generated/artifact outputs. The historical fixture Runtime matches `b2a1d9fd82121a5509769531a2e91aece97d78b9` exactly. Parent fixtures use genuine managed settlement and retained decodable PNG/MP4 sources through historical public baseline creation, then normal migration/current-private acceptance and immutable reload. No fabricated accepted history, SQL seeding or patched validators. Live Runtime has since advanced; this evidence does not qualify its latest release pair.

Independent reviewer evidence, all exit 0:

| Command/lane | Result |
| --- | --- |
| Exact candidate: eight reported command/provider/inverse/clear test files | **481 passed in 49.00s** |
| Exact candidate: `pytest -m integration tests/editing_conformance/test_commit_runtime_parent_media.py`, private S2 + historical seed | **22 passed in 68.03s** |
| Exact candidate: `pytest -m integration tests/editing_conformance/test_commit_runtime_occurrence_media.py`, original historical fixture Runtime | **48 passed in 41.04s** |
| Separate parent `::test_selected_swap_capture_accepted_reload_restart_retry_undo_and_redo`, both renderer evaluation entry points trapped | **2 passed in 6.37s** (included in the 22, not two new behaviors) |
| Supplemental deterministic probes: direct/nested/dual registry ABA/order, bool-number guard, remap rejection, opaque dependent, timing booleans, same identity/window | **27 passed** |
| Candidate patch on isolated archive of current integration, `patch --fuzz=0`; parent, replacement, original occurrence and video-unplace neighboring files | **122 passed in 32.04s** |
| Runtime `generators/generate.py --check`, Runtime and Agent `scripts/artifact_manifest.py --check`; selected changed-file Ruff; candidate diff check | **PASS** |

Renderer-trapped tests perform dry-run/capture/acceptance, immutable stored reload after restart, exact-key retry with engine execution trapped, changed-payload same-key refusal, exact canonical undo/redo and integrity check. The selected SDK adapter uses the commit door and original head/publication pair; invalid partial selections never fall back to publication.

No full/full*, make check, browser/HTTP/socket, live App, public cohort, producer/requester, macOS or owner-film/pixel/audio qualification is claimed. Actual `currentVideo85` owner-film data was not supplied/found; a supplemental synthetic clip with that ID preserves nontrivial raw from/to/hold/speed and exact inverse, but is not film qualification. The original occurrence 48 use pre-cut baseline APIs; current parent 22 use the normally generated private S2 acceptance path. No test expectations were weakened, skipped or converted to refusal.

Next: retain source approvals separately; compose full schema/provider successor, regenerate normally, qualify the real paired consumers, and only then authorize legacy cutover/deletion with original behavior tests intact. No review blocker remains.

Exact commands, scripts, logs and detailed limitations: [review report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-parent-swap-current/notes/report.md).
