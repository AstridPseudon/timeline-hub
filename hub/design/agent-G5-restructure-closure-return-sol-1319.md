# G5 restructure closure return — bounded caller repair, successor blocked

**G5 DRAFT ONLY / P1 NO-GO.** The original exact-current-closure mismatch is
causally explained and repaired at the permitted `publish.py` callsite. The
unchanged guard now passes with fully equal authenticated bundles. An actual
normal public publish attempt then exposes a separate Agent native-helper pin
shape incompatibility before the restructure write. **Not ready for the Runtime
inverse observer.** Original 503 cause remains unknown; no Runtime bug inferred.

## Source and immutable body

- Parent Agent commit: `77ab3908fbf827fd591f077a3ef00664c073409d`.
- Parent tree: `1ed8f102bf0ab10f7e62c0fc6e85c2f5b545af0c`.
- Successor source tree: `5fecdabcb0eff53a9329779073caf77772116f74`.
- Successor commit SHA: pending harness commit after worker exit. No Git writes
  were performed; this report cannot truthfully supply an uncreated commit SHA.
- Runtime: `/home/user/work/wt/rt-pin-3b926efa`, commit
  `3b926efab2eed122d374540baee297d4cdcec62a`, tree
  `b794170504544b259781e50d7ca4d61b6729e67c`.
- Original whole inverse test source SHA-256:
  `c2711a2d10765828694ee1906d75bdf62a91ed6ac0bbef8e4cb0d823e48ec30d`.
  Hash input is the complete function source, from its `def` line through its
  final assertion, including terminal newline. It is byte-identical to the
  parent commit. AST hash (attributes excluded):
  `173f444428cca18bc6b8b3a3c21fe9b111b09049d7ae5f1d5dd880a4f38a18a7`.

Only `astrid/sdk/timeline/publish.py` and
`tests/sdk/test_timeline_restructure_guarded_runtime.py` changed. The inherited
fixture, core helper, native provider, inverse/rebase, Runtime, pins, generated
files, schema, contract and shared dependencies are untouched.

## Report-all causal capture

Read the supplied PLAN, Runtime1305 handoff, Agent1250 report, and independent1305
review before editing. The fixture keeps the single inherited RuntimeService
owner and its existing teardown. Public `RemoteTimelines.open_bundle`, resolver,
inspection and history remain production methods, with generated-boundary
forwarding to that service. No private source/cache is supplied by the fixture.

The first preflight used the same accepted `inverse-name` naming edit as the
original journey, then called the actual normal
`Checkout.open(...).publish(..., restructure=True)` path. A read-only Python trace
captured the complete `local`, session `base`, and outbox `state` immediately
before the real equality guard. The public-reader proxy forwarded its complete
arguments and result unchanged. The capture also includes detached raw and
`document()` projections, full history, accepted naming reply/receipt/canonical
document, digests, and all source mappings.

A recursive comparison of the complete nested guard bundles found **exactly two
missing local paths**, with no differing existing values:

| Path | Detached local | Session base |
| --- | --- | --- |
| `/base_parent/publication_id` | absent | authenticated receipt ID |
| `/source_mapping/_runtime_document` | absent | verified full canonical closure |

All authored parent/shot/internal payloads, membership, source maps, base
payloads and content digests were equal. Detached raw bundle equals its
`document()` projection in this fixture: the failure was not caused by derived
projection, migration, flattening, different scope, or a different snapshot.
The session canonical document exactly equals the accepted naming receipt's
canonical document.

The initial failing pin was:

```json
{"revision_id":"authoring-parent-revision-09d0062384631ddd43143024dd750b5cb90d65bed764b5cdf0fc8f84536aa7ca","publication_id":"txn-ee5febc3c91647458a70349ba8044c78","content_digest":"sha256:18bf4a717fc18d5e29abaa3d1a1a9684fa2179b28fdef22ccef447f9f76d469d"}
```

