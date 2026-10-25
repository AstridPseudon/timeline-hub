# D116 current17 shared-source applicability

Verdict: **PASS_SOURCE_APPLICABILITY / NOTRUN FUNCTIONALLY**.

This is a read-only review at Agent base `20177e66564f9f91735ed1a11bac821682d60edf`.
The exact-safe map contains 27 rows; its first ten D107-approved rows were excluded.
All remaining 17 selectors were matched to exactly one AST function at this base:
native checkout 4, native frontends 3, owned move 6, parent-track 3, scalar 1.

## Current producer seam

`current_word_baseline_fixture.retained` is only an alias for
`native_word_anchor_fixture.current_retained`. The genuine route is
`native_word_anchor_fixture.seed(current_form=True)` → Runtime-ingested media and
transcript → registered Agent commit provider → authenticated `clip.anchor` with
the exact transcript pin and word IDs → retain-and-clear. It is a real public
provider route, and the setup is source-valid. It targets `parent/clip:card` with a
single current voice source; it does not produce the historical `m1.film`
`music-bed`/`music-other` parent and occurrence topology.

Therefore the smallest safe seam is the current seed's authenticated source,
document pin, and provider-backed anchor/clear sequence. It can be a prerequisite
for future selector-specific companions, but it is not a blanket transplant and
does not itself qualify any of the 17 cases.

The retained historical route remains untouched: Runtime precut-v31 intentionally
uses an unpinned authored word input. No fixture, manifest, archive, authority,
pin, generated file, product body, or original test was changed.

## Exact compatibility result

Every retained purpose remains conserved, but every row is **seam-only** rather
than selector-complete. The precise missing evidence is in
`current17-source-map.json`. In summary:

- 1143/1147 need a current authenticated binding on `music-bed` plus the exact
  disjoint/touching peer variants.
- 1152 needs the current target plus opaque parameter and commands-file ingress;
  1159 needs a current Gate3 occurrence-free/text-card topology.
- 1165/1171/1180 need the authenticated target and their NativeSheet pending,
  disjoint, or touching-peer paths.
- 2913/2923/2927/2940/2958/2996 need their distinct owned parent variants,
  including transition, trim numerics, split source window/speed,
  occurrence-free, or duplicate-owner topology.
- 3649/3651/3653/3654 need grouped parent-track, label CLI/suffix, and scalar
  occurrence-parameter topology respectively.

These are setup/applicability gaps, not reasons to change predicates. The exact
caller for any future companion must submit the approved v2 body with base pair,
commands, label, steps/patches, merge, reads, idempotency key, dry-run, source,
rationale, and group_id through a genuine registered provider; replies and
conflicts remain the contract's accepted/merged/conflict/invalid forms.

## Checks

All commands were read-only with respect to the repository and used private
temporary caches.

- AST parse and exact function matching: **17/17 PASS**.
- `PYTHONPYCACHEPREFIX=/tmp/w-afd8f68440/app-D116-current17-source-1540/pycache /home/user/work/venv-agent/bin/python -m py_compile` on the seven mapped files: **PASS**.
- `/home/user/work/venv-agent/bin/ruff check` on the same seven files: **PASS** (`All checks passed!`).
- `/home/user/work/venv-agent/bin/mypy --follow-imports=skip --cache-dir /tmp/w-afd8f68440/app-D116-current17-source-1540/mypy-cache` on the same seven files: **PASS**, no issues in 7 source files.
- `git diff --check`: **PASS**.
- `git status --porcelain=v1`: **empty**.
- Tests, pytest, Runtime service, sockets, browser, node execution, original replay, and full/family suites: **NOT RUN by scope**.

The first compile attempt was unable to create the harness `tmpdir` because it is
a pointer file, not a directory; no repository or pointer file was changed. The
retry used its declared `/tmp/w-afd8f68440` target and passed.

## Next step

Keep all 17 original selectors and the historical archive read unchanged. A
future source-only companion may reuse only the authenticated current seed after
its sample gate, then must add selector-specific current setup and preserve every
original predicate, input, step, read grouping, and public caller route. Functional
execution of every companion is still required before any retirement or behavior
claim.
