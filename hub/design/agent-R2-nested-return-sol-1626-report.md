# R2 nested return — agt-R2-nested-return-sol-1626

**Cumulative verdict: FAIL / BLOCKED / HELD.** The native-only compatibility regression is repaired. Exact inherited source identity remains vulnerable; six durable security tests deliberately retain the required refusal expectations and fail. Do not land the cumulative candidate or run a joint/public body on this evidence.

Read PLAN.md and the exact independent review `ORCH/design/agent-R2-nested-review-1617.md`. Base is `acc7ce17a5339de5b64306922eae5f6f09e8baa0`, atop held `6aec04e8bdbdcbcca7e6ee7d979c105618357f87`, atop `98ef2f9c95fd43d88cca2909d8d1518302e3050c`. The harness owns the new commit; no new commit hash exists at report time. No Git write was performed.

Only `_step_undo.py` and `test_captured_nested_redo.py` changed. Native-only stages without canonical commit.effect bindings use the existing whole-native reversal; no effect ranges or full v2 facts are manufactured. V2 captures still require complete effect ranges, including when an attacker removes every range. Missing or malformed ranges now produce CommandError rather than KeyError. The registry presence repair, strict ABSENT/null/{} distinctions, four original source guard assertions, and all existing tests remain unchanged. No skips, xfails or weakened expectations.

**Why exact identity is blocked by the permitted scope:** `_step_undo.inverse_stages` receives only the immediate accepted inverse entry. `_commit_patch.inverse_address_resolver` receives that entry plus `load_boundary`; its callback returns two document bundles, not the original source's accepted step/command records. The original `fork-edit-*` identities are not document facts and cannot be derived from names, ordinal guesses, content digests or equal bytes. In production, the authenticated lookup is `port.history_entry` in `commit.py` (target loading around 999, boundary loader around 1018, resolver construction around 1037). It is not supplied to the four permitted helpers. The original source publication is earlier than the target-to-base history supplied to the resolver. Receipt result commands carry semantic metadata, not the native inverse.stage bindings; they cannot authenticate these original partition identities.

A complete repair therefore needs the provider to expose the existing authenticated source-record lookup to the inverse helper, requiring minimal `commit.py` plumbing outside this task's explicit four-file limit. No callback-closure introspection, caller-provided history authority, fabricated accepted edge, new wire shape, content-equality substitute or guard waiver was introduced. An asynchronous scope question was sent; no scope expansion was received as of this report. This is a scope conflict evidenced by the actual production call path, not a proposed contract decision change.

Durable added cases cover both original regressions (one of ten notes and semantic creation), missing one/all effect ranges, missing stage, extra effect and extra history. The six identity cases mutate the exact lossless capture and use its actual original source step/command records to identify wrong-step and wrong-ordinal substitutions. Negative, out-of-bounds, reordered and extra ordinals are also tested. All six still fail because no CommandError is raised. Refusal cases preserve the captured input; native compatibility tests also preserve the exact bundle and records. No original fixture bytes were changed.

