# D132a/G3/R2 independent review commands and results

- Read the settled `/tmp/.../PLAN.md` and reviewed all five worker1744 artifacts — PASS. The settled decision was preserved; no alternate qualification was attempted.
- Read-only source inspection of the Agent graph fixture/test, recorder, command executor, preview, and patch paths; Runtime service, store, auth, port/provider, and C0 contract paths — PASS.
- `git -C /home/user/work/wt/app-D132a-child-boundary-review-1753 rev-parse HEAD HEAD^{tree}` — PASS: `224de4697c36b8958d94c0b85626e0fedaf007cb`, `3db8babbbdaf9a011d2eab9e27884c6c195cd76c`.
- `git -C /home/user/work/wt/rt-pin-5e9ad1c6 rev-parse HEAD HEAD^{tree}` — PASS: `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`, `de2954a0ceadb4455903d9abdfec3b773318a50f`.
- `git -C /home/user/work/wt/rt-pin-ab1e4f61 rev-parse HEAD HEAD^{tree}` — PASS: `ab1e4f6141987706132916e2da16477f5a019464`, `7d8e77b2f5a4af79305c9212ce5174d3ea9fd657`.
- `git diff --no-index --unified=4 rt-pin-5e9ad1c6/runtime_protocol/timeline_commit_auth.py rt-pin-ab1e4f61/runtime_protocol/timeline_commit_auth.py` — PASS: only inverse/materialization/validation-order hunks differ; `native_site` is unchanged. Exit status 1 was the expected non-identical-file result.
- Private-cache `python3.11` AST parse plus `compile(source, filename, 'exec')` on 11 cited Python files — PASS; no bytecode/source writes.
- `python3` JSON parse of prior worker1744 `facts.json` and `source-custody.json` — PASS.
- `git -C Agent diff --check` and clean-tree/base assertions — PASS; no repository changes.
- Clean-tree assertions for both immutable Runtime pins — PASS; no pin changes.

## Trace result

The registered `astrid` provider path reaches Runtime `commit_timeline`, prepares the Agent record, and then enters Runtime authenticated closure validation. For the first command, frozen `validate()` uses the source closure as `command_boundary`; frozen `validate_step()` invokes `native_site()` on the recorded child collection/clip aliases. Because `occurrence:new-occ` is absent from that pre-command boundary and the alias is not itself a created root, `native_site()` rejects at line 156 with `provider occurrence alias is outside its boundary`. This precedes output/materialization, inverse-stage work, reload, and redo.

The ab1e4f61 changes do not touch that initial resolver or ordinary create path. The reviewed worker's `NOT_APPLICABLE` classification is therefore independently confirmed. Its one producer explanation is corrected in the evidence: ordinary create reads are staged `record["reads"]`; public command guards are later projected from `command_input`.

No pytest, own1/own9, service body, socket/browser/native/full/family suite, recovery/SWAP inspection, source edit, collector, or test rewrite was run.
