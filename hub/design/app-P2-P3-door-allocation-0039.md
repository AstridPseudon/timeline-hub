## Report

Changed only the P2 and P3 rows in [`tests/suites.conf`](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf:75).

- Replaced fixed ports with Node 20 loopback ephemeral allocation via `ASTRID_APP_DIRECT_DOOR_PORT`.
- Allocation validates, closes, exports once, and fails closed before later stages.
- Historical sources, guards, diagnostics, bodies, hashes, and final invocations remain unchanged.
- Outside-row projection remained byte-identical.

Hashes, including newline:

- P2: `ada633…bc731` → `729a79…7446`
- P3: `0d73e0…641ba` → `ab6797…03e85`
- Outside rows: `4e199c…9756` before and after; 462225 bytes.

Validation:

- Outer and decoded inner `bash -n`: PASS for both rows.
- Real outer `bash -c` interception: argc/`-c`/payload byte identity PASS.
- Node 20 sequential/concurrent allocation: distinct valid ports PASS.
- Allocation failure with invalid Node executable: stopped before sentinel stage PASS.
- Ordered stage/export/eval stubs: same port through build/setup/native/list/leaf/body/final tail PASS.
- Fresh-read isolation: only lines 75 and 245 changed.
- App worktree remains clean.

No build, browser, native, backend, journey, service, or full suite was run. Readiness remains UNKNOWN/HOLD as directed; the release-to-bind race window is inherent after closing the ephemeral probe and is not protected by a shared lock.

Commit message and `DONE` marker created.