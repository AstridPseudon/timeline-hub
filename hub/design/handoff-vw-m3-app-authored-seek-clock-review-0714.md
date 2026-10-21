# App authored-seek clock review handoff

**Verdict: REQUEST CHANGES** for `a97f7cc383007ed19b7cd2afc3a89ff47cb83f40`
(`tree37065fdeda343f82c349f65684da5cd976037d2d`).

The four-file seam is otherwise narrow and correct: keyboard relative seek is
forwarded one-to-one through `editorOps.onClickTimeArea`, final release input is
not dropped, drag/playback paths remain unchanged, and no fps/source/player,
DTO/store, or authority change is present.

The real installed Remotion 4.0.509 Player emits `frameupdate` from a React
`useEffect` after frame commit. App `RemotionPreview` can dispatch a queued
latest seek from its own RAF. With rapid A→B seeks, that queued B commit can
emit after the candidate's one-RAF `isSyncingFromTimeline` clear, allowing the
rational B echo to replace authored time again. A tiny React DOM timing witness
reproduced the equivalent ordering (`frameupdate-effect frame:2 guard:false`).

Minimal owner correction: keep the existing timeline-origin carrier/seam, but
hold it through the preview mailbox's active + queued authored seek feedback (or
use an internal seek-generation/completion carrier), and add one focused rapid-
seek regression. Do not revive the early return or introduce a second clock,
quantization/clamp, new DTO/store/authority, or preview/player redesign.

Peer DETAILS/report was not delivered in the mirrored coordination paths. The
stated 149-test green result is therefore recorded as owner evidence, not
independently rerun here. Full, browser, physical/native, and mounted-split
qualification remain unclaimed.
