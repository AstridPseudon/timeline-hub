# G3/P4 current ordinary-show port review — PASS

Reviewed `126aff176cab03ec9659fbdbb824ec41d2c9de19` (`tl/agt-G3-show-port-review-0548`)
against `bf40d6bb5`, integration `900ba8f09`, and exact reviewed source
`1f93b8b3057a7c2a611f7bdc186c943418b62bc` on `9b658b28c3a7bc3ebda3ad5a7b5b417d78553720`.

**PASS.** Exactly the requested three paths are changed. Parent and final blobs
match the reviewed base/final blobs for all three paths; stable patch-id matches
the donor: `61ea449935e17a160fa295a4630df8fc5f9a91ea`.

The production caller is wired: `cli_show.py:224` → `build_cut_table` →
`occurrences_from_bundle`. No unrelated source, metadata, inverse `076`, V4
`5292`, Runtime producer `34e`, canonical schema `d106`, generated file, pin,
fixture, HTTP body, or test expectation changed. `git log 900ba8f09..HEAD` has
only `126aff176`; worktree clean.

Evidence:

- Exact targeted command with `venv-agent`, `PYTHONPATH=$PWD:/home/user/work/runtime`,
  pinned runtime env, and cache disabled: **55 passed, 2 subtests passed**.
- Changed core/test Ruff: PASS; SDK scoped Ruff has its unchanged 10 existing
  findings.
- `make ... ruff`: **2150/2150**; persistent typecheck-v2 `make ... mypy` and
  `compare_mypy_baseline`: **1915/1915**.
- Vendor lock against `/home/user/work/wt/rt-pin-34eac004`, artifact manifest,
  and `git diff --check`: PASS.
- Old normal mypy remains environment-blocked by known YAML-stub/NumPy-stub
  issues; scoped touched-file output is the same 3 existing diagnostics.
- Import origins: Agent modules from this worktree; `runtime_protocol` from
  `/home/user/work/runtime`.

No full/browser/live-socket suite was run. Queue decision: PASS; merge may
proceed independently of the disjoint current G234 merge.
