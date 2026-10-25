# D118a protected review

Disposition: **PASS_SOURCE** — not a functional GO.

- Reviewed `528ec4f21` against parent `36e44e1c0`.
- Current SHA-256: `d688735227bee66f38c420f23abd3c5457c8d6471919a2c96f754708509802c0`
- Original SHA-256: `b53c2c4bc53789dd4667b99c4219ec28c4cd9ce850d638f298dfa88d48ad9e8d`
- Pristine `08e6b905...` lacks the target file (`git cat-file -e` exits 128).
- Diff is exactly one test-scoped `PYTHONNOUSERSITE` removal.
- Causal chain verified: `host_frames_at → _query → strict probe_context → _scene_only_spans → Checkout._scene_problems`.
- AST/input/assertion conservation passed.

Checks passed:

- Ruff
- mypy with `--follow-imports=skip`
- `py_compile`
- `git diff --check`
- Direct validator causal probe

The exact renderer test was **not run**: no receipt-backed current host/profile exists locally; required Node/profile/module paths are absent. No acquisition, install, bypass, or broader suite was attempted.

Evidence and completion marker were written; no product/source fixes were made.