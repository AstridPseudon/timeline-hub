# CHANGES REQUESTED — grouped clip-root inverse review

One P2 defect in `9ccf10ec` versus `b5cfce50`: `astrid/sdk/timeline/commit.py:256` drops an introduced transcript pin when a surviving opaque reference to it is on an occurrence. `_inverse_clip_transcripts` searches parent and shot data, but authored occurrences live separately in `bundle['placements']`. A real normally generated S2 + candidate run accepts birth + anchor + grouped inverse, preserves the occurrence's exact pin dictionary, and incorrectly returns `dependency_manifest.documents=[]`. The same pin on the parent is retained. Include surviving occurrence authored data in the scan and add a main-suite regression before approval.

The root-cache staging itself passed review and reproduction: accepted before/after provenance, no broad root ignore or new numeric normalization, and no whole-document restore. Original grouped failure reproduced on untouched base; repaired joint cases and exact full-group redo/restart retry pass. Genuine accepted authored `at` and `hold` writes still refuse undo even when the compiler also writes the same path. All eight changed files inspected.

Fresh targeted evidence (overlapping counts):

- Portable lanes: **249 passed**, then **255 passed / 4 existing xfailed**; all 10 new cache controls included.
- Real Runtime neighbours: **116 passed / 2 preexisting fixture-import failures**. Both old `_binding_descriptor` failures reproduced unchanged on baseline; requirements remain live.
- Independent compiler-masked authored-write and pin-location controls: **3 passed / 1 failed** (the occurrence omission above).
- Exact original media grouped undo → redo → restart/retry: **1 passed**.
- Baseline original counterexample + old fixture controls: **3 expected reproductions of failure**.
- Normal private Runtime generation and `--check`, changed-file Ruff, and diff whitespace checks passed. Schema unchanged: **53 definitions / 26 operations**.

No source fixes, git mutation, integration, public freeze/pin, first-occurrence claim, or full-suite request. Review complete; no execution blocker. Next step: repair the occurrence pin scan and rerun these targeted controls; separately migrate the two old manifest fixtures without weakening their requirements.

[Detailed report, exact commands and limits](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-grouped-root-inverse/notes/report.md). Reproduction scripts and logs are retained beside it; private source archives were removed.
