## WC3 review: concrete bug — do not approve

Found a blocking retry bug: `timeline_media_replacement.py:233-239` flushes any pending media-swap command with the same operation/head, without matching clip/occurrence, source, or media identity. This can submit unrelated pending work.

Evidence:

- `tests/test_timeline_clip_replacement.py` — 6 passed.
- Native parent/occurrence recipes + sync tests — 142 passed.
- Adversarial probes: ambiguity and fresh mismatch refusal passed; unrelated pending retry bug reproduced.
- Real parent-provider integration is blocked by Runtime schema mismatch (`parent` ownership rejected before adapter execution).

Integration overlap and full findings are in [agent-review-wc3-media-swap-final.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-review-wc3-media-swap-final.md).

No source files changed. Wrote the commit message and `DONE` marker.