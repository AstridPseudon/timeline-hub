# Runtime peer clarification — transition ID, frame, and revision boundary

New findings only; this does not resend the earlier five App findings.
Full bounded report: `design/runtime-transition-frame-id-source-clarification-1000.md`.

- **Exact ID:** Agent's built-in descriptor is `cross-fade`; `crossfade` is an
  alias/renderer spelling. Main preserves the selected ID. App must emit the
  selected descriptor ID verbatim in both transition `type` and `elementRef.id`;
  Runtime must not normalize aliases.
- **Frames/seconds:** Main's real `timeline.apply_transition` and
  `timeline.update_transition` path validates positive integer
  `duration_frames`, then stores `duration_frames / fps` seconds. Agent ca9
  accepts authored seconds whose FPS product can be fractional (including
  `0.75 * 30`). The carrier may remain seconds, but the unconditional Main
  parity claim must be removed. Agent owns whether a complete Main-compatible
  source narrows admission to integral frame products; App converts Main integer
  frames to seconds exactly and does not round authored values.
- **Revision/reference:** Selected SET requires a non-empty matching revision
  in both transition and `elementRef`, plus existing selected-pack authority.
  Authenticated legacy no-ref updates are distinct: they may preserve an
  absent or present revision state only when the existing transition already
  exists, both reference spellings are absent, and requested type plus tagged
  revision presence/value match exactly. Present `null`/empty/malformed refs
  are present claims, not absence. Use explicit membership/sentinels, never
  `.get()` or truthiness. Agent owns this source correction; App must preserve
  the raw legacy envelope and omit `elementRef` on that path.

No generation, pinning, activation, or consumer qualification is implied.
