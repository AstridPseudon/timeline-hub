# D115 command-output projection ownership review

Disposition: **CONFIRMED Runtime seam**. No Runtime, Agent, test-body, collector, generated, pin, or authority change was made.

## Basis

- Runtime base is `tl/integration` at `369ffa7c00bd3d45c610fac7651ff79e7a283a1a` (tree `9bf331d68df8c966e8927a3f083ba03687803c99`).
- Agent producer candidate is `82b6d00d7fcca643c6eaf3246028d9a20f96252a` (tree `019ae9944d5f445776bd19c7d0c441190955c1a3`), held as instructed.
- The authentic flat pairing is `handoff-agt-F-D118-peer-inputs-1020-producer-pairing.json`, SHA-256 `1b2a1f80e3669d2b54735e16b29b217ad0629cd9155799cf9daf6222cb079fe0`.
- That pairing names the genuine case: exact sealed P1 predecessor input; the consuming `clip.set-element`/`clip.set` path admits P2; final parent payload and content digest stay equal while the document manifest gains P2 and the deterministic parent revision changes.

## Source trace and ownership

1. Agent hydration calls the authenticated Runtime source caller (`commit.py:442-525`), records verified captures, and sets `_copy_manifest` from the sealed Runtime document. `CommitPatch.after` (`_commit_patch.py:457-470`) adds a verified source only after the consuming command.
2. Agent `document_from_bundle` (`commit.py:366-419`) derives the manifest and parent revision from `{parent payload, manifest}`. Therefore a manifest-only source consumption legitimately changes the parent revision while leaving the payload digest unchanged. The candidate's preserved-input change is upstream of this boundary and is held.
3. Runtime's canonical caller is `service.py:2447-2525` → coordinator provider execution (`timeline_commit_execution.py:222-275`) → request port (`timeline_commit_port.py:665-675`) → `validate_sequential_capture` and `timeline_commit_auth.validate` (`timeline_commit_store.py:1459-1505`). Initial input authentication is retained at `timeline_commit_auth.py:2538-2545`.
4. Runtime `validate` advances a local manifest from command dependencies (`timeline_commit_auth.py:2813-2845`) and computes the consumed-input parent identity with `_authoring_parent_identity` (`:1791-1805`).
5. The proven seam is `command_output` (`timeline_commit_auth.py:2129-2258`): it projects writes only; at `:2158-2161` it continues when payload digest is unchanged, and parent revision turnover is only handled in the changed-image/promotion paths (`:2162-2242`). It does not project the manifest-only parent identity supplied by the consumed command boundary.
6. The next-input check then compares the authenticated Agent output to this stale Runtime projection (`:2855-2867`), producing the reported refusal at line 2864. This is a Runtime projection ownership defect, not a source capture or Agent output-metadata defect.

The existing passing source-consumption caller is the same Agent hydration/consumption path above. The held candidate's controls establish sealed predecessor input and verified source admission; they do not and must not repair Runtime's command-output projection. No fabricated effect ordinal, payload change, guard relaxation, or source omission is valid.

## Guard and acceptance disposition

Preserve initial input identity, exact document/media pins, native/materialization/effect/read coverage, strict binding checks, immutable source capture, CAS/idempotency, and no-write-on-refusal behavior. The D115 per-step image fix remains strict and untouched.

The requested C0 acceptance shape remains unexecuted in this read-only review. The production caller is the real provider/Runtime path above; a future Runtime author must prove requests containing `api_version`, `project_id`, `timeline_id`, `base_revision_id`, `base_publication_id`, `commands`, `label`, `steps` (`id`, `label`, `intent`, `tags`, `command_ordinals`, `patch`, `reads`), `merge`, `reads`, `dry_run`, and `Idempotency-Key`, with accepted/merged canonical document, receipt, head, effects, bindings, dependencies; conflict head/reason; invalid code/path/hint; and unchanged dry-run state. No test or full-suite run was performed because this task is read-only and explicitly forbids a fabricated replay.

## Missing custody inputs

The flat pairing is present. The original worker-local replay inputs are not present at the exact paths named by the brief:

- `.../workers/agt-F-D115-producer-input-sol-1002/evidence/unapplied-pairing.json`
- `.../workers/agt-F-D115-producer-input-sol-1002/evidence/checks.json`
- `.../workers/agt-F-D115-producer-input-sol-1002/evidence/producer.xml`

The published handoff supplies enough source/ownership facts for this review; those files were not recreated or replayed.

