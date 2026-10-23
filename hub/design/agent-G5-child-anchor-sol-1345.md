# G5 child anchor diagnosis — BLOCKED, draft only

Worker: `agt-G5-child-anchor-sol-1345`. Agent base remains
`74b92b2a903ff988489b6dfaa2add01e848bdb1a`. No product, test, schema, generated,
pin, contract, dependency or Git-state changes. All thirteen original function
ASTs in `test_timeline_helper_capture.py` are unchanged. NO MERGE / P1 NO-GO.

## Finding and scope question

This is a missing child-target capture/adapter contract, rather than a supported
target binding lost by the emitter. The pure timing kernel already supports
child `WordBinding.target` tuples. The old mutable helper also supports child
word moments. Those facts do **not** make the registered native anchor carrier
accept a child target or authorize selecting a new exact word binding from a
legacy text declaration.

**Question for the orchestrator:** Does G5 authorize extending the existing
`clip.anchor` target contract from parent/raw clips to an explicitly selected
child occurrence, together with its authenticated ownership, captured source,
compiler and inverse adapters? That requires changing the current command
schema's explicit parent-only selector, which this brief forbids. Alternatively,
if `doc.patch` is intended as the carrier, what existing, authorized caller input
supplies the child target's exact transcript pin and stable word choice before
the unchanged raw-text setup commit? Generic physical addressing supplies no
such semantic choice. Automatically discovering/creating a transcript or
reselecting a word from `on='"second"'` would introduce the unapproved relational
capture behavior. No new API, schema, choice or validator exemption was invented.

The precise old/new boundary is:

| Path | Existing support | Missing migration input/boundary |
| --- | --- | --- |
| Old `Clip.nudge` → `Clip.on` → `retime` | Child cut moments, text lookup, offset preservation and cut end rules | No persisted exact native child word choice from that lookup |
| Frozen R4 compiler | Detached checkout compatibility calls and mutable evaluator state; separate frozen transcript dependency mechanism | Not the current `media.transcript/v1` native `clip.anchor` target contract |
| Current pure kernel | Exact child target/source owner tuples, immutable captures, exact pin/word checks | Requires caller-supplied `WordBinding`; never discovers it |
| Registered current `clip.anchor` | Exact transcript choice and source binding on a parent/raw target | Child selector explicitly rejected by schema and handler |
| Current `doc.patch`/emitter | Lossless physical child addressing and raw values | Does not select words, mint authority or synthesize semantic commands |

This refines return1335's suggested “physical-alias handoff”: parent carrier and
child target are different physical sites. There is no same-site alias to repair.
The old behavior is real; the current native carrier's target scope is narrower.
This finding is not a proposal to cut G5 or classify the promised writer as V4.

## Exact source trace

- `model.py:259,358` and `reflow.py:352,562`: `nudge` adds a Moment offset,
  `on` places and retimes, and the mutable lookup resolves against checkout
  words. It does not record a current exact `DocumentPin`/stable-ID child choice.
- Frozen R4 `compiler.py:385,463`: compilation uses a detached checkout and
  compatibility evaluator methods. Frozen `transcript_binding.py` requires an
  independently admitted frozen dependency, snapshot and explicit occurrence;
  it cannot be transplanted into today's v1 transcript/pin format. These frozen
  sources were read with `git show`, never checked out.
- `compiler.py:54,128`, `tests/sdk/test_timing_compiler.py:24,74`: the present
  pure kernel supports an exact child tuple, but its tests explicitly supply
  the binding. Kernel capability is not a frontend binding capture contract.
- `schema/edit-command.schema.json:1756,1770`: the `clip.anchor` branch requires
  `select` matching `^parent/clip:(?!.*::)[^/]+$`.
- `native_checkout.py:348,357`: attached anchor capture holds non-parent targets.
- `native_word_anchor.py:48,131,162,230,284,346`: authored enumeration is parent
  only; both binding adapters construct a parent target; declaration rejects
  non-parent selectors; compilation explicitly refuses child `word_anchors`.
- `_commit_timing_validation.py:192,202,479,483`: child legacy words cannot gain
  the retained-declaration exemption, and explicit child typed anchors are
  refused. Parent typed choices alone are extracted into bindings. Removing
  just this guard would leave the missing binding and break D12 causality.
- `journal.py:113,223,241` captures operation-time reads, replays the old helper,
  and emits structural patches. `emitter.py` expressly avoids guessing semantic
  commands. Neither drops an already captured child anchor: none reaches them.
- Runtime859 contract C0c closure identity/addressing preserves exact physical
  images, prevents broadcast and requires a fork for occurrence-local shared
  ownership. It does not widen a registered operation's semantic target scope.

## Authentic capture and physical mapping

The diagnostic hook only observes the existing genuine capture test and calls
the existing native capture on its explicit child selector. It changes no test
body, fixture topology, command execution result or assertion. The complete
preflight was written before the original second positive ran once.

Publicly created/read transcript capture in this run:

```text
project: af4f4b3d2f0c44f7ba809751b924e543
source: occurrence:occ-film/clip:vo2
document: transcript:6b6af9247fb69bcf5ceb61e6fac624c426f4e3dbb10021ee8be5df489a287900
version: 1
digest: sha256:f01e8e5776c7bda992a54db9022576facda56b1e0e73528b06b96dbcf23c11f2
word: word:0759e1ca31a50b4c2b49f59e406ca8ae4b6be00f6e864255875ed7c00bf33934
compiled source owner: (occ-film, film, vo2)
compiled target owner: (parent, "", anchor-carrier)
desired target owner: (occ-film, film, inside), cut c2, on '"second"', at 4.6
source and desired target root:
  internal-revision:authoring-timeline-revision-22bdaf9fa7d4a54b744cf552e241655d37ec5d341f5c612d1b56eeb23dd379da
root digest: sha256:193129434ea3e4eed48ff461d0f06e22e18ac1923ce7ff02a0ce007a0281896a
source path: [clips, id:vo2]
desired target path: [clips, id:inside]
captured target: parent / [config, clips, id:anchor-carrier]
```

