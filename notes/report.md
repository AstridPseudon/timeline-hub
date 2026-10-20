# Parent media: actual Runtime qualification

Worker: `agt-m2-parent-media-real-proof`. Agent base:
`63f0bec150115a6c12962a597115a40c799d61de`.

Added only `tests/editing_conformance/test_commit_runtime_parent_media.py`
and this report. No production, schema, pin, integration, ledger, or dependency
changes. No Git mutations, push, full suite, daemon, browser, or sockets.

## Result and limits

**30 passed, 4 strict xfailed** against an unmodified archive of actual Runtime
`8609333456b9537339ee1a5dfc7ffd9609242de8`. Neighboring native recipe tests:
**233 passed, 5 existing strict xfailed**. Ruff and whitespace checks passed.

Ordinary existing-film parent birth and literal ordered replacement are proven
through real managed custody and acceptance. Unrestricted qualification remains
blocked by two existing guards, retained as permanent positive strict xfails:

1. A fresh Runtime timeline has `registry: {}`. Parent media birth requires an
   already-authored `registry.assets` object. Both image/video first-film birth
   fail before `accept`, with `media edit requires an authored asset registry`.
   The positive test still expects birth and exact inverse to the bootstrap.
2. The approved pre-cut film contains an incoming transition in occurrence-2.
   Ordinary `clip.delete` scans all occurrences and refuses any transition,
   including this unrelated one. Both image/video replacement tests still
   expect `[music-bed,A,reserved-row,C]`, preserved child revisions, and exact
   inverse. They xfail only on the specific `unsupported_dependency` seam.

The xfails use `strict=True` and a dedicated exception raised only after checking
the exact observed error and unchanged database. Unexpected errors/assertions
fail normally; a repaired seam becomes XPASS and requires removing the mark.
No passing behavior expectation was weakened or rewritten as a refusal.

The passing ordered case explicitly clears the captured unrelated transition
through the normal `clip.set` command first. This creates real accepted history;
it does not alter a historical image or bypass lifecycle/admission. All subsequent
preservation/inverse comparisons use that accepted input boundary. This proves
the supported literal case, not replacement of every existing film.

## What the actual tests prove

- Image/video first parent **visual** birth in the existing film preserves the
  reserved row and asset IDs, literal `at`, `hold`, null `params`, nested opaque
  JSON, nullable image speed, and video `from=2,to=6,hold=4,speed=2` exactly.
- Explicit replacement uses precisely `timeline.assembled-target`,
  `clip.add-media {row,media}` inserted after the target, and `clip.delete`.
  The parent order stays `[music-bed,A,reserved-row,C]`; siblings are not appended
  around the replacement. The ordinary music row, registry entries, playback,
  shot/internal revisions, media pins, and document pins survive.
- Real dry-run changes no database rows. Real acceptance equals the preview.
  Closing/reopening `RuntimeService` reloads the same canonical document.
  Receipt-based inverse, redo, and second inverse restore exact documents/order.
- Exact birth/inverse/redo retries return the original results without executing
  Agent semantics, including an original birth retry after restarting Runtime.
  Changed payload under the birth key refuses with 409 and no writes. A fresh
  request cannot reuse a retired created identity.
- Foreign project media, mismatched variant/object binding, wrong catalog
  fingerprint, stale lifecycle selection, occupied row ID, and occupied registry
  alias refuse before `RequestCommitPort.accept` and leave the full database dump
  unchanged.
- A captured replacement rebased over a later accepted row creation refuses its
  stale membership with `selection_changed`, before acceptance or writes.
- Actual later accepted dependents and exact row ABA (hold A→B→A, entire row
  restored) prevent inverse. The authenticated suffix check reports
  `intervening_write` before the structural dependent check; no acceptance occurs.
- `generation.variant.append`, admitted and settled with its source object as an
  input and `primary_policy=promote`, changes the real primary variant/object.
  The old immutable `(media_id,type,generationId,variantId)` registry tuple,
  explicit old selection/catalog digest, and old media manifest pin remain exact
  through replacement, inverse, and redo. No SQL mutation models this change.
- These requests have no `producer.guard`, producer attempt pin, or authority
  dependency. Runtime's normal `request_pin` returns `None`. Real generation
  settlement grants selected-media custody; it is not an assembler proposal.

## Fixture and authority boundaries

The normal Agent provider is installed through
`load_timeline_commit_provider('astrid')`; every mutation calls actual
`RuntimeService.commit_timeline` with a projects-write credential and the normal
`/v1/projects/.../timelines/film/commit` invocation path.

Managed media uses the existing Runtime generation publication fixtures
`test_generation_publish_v1_settlement._fixture/_effect/_output/_settle`, actual
project CAS objects, generation/variant registration, completed attempts, and
`get_project_media_selection`. Historical source films come exclusively from
the approved committed `schema31/pre-cut80973d3` backup through Runtime's current
`build_film_fixture` and real backup verification/restore. The original historical
backup is unchanged; tests open its duplicate. Baseline installation uses the
normal verified history read.

`RequestCommitPort.selected_media` and `accept` are observed by wrappers which
call their original methods. No prepared provider, fabricated VerifiedMedia,
accepted-history insertion, SQL writes, schema substitution, direct generation
publication, or lifecycle bypass is used. `iterdump` is read-only refusal evidence.

No authentic assembler producer/proposal lifecycle, settled child authority,
`producer.guard` implementation, producer artifact consumption, or requester
outbox path is qualified here. Those retain their separate strict requirements.
The neighboring producer test's existing strict xfail is not a producer pass.

## Schema and pair

Agent edit schema SHA-256 (unchanged):
`65e8e0338110f85c7f9b8f42b0364c9bf55cc414e6af7f26e95a71a68e5cb19a`.

Runtime schema digest:
`sha256:3e5e78d0a689b32c46738455b5f7875999eb7d3da4917a38bd6a9eaaf41d0f3c`.

Runtime `timeline-commit-bundle.json` file SHA-256:
`37f31ffd6ce63f54897cb7880a7c89811e4cfed3125ab0183127d34774a02d32`.

The generated Runtime `EditCommand` still has a generic operation-name pattern
and finite JSON `args`; it has no `clip.add-media` or
`timeline.assembled-target` conditional/typed definition. Consequently the real
`CommitRequest` validator accepts both the new candidate command and the obsolete
scalar spelling. The normal Agent provider's closed operation schema rejects the
obsolete scalar spelling before any media read or acceptance. The tests explicitly
exercise both levels; neither validator nor schema resources are patched.

This is candidate semantic/custody qualification through the existing generic
envelope, **not an official parent command release**. A reviewed full superset
schema freeze and normal Runtime regeneration/pair remain required. This worker
does not replace S2, change an existing public tuple, or compose a successor freeze.
The manager must preserve all concurrent ordinary/producer fields in that union.

## Exact final commands and results

All commands ran from `/home/user/work/wt/agt-m2-parent-media-real-proof`.
The Runtime integration checkout moved during development, so the final run used
a private, **unmodified** `git archive --format=tar` of the exact commit above,
extracted under this worker's scratch directory. Shared dependencies stayed read-only.

```bash
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-parent-media-real-proof/runtime-source PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q --tb=short -rx -p no:cacheprovider -m integration tests/editing_conformance/test_commit_runtime_parent_media.py > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-parent-media-real-proof/actual-tests.log 2>&1
```

Exit 0: **30 passed, 4 xfailed in 76.11s**. All four precise seams are listed
above; no skips. Log retained in the named worker directory.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q --tb=short -p no:cacheprovider tests/editing_conformance/test_recipe_m2_parent_media.py tests/editing_conformance/test_producer_insertion.py tests/editing_conformance/test_recipe_occurrence_media.py tests/editing_conformance/test_occurrence_media_manifest_inverse.py > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-parent-media-real-proof/neighbor-tests.log 2>&1
```

Exit 0: **233 passed, 5 xfailed in 38.73s**. Existing xfails are four parent
auto-placement cases and one producer/requester integration case.

```bash
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check tests/editing_conformance/test_commit_runtime_parent_media.py
git diff --check
```

Both exit 0. No full or live test service request was made; the targeted tests
instantiate RuntimeService directly and need no sockets.

Development runs against the moving Runtime checkout found the missing bootstrap
assets seam, the retired `_binding_descriptor` helper in the older occurrence
fixture, and the global transition guard. The setup was corrected to restore the
current approved pre-cut backup rather than rebuild historical state. Earlier
dependent tests incorrectly required `surviving_dependents`; actual authenticated
suffix checks refuse earlier with `intervening_write`. The final tests prove the
same no-write refusal with the actual accepted records. All final commands above
ran after these test corrections.

## Decisions and next steps

No narrow product fix was applied: missing registry/assets refusal is an existing
explicit passing requirement, and global deletion dependency logic is outside the
allowed parent-module/provider-order scope. Both are reported instead of changing
the settled semantics. The provider order helper itself passes actual acceptance,
restart, inverse, and redo and needs no further change for the literal case.

Manager follow-up: decide the fresh-film assets-container seam and the unrelated
transition deletion seam with their owners, then remove the corresponding strict
xfails after positive acceptance/inverse passes. Compose the official full
superset schema/Runtime pair separately. Qualify authentic assembler proposal,
settled-child fencing, and requester flow separately. No HTTP/browser/App or
full-suite qualification is claimed.
