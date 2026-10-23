# D17 current authenticated inverse: bounded classification

**Observed cause: Runtime 49ce compares a native authored occurrence image to a canonical occurrence image containing a provider-managed revision pin.** The first native inverse write is valid against its accepted forward capture. The complete physical parent effect contains the pin, and the complete inverse candidate exactly equals the original destination document. This is evidence of a representation error in Runtime inverse-stage reconstruction, not evidence of an invented Agent occurrence claim. No repair or guard waiver was made. Runtime peer 1058 retains implementation ownership.

## Boundary and scope

- Agent: `/home/user/work/wt/agt-D17-current-auth-diagnosis-1058`, commit `ce1d1cca87379029924b0be6f98564f556597107`, tree `68dee9124ab8f4026ac4119f816eceec654f0bba`.
- Actual Runtime: `/home/user/work/runtime`, commit `49ce53289bc37d9387a7d9e6b9c9b16072162181`, tree `364380ae064c512c0a0d2b8903a599b7026642f4`.
- Both trees were clean before and after. All observed Runtime modules originated inside the actual Runtime checkout; every module already loaded before the case retained its path and hash afterward. The JSON retains 106 Agent/Runtime module origins after the case.
- Read PLAN first, including R2/G4/G5; read C0 §§2/5, integrated1053, finalreview1042, normalizer1024 and its capture script/wire provenance. The 1053 observer retained origins, not full wires. The 1024 full wire used old Runtime1365. Therefore the task's one diagnostic authorization was needed.
- This report does not change the current integrated **36 PASS / 4 FAIL** finding or the existing **281 PASS** result. Neither selection was rerun. Old1365 40 PASS is not current qualification. P1/G5 retirement stays held.

## Exactly one new execution

Working directory was the assigned Agent worktree. Exact command:

```sh
PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/w-af52f724b2 PYTHONPATH=.:/home/user/work/runtime:/tmp/w-af52f724b2 ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime D17_CAPTURE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-D17-current-auth-diagnosis-1058.json timeout 25s /home/user/work/venv-agent/bin/python -m pytest -q --tb=short -o addopts= -p no:cacheprovider -p d17_observer --timeout=25 --basetemp=/tmp/w-af52f724b2/pytest-single 'tests/editing_conformance/test_commit_runtime_source_copy.py::test_repeated_source_copy_real_port_idempotency_and_guarded_inverse[False]'
```

Result: **exit 1; 1 failed in 4.30s**, at the already-known inverse-store rejection `inverse stage write differs from its sequential input`. No all4/40/281/58/P1/P4, full suite, daemon, socket or browser execution occurred.

The node uses the production `duplicate_timeline -> _duplicate -> _commit_bundle -> session.submit -> generated commit -> RuntimeService.commit_timeline -> RuntimeCommitService.commit -> real store.accept/_validate` path; undo uses normal `timeline.open(...).undo -> session.undo -> flush -> same production boundary`. The source fixture is trusted setup, not a replacement copy executor. The accepted duplicate and idempotent replay complete; undo reaches real store validation and rejects; redo is not reached.

The observer only uses Python trace callbacks, snapshots values, reads module files/Git metadata, and reads SQL with `iterdump()`. It does not wrap/replace methods, alter requests/prepared values/history, change imports, catch product errors, or bypass the store. The original test and assertions are unchanged.

## Exact counterexample

The JSON's `events` preserve the unmodified captured values; indices below are zero-based. `diagnosis` contains independent value comparisons and an index map.

| Boundary | Event | Captured contents |
| --- | --- | --- |
| Forward service call | 5 | Full actual request, key, publisher and invocation path |
| Forward provider | 6 | Full context, request hash and original invocation body |
| Forward store accept | 7 | Full prepared canonical document, records, effects, dependencies, bindings, expected head and digests |
| Forward accepted response | 21 | Full original data/receipt envelope |
| Exact replay response | 39 | Full original replay response |
| Inverse service call | 48 | Original undo request and `undo-copy` key |
| Inverse provider | 49 | Full original context and request hash |
| Inverse store accept / validation | 176 / 185 | Complete prepared inverse and store SQL before validation |
| Authenticated inverse boundary | 191 | Request, prepared, source/base canonical documents, continuations and complete store-authenticated selected history |
| Failing sequential input | 194 | Exact write, current native image, stage before/after images, ordered writes, native/effect ranges and stage binding |
| Runtime refusal | 196 | Original typed failure: HTTP422, `validation_error`, details reason `invalid_records`, status `refused` |

