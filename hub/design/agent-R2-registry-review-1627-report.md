# R2 registry-presence review handoff

Independent read-only review of `6aec04e8b..acc7ce17a` (`tl/agt-R2-registry-presence-sol-1617`).

## Verdict

- Isolated registry source repair: **PASS**.
- Complete redo: **FAIL**, separately, at the later `parent.occurrences` guard. This is not a reason to reject the isolated registry repair and is not attributed to the nested or shot-id causes.
- No public execution, original `c271` body, Runtime service, product edit, Git mutation, or full suite was run.

The four-line `inverse.py` change only makes `coalesce.value_address` retain a directly authored `parent.registry` physical address. `logical_address` and conflict/history overlap remain unchanged. The captured before/after both have top-level `parent.registry` present and `parent.config.registry` absent; offline probes also retain distinct absent, empty, null, and existing mirror states. The captured source subset is lossless and input mutation is false.

## Exact evidence

- Packet: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-redo-budget-sol-1605/evidence/agent-G5-redo-budget-1605-7ab92b619cbe6466b782852afd63c46309722d6d65d88f8fbb8c1e93111a6c15.packet.jsonl`, SHA-256 `7ab92b619cbe6466b782852afd63c46309722d6d65d88f8fbb8c1e93111a6c15`, 320 events.
- Retained input: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-registry-presence-sol-1617/captured-input.json`, SHA-256 `b55cca41df4ee9490c537e01e77742310fc198729f9c4c7acb595da8d833a266`, events 154/264/266.
- Candidate `inverse.py`: `fb0cb16bab8a4fbd72a24c9dffadd6992e397925b383ce9ec79f6cc6bbb00d5a`.
- New captured test: `ad96279d8cee5bbf1fcf6e0a91f053bb26019ae4096e1c3e2c737fc290882606`.
- Unchanged source checks: `_step_undo.py` `6cedff390a06ff74a957b962199efb4144b82e2e7e48664269098f39fbae8915`; `_root_inverse.py` `0d81d995582622367cca770855d7604735d3a707a7e8d6d6d5d6102367c4949a`; `_commit_patch.py` `06e35825df4f6578ef192de92ab27dbc5131484d99c4953f001293f9bad9490c`; `_recording.py` `85aefe0328a7c9787a18c2b7e19eb8b3e4220a1c53627d1e16102b42b29c8b43`; `timeline_restructure.py` `842850e1e867eaf2a8c003897b6624bb040a2b7c8f910eecad1d5aa8c9f851ee`.

## Tests and checks

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-cfa0af0d /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_captured_registry_redo.py --basetemp=/tmp/w-agt-R2-registry-review-1627-registry
19 passed in 1.08s

same environment + bounded original alias/ABA/storage node set (12 tests; --basetemp=/tmp/w-agt-R2-registry-review-1627-original)
12 passed in 7.65s

python3 .../workers/agt-R2-registry-presence-sol-1617/audit_packet.py
PASS: 320 contiguous payload hashes; exact captured source subset; absence mismatch; original no-write closure/head/history/SQL

scripts.reshape.compare_ruff_baseline
Ruff findings: current=2149 baseline=2149
ruff check inverse.py test_captured_registry_redo.py
All checks passed
scripts.reshape.compare_mypy_baseline
Mypy findings: current=1912 baseline=1912
mypy inverse.py --cache-dir=/tmp/w-agt-R2-registry-review-1627-mypy-scoped
Success: no issues found in 1 source file
vendor_lock.py check runtime.lock.json
ok runtime.lock.json
artifact_manifest.py --check
artifacts.json is current
git diff --check
PASS
```

## Separate next-occurrence diagnosis

The one allowed offline validator replay reproduces `CommandError: original authored guard changed`, `kind=inverse_conflict`, `ref=parent`, `path=['occurrences']`, with no bundle mutation. The retained accepted undo command is ordinal 0, step `inverse`; its authenticated historical native step is `restructure-0`, native write range `[0,10]`, effect range `[0,9]`. The accepted same command has an aggregate `parent.occurrences` after-image with three rows in order `occ-film`, chapter-8373, chapter-3f75, followed by per-occurrence removals of the two chapter rows. The canonical accepted after document has only `occ-film`.

The exact source-folding seam is `inverse.py:150-195`: aggregate and occurrence-root writes receive different physical addresses, so coalescing does not apply the later alias removals to the parent aggregate before the strict guard. A future fix should be limited to an authenticated batch containing both that aggregate and matching occurrence-root writes: fold by `occurrence_id` using the recorded historical order, while preserving membership/order checks, intervening ABA checks, and physical identity bindings. Return this continuation to the existing Sol1626 inverse owner; this review proposes no competing author.

Minimum flat facts export: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-R2-registry-review-1627-facts-0b37b1b31b806275d8454201a01ef198837e60a8edc3da6108fe877fb5f3fbd2.json`.

