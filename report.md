# D13 current nine-path preservation review

Verdict: APPROVE for the bounded source custody/security delta only.

Reviewed exact port `5be2918c45909abcf0c91b79b53a2ce73eed83b1`, tree
`218da96139901ced0a059cdce37146cb7fc314db`, against current
`a9f4cfdaee40f3382b51d6cdb291d7012be96b8c` and donor
`6951c176f326e99f0e4d61c89233d1de49a9c05b`.

Findings:

- Exactly nine allowed paths changed from current to port. Eight port blobs
  match donor byte-for-byte; `sync.py` differs only by the intentional current
  transcript-input carrier/call-site delta.
- Existing source/custody guards are byte-identical current-to-port:
  `host_bootstrap.py`, `source_identity.py`, the installed-origin tests, and
  the Runtime substitution tests. The eight-origin isolated probe and the
  current line-457 source/runtime-tree equality check remain.
- The c4a RECORD fence remains. Six controls are represented: absolute,
  parent, symlink-component, normal positive, installed hash/size tamper, and
  installed package-byte tamper.
- Current presence b476, core-types, transcript, and WC8 size carriers remain;
  representative carrier files are byte-identical. `runtime.lock.json`,
  `artifacts.json`, and `cli-surface.json` are unchanged, so normal95/C13
  artifact surfaces are unchanged.
- No current test assertion was removed. The old legacy host-hook test keeps
  its assertions under strict expected failure; the registered native positive
  remains active and adds the current requester/custody assertions.
- Missing installed-preflight environment is not product evidence and was not
  counted.

Checks run:

```text
git diff --check a9f4cfdae 5be2918c
  passed
git diff --name-only a9f4cfdae 5be2918c
  exact nine-path allowlist; passed
git diff --name-status a9f4cfdae 5be2918c -- runtime.lock.json artifacts.json cli-surface.json
  empty
source/custody and representative current-carrier blob comparisons
  passed
donor blob comparisons
  eight identical; sync.py intentional current-only delta
```

No build, install, native process, HTTP/socket, render, browser, or full
execution was run. The existing 82 passed / 2 deselected / 1 xfailed count and
six RECORD controls are retained in the port inventory but were not rerun here.

Manager handoff: create a fresh private noneditable Agent wheel from the exact
port commit/tree; install it with the exact Runtime b92/tree6abc and client
95bd/tree d3a290 pair and existing dependency closure; bind only the existing
four-field profile carrier with source/runtime checkout equal to the private
installed root; verify the selected venv interpreter, eight isolated installed
origins, source/Git-blob and wheel/RECORD byte/hash/size parity, no symlink
components, and the unchanged C13 Node/Remotion/browser/ffmpeg/ffprobe/fonts
closure. Run the installed preflight only with complete exact bindings; missing
environment must fail, never pass. Keep native/HTTP/render/full qualification
for its separately authorized named run.
