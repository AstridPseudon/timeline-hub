## Verdict: FAIL

Reviewed cumulative component at:

- Commit: `a458bd76b234a70fc891da3762b27e16ad915d8c`
- Tree: `d2351b7e84c7e42b1a8a9b03c5444a10be37934c`

Finding: [`verify_farm_distribution_inputs.py:465`]( /home/user/work/wt/rt-OPS-farm-component-review-1007/ops-handoff/child-dependency-reuse/candidate/verify_farm_distribution_inputs.py:465) checks directory type but not directory modes or filesystem ownership. A private fixture with the schema package directory changed to `0777` was accepted. No UID/GID authentication exists.

All required attacks refused:

- Self-consistent forged `evilpkg2` additional wheel
- Ignored escape symlink
- Ignored extra file
- Nested ignored directory
- Prior attack reproductions

Checks:

- Focused pytest: **17 passed**
- Ruff: passed
- Plain and normalized mypy, parent/candidate: passed
- Compile: passed
- `git diff --check`: passed
- All 12 prior controls and 5 new controls preserved
- Reviewed five-wheel packet hashes match
- `proof.lock` SHA `236d…c778` and `67` wheel unchanged

Authentic schema remains unavailable. `/home/user/work/agent` refuses because it is not pinned commit `242f9c4…`; that commit object is absent. Forged `_git` fixtures only validate receipt shape and refusal branches, not real Git authority.

No source edits, installation, network, acquisition, wiring, or full suite run. Production interface remains:

```python
validate_farm_distribution_inputs(
    schema_source=agent_checkout,
    wheelhouse=reviewed_wheelhouse,
    additional_wheels=reviewed_additional_wheels,
)
```

It remains not wired. Directory mode/ownership authentication must be fixed before another review or coordinated join.