Selected publication: `txn-3bd50bc6dee542338a988a02c96d082f`; source step `copy`; command ordinals `[0]`; native range `[0,4)`; effect range `[0,3)`.

1. Accepted forward command0 writes, in order: `parent:[config]`, `shot:copy-film:[]`, `occurrence:occ-copy-occ-film:[]`, `occurrence:occ-copy-again:[]`.
2. Inverse command0 retains all four native writes in reverse order. Its first write removes `occurrence:occ-copy-again`, with `before` exactly equal to accepted forward write3's `after` and `after={state:absent}`.
3. Runtime `_inverse_stage_ranges` authenticates that order and those ranges against the selected stored history. It accepts the native representation before reconstruction.
4. Runtime `_inverse_stage_write_site` resolves that native occurrence to `parent:[occurrences,occurrence_id:occ-copy-again]`. `_inverse_stage_state` reads the complete canonical row.
5. That canonical row and the claimed authored `before.value` have identical values for every authored key. The sole extra canonical key is `shot_revision_id=authoring-shot-revision-d3c9da578f236879c92f9fbf745c45bbef283b97e9ec4b991d231f7c05830a25`.
6. The pin names the authenticated captured shot image; both copied occurrences point to precisely that same physical image. The pin is not guessed or lost from the canonical effect.
7. Runtime compares the entire canonical row to the native authored `before` at `timeline_commit_auth.py:884`, fails equality, and rejects before applying the first inverse native write.

Physical effects retain the complete parent before/after payload because raw mirror topology changes. The parent before effect equals the current canonical parent byte-for-value; the parent after effect restores `config={clips:[],tracks:[]}`, empty occurrences, existing raw `clips:[]` and `registry:{}`. Effects1/2 remove the exact bound shot/internal roots. The complete inverse canonical document equals the original forward landing input, including manifests and revision identities. Native shot-aggregate `before` independently equals `{payload: authenticated shot payload, internal_timeline: authenticated child payload}`.

## Agent claim versus Runtime reconstruction

Agent intentionally removes revision pins from authored occurrences in `native_timeline_duplicate.py:108` and `physical_content` near line166; `_command_state.py:282` rejects authored occurrence creation with those pins. `State.entity/get` therefore observes the authored row, and `_recording.py:121` records that native value. `inverse.py:585` restores those native captures; lines698–738 retain sequential stage provenance. `_root_inverse.normalize_root_inputs` rejoins only unchanged aliases through authenticated source mappings. `_commit_patch.effect_diff` near line201 emits a complete physical parent effect when raw mirror presence changes. These are separate representations of the same verified transition.

C0 §2 explicitly retains native command provenance alongside complete physical effects, including managed links inside complete rows/roots. C0 §5 requires authenticated boundaries and sequential inversion. It does not require replacing native authored captures with canonical managed-link rows. Adding `shot_revision_id` to the authored occurrence would violate the existing native creation validator and would not explain the accepted forward history.

Runtime49ce introduced `_inverse_stage_boundaries` relative to1365 and invokes it from `validate` before binding validation. Its first-write comparison fails to project the canonical occurrence to the native observation representation. This is the precise observed cause; the exception message alone was not used as attribution. The intended fix must still authenticate the managed pin from the selected physical images, not blindly ignore links.

Two additional compatibility risks are visible but **not executed past the first refusal**:

