Ask: Agent uses the exact per-node extracts for D48 accounting; no repeat farm run / Owner: Agent / By: 2026-10-24T08:00Z

Done by worker tf-trace-export-0705 (read-only; no test, build or probe). Source log tests/agent-full-farm-1024050351-26511/log.txt, SHA256 06d435fed2622a4d9a8680e1071a650d5e34272090b08af5fe3ba0bd274dea06 verified first. Run subject: Agent 9cd3dbe8 / tree 57f0231d, Runtime 45c3a7f4 (unchanged, non-gate).

Counts: closed-historical farm-FAILED 88/88 found, closed-newer farm-FAILED 8/8 found, errored 187/187 found; 0 UNKNOWN. Matched by full id; every short name was unique. The 7 summary failures with no FAILED line are NOT identified or invented.

Published (design/farm-trace-export-0705-<name>): failures-closed-historical-88.txt (742107 B, SHA 597c7445...7563), failures-closed-newer-8.txt (43677 B, SHA ff2fa869...5e21), errors-187-causes.tsv (51267 B, SHA 309fc843...7c51), extract-manifest.json (78899 B, SHA dad95d48...e7), with per-node byte offsets and line ranges in log.txt. Full sections, no truncation, no redactions (secret-pattern scan found none).

Literal exception counts (quotes only, no cause analysis):
- 187 errors, first E line: 47 ImportError cannot import name external_pack_sources from runtime_protocol (rt-pin-45c3a7f4); 33 KeyError ASTRID_REMOTION_PROJECT_DIR; 33 requires provisioned renderer peers; 29 no Node v20.19.4 for the renderer (found only v22.22.0); 42 missing provisioned peer .../remotion/node_modules/react; 3 FileNotFoundError .../runtimes/agent-remotion-composition14-255b6856.
- 88 historical, last E line: 35 ModuleNotFoundError No module named runtime_protocol; 12 RendererInternalError renderer command exited with status 1; 8 capability 'unrelated.calculate' child exited 1; the rest a long tail of 1-3.
- 8 newer: 7 end with a CompletedProcess(... '-I', '-c' ...) exit 1 line; 1 is the external_pack_sources ImportError.
