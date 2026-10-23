# Agent G4 corrected-current handoff

Prepared from `d32744b33d4a87557d50b085557f11fe8abd02d2` with dispatch merge parent `ecea7d8563c93059283ef9475ecb41a37e628a38`.

The parent diff was applied to all non-writer paths. Current G4 `publish.py` and `timeline_elements.py` were retained, including narration’s `TimelineSession.submit`/durable-flight retry, exact UTF-8 source custody and inverse/opaque preservation, and the production element source/retry/submit path. Parent emitter/step-undo/G3-R2/R3/client/lock additions were preserved verbatim. Runtime lock source is `780da6d605033ca71dbe2ad48c10ec2870ea4865`; all 15 mapped files and `runtime.lock.json` match the parent. Approved six V4 live-scenes deletions remain absent.

Evidence: targeted non-integration lane **237 passed, 2 deselected**; vendor/artifact tests **24 passed**; Ruff baseline **2150/2150**; private mypy baseline **1915/1915**; vendor lock and artifact manifest checks passed; compileall and diff-check passed. A live-socket integration test was not claimable in the sandbox (`PermissionError` on localhost bind), and no full/browser/P5 wire suite was run. See the worker report for exact commands and details.
