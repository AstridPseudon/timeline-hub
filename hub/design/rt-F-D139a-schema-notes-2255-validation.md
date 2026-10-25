# F-final D139a schema provenance note

## Result

Installed one truthful D139a schema-provenance paragraph into each existing
delivery-builder input: `README.template.md` and `gate-results.md`. The
paragraph records the authenticated installed `banodoco-timeline-schema==0.0.2`
input, its pinned ArtAgents commit and subdirectory, the exact 18-row RECORD
closure (12 hashed plus six named standard unhashed rows), the unavailable
source-tree tie, and the absence of source acquisition or a fresh source build.
It does not claim an actual child, core suite, or render passed; the 111171-byte
maker candidate remains awaiting security review 2250 and CAS.

## Exact checks and results

- Captured predecessor backups before editing: PASS. README hash
  `df9b4a622fddcb570a6919f4ff1dfd793f2929f0db87bb9aa55f3b529eba79b9`, gates
  hash `5661b6b698620bb6a486fad9677d2dad7117646a2723845f389a73dd40b63b8e`;
  both mode `0644`.
- Builder idle check at CAS: PASS; no active `delivery-build`,
  `build-delivery`, or `render_readme` process.
- Atomic installation: PASS at `2026-10-25T22:51:43Z`; predecessor hashes
  matched immediately before same-directory temporary candidates were renamed.
- Candidate/readback hashes and modes: PASS; README
  `ffe1da575b397629f301c3b8043bc1cc7ed8d6f17fde0505b0bdc0c4fffded51`, gates
  `1d47199bcadb6d463ed94cb5e41a5a9845a167dacdea3ce8aaa6ab26d4a49835`, both
  mode `0644`.
- Outside-byte equality and exact paragraph count: PASS; removing the one
  inserted paragraph from each candidate reproduces its predecessor byte for
  byte, and each installed input contains exactly one paragraph.
- `git diff --no-index --check` against each predecessor: PASS (expected content
  difference status 1, with no whitespace diagnostics).
- Real `delivery-build.render_readme` with the prior controlled four-repository
  stub shape: PASS; four rows, the paragraph rendered twice through the actual
  template-plus-gate path, zero unresolved placeholders, balanced fences, and
  link check passed. This was a renderer check only, not a delivery build, ZIP,
  install, child, core, or render qualification.

No product, source, test, generated, pin, kit, ZIP, child, provider, browser,
server, acquisition, or suite action was performed. The v2 commit request/reply
shape remains unchanged.
