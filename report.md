# R2r native history probe 1003

Result: **FAIL (candidate)**.

The corrected probe used the real Runtime `music-documents` store fixture and
the real Agent provider under the required candidate-first import order. The
forward split+unrelated-note request authenticated and was accepted. The
inverse request was sent in the full v2 production argument shape, with
history derived only from `TimelineCommitStore.history_entry` for the accepted
forward publication. Candidate Runtime refused both production acceptance and
direct authenticated validation:

`invalid_records: inverse stage write differs from its sequential input`

The captured inverse request, prepared records, all writes/reads/bindings,
stage ranges, canonical documents, store-authenticated forward history, module
origins and SHA-256 values are in the full JSON output:

`/tmp/w-71481117c1/candidate.json`

Output SHA-256: `c4d528ffc7cdbf56bb25298e3211fbd229ec1c0b1c08e543f2fb48f16968fe05`.

The exact failed inverse request used the accepted forward publication
`txn-87cb7be5a6464ad9add5b2d923d615bb` as both base publication and undo
target. Its captured inverse stage was `step_id=split`, `command_ordinals=[0]`,
`native_write_range=[0,8]`, `effect_range=[0,3]`; the failure occurred while
validating that retained stage, before a durable inverse receipt existed.

The three bounded negative probes refused as required: missing history,
caller-forged source step history, and an extra caller-invented future history
entry. The history provenance assertions also passed: the supplied inverse
history contained exactly the accepted forward publication, matched the store
entry and receipt byte-for-byte, and excluded the inverse/new publication.

Comparison against original Runtime `1365e4b17b31c4a7093d5943674637067fd2bab4`
with the unchanged request accepted the inverse and reported direct auth pass.
That validator has no `history` parameter, so this is only a binding mismatch
comparison, not candidate acceptance evidence. Its full output is
`/tmp/w-71481117c1/original1365.json` (SHA-256
`43d66be5b6aba2bc8d349f69131ef17eaf489947515ead441fc4420cd05fbe28`).

## Commands

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/rt-R2r-native-history-probe-1003:/home/user/work/agent /home/user/work/venv-agent/bin/python -m py_compile /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-R2-stage-repro-1003-store-authenticated.py` — PASS.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/rt-R2r-native-history-probe-1003:/home/user/work/agent /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-R2-stage-repro-1003-store-authenticated.py` — exit 0, JSON status `FAIL` as required by the retained product refusal.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/runtime:/home/user/work/agent /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-R2-stage-repro-1003-store-authenticated.py` — exit 0, inverse accepted on original1365; comparison limited by the old validator API.
- `git diff --check` — PASS.

No Runtime/Agent production files, schema, client, pin, fixture, or original
0912 repro bytes were changed. No HTTP/browser/full suite or prohibited rerun
was performed. The independent 0957/static/freeze evidence was reused.
