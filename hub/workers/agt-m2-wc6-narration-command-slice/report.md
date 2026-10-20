Implemented the WC6 document-view timing slice.

- Reordered existing native media swap before `clip.move`/`clip.set` timing capture.
- Extended exact ordinary014/generated014 HTTP proof with timing, narration/metadata/source-window/opaque preservation, inverse/redo, and ABA checks.
- SDK `publish_authoring_candidate` positive remains unchanged.

Tests:

- Local: `88 passed, 2 deselected`
- Ruff and `git diff --check`: passed
- Central HTTP proof: `1 passed`
- Full suite: not run.

Files: [document_diff.py](/home/user/work/wt/agt-m2-wc6-narration-command-slice/astrid/sdk/timeline/document_diff.py), [test_authoring_media.py](/home/user/work/wt/agt-m2-wc6-narration-command-slice/tests/timeline/test_authoring_media.py)