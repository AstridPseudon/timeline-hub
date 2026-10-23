OPS-bench-store lease1918 caller boundary, 19:20Z.

Prepared all prior 21 fixtures plus faithful custom absolute managed-path regression, conservative-lease control, and row removal/tamper after lookup cases (24 total). Waiting for final core1915 export/hash; no core changes requested or made.

Source concern: unchanged suite_lease checks current_command after lookup only when names is empty. Core1915 conservative names are nonempty, so custom row removal/tamper between lookup and acquire can pass the caller boundary. Pending final-core reproduction; if confirmed, lease1918 will narrowly recheck raw command INSIDE acquired lease before yielding. No API or core implementation change needed. Prior empty-name diagnostic against immutable core1854 correctly refuses both races; this is not final qualification.

All original exports immutable; only new lease1918 prefix is written. No combined creator, chmod, host/service, or readonly lifecycle run.

FINAL: core1915 SHA256 88ae9e5af3425639b7eba0b79aa6b84e78a319fe810c0c6a2d3ceece1be8b5f3 published. Row removal/tamper race reproduced (2 failing subcases); fixed only in lease1918 caller with 2-line acquired-lease row check. Final 24/24 PASS, 8.643s. No unresolved API need; no core change. Independent review next; overall installation unqualified.
