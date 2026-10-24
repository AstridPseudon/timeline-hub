## Report — FAIL for staged source custody

Base inspected: `a458bd76b234a70fc891da3762b27e16ad915d8c` / tree `d2351b7e84c7e42b1a8a9b03c5444a10be37934c`.

No product changes were made.

### Source → receipt

The selected declaration is the current Agent pin at `/home/user/work/agent/pyproject.toml:59`:

- repository: `astrid-agent`
- commit: `242f9c4306bf3b501222cb041a9eb246ef47bc85`
- subtree: `packages/timeline-schema/python`
- package: `banodoco-timeline-schema==0.0.2`

The component repeats this identity at [`verify_farm_distribution_inputs.py:40-47`](/home/user/work/wt/rt-OPS-farm-custody-path-1012/ops-handoff/child-dependency-reuse/candidate/verify_farm_distribution_inputs.py:40).

The selected commit object and physical subtree are absent from both available Agent repositories. The previously recorded HTTP 403/access refusal remains authoritative. The installed ArtAgents distribution and RECORD evidence are not equivalent original-source authority.

`validate_schema_source()` produces a receipt at [`verify_farm_distribution_inputs.py:500-567`](/home/user/work/wt/rt-OPS-farm-custody-path-1012/ops-handoff/child-dependency-reuse/candidate/verify_farm_distribution_inputs.py:500), including commit, tree, per-file hashes, modes, and `content_sha256`.

However, source custody is not PASS:

- The validator trusts ambient `git` subprocess output; it does not authenticate the executable or remote provenance ([lines 397-407]).
- It checks cleanliness before reading files, but does not snapshot files, compare each file to the selected Git blob, or recheck status afterward ([lines 507-518, 521-557]). A tracked file can change between the checks and receipt generation: a real TOCTOU gap.
- File modes are checked, but directory modes and UID/GID are not; `_read_regular()` checks regularity and link count only ([lines 179-185, 456-485]). This matches the existing 1007 failure: a `0777` schema directory was accepted.
- Ignored/untracked entries inside the selected subtree are physically enumerated and rejected ([lines 442-497]). Ignored content elsewhere in the Agent checkout is not part of the schema receipt.
- The private fixture passes only because `_git` is monkeypatched with synthetic output ([tests/test_farm_distribution_inputs.py:170-212]); it proves receipt shape, not real Git custody.

The TOCTOU and directory ownership/mode findings should go to the existing Sol1012 component owner. No competing fix was authored.

### Wheel path

The fixed five-wheel packet is PASS as an independently reviewed input:

- Exact filenames, versions, hashes, ZIP safety, metadata, RECORD completeness, and role partition are enforced at [`verify_farm_distribution_inputs.py:95-136`](/home/user/work/wt/rt-OPS-farm-custody-path-1012/ops-handoff/child-dependency-reuse/candidate/verify_farm_distribution_inputs.py:95).
- Additional caller wheels are refused because no independent authority exists ([lines 324-342]).
- Prior exact review recorded 17 tests passing; I did not rerun them.

This is byte/hash authority, not full physical custody: the component does not authenticate wheelhouse UID/GID/modes. The existing helper separately validates the committed lock and wheel hashes, snapshots original bytes, and installs through a sealed lock/fd path ([`verify_dependency_seed.py:489-505`](/home/user/work/wt/rt-OPS-farm-custody-path-1012/ops-handoff/child-dependency-reuse/candidate/verify_dependency_seed.py:489)).

### Normal-maker comparison and join gap

The existing normal maker has stronger source-snapshot behavior:

- It checks clean HEAD identity at [`make-child-venv:77-85`](/home/user/work/wt/rt-OPS-farm-custody-path-1012/ops-handoff/child-dependency-reuse/candidate/make-child-venv:77).
- It archives the exact commit, excluding ignored/untracked files ([lines 405-416]).
- Reuse verification regenerates committed files through `git archive` and compares the retained snapshot ([lines 701-746]).
- Retained trees are owner-checked, non-writable, and link/hardlink constrained ([lines 655-668, 841-842]).

This is a genuine clean Git archive plus owner-only retained-source model, but it still trusts the local Git process/object store and performs committed-file type rejection after installation.

The component’s supported producer/join interface is [`validate_farm_distribution_inputs()` at lines 570-582](/home/user/work/wt/rt-OPS-farm-custody-path-1012/ops-handoff/child-dependency-reuse/candidate/verify_farm_distribution_inputs.py:570). There is no production caller in this Runtime tree.

The smallest real integration gap is therefore:

1. Normal maker must call the validator with the same Agent checkout and wheelhouse used for the build.
2. It must retain the resulting receipt and bind `component_identity` to the Store identity/reuse checks.
3. The retained archived schema subtree must be checked against the receipt before publication and on reuse.
4. The existing Store key currently accepts only `agent_sha`, `backend_sha`, and `client_tuple` ([`bench_store.py:39-54`](/home/user/work/wt/rt-OPS-farm-custody-path-1012/ops-handoff/child-dependency-reuse/candidate/bench_store.py:39)); the maker currently constructs only those fields ([`make-child-venv:240-241`](/home/user/work/wt/rt-OPS-farm-custody-path-1012/ops-handoff/child-dependency-reuse/candidate/make-child-venv:240)). Thus the receipt is presently neither keyed nor revalidated.

### Checks

- `PYTHONPYCACHEPREFIX=<temp> python -m py_compile .../verify_farm_distribution_inputs.py` — passed.
- `git diff --check HEAD` — passed.
- Worktree clean.
- No targeted test rerun, full suite, acquisition, installation, wiring, or network access performed.