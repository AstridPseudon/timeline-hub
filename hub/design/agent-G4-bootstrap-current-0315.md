# Agent G4 bootstrap/current forward

PASS on the bounded merge-forward and static/protected-source gates; see worker report for exact commands.

Parents:
- base: a8c2b5b88533c7b58207f0b77d179a1dc523c0d2
- true merge parent: ecea7d8563c93059283ef9475ecb41a37e628a38
- approved schema source: 7d3562028, digest d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d

Resolutions:
- timeline_document.py: retained verified original-publication hydration and exact media capture.
- emitter.py: retained verified materialized successor-owner resolution.
- inverse.py: retained R2 step undo and current authenticated timeline-scope binding semantics.
- No State.entity, V2 policy, client, or test-weakening changes.

Evidence:
- create-empty 13 passed
- provider 111 passed
- step-undo/emitter 97 passed
- scope/doc-patch/graph/schema 177 passed, 33 deselected
- parent-media lanes 174 passed, 61 deselected
- non-integration authoring-media/clip 82 passed, 2 deselected
- Ruff 2150/2150; mypy 1915/1915; vendor lock, artifact manifest, diff-check passed
- 15/15 lock blobs exact to ecea; six V4 live-scenes paths absent
- Prior scope review: three Runtime-780 bootstrap positives passed

Known red evidence: preserved real-runtime document-script test still expects semantic clip.move/clip.set after occurrence.swap-media, while merged G3 emits doc.patch. The original assertion remains unchanged and this discrepancy is reported rather than hidden.