The genuine native record contains the exact `anchor.transcript` dependency and
`anchor.source` binding. The existing adapter produces the parent target above.
Using the explicit child selector with that genuine source choice fails at the
schema pattern before native capture; its input stays byte-equivalent. No
parent binding was retargeted or attached to the child.

The retained positive uses a **separate** function-scoped Runtime project,
`bd69f5cef3e44108b4023ab9cd4ff8ac`. Its unchanged setup does not invoke the genuine
capture helper or create a transcript. The prior test's exact source pin is not
authority in this project. Its actual request is preserved separately; no
cross-test pin transfer is claimed. It contains one `doc.patch` setup request
and receives an invalid failure before nudge/save/restart or peer publication.

## Commands and results

Acceptance, exactly as executed (diagnostic plugin adds observation only):

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/tmp/w-05eb0f4c3b:/home/user/work/wt/rt-pin-8592822f ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8592822f /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -p preflight_capture tests/sdk/test_timeline_helper_capture.py -k 'genuine_anchor or missing_or_forged_anchor or (cut_nudge_restart_merges_other_cut and second)' --basetemp=/tmp/w-05eb0f4c3b/acceptance
```

**3 passed, 1 failed, 21 deselected in 24.58s**, exit 1. Failure is the unchanged
`test_cut_nudge_restart_merges_other_cut["second"]` at `Cut setup`:
`candidate.timing: missing exact word binding for ('occ-film', 'film', 'inside').on`.
The three passing cases verify genuine scope/base/pin/source capture and missing
pin/forged word no-write refusal. The positive was run once, after the completed
preflight, without any changed assertion. This is RED evidence, not GREEN.

Focused source/physical-owner/pure-validator guards:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-8592822f ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8592822f /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timing_compiler.py::test_binding_refusals_are_atomic_and_never_repair_by_same_text tests/sdk/test_timing_compiler.py::test_exact_binding_uses_selected_duplicate_word_and_preserves_authored_commands_and_clears tests/sdk/test_timing_compiler.py::test_compilation_has_no_io_random_clock_renderer_or_mutable_checkout_dependency tests/editing_conformance/test_commit_timing_validation.py::test_cut_identity_follows_physical_child_images_and_keeps_occurrences_local tests/editing_conformance/test_commit_timing_validation.py::test_validation_has_no_io_or_mutable_checkout_dependency tests/editing_conformance/test_commit_boundaries_d12.py::test_legacy_map_retention_never_exempts_a_changed_timing_basis tests/sdk/test_capture_closure_source.py::test_saved_closure_scope_and_revision_mismatch_refuse_without_head_fallback --basetemp=/tmp/w-05eb0f4c3b/guards
```

**29 passed in 3.43s**, exit 0. Includes stale/missing/ambiguous/forged source
inputs, exact selected child bindings, unknown/null preservation, foreign scope,
revision mismatch, physical cut ownership and no mutable/IO validator dependency.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-8592822f ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8592822f /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_commit_v2_validation.py::test_production_validation_refuses_all_timing_probes tests/editing_conformance/test_commit_timing_validation.py::test_child_declarations_are_not_filtered_and_valid_relations_are_resolved --basetemp=/tmp/w-05eb0f4c3b/declaration-guards
```

**12 passed in 1.46s**, exit 0. Newly written invalid child/parent timing remains
strict, and child declarations cannot be hidden from validation.

Static/integrity commands:

```sh
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-05eb0f4c3b/ruff /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-05eb0f4c3b/mypy /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
/home/user/work/venv-agent/bin/ruff check --no-cache tests/sdk/test_timeline_helper_capture.py
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
git status --short
```

All exit 0: Ruff **2149/2149**, private mypy **1912/1912**, scoped test Ruff
passes, vendor lock and artifact manifest current, diff clean, worktree clean.
Tracked source hashes and AST comparison are retained. No diagnostic identities
can be added/removed by this task because there is no source change; a separate
raw baseline diagnostic multiset rerun was unnecessary and is not claimed.

No full25/full suite, moved-head retry, HTTP/browser/socket suite, native14/58,
D17/V454, P1/P4 or Runtime edit was performed. Shared dependencies were read only;
all tool caches were private. No deletions, Git writes or daemons.

## Durable packet and next step

Flat packet: `design/agent-G5-child-anchor-sol-1345-packet.json` (72,542 bytes).
SHA-256: `b07035a8594e0240c6e05c287eb7d6f83bb4afe0527833f6c992553a1f3f1726`.
It embeds exact capture/binding/physical maps, unmodified second-positive request,
observed failure and module origins, plus hashes for every evidence file.
Full logs, frozen source reads, AST/source integrity hashes and observer source
are in `ORCH/workers/agt-G5-child-anchor-sol-1345/evidence/`.

All observed request fields, command/step patches and reads, idempotency keys,
raw values, nulls and absences are retained verbatim. No accepted/merged reply
exists for this failed setup, and none is fabricated. The fixture's successful
reply array is empty for that call; the invalid client failure is retained in
the traceback. No downstream history/undo/preview or anchored-helper success is
claimed. Those remain to qualify after the contract/capture scope is settled.

Return the scope question above to the contract owner. If the explicit child
capture path is authorized, qualify it against this same physical child target,
then restore the requested positive and all no-write controls without changing
its topology or weakening the original behavior assertion. Runtime859 source
authority is not the blocker. Runtime R1 moved-head peer1342 remains independent.
