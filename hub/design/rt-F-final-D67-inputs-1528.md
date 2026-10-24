## F-final-D67 report

Extracted the truthful post-install D13 README appendix and selector command. No product files or README were modified; the worktree remains clean.

Command:

```sh
<runtime-environment>/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  tests/packs/video_editing/test_runtime_publication_chain.py::test_d13_installed_native_preflight
```

Required env: 13 exact names from `_d13_inputs`; expected bindings has exactly:

`agent_commit`, `agent_tree`, `agent_wheel`, `agent_wheel_sha256`, `source_checkout`, `source_digest`, `runtime_environment`.

Evidence:

- [D13 README appendix](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-final-D67-inputs-1528/evidence/d67-readme-appendix.md>)
- [Source inventory, hashes, citations](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-final-D67-inputs-1528/evidence/d67-source-inventory.md>)

Source captured: Agent `d27b6601e56b19334c9534338ce1f3ac80e85fc7`, tree `2449edb7729b2de0fa57093b788fa0f13058ae4a`; target body hash `6d05a3226dbdb752502a3e0fa1098df371498f75437a8690deb8482f23305b10`.

Tests: not run, as explicitly required for this read-only extraction. No deployment or inputs were provisioned. D67 remains the settled non-core-blocking environment gap.