# FAIL — P2 SWAP3250 protected source review

Reviewed `tl/rt-P2-SWAP-3250-tags-1426` at `938aa54e11`; no code/test edits made.

Findings:

1. `RuntimeHandler._request_id()` caches the ID on the handler instance (`runtime_protocol/server.py:95-102`). `BaseHTTPRequestHandler` reuses that instance for keep-alive requests, so subsequent requests reuse the first public ID and correlation hash. Socket-free control reproduced this.

2. The provider-unavailable path emits `self._request_id()` directly as the private diagnostic ID (`server.py:302-307`). A valid 32-hex public ID is therefore logged raw, with no `public_request_id_hash`. Control reproduced both conditions.

3. Ruff has one new baseline delta: current 38 diagnostics versus parent 37, caused by import ordering at `service.py:2490-2502`. Other diagnostics are inherited.

Tag census passed: distinct `provider_history_guard`; 31 store tags; projection tags `store_reference_projection_prepare_history` and `store_reference_projection_apply_history`; six port tags. Remaining lumped history emitter: `history_provider_or_store_guard` for unmapped history refusals.

Evidence:

- Required test: `7 passed`.
- Adjacent tests: `34 passed`; one door test blocked before execution by sandbox socket permission.
- Compile: passed.
- `git diff --check`: passed.
- Nested context/thread controls: passed; no context leakage.
- Packet consumed; native replay not run because disk remained below the 5 GB requirement and the packet lacks complete native request history.
- Relevant refs identified without attributing root: `tl/rt-P2-swap-source-2308`, `tl/rt-P2-SWAP-native-result-review-1122`, `tl/rt-P2-SWAP-native-prep-1440`, and the reviewed 3250 branch.

Recommended next steps: make request IDs request-scoped, generate a private ID on the unavailable path, fix the added import-order diagnostic, then rerun the central live/native checks.