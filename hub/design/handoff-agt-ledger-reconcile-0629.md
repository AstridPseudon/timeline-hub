# F-D86 ordinary ledger recovery

Status: **RECOVERED — source-qualified / behavior-pending**.

The canonical ORCH ledger was repaired by appending the exact D106 worker0604
publication bytes once, after the complete current prefix. No ledger entry was
rewritten, reordered, dropped, or guessed.

## Reconciliation

- D106 worker0604’s retained report claimed an append from `168319` bytes,
  SHA-256 `c2cd8e68f8ae8566fbcea45aef58e50904c40e42544e80766516ee635ae80871`,
  to `172066` bytes, SHA-256
  `eb745e019c99fe2daa655d81838995e34dc28b7e1dddbaee71646bc9609af306`.
- The canonical ledger actually contained the exact 168319-byte prefix plus
  the later `F-D86-word-mirror-0622` entry: `169973` bytes, SHA-256
  `fb7ac929e609161e41f70ab7f6fe0ebb377a9cd0ac46151aa1a775539670ca80`.
- The missing D106 append was retained verbatim in
  `workers/agt-F-D106-ledger-0604/log.txt`. Its ten lines are 3747 bytes and
  replay to the claimed D106 172066-byte hash from the claimed old prefix.
- Repair result: the full current 169973-byte prefix is preserved exactly, and
  the retained 3747-byte D106 block is appended once. Final ledger: `173720`
  bytes, SHA-256
  `ebe797dc4f450f1895e111aadf34e6368ae450f907f0ac907fccec629f6d90ee`.

The discrepancy is therefore explicit: worker0604’s five approved entries
were published in its retained log/report, but were absent from the later
canonical file that had acquired the word-mirror entry. The word-mirror entry
remains before the recovered D106 block. No refusal occurred on the authorized
ORCH route; no hub write or retry was attempted.

## Recovered D106 content

The five exact source-qualified / behavior-pending entries are:

- `D106-opaque6`
- `D106-script4`
- `D106-D98a`
- `D106-parentmedia`
- `D106-sheetCLI`

The six existing handbacks and manifest remain unchanged. The projection
handback remains source-qualified / behavior-pending and explicitly **not
MAIN9-eligible** because its D100 dependency is actual `30890` NO-GO; it was
not one of the five ledger rows.

All source hashes, review references, normal receipts, memberships, preserved
inputs/topology/opaque values/assertions, refusal/retry/inverse/ABA guards, and
the D100 hold remain as handbacked. No behavior credit, retirement, fixture
validity phrase, or policy/authority change is claimed.

## Static validation

- D106 replay from the old prefix: `172066` bytes,
  `eb745e019c99fe2daa655d81838995e34dc28b7e1dddbaee71646bc9609af306`.
- Repaired ledger current-prefix hash: first `169973` bytes equal
  `fb7ac929e609161e41f70ab7f6fe0ebb377a9cd0ac46151aa1a775539670ca80`.
- Repaired ledger final: `173720` bytes,
  `ebe797dc4f450f1895e111aadf34e6368ae450f907f0ac907fccec629f6d90ee`.
- `F-D86-word-mirror-0622`, the D106 section heading, and all five D106 row
  markers each occur exactly once.
- Manifest shape check: header plus six records, 14 tab-separated fields per
  line; frozen candidate commit objects resolve read-only.
- No pytest, imports, collection, helper/fixture/function execution, probe,
  service, full suite, browser, install, or hub write was performed.
