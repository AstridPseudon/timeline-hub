# Runtime parent `afterClipId` source review — SOURCE ACK

Date: 2026-10-20 UTC  
Worker: `rt-m2-review-parent-afterclip9e-source`

## Verdict

**SOURCE ACK** for the committed Agent source/schema only.

The exact reviewed candidate is Agent commit
`9e24068c553f786f467b8838a0f92a02e2474f37`, tree
`620c0269751e75400681cac979853064eb5d02c3`, with parent
`1c18c8c84cec366ce683349858fb2399435c9265`. The commit changes only:

- `astrid/sdk/timeline/native_parent_media_commands.py`
- `astrid/sdk/timeline/_recording.py`
- `astrid/sdk/timeline/commands.py`
- `tests/editing_conformance/test_recipe_m2_parent_media.py`

The canonical Agent schema is byte-identical to the handoff and has SHA-256
`21f313a7005f94a2525013ab9fd628afa626a7886bc098840a73ac012c0fcac2`.
The exact changed-file hashes match the proposal, and `git diff --check`
passes. No new wire field, DTO, endpoint, store field, generation artifact,
or schema operation was added by this commit.

## Source contract findings

- The existing `clip.add-media` envelope carries the intention through
  `select: "parent/clip:<raw-id>"`; `parent` retains append behavior.
- Capture resolves the raw parent row and derives the destination start from
  the source's authored interval. Caller timing is not authoritative: the
  captured row clones source metadata and changes only the reserved clip
  identity, effect identity, selected asset, and derived start codecs.
- Execution records the complete parent clip membership/order, raw anchor row,
  source asset binding, parent output rate, verified destination media, and
  reserved created identities. It inserts immediately after the exact raw
  anchor and shifts later clips on that same track by
  `max(0.05, clip_timeline_duration(source))`. Other tracks and occurrences
  are untouched.
- Missing or non-parent anchors, changed owner/track/timing/order/media/rate,
  malformed clone rows, and occupied reserved identities refuse. There is no
  display-ID inference, append fallback, clamping, or late catalog selection.
- The recorded peer writes, ordered selection, mirror-derived write, and
  created IDs feed the existing guarded inverse/replay machinery. The
  preceding `timeline.assembled-target` replacement sequence remains the
  explicit non-ripple exception.

## Evidence reviewed

The handoff reports 7 focused and 267 neighboring Agent tests. The independent
Agent review reports 6 decisive after-clip controls, plus inline controls for
changed peer extent, new same-track membership, exact inverse refusal, and
source-window/rate duration. I verified the committed bytes, exact tree,
changed paths, schema hash, file hashes, and diff cleanliness directly.

Runtime existing boundary controls also pass:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
/home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
tests/test_timeline_commit_validation.py tests/test_timeline_commit_provider.py
53 passed in 3.76s
```

## Explicit boundary

This is a reciprocal Runtime **source/schema** ACK only. Runtime's currently
checked-in public contract remains a separate older schema artifact; this ACK
does not claim a current-public pin or installed-provider acceptance for the
private Agent schema. A future compatible private counterpart must carry the
existing `clip.add-media` operation, but needs no new after-anchor wire field.

This ACK does not certify a native App workflow, Runtime/App qualification,
generation, pinning, publication, activation, browser/live-socket behavior,
renderer behavior, or writer retirement. No source incompatibility was found.
