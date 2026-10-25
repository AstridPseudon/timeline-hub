# F-D86 actual9211 source-only report

## Result

No repository files were changed. The nine primary rejects all converge on Agent’s current V2 historical-reference predicate:

- `astrid/sdk/timeline/validation.py:405-445`
- Exact check: unchanged `elementRef` declaration, clip type, and `_text_reference_basis`
- Basis includes project/timeline identity, text-binding rows, source-shot mapping, and pinned documents
- Runtime `service.py:2518` only wraps the provider rejection

The exact changed field/source snapshot is not present in the 9211 export, so no narrower cure is justified.

## Primary cases

| Family / IDs | Cases | Minimal correction target | Owner |
|---|---|---|---|
| `ownedmove8` 132–137 | `test_owned_move_publish_runtime.py`: parent asset clear, transition clear, trim rebase, split rebase, delete rebase, ambiguous owner/mixed edits | Preserve the exact historical child `elementRef` and authenticated source basis through `_commit_parent_variant` closure initialization and emission. Keep occurrence deletion and parent-only edits unchanged. | Agent producer/caller seam |
| `word11` 99, 101 | `test_rebind_existing_main_descriptor_undo_is_exact`; `test_clear_existing_main_descriptor_and_inverse_are_exact` | Preserve the existing child declaration/source basis while applying the native text-binding operation and restart/inverse path. Do not alter transcript bytes, bindings, or inverse assertions. | Agent fixture/provider source boundary |
| `scalar11` 129 | `test_move_then_scalar_outbox_handoff_reload_and_guarded_inverse` | Preserve the historical child declaration/source basis across outbox retry and scalar follow-up. Do not change scalar fields, opaque values, or numeric scope. | Agent provider/source boundary |

Current callers were inspected:

- Owned move caller uses Runtime’s registered provider, authenticated `revision_closure`, `bundle_from_document`, registered occurrence deletion, and C0 emission in `test_owned_move_publish_runtime.py:39-100`.
- Word tests capture genuine Runtime closures and original transcript bytes before restart/inverse in `test_commit_runtime_text_binding.py:245-367`.
- Scalar fixture setup uses `media.admit`, verified media, current provider, and staged shared placement in `test_commit_runtime_clip_scalar_fields.py:49-139`; the primary later exercises real outbox retry in `test_commit_runtime_scalar.py:22-92`.

## Distinct non-primary failures

- `word11` IDs 96–98: inverse stage materialization differs from authenticated source image. Runtime authfour handback remains owner; no duplicate Agent fix.
- `word11` ID 100: moved-head staged physical input lacks private sequential proof. Runtime auth/physical-boundary owner.
- `word11` IDs 102–103: stale `clip.add v1 does not support on` command shape at `_clip_commands.py:49`; separate Agent caller/command issue, not historical text binding.
- `word11` IDs 104–106: Gate-1 assertion failures; exact source defect is not evidenced.
- `scalar11` IDs 119–121: Runtime parent composition revision lookup failure at `runtime_protocol/service.py:2347`; Runtime admission/closure owner.
- `scalar11` IDs 122–128: authenticated inverse/fork materialization mismatches. Runtime authfour remains owner; Agent is only a conditional follow-up if future evidence proves malformed producer effects.
- `ownedmove8` IDs 130–131: assertion failures after source-reviewed setup; functional cause remains unverified.

The D23 deferred boundary does not apply to the nine primary cases: these are legacy `elementRef` historical references, not child-word-anchor `word_anchors`.

## Provenance

- `ownedmove8`: source commit `73998ac446ea2e4bceed1e0df2c5e2c68c558e82`; receipt `6386c700ee56264aebe12da4558ac74dda0d60ca`; owner report `handoff-agt-F-review-batchD-0135-verdictowned.md`.
- `word11`: source commit `32619f8656d0ab481c1486ee6cea23969bd7a788`; receipt `7c94e9d2d753fc8f082877ef3de50b3a55a18689`; owner reports `rt-D86-word11-review-0022-report.md` and `rt-D86-scalar-word-review-0110.md`.
- `scalar11`: source commit `721189cbc8aeab7fed64643ca625e505e52b8d54`; receipt `1793b8e900b5c84a405fb93d44f1cd252fdb8080`; owner report `verdictscalar.md`.
- Frozen R4 SDK lacks the current V2 validation/source-basis predicate, so it cannot establish a direct historical implementation comparison.
- An older word report identified a `_copy_manifest` pin-retention seam, but current `commit.py:366-376` explicitly appends captured pinned documents; that report alone is not proof of a present defect.

## Verification

Commands run:

- AST parse and in-memory compile of 9 traced source/test files: **passed**
- Scoped Ruff with `/home/user/work/venv-agent/bin/python -m ruff check --no-cache ...`: **All checks passed**
- Scoped mypy with `/home/user/work/venv-agent/bin/python -m mypy --no-incremental ...`: **Success: no issues found**
- `git diff --check`: **passed**
- `git status --short`: **clean**

No pytest, collection, fixture execution, services, browsers, probes, or full suites were run per the source-only requirement. Functional behavior closure remains unverified.

Required `DONE` marker and commit message were created.