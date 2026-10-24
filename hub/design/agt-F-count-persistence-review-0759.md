# PASS — F-count persistence review

- Baseline: `a3dff9d...`, 261 closed / 6 open; baseline census SHA `22ee4d6d...`.
- Current: 267 total, 262 closed, 5 open.
- Delta: `+restart +two-writer -giant` = net +1.
- 122 mappings: 121 current closures + 1 historical challenged restart.
- All 264 unaffected records, 267 IDs/phases/tags, CSV/JSON parity, proof links, owner/family sums, prior metadata, coverage, mappings, and `CONTRACTINVENTORY` preserved.
- Contract inventory retains the full request/reply requirements and production-caller requirement; evidence remains source-mode/FakeTimelines only, with no complete HTTP/wire qualification.

Current persistence proof: 2 passed in 4.17s, Agent `3f7e63b0...`, Runtime `becfe6db...`; independent named XML SHA `d2699be...`. Both selectors, ten body/assertion AST pairs, source, fixture `848bfb...`, and origins qualify. Restart receives current credit once; two-writer receives separate credit once.

Giant challenge remains open: current source 14,313 lines vs rationale 13,998 (315 mismatch), with author 0742 RED and independent 0733 confirmation. Future docs source `8c5ae21...` has 14,330 lines and passes independently, but is not HOME and receives no credit.

Open five:

1. ThreeJS unsupported-timeline support
2. D23 helper restart “second”
3. Persistence moved-head restart
4. Generic-host reopen
5. Giant-file inventory rationale

Validation command:

```text
sed -n '158,328p' evidence/agent-D32-current-node-reconciliation-H30-limits.md | sed '1s/^```python//' | sed '$d' | python3
```

Result: PASS. No product tests, probes, source execution, full/browser/gate runs, or evidence edits performed. Raw XML is unavailable locally; no local raw parse is claimed.

Five artifact SHA-256 values:

```text
286047a522d61e57f8c46bb655d63d96bd82fd21e6f597fa72a2e017b2552eb2  corrected.json
3ef82fc3c02cc9f0efb4caa5688cbe5475f24cb5313515bea8d9c6efb17cf843  corrected.sha256
131485dd469175ea87437a959be1612863c4bf70ac4718930a06382781fbc5fb  delta-mapping.json
366ed07aa2794f054f176b92e1c77a09d9feb91c0e897730019675508cb5996c  delta.csv
3166d41ec780f32cdb3c11be2a1f7090bfb674254da3b2427e08e0f53f9e7528  limits.md
```

Package SHA: `d1aa34872d19e515861130103f3aa49b1e31b5b170a18ed22fde2893503a92f`.

No blockers. Commit message and `DONE` marker were created; worktree remains clean.