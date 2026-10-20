# M2 popup native contract — BLOCKED at the shared recipe

Worker: agt-m2-popup-media. Agent base: `5b51b936` on
`tl/agt-m2-popup-media`. This is a blocker handoff, **not an App-consumable
command publication**. The task explicitly requires stopping if a foundational
contract is missing. PLAN 4.1 and the Agent INBOX 2026-10-20 00:05 decision remain
unchanged; registry policy is create-or-require, placement is separate, and all
M2 integration merges remain held pending the PLAN M1 record.

## Publication status

| Artifact | Exact status |
| --- | --- |
| Occurrence ADD/SWAP wire operations and parameter schemas | Not published |
| Capture exports from native_occurrence_media_commands.py | Not published; that product file is not added |
| App command args / authoritative recorder goldens | Not published; App must not invent either |
| Native feasibility reproducer | `/home/user/work/wt/agt-m2-popup-media/tests/editing_conformance/test_occurrence_media_manifest_inverse.py` |
| Runtime/provider positive acceptance | Not qualified; stopped at the converter blocker |

The reproducer's `test.popup-media` opcode is installed only by its pytest
fixture. It is **not** a product operation, capture API, golden or replacement
provider. Its detached hashes are unit data, not claims of Runtime provenance.

## Foundational counterexample

At `/home/user/work/wt/agt-m2-popup-media/astrid/sdk/timeline/commit.py:221-225`,
`document_from_bundle` unions every source-document media pin into the compiled
manifest. Source pins must be retained because they can be consumed by immutable
sources even when no clip selects them.

Both popup operations introduce a new media dependency when their binding was
absent. A native recorder can atomically write that registry binding, add the
reserved child (ADD) or change the existing child asset (SWAP), and reverse all
those authored writes. After compilation and reopening, however, the source
document is the accepted document containing the new media pin. Undo retains
that pin even after the registry key and its last consumer disappear. Supplying
the original authenticated source bundle does not solve this: the manifest
union still retains the pin, and historical revision reuse requires exact
manifest equality (`commit.py:235-238`).

The permanent repro uses rational 30000/1001 fps, a nonzero occurrence placement,
literal image timing, shared source shot with independent occurrence owners,
opaque/null data, and a registry initially lacking the new binding. There is no
nontranslation map or source window involved. Actual native recorder writes
drive the probe. It demonstrates:

* Detached deterministic replay and authored inverse succeed.
* Parent state and the sibling occurrence remain unchanged.
* Compiled/reloaded inverse restores the original parent payload and exact
  shot/internal images.
* Exact full-document restoration fails: media manifest retains the new pin,
  and `parent-1` becomes a different `authoring-parent-revision-*` identity.
* Ordinary roundtrip must continue retaining unselected source media pins; a
  global prune would lose existing behavior.

Both exact-equality expectations remain intact under `xfail(strict=True)`, with
a comment naming PLAN 4.1 / bundle2 restoration. They fail normally with
`--runxfail`; no existing passing expectation was changed.

The previous parent-only existing-slot proof does not cover this: its new media
pin was already present in the original manifest. Preseeding the popup's new pin
would conceal the create-or-require case. A command-local manifest override,
blanket prune or provider schema bypass is not supplied here.

## Existing ABI and source checked

* Agent parent swap/provider proof:
  `tl/agt-m2-media-real-proof`,
  `9ebd87afca97382e51c060fa2ca018c43f09f8bd`.
  Read `astrid/sdk/timeline/native_media_commands.py` and
  `tests/editing_conformance/test_commit_runtime_media_swap.py` with `git show`.
  Its 24 prior REAL tests were inspected, not rerun or claimed as popup evidence.
* App immutable selection read:
  `3368b73fed19a37a4b17d6a8b2ad95a2ae0bebde`,
  `src/integrations/runtime/dataProvider.ts`, `getProjectMediaSelection`.
  Exact selection is `(asset, generation_id, variant_id, object_id,
  catalog_digest)`. Reuse ABI 1 `selected_media(MediaSelection) -> VerifiedMedia`;
  do not invent intrinsic media metadata or another provider method/schema.
* Popup source inspected in `/home/user/work/app`:
  `src/tools/travel-between-images/components/shotTimelineDataProvider.ts`,
  especially `createCanonicalTimeline` and the existing compatibility writer;
  `src/tools/video-editor/data/shotCompositionProjection.ts`, especially
  `projectClip`. Display `${occurrenceId}:${clipId}` is not the raw child ID.
  Projected `at` includes occurrence start; a future capture must explicitly
  retain raw child-relative timing rather than copying projected coordinates.
* Ownership requirements: `design/app-writers.md` row 5 and
  `design/app-popup-command-handoff.md`; decision: Agent INBOX 00:05.

## Required next step and unsupported scope

Agent recipe owner should supply a guarded, recorded way to reverse media
manifest additions across reload while preserving retained immutable source
pins and newer dependencies. Keep the exact-equality reproducer and add
later-reference/ABA/redo acceptance coverage to that shared fix. Then resume
this bounded popup slice and publish actual capture exports, args and goldens;
prove the Runtime/provider path using real media selection fixtures before App
consumes it. No integration merge request is made.

Until that happens **all occurrence media ADD/SWAP captures are unavailable**.
Future bounded support must explicitly refuse parent/display selectors, missing
occurrence or immutable closure pins, wrong raw child owner/track, ambiguous
membership, registry collisions, missing/mismatched old/new media tuples,
implicit shared edits, unsupported source/timing maps and out-of-occurrence
intervals. Clear, shared editing, placement, relational `timeline_frame` /
`metadata.end_frame`, standalone registry upsert, new provider I/O, ABI/schema
expansion and fallback whole-document publication are not authorized substitutes.

## Verification

From `/home/user/work/wt/agt-m2-popup-media`:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_occurrence_media_manifest_inverse.py tests/sdk/test_timeline_commit_provider_document.py tests/editing_conformance/test_recorded_graph_roots.py
```

**47 passed, 2 xfailed**, 1.92s, exit 0. Both expected failures are the newly
documented exact document restoration requirement (ADD and SWAP).

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_occurrence_media_manifest_inverse.py --runxfail -k compiled_popup_inverse
```

**2 failed, 3 deselected**, 0.55s, exit 1: intentional blocker reproduction.

`/home/user/work/venv-agent/bin/ruff check tests/editing_conformance/test_occurrence_media_manifest_inverse.py`
and `git diff --check`: passed. No full suite, install, sockets, browser,
Runtime/provider acceptance, merge or push was run.
