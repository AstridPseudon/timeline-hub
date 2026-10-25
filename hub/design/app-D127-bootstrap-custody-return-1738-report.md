# D127 report

Recovered and independently qualified the retained 1731 bootstrap result.

- Exact App source verified: commits `9bf465…` and `54c91d…` share tree `7be73e…`; target SHA256 `92586e…`.
- Retained selector: `P2 Runtime observer bootstrap` — exit 0, 1 passed, 4 skipped, 0 failed.
- Agent/Runtime commits, interpreter paths, module origins, and helper SHA256 `4ee042…` were verified.
- No code changes or tests were run by this worker.
- Required evidence files were created and JSON-validated under the absolute `evidence/` path; `DONE` created.

Important limitation: the original `1731/evidence/` directory, selector log, helper copy, and JSONL capture are absent. Event count, mode, capture hash, phase/lifecycle, and privacy results are therefore retained-log assertions—not current raw-capture custody.

No commit needed.