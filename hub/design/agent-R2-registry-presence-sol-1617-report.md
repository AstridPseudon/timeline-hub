# R2 registry presence repair — agt-R2-registry-presence-sol-1617

Registry source repair and focused offline qualification: **PASS**. Complete captured redo: **FAIL at a later occurrence guard; public execution not run**. Independent review remains required. No merge request is made.

## Change and evidence

Base `6aec04e8bdbdcbcca7e6ee7d979c105618357f87`, retaining `98ef2f9c95fd43d88cca2909d8d1518302e3050c` and predecessor 1603's complete source and eleven tests. Only four lines in `astrid/sdk/timeline/inverse.py` and one new focused captured regression file changed.

`coalesce.value_address` now retains directly authored `parent.registry` writes at their physical address. Previously `logical_address` moved that write under `parent.config.registry`; folding it into an accepted whole-config write fabricated an expected empty registry mirror. The config and registry landing guards now remain separate and exact, including their before/after presence. This also preserves both physical guards when a config mirror already exists, is empty, or is explicit null. Historical conflict overlap continues through its existing logical address resolver. No guard, source record, binding, effect, pin, owner or physical canonical address is rewritten, and no absence is normalized to an empty object.

Read PLAN and independent1612/1605/1603 reports; verified the entire immutable packet (all 320 events and dedup payload hashes). Packet SHA-256 `7ab92b619cbe6466b782852afd63c46309722d6d65d88f8fbb8c1e93111a6c15`, absolute source:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-redo-budget-sol-1605/evidence/agent-G5-redo-budget-1605-7ab92b619cbe6466b782852afd63c46309722d6d65d88f8fbb8c1e93111a6c15.packet.jsonl`.

The new test embeds the exact complete immediate accepted undo entry, before/after canonical documents, evaluated head and original redo request extracted from events154/264/266. No accepted history or ordinal is invented. Source subset is 104,781 bytes, SHA-256 `b55cca41df4ee9490c537e01e77742310fc198729f9c4c7acb595da8d833a266`; retained in `workers/agt-R2-registry-presence-sol-1617/captured-input.json`. The eight storage-topology unit variants are explicitly labeled as helper inputs rather than accepted history.

Early seam: `design/agent-R2-registry-presence-sol-1617-interface.md` and worker `interface.md`. Machine-readable source hashes, unchanged-source comparisons and immediate source facts: `design/agent-R2-registry-presence-sol-1617-source-checks.json` and worker `source-checks.json`. All these paths are under the absolute ORCH above; none is in the product commit.

## Exact commands and outcomes

Commands run in `/home/user/work/wt/agt-R2-registry-presence-sol-1617` unless specified. All dependency environments were used read-only, with private caches and bytecode disabled.

```sh
python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-registry-presence-sol-1617/audit_packet.py
# PASS: 320 contiguous payload hashes; exact source subset; original absence mismatch;
# unchanged closure/head/history/SQL on the original refusal.

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-cfa0af0d /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_captured_registry_redo.py tests/editing_conformance/test_captured_nested_redo.py --basetemp=/tmp/w-7cf930c802/pytest-final
# PASS: 30 passed in 1.89s. Retained nested eleven run once after the source edit.
# Subsequently only the NEW file's source-tamper tests were made more precise.

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-cfa0af0d /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_captured_registry_redo.py --basetemp=/tmp/w-7cf930c802/pytest-registry-final
# PASS final new file: 19 passed in 0.90s.
```

Final causal RED runs the same final nineteen tests against the immutable `git show HEAD:astrid/sdk/timeline/inverse.py`, in a private source overlay; other package files are read-only links to this worktree. No shared dependency modification or injected history:

```sh
cd /tmp/w-7cf930c802
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/w-7cf930c802/baseline-source:/home/user/work/wt/agt-R2-registry-presence-sol-1617:/home/user/work/wt/rt-pin-cfa0af0d /home/user/work/venv-agent/bin/python -m pytest -q --import-mode=importlib -p no:cacheprovider /home/user/work/wt/agt-R2-registry-presence-sol-1617/tests/editing_conformance/test_captured_registry_redo.py --basetemp=/tmp/w-7cf930c802/pytest-causal-final
# Expected RED, pytest exit1: 11 failed, 8 passed in 0.91s.
# Includes exact captured coalescing mismatch, missed changed physical guards,
# and all eight topology/order cases. Log: /tmp/w-7cf930c802/causal-final.log.
```

Static and integrity checks, from the worktree:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-cfa0af0d RUFF_CACHE_DIR=/tmp/w-7cf930c802/ruff-cache /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline
# PASS: current=2149 baseline=2149.
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-7cf930c802/ruff-cache /home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline/inverse.py tests/editing_conformance/test_captured_registry_redo.py --output-format concise
# PASS: All checks passed; zero scoped diagnostics.
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-cfa0af0d MYPY_CACHE_DIR=/tmp/w-7cf930c802/mypy-private-cache /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
# PASS: current=1912 baseline=1912.
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy astrid/sdk/timeline/inverse.py --cache-dir /tmp/w-7cf930c802/mypy-scoped --hide-error-context --no-pretty
# PASS: Success: no issues found in 1 source file.
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
# PASS: ok runtime.lock.json.
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
# PASS: artifacts.json is current.
git diff --check
# PASS.
```

