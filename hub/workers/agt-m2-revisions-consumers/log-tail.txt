I made no code changes and wrote the BLOCKED file. No registered command covers either consumer, and your brief says to stop there rather than invent a writer. I ran no tests, since nothing changed, and wrote no commit-msg.

**1. `authoring_bundle.py`** (`promote_approved_authoring_candidate` at line 1605, `publish_authoring_candidate` at line 1640):
- Both call `writer.publish_parent_composition(...)` with a whole compiled candidate: the parent, the changed shots, internal timeline revisions and the media manifest. The approval is bound to that candidate's digest.
- The missing piece is a command that applies a whole candidate publication. The registered commands are per-clip, track and placement edits, and none of them can express it.
- A `candidate.apply` command would be the compatibility writer under a new name.
- This needs your call before anything is migrated. Either split each candidate producer into real commands, or delete these two functions as the whole-document fallback writer.
- They have other callers: `sdk/timeline/store.py`, `sdk/remote.py`, `sdk/authoring_remote.py`, `packs/rendering/docs/scripts/timeline_document.py` and the docs.

**2. `timeline_elements.py`** (`update_parent_element`, around line 59–64): only partly covered.
- The `hold` change maps to `clip.set`.
- The params merge maps to `clip.set-params`, which also needs a schema pin.
- Missing is a command that sets a clip's `elementRef`. `tests/core/test_timeline_element_publication.py` changes `elementRef.revision`.
- Also unhandled are the removal of the legacy `config.app.elements` entry and the `config.clips` mirror sync.
- The function works on the legacy parent-bundle shape from `open_bundle`, not the native document the commit service runs.

Next step: add a `clip.set-element` command. It would need a same-identity guard, a recorded write and a guarded inverse. You would also need to decide what happens to the legacy `app.elements` entry. After that, `update_parent_element` can send `clip.set`, `clip.set-params` and `clip.set-element` in one grouped commit.

The details are in `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-revisions-consumers/BLOCKED`.
