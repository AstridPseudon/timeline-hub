## F-D86/D92 protected source review

### D92 — PASS_SOURCE

- Commit: `da61c4b29a2fa5d1c49eb36922c1b042e9e72852`
- Branch: `tl/agt-F-D92-import-return-0340`
- File blob: `dc9b03efa98adb1d344e93040fa7c085f479facc`
- Canonical ID newly MAIN-eligible: `D92-docpatch5-compound3`
- Only change: forwards `duration_seconds=1.0` for the genuine 8000-frame/8000-Hz WAV to `RuntimeService.import_media`.
- Existing A/B history, `media.admit`, unused managed pin, atomic/ABA/no-write predicates and assertions remain conserved.
- Current source traces genuine `RuntimeService`, registered commit provider, and `commit_timeline`; no DetachedRealm or synthetic authority.

### word-bootstrap46 — PASS_SOURCE

- Commit: `b2cb7728522910e0196c677b1b42b72e67491ebd`
- Branch: `tl/agt-F-word-bootstrap46-0338`
- Fixture blob: `b5247b5ef47b80f2810d8d2af67412a7b7687643`
- Canonical ID newly MAIN-eligible: `word-bootstrap46`
- Native clip birth now uses literal timing; the exact original `app.astrid.on`/`for` declaration is restored by guarded `doc.patch` immediately afterward.
- Rational FPS, transcript/pin/choice IDs, opaque data, placement, sequential boundary, and all 46 selectors remain conserved.
- `test_timing_retained_inputs.py` is byte-identical: blob `6ea60c464413c25fbefb3a94c161f6f61ee32677`.

D14 and D23 deferred tests remain unchanged and visibly deferred:

- D14 blob: `5db819f485da679f613ef04455ec19708d316d6a`
- D23 blob: `0f21ba525996c539aaec60f4a39da49e56bf5a50`

### Evidence

- Python AST parse/compile: passed.
- Ruff parent/candidate: passed.
- AST conservation: passed.
- `git diff --check`: passed.
- Mypy was blocked identically for parent/candidate by the installed NumPy stub’s Python-3.12-only syntax.
- No pytest, collection, fixture/helper/function execution, Runtime, service, probe, or functional qualification was run.

Base integration: `68404b8484749d1d8ec2bdaef34faa004ad87dbe`.

Evidence: [source-review.txt](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-word-D92-review-0348/evidence/source-review.txt).