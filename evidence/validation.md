# F tiny Composition frozen-ref final review

Verdict: **PASS** for the one residual `frozen-ref-crosswalk` finding.
The corrected durable evidence binds the frozen Composition candidate ref to
the actual 40-hex Git commit/tree/parent and leaves named `origin/main` as a
separate immutable capture. The prior 1904 four-finding PASS and the 1911 D133
author installation receipt are reused; they are not new gates in this review.

## Exact validation commands and results

- `git -C /home/user/peteromallet/timeline-composition show-ref --verify refs/remotes/origin/codex/handover-timeline-r4-20261019-candidate-composition` — PASS; resolves `c82eb7c459d0a41263954bf007071a6a0e8e0a6a`.
- `git -C /home/user/peteromallet/timeline-composition show-ref --verify refs/remotes/origin/main` — PASS; resolves `67b8aa3d0d6831d3e3504a340ff583c3da253707`.
- Read-only `git rev-parse` checks for both refs’ commits, trees, and parents — PASS: frozen `c82eb7c` / `49975e7a54fd594e1b7fc807681fe28611d57864` / `5947abc`; named upstream `67b8aa3` / `62f4456b71234a9d4d4ad9e2aa58cf7fe0de1120` / `bd1011b`.
- Read-only `git cat-file -t` for the two commits, two trees, and two parents — PASS; each object type is correct.
- JSON parsing of corrected `inputs.json`, corrected `source-manifest.json`, and `composition-correction.json` — PASS.
- Recursive field diff against immutable 1857 `inputs.json` and `source-manifest.json` — PASS; exactly four allowed Composition mapping paths changed in each, with no outside-field changes.
- `sha256sum`/byte comparison against immutable 1857 — PASS for unchanged `commands.md`, `selector-map.json`, and `validation.md`.
- Crosswalk assertions — PASS: 100 Python sources, the TypeScript target, 22 route roots/order, five missing route roots plus D73 launcher as `UNKNOWN_MISSING_UPSTREAM_SELECTOR`, and 33 stable source-only files remain unchanged evidence.
- D133 receipt reuse — PASS by exact 1911 author receipt (`receipt.json`, SHA-256 `2510e2ea764c81864b0d92b12cd347b24572134ef250ded2a6461dc64b588113`); no independent renderer was run.

## Boundary and limitations

The historical 1904 tree text had one extra trailing `e` (41 characters).
That error is preserved in the correction record for traceability; the valid
40-character local Git tree object is authoritative. No ref was rewritten.

Full preparation remains **PENDING/UNKNOWN** within the real missing-input
limit: five named-Agent route roots and `tools/p4-d73-pinned-launch.sh` are
absent. No pristine executable gate, zero/PASS inference, or final tuple was
claimed. No tests, lint, typecheck, preflight, core/full/E2E suite, install,
clone, build, ZIP, provider, Store, network, or Git mutation was run.

No Composition product files changed; this review adds evidence artifacts only.
