# AP2-M2 bootstrap baseline conversion review

## Verdict

**APPROVE** the exact candidate commit/tree:

- commit: `541f07f5754fd0ebc6b16767d692baba736bbdb3`
- tree: `a29cf2b0928a65c1e22bad25ee4d0239e336570d`
- base parent: `780c502368cb6eb379cf3848af7009067c7cd744`
- base parent tree: `8eed52bb7f8555c7765a8b485e00920bbf906639`

This is an independent test-conversion approval only. The candidate changes
only `tests/e2e/local/three-products.spec.ts`; no product/source path was
edited.

## Contract verification

The conversion is supported by the real Runtime sources, not guessed
fixtures:

- Main95bd `runtime_protocol/service.py:1698-1743` creates the timeline and,
  when the timeline commit provider is registered, calls `commits.bootstrap()`
  before returning the create result.
- Main95bd `runtime_protocol/timeline_commit_store.py:989-1026` records a real
  `parent_composition.publish` receipt with key `bootstrap:<timeline_id>`,
  `old_head: null`, `new_head` equal to the baseline revision, and the exact
  project/timeline scope; the subsequent native request is a separate
  `timeline.commit` history edge.
- Main95bd and old202 both construct history entries with `publication_id`,
  `revision_id`, nullable `previous`, the receipt envelope, `intent`, nullable
  `records`, and the `HeadPin` ancestry shape. Their `HistoryEntry` schema and
  `history_entry()` implementation match the fields asserted by the
  candidate.
- Retained gate 14046 output shows the actual ordered pair: baseline
  `parent_composition.publish` with `intent: bootstrap`, `records: null`, and
  `previous: null`, followed by `timeline.commit` with `intent: recorded`,
  `previous` pointing to the baseline, and the three native commands.

## One-to-one ledger conversion

The old assertions map directly as follows:

| Previous assertion | Candidate assertion |
| --- | --- |
| History length exactly 1 | Raw history length exactly 2 |
| One entry had `previous: null` | Baseline has `previous: null`; native entry has the exact baseline revision/publication predecessor |
| One entry was assumed to contain native records | Exact ordered receipt kinds are baseline then `timeline.commit`; only the native entry is inspected for records |
| Native command sequence `timeline.init`, `track.create`, `track.create`, version 1 | Same sequence, now also requiring `select: 'parent'` |
| Head was the sole entry | Head is exactly the native entry |

The baseline additionally requires receipt/publication identity, `bootstrap`
intent, null records, exact `bootstrap:<timeline_id>` key, exact project and
timeline scope, and null-to-baseline result ancestry. The native entry requires
receipt/publication identity, `recorded` intent, `timeline.commit`, exact
scope in `canonical_document`, and exact baseline predecessor. The ordered
receipt-kind array makes the native initialization count exactly one and does
not filter either accepted history record.

## Preservation audit

The diff is limited to the former six-line history block. The surrounding
assertions remain unchanged, including:

- canonical create route/body, create scope, one create request, one init
  request, status/order, and native command-session checks;
- the exact create/init request sequencing and zero legacy snapshot traffic;
- the native edit result and its base head;
- lost acknowledgement, exact retry body/key/response, reload, and Runtime
  restart recovery;
- guarded undo/inverse and restored native track result;
- raw/opaque data preservation and all `wire.legacy` zero assertions.

No history filtering, retry/restart weakening, original create assertion
removal, or user-visible native-result change was introduced.

## Verification run

- `./node_modules/.bin/eslint --no-cache --report-unused-disable-directives --max-warnings 0 tests/e2e/local/three-products.spec.ts` — **PASS**.
- `git diff --check HEAD^ HEAD` — **PASS**.
- Read-only source checks against Runtime95bd, old202, and retained 14046 —
  **PASS**; shapes and observed values match.

Per the brief, no browser run, central gate, localhost/live-socket suite, full
suite, pin, or re-review qualification was performed. The existing 14046
browser result remains historical failure evidence for the old length-one
assertion, not a new qualification.

## Recommendation

Land this exact test-only conversion. The orchestrator may run the separately
authorized browser gate later against the coordinated source tuple; this
review does not claim that gate or product activation.