- The third native inverse write is the complete `shot:copy-film` aggregate. Current `_inverse_stage_write_site -> native_site` maps that native aggregate to `timeline:[]`, which is a read-only closure scope and is absent from the physical image map. Reconstruction needs to authenticate both shot and internal images as a pair; merely fixing occurrence equality will not cover this native representation.
- This production `session.undo` request lacks `label`, `steps`, `merge`, and `reads`. It has no `rationale` or `group_id` either. `_commit_patch.CommitPatch.v2` is consequently false and the inverse record has only `inverse.stage`, with **zero `commit.effect` bindings**. Runtime's later stage binding loop near line926 unconditionally requires per-effect before/after pins. This is a separate normal-caller/provider/auth compatibility gap. The observed first refusal is still the native occurrence mismatch. The owning lanes must settle how ordinary undo receives the existing v2 metadata/binding guarantees; this diagnostic does not synthesize options or waive requirements.

The forward production wire includes label, atomic merge, reads and steps with empty submitted patch and ordinal `[0]`; rationale/group_id are absent. The inverse wire retains the exact actual options and omissions. The capture's `wire_inventory` records presence/absence explicitly. Accepted data/receipt, full canonical documents, records/dependencies/effects/steps/history/undo_steps and original error shapes are preserved. No preview/merged/conflict reply was fabricated: this one node executed accepted/replayed copy and refused inverse only. The original refusal has no synthesized path/hint/suggested-command fields.

## Durable artifacts and verification

All paths are absolute and survive worker exit:

- Full flat capture: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-D17-current-auth-diagnosis-1058.json` (1,907,448 bytes; SHA256 `ffcc26d88d28039ae05171d2033b3f74636533f8cb9d9b6733242d22cc1fe8db`). Original events are retained; formatting was compacted after capture and `diagnosis` was added.
- Exact observer: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-D17-current-auth-diagnosis-1058/d17_observer.py` (SHA256 `c27d839efa9eb41bf0ac53daf40c01093910afd27fd6974b4dc6b19544dd8ffb`). Identical to the loaded scratch plugin.
- Full pytest output: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-D17-current-auth-diagnosis-1058/single.log` (SHA256 `1550ff163c875cddb4c44c9e23c5eb66febc280debb68c65ffb486c1bce52a8e`).
- Comparison checker: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-D17-current-auth-diagnosis-1058/verify_capture.py` (SHA256 `6758c21135e290f4cb9e8fd519af93778cb14b2c41289a44b6963992cd350aaa`).
- Full hash/byte inventory and 19 comparison results: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-D17-current-auth-diagnosis-1058/verification.json`; human output: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-D17-current-auth-diagnosis-1058/verification.log`.

Exact offline check command:

```sh
python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-D17-current-auth-diagnosis-1058/verify_capture.py
```

Result: **exit0; 19/19 comparisons PASS**. This checks retained data only and does not execute another copy/inverse, alternate executor or qualification suite.

For later owner-authorized reproduction, use the same node/flags, load the durable observer by putting `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-D17-current-auth-diagnosis-1058` on PYTHONPATH instead of `/tmp/w-af52f724b2`, and select a fresh private basetemp/output. Generated project/publication UUIDs vary, while the authored-versus-managed-pin counterexample is structurally deterministic. This report does not authorize or perform another run.

Limits: port objects are recorded as types, not serialized Python internals; actual canonical manifests, native dependencies, request contexts, complete selected history and three SQL snapshots retain the relevant inputs. Python3.14 represents `frame.f_locals` as a proxy: the failed-require event itself holds a type marker, but the immediately preceding line884 snapshot explicitly copies every required write/image/range/binding and is complete. No after-refusal SQL snapshot was taken, so rollback persistence was not newly asserted. The other three failing nodes and redo remain unexecuted here. No complete downstream validity claim follows from equality of the candidate alone.

## Handoff

Runtime peer1058 should repair native-to-physical stage authentication while keeping complete ordered native captures, source history, bindings, pin/allocation proofs and all guards. Resolve the normal undo metadata/effect-binding compatibility separately with the Agent owner before declaring the chain fixed. Then the orchestrator can authorize qualification on the changed integrated tuple. No Agent/Runtime product, test, environment, pin, contract or dependency edit was made; no Git write occurred. This bounded diagnostic is complete and does not mark D17 green.