Accepted naming document digest:
`sha256:a8caae6d156eb63a72aa74d763b863a5f63e240e3b182b5928a859d14a263810`.
Actual detached public call: `open_bundle(project, "t", revision_id=None)` with
no publication pair. Actual session call: the same project/timeline, with the
above revision and publication IDs. The complete public argument sequence is
retained in the raw capture, without historical-to-current substitution.

Full machine-local artifacts, relative to this worker's `private-tmp/` directory:

- `red.log` and `red/test_fixture_restructure_publi0/closure-preflight.json`:
  original normal public call fails at the exact-current-closure guard.
- `green.log` and `green/test_fixture_restructure_publi0/closure-preflight.json`:
  unrestricted normal public call after hydration passes that guard, then fails
  at the separate native helper described below. Full nested guard difference
  list is empty. Naming canonical document still equals verified source.
- `closure-differences.json`: recursive red/green differences, exact pairs,
  document digests and public argument sequences.
- `final2.log` and `final2/test_fixture_restructure_publi0/closure-preflight.json`:
  final read-only preflight passes the actual equality guard and stops before
  candidate/command execution. It additionally records generated listing,
  inspection options (including revision/limit), and history arguments.

These captures live outside the worktree; no large capture belongs in design/.
The final capture's exact pair is
`authoring-parent-revision-798cbbc493b7215998f4624d1a9b6b4e5330348e6cc6141e596a93ce7a5a4986` /
`txn-1623216e07054e64923b405a9d4dfae3`, and document digest is
`sha256:646fce8bb3661c184444e4e2246b7674eacd713c6b5ef3e73516e07465a12397`.
Each invocation builds its own genuinely scoped service fixture, hence distinct
project IDs, receipt IDs and content-derived revision IDs across invocations.

## Bounded repair and proof limits

At `_commit_restructure`'s local hydration callsite, the existing verified public
loader reads the detached caller's **original revision**, paired with its own
publication ID when present, otherwise the session's publication ID. The reader
must validate that exact pair. It does not substitute the current revision for
a historical one. Fetched base-pin and source-map metadata fill missing fields;
existing local values take precedence, preserving wrong digests/pins and unknown
provenance for refusal. No authored content or request/reply is reconstructed.
The equality guard itself is unchanged, including exact `base_parent` equality
and shot-membership equality. No fields are deleted to make comparisons pass.

The final smoke calls the real normal public publish entry, observes the actual
guard, and raises a test-only sentinel at the following candidate-assignment
line. It does not replace any executor or modify a guard result. This explicitly
bounds the smoke to read-only closure preflight, with full `local == base`,
canonical/receipt equality, and unchanged write-call list, complete history,
canonical document and SQL dump. It grants no accepted-restructure/undo credit.
The preceding unrestricted attempt remains recorded as a failure, not hidden.

Four caller negatives assert the specific refusal seam and no-write invariants:
wrong local content digest; wrong original publication; a valid detached base
followed by a real accepted concurrent head advance; and missing timeline scope.
The historical case keeps the original valid checkout rather than constructing
an arbitrary old snapshot. The authority smoke also opens an exact historical
receipt pair, proves it is not head, and refuses wrong pair, missing scope, and
a corrupted digest from an immutable read. Complete history, canonical readback,
head and SQL dump remain unchanged.

Full v2 scope/base pair/commands/select/args/label/steps/merge/reads/key/dry-run/
source/rationale/group ID and replies/data/receipt/canonical/records/bindings/
effects/dependencies/history/undo_steps/accepted/merged/preview/would_status/
structured conflict/invalid are untouched. Existing original assertions remain
byte-identical. The new smoke does not claim contract coverage for unrun replies.

## New blocker — outside allowed scope

The unrestricted post-hydration setup attempt reaches
`astrid/sdk/timeline/native_restructure.py:17-22` through the existing
`commands.execute(candidate, ...)` in `publish.py`. Its guard compares:

```python
{key: document['parent_revision'][key] for key in ('revision_id', 'content_digest')}
!= bundle['base_parent']
```

