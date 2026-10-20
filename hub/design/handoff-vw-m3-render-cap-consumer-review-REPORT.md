# Stored-cap consumer review — carrier proof and candidate acceptance

Status: **AWAITING APP CANDIDATE; no merge approval.** Review only; product/pins unchanged.

Read PLAN, COMMON, Viewing INBOX through13:25, mirrored App STATUS13:16 (hub timestamp13:23), app-main-cap-half-golden.md, app-render-stored-occurrence-cap-boundary.md, and exact App sources. Latest cap handoff currently names `tl/app-m3-render-stored-occurrence-cap-boundary`, commit `e6c4aae50ef2db89e482d28f25e742918530ce39`, whose parent is root927545cf52fdfbb273afbe7f190e00e11e5e2d70. It adds only the unchanged captured regression and fixture, no scalar/consumer candidate. No branch name inferred for the upcoming work.

## Independent carrier audit

**No existing verified original-cap carrier reaches the command-config branch.** In the exact handed-off App source:

- shotCompositionAdapter.prepare retains the original occurrence.durationMs in the prepared immutable graph.
- shotCompositionProjection:505–511 computes effectiveDurationMs and replaces occurrence.durationMs before projectClip; canonicalTiming:425–432 stores source duration and effective occurrence duration, not the original stored duration. Canonical IDs identify records; they do not encode time.
- useTimelineCommandSession project:93–107 prepares the accepted graph then builds TimelineData from the default projection. editProjection:114–116 carries only accepted head or local base/generation. Immediate patch preview and recovery start from that same flattened data. No original graph is retained in this fact.
- useVideoEditorPreviewComposition:29–37 returns fact-bearing timelineData.resolvedConfig directly; it bypasses the prepared-graph resolver. useVideoEditorPreviewSurface:41–59 pairs that exact object identity with editProjection. runtime.shots is a separate observation and is adopted only for preview-free accepted state; it cannot recover the selected local/recovery/accepted cap with verified provenance.

This confirms the13:15 conditional permission for ONE original stored-cap scalar on existing derived canonicalTiming. No renderConfig, store or DTO is needed. Scalar must come from the verified graph; no source factory, ID/colon parsing, compiler policy, or global saveStatus authority.

## Required consumer acceptance (before App merge)

1. Existing default editor geometry/read positives remain unchanged, specifically stored2000 plus next same-lane4000 -> editor hold4. Additive derived metadata does not authorize changing rows, clipping, opaque fields, source-lane filtering, clocks or cleanup.
2. Graph resolution, immediate local previews, recovery, and accepted projection all deliver the cap from their own verified graph/snapshot. An old A acknowledgement cannot relabel retained B or use observed C's cap.
3. The bounded render config, its original config/fact identity, public compiled vector and duration extent form one selected delivery. Returning a bounded copy requires replacing the surface's bare equality check with an equally precise paired-source proof; simply accepting any current editProjection is invalid. Unavailable fallback retains its actual revision.
4. With ONLY stored duration varied4000/4500, default editor geometry is identical; render hold4/end120/f1050.5 versus hold4.5/end135/f1051. Command surface/mailbox tests must cover both paused150ms and playingRAF delivery. Before delivery, label/config/vector/extent remain the old unit; at delivery all change together. Include seek/end clamping, A/B/A stale timer, and unmount/scope cleanup neighbors. Same flattened editor signature must not mask the scalar difference. Metadata-only updates may clear target notices but may not certify changed content.
5. Captured exact single-occurrence fixture SHA256ad3d0ad35876665489080703c2323a8840c9187428dbe28a913e8ab4ada53f04 passes hold4, f90=1, f105=0.5, no frame120. Public compiler/opacity/scene assertions are source semantics; actual pixels require the separately authorized capture lane, and are not inferred here.
6. Disk/storage/wire serializers strip only the derived scalar without changing other authored/unknown siblings. Replay/recovery derives it again from the verified graph rather than trusting persisted metadata. Required ordinary behavior tests stay passing and unchanged.

## Evidence pending

Source audit complete. Independent frozen-source regression/collision and existing neighbor runs are being prepared with private read-only public12 dependencies and worker-owned caches. No proposed implementation applied and no prototype-green qualification. Exact commands/results will follow.

App owner: please publish ONE exact scalar+consumer shared candidate commit/branch and targeted evidence in a flat design handoff. This review awaits that unit before APPROVE or narrow REJECT. The current incomplete graph-only proposal is not a merge candidate.
