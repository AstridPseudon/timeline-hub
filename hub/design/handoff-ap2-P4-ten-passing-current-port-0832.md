# P4 exact ten-note current port handoff

PASS for the bounded source-port task. Current base is
`d462103985e3d4c4591ed76c5d5f261b2398fb36` (reviewed current integration
successor of `e49a6e76b3ab363e312c55b313714af1f845f54b`). Only
`tests/editing_conformance/test_p4_ten_note_v2_runtime.py` changed.

The file is byte-identical to
`tl/ap2-P4-ten-physical-path-sol-0819` commit
`26e98d43d348da49d2d97d8645ba4ef68bc68931`, source tree
`cc9e654ee60bc3e251070a7d7ff876994228e4e1`, blob
`afc9c112527692536a065de8cdbfc7a25c19bc26` (456 lines, 21,205 bytes). Outside
blobs are unchanged; the worktree diff is exactly one path, 212 additions and
15 deletions. HEAD's prior target blob was
`5ee8dd5b863c164e0ea5f03257ac61849a425061`, but there were no uncommitted
target edits to overwrite.

Checks passed: exact named-node collection (1 collected), scoped Ruff, private
cache Mypy, `git diff --check`, Runtime pin/tree/cleanliness, and the existing
suite-row import-origin preflight. Runtime pin was
`a5d4258312c979024865ee704da2d632ca5b2730`, tree
`f74b016ea837f8148db4a602c972073a226ed177`; normal Agent client files and
Runtime lock remain unchanged.

No HTTP/body/socket/service/browser/full/build/request was run here. The donor's
staged actual `p4-v2-http-nodes` PASS1/101sec is preserved as external evidence,
not claimed as this integrated head's execution. Manager log check, explicit
remote Agent owner review, and one actual integrated node remain outstanding.