The left side has exactly two fields. The authenticated public reader's base pin
has those same values **plus `publication_id`**, so equality is necessarily false.
The normal call raises `CommandError(kind='history_unavailable',
'restructure requires the authenticated current closure')` before submitting a
restructure commit. This is source-backed Agent native-helper evidence, not
Runtime semantic evidence or an explanation of the older inverse 503.

The brief forbids core helper edits, guard waivers, removing provenance to make
a comparison match, or forged canonical images. Therefore this worker did not
remove the publication field, alter the canonical image, change that guard, or
rerun the original undo body. A settled assumption that callsite hydration alone
can make the current public path ready is contradicted by this new evidence.
The closure repair is reviewable, but the successor remains **BLOCKED** for the
inverse observer pending a separately scoped Agent native-boundary decision.

## Commands and results

All pytest runs used:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa /home/user/work/venv-agent/bin/python -m pytest
```

The precise suffixes were:

```text
-q -o addopts= -p no:cacheprovider --timeout=30 --basetemp=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-restructure-closure-return-sol-1319/private-tmp/red tests/sdk/test_timeline_restructure_guarded_runtime.py::test_fixture_restructure_public_call_hydrates_exact_current_closure
=> 1 failed in 13.36s: original equality guard (expected causal RED).

-q -o addopts= -p no:cacheprovider --timeout=30 --basetemp=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-restructure-closure-return-sol-1319/private-tmp/green -k 'fixture_' tests/sdk/test_timeline_restructure_guarded_runtime.py
=> 1 failed, 1 passed, 1 deselected in 23.63s: equality repaired; separate native guard blocker captured.

-q -o addopts= -o tmp_path_retention_policy=all -p no:cacheprovider --timeout=30 --basetemp=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-restructure-closure-return-sol-1319/private-tmp/final -k 'fixture_' tests/sdk/test_timeline_restructure_guarded_runtime.py
=> 6 passed, 1 deselected in 81.70s (initial bounded smoke/negative controls).

-q -o addopts= -o tmp_path_retention_policy=all -p no:cacheprovider --timeout=30 --basetemp=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-restructure-closure-return-sol-1319/private-tmp/final2 -k 'fixture_' tests/sdk/test_timeline_restructure_guarded_runtime.py
=> 6 passed, 1 deselected in 41.61s (final source, precise negative-refusal assertions).

--collect-only -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_restructure_guarded_runtime.py
=> 7 tests collected.

/home/user/work/venv-agent/bin/ruff check --no-cache tests/sdk/test_timeline_restructure_guarded_runtime.py
=> All checks passed!

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa /home/user/work/venv-agent/bin/python -m mypy --cache-dir=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-restructure-closure-return-sol-1319/private-tmp/mypy-test tests/sdk/test_timeline_restructure_guarded_runtime.py
=> Success: no issues found in 1 source file.

git diff --check
=> PASS.
```

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-restructure-closure-return-sol-1319` is the absolute worker directory named below; there are no shell
placeholders in the actual recorded tool invocations.

Scoped product Ruff (`ruff check --no-cache --output-format=json publish.py`)
finds the same two baseline findings, I001 at line 2 and E741 at old line 511 /
new line 521. Scoped product Mypy finds the same 19 existing mixin `attr-defined`
errors. Both tools were also run on the exact parent file copied read-only into
the private scratch directory; ordered diagnostic code/messages are identical.
Comparison artifacts are `baseline-ruff.json`, `current-ruff.json`,
`baseline-mypy.log`, and `current-mypy.log`. These product files are not claimed
clean. No diagnostics occur in the new hydration lines.

No full suite, localhost/browser/socket suite, original inverse/503 body, P1/P4,
HTTP/native14/58, D17, daemon, dependency installation or Git mutation was run.
The existing Runtime observer retains sole ownership of the next instrumented
inverse diagnosis, after actual readiness is established.

## Next step

Independently review this bounded caller hydration and unchanged-body evidence.
Have the orchestrator scope the newly proven native-helper pin-shape mismatch
without relaxing source authority. Keep the Runtime observer waiting; do not
spend its one next invocation on this known pre-submission refusal. No merge.