Commands below run from `/home/user/work/wt/agt-R2-nested-return-sol-1626`.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-cfa0af0d /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_captured_nested_redo.py tests/editing_conformance/test_captured_registry_redo.py tests/editing_conformance/test_inverse_stage_images.py tests/editing_conformance/test_step_undo_v2.py --junitxml=/tmp/w-414cd1f329/final-tests.xml --basetemp=/tmp/w-414cd1f329/pytest-final-security > /tmp/w-414cd1f329/final-security.log 2>&1
# FAIL, exit 1: 73 passed, 6 failed in 3.82s.
# Original nested 11: PASS; nested file including additions: 18 PASS / 6 FAIL.
# Registry focused: 19 PASS. Original bounded files: 1 + 35 = 36 PASS.
```

Final failing test IDs are `test_captured_nested_identity_must_match_original_accepted_source[wrong-step]`, `[wrong-ordinal]`, `[negative-ordinal]`, `[out-of-bounds-ordinal]`, `[reordered-ordinals]`, `[extra-ordinal]`.

Causal old-source run uses the exact HEAD `_step_undo.py` loaded into its own module before pytest imports consumers. The wrapper is `/tmp/w-414cd1f329/causal_old.py`; it reads the source with `git show`, compiles and executes it in that process, then calls pytest.main. It neither edits the worktree nor changes dependencies.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-cfa0af0d /home/user/work/venv-agent/bin/python /tmp/w-414cd1f329/causal_old.py -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_inverse_stage_images.py tests/editing_conformance/test_step_undo_v2.py tests/editing_conformance/test_captured_nested_redo.py --junitxml=/tmp/w-414cd1f329/causal-old-tests.xml --basetemp=/tmp/w-414cd1f329/pytest-causal-old-final > /tmp/w-414cd1f329/causal-old-final.log 2>&1
# RED, exit 1: 48 PASS / 12 FAIL.
# Original bounded files: exactly 34 PASS / 2 FAIL (the two reported KeyErrors).
# Native-only added regressions: 2 FAIL old -> 2 PASS new.
# Missing-effect-range cases: 2 FAIL old (KeyError) -> 2 PASS new (structured refusal).
# Identity attacks: 6 FAIL old -> 6 FAIL new (unresolved, not hidden).
```

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-cfa0af0d RUFF_CACHE_DIR=/tmp/w-414cd1f329/ruff-cache /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline
# PASS: 2149/2149. Logged in /tmp/w-414cd1f329/ruff.log.
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python /tmp/w-414cd1f329/scoped_lint.py
# PASS: added diagnostic identities {} across four inverse files and both captured tests.
# Compares code/message/path counters against exact HEAD files in a private directory.
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-cfa0af0d MYPY_CACHE_DIR=/tmp/w-414cd1f329/mypy-cache /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
# PASS: 1912/1912. Logged in /tmp/w-414cd1f329/mypy.log.
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy astrid/sdk/timeline/inverse.py astrid/sdk/timeline/_root_inverse.py astrid/sdk/timeline/_step_undo.py astrid/sdk/timeline/_commit_patch.py --cache-dir /tmp/w-414cd1f329/mypy-scoped --hide-error-context --no-pretty
# PASS: no issues found in 4 source files; scoped diagnostic identity set remains empty.
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
# PASS: ok runtime.lock.json; official source_commit 34eac0041b0891e9011966b39bcbd26053fde5bc unchanged.
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
# PASS: artifacts.json is current.
git diff --check
# PASS.
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-cfa0af0d /home/user/work/venv-agent/bin/python /tmp/w-414cd1f329/export_evidence.py
# PASS: records, steps, request and canonical output exactly equal retained 1603 emission.
```

An initial test attempt incorrectly treated the worker's `tmpdir` pointer file as a directory, causing 36 setup errors before behavior ran. Reading the pointer yielded `/tmp/w-414cd1f329`; all final runs use that private directory. An initial scoped Ruff comparison found one new import-format identity; the new inner import was formatted and the final comparison is empty. Neither issue was a tool/classifier/permission refusal. No dependency/shared cache was modified.

The full retained packet remains SHA-256 `3a718d9537faec492723efcd0b49a86675054ae03cfa580361058c58ba780c09` (verified with sha256sum). The embedded untransformed capture remains 444166 bytes, SHA-256 `9a47bb934b879efa0f6147d673038cee76299ba4e30ab22b6d5bcb1377ade589`. Exact emitted native writes, physical bindings, outward immediate undo-0/[0] identity, two stage ranges, nine effects and complete canonical output are unchanged from the retained emission. The new emission metadata explicitly states cumulative source FAIL.

No Runtime/public redo, c271, P1-P4, full suite, broad40/281/58, native14, V4, browser, live socket, daemon, provisioning, schema/client/pin/lock/dependency update or merge request occurred. C0 request/reply routing code was untouched; accepted/merged receipts, v2 previews and structured reply fields were not newly exercised. Runtime1606/f054 independent PASS is a supplied prior fact, not reverified here.

Recommended next step: orchestrator authorizes the minimal production authenticated-history plumbing beyond the four-file limit, assigns the exact identity repair, retains these failing tests, then obtains independent cumulative Agent source PASS. Only the manager can assign one joint body after both final source reviews pass. This worker does not advance that gate.

Final SHA-256 values:

- `astrid/sdk/timeline/_commit_patch.py`: `06e35825df4f6578ef192de92ab27dbc5131484d99c4953f001293f9bad9490c`
- `astrid/sdk/timeline/_root_inverse.py`: `0d81d995582622367cca770855d7604735d3a707a7e8d6d6d5d6102367c4949a`
- `astrid/sdk/timeline/_step_undo.py`: `493b458084b9bb6b2e2450d611fe833bae45e1480fc9ad46f6c3cd6a24098b4d`
- `astrid/sdk/timeline/inverse.py`: `fb0cb16bab8a4fbd72a24c9dffadd6992e397925b383ce9ec79f6cc6bbb00d5a`
- `tests/editing_conformance/test_captured_nested_redo.py`: `e8b9849e198a33a2026fb47ab5a36574171678f33037f6a953647d0e26ea9a7b`
- `tests/editing_conformance/test_captured_registry_redo.py`: `ad96279d8cee5bbf1fcf6e0a91f053bb26019ae4096e1c3e2c737fc290882606`
- `capture`: `9a47bb934b879efa0f6147d673038cee76299ba4e30ab22b6d5bcb1377ade589` (444166 bytes)
- `request_body`: `9a7586bbefe0ed9281eabd1d0de3a03008f15ece347bf70a6acd26b770637449`
- `emission`: `e2eace2a358ffdedf3e778ad96b3ef47a4ee16c5b813c21cecb27ff54a52c830` (91932 bytes)

Updated emission and source hashes are at absolute ORCH/design paths:

- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-R2-nested-return-sol-1626-emission.json`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-R2-nested-return-sol-1626-source-checks.json`

Security-case results are published beside this report as `agent-R2-nested-return-sol-1626-security-cases.json`. Full logs and JUnit XML are in `/tmp/w-414cd1f329/`. Worker artifacts remain outside the product commit.
