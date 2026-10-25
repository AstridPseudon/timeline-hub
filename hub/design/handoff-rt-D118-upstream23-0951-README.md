# Runtime D118 upstream23 handback

Ask: Consume this D54a proof for the exact 23-node Agent scope.
Owner: Runtime (D118), with Agent owning the seven source-absent nodes.
By: 2026-10-25T09:51Z handoff; central run completed at 2026-10-25T09:56Z.

The authoritative source audit against pristine Agent `08e6b905114a3ee2b05c3e7980421f26b4abf15c` finds 23 requested nodes: 16 real upstream counterparts and 7 absent after function/name/body matching. No missing node was installed into upstream. The paired pristine Runtime is `d4f496ec4fbcae7a1f3a51d47ed5147c561117ad`.

The normal central targeted route ran exactly the 16 runnable upstream counterparts with `-q -n 3 -o addopts= -p no:cacheprovider --timeout=45 --junitxml=...`, no test exclusion, skip, xfail, or timeout weakening. Result: 15 PASS, 1 FAIL, 0 ERROR. The render MP4 counterpart fails at the renderer command with status 1; it is not treated as the same D54a failure because the actual upstream exception/location pair does not match the current handoff pair. The 15 passing upstream tests are current-only failures (`NEW-OURS`); the seven absent nodes remain `NEW-OURS`; the render row is `UNKN` pending a stable exception/location pair.

The first run exposed a child import-provenance problem (`runtime_protocol` missing). It is retained as `first-run.xml` evidence. A private overlay of symlinks to the two pristine checkouts was then admitted through the upstream environment policy; child-origin evidence proves the rerun used only the pristine Agent/Runtime sources. The shared venv probe records the current editable Runtime and confirms it was not admitted.

No production source, test, pin, generated file, or product C0 path was changed. Historical 924-runtime isolation remains uncertain outside this exact 23-node replacement scope. This is not a broad regression, core-zero, or full-suite claim.