New tests cover exact full config preservation and absent mirror, strict stale config/registry guards, absence versus empty/null changed heads, changed owner, missing accepted boundary, foreign inverse-stage publication, tampered source digest/effect, intervening ABA and no input mutation. The retained nested eleven and their source file SHA-256 are unchanged.

Development evidence is retained honestly: the initial full captured execute test on baseline produced the original config guard failure (1 failed/10 passed). With the four-line source change the same whole execute passed that guard and failed at a subsequent `parent.occurrences` guard (1 failed/10 passed, `/tmp/w-7cf930c802/candidate.log`). The final positive regression explicitly tests the requested coalescing and exact config/registry guards; it does not claim whole-redo acceptance. Two initial new source-negative assertions did not reach their intended boundary, so they were corrected to use actual tampered effect bytes and a foreign inverse-stage publication, then rerun (4 passed); no pre-existing passing test was modified or weakened. A new-file import-order diagnostic was fixed before final lint.

## Limits, decisions and next steps

The remaining occurrence mismatch is directly observable in the immutable accepted source: the native whole `parent.occurrences` write's after guard has three rows (`occ-film` and two chapter occurrences), whereas the accepted canonical after document has only `occ-film`. The same record contains subsequent per-occurrence removals. This is a different physical collection/aggregate folding issue, beyond the requested parent-registry seam. It was not fixed, bypassed or declared equivalent to the shot-id or nested source causes. Manager should assess it before assigning the one eventual meaningful original-body run. The later failure is a follow-up blocker for complete G5 redo qualification, not for reviewing this isolated registry repair.

No public c271 body, original-body duplicate, preview, localhost/live socket/browser, full suite, P1-P4, native14 or V4 run occurred. No native_restructure or publish migration was added to this base; the G5 draft91ac remains separate. No old-writer fallback, _recording change, forward semantic change, R1/private interface change, C0/wire/CLI/schema/client/pin/lock/dependency change or Git mutation occurred. Full v2 fields/replies remain untouched, but production accepted/merged/preview/error envelopes are not qualified by this focused offline test.

Recommended next step: independent source review of this isolated R2 diff; normal manager-owned merge only after independent PASS. Separately assign the remaining occurrence aggregate source cause, then port reviewed source to the G5 migration draft and authorize its eventual one original-body run. G5 deletions remain gated by P1.

Final SHA-256: inverse.py `fb0cb16bab8a4fbd72a24c9dffadd6992e397925b383ce9ec79f6cc6bbb00d5a`; new regression `ad96279d8cee5bbf1fcf6e0a91f053bb26019ae4096e1c3e2c737fc290882606`; retained nested regression `36e2ea620e558e7516ccf93e0090c65d4f3fa85a3487ecc4c0d001a741b20fa4`.
