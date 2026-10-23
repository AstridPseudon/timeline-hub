# Independent G5 current-draft review

## Verdict

**PASS — source-preservation review only.** `c59a751774cf74267daab779f6e3dc2604fc3993` is a direct child of current base `78738040d72ce74c42ddf7731221aecb06f9246d`. It preserves the reviewed G5 delta from `6531622c8..bda966e9c` and remains a draft. P1 is **NO-GO**: this review does not authorize a merge, integration activation, source-actor approval, or Runtime qualification.

## Source union and ancestry

- Current and reviewed deltas both contain exactly 47 paths. The sorted path-set SHA-256 is `20c856122acfc8074d608a15a816cc91fcc21a54fc114dccc8e378382182255c`.
- The current commit has one parent and `git rev-list 78738040d..c59a75177` is `1`; there is no unreviewed merge ancestry or imported report artifact.
- Of the 46 final donor paths, 45 existing/added blobs match the donor exactly. `astrid/sdk/timeline/document_diff.py` is the authorized deletion. `astrid/sdk/timeline/store.py` is the only surviving content mismatch and is the intentional mechanical union.
- `store.py` retains the current exact revision/publication head-pair reader and publication hydration, while carrying the reviewed retirement. The obsolete unique-by-revision lookup, `three_way`, and `publish_bundle` are not present.
- Outside the 47-path set, current R1 `f078d0229`, registry `22f1cb169`, A4 track/transcript witnesses, legacy `d1d41c405`, source-auth files, and all other current product/test blobs are unchanged from `78738040d`.

## Behavior and caller preservation

- The four authentic SDK test bodies and decorators are AST-identical to reviewed `9da584010`/`dc5c84b9a`; the hashes are recorded in `evidence/ast-locks.md`. The c271 body and its fixture-control bodies match reviewed donor `bda966e9c`.
- No test skip, xfail, deselection, assertion weakening, fake authority, new Runtime guard, API/pin/schema/Git/daemon change, or source/test edit was introduced by this review.
- Production caller wiring remains the normal commit path: CLI restructure uses `Checkout.publish`; SDK/public publish emits commands and calls `TimelineSession.open`/`session.submit`; generated `WorkspaceClient.commit_timeline` remains the request/reply boundary. The retained `cli_native._normalized_document_diff` is a local normalization helper, not the deleted module or a writer.
- Production route scan found no active `commands-file`, `publish_bundle`, `store.three_way`, deleted `document_diff.py`, separate-publish, legacy publication writer, or `apply --native` writer. Historical tests still contain old-route expectations. The inherited stale text at `astrid/packs/rendering/docs/SKILL.md:229` explicitly mentions `publish`, `apply --native`, and legacy three-way merge; it remains open evidence, so this is not a grep-zero claim.

## Evidence run

All permitted checks ran on this current tree with private temporary directories:

```text
current-pair reader: 16 passed in 3.70s
owner-scope controls: 6 passed in 0.60s
bounded eight-file acceptance: 184 passed in 48.23s
Ruff findings: current=2148 baseline=2148
Mypy findings: current=1911 baseline=1911
vendor lock: ok runtime.lock.json (matches producer manifest)
artifact manifest: artifacts.json is current
git diff --check: pass
credential-shaped scan over existing reviewed-scope files: 0 matches
```

The exact commands and outputs are retained in `evidence/commands-and-results.md`; source/object hashes are in `evidence/source-sha.md`, and the credential scan record is in `evidence/credential-scan.txt`.

Frozen values remain Runtime producer `34eac0041b0891e9011966b39bcbd26053fde5bc`, schema digest `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`, and Composition artifact `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.

## Limits and next steps

The original SDK FOUR, c271 qualification body, public redo, old 14/110/9 suites, full suite, P1/P4, browser, live HTTP/socket, and other prohibited bodies were not run. The retained joint-audit evidence is qualification FAIL/unproven; source proof does not satisfy Runtime qualification. Keep P1 NO-GO and require the separately authorized clean mechanical forward and independent Runtime qualification before activation.

The supplied `/home/user/peteromallet/astrid-agent/docs/projects/timeline-r4` control-doc path was absent in this environment; the frozen candidate branch remained readable via `git show`. No merge, push, checkout, or integration request was performed.
