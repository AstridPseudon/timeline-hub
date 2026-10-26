# D141 popup identity correction validation

Status: `PASS_IDENTITY_CORRECTION`. This is a read-only metadata derivative. The six original 0232 artifacts and the related 0226 source map were not rewritten.

Commands and results:

- `git -C /home/user/peteromallet/astrid-agent rev-parse 070dfc5e^{commit}` — PASS, resolved to `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2`.
- `git -C /home/user/peteromallet/astrid-agent rev-parse 070dfc5e^{tree}` — PASS, resolved to `6056414359ae9fce08d999d54cbecf719fda33c3`.
- `git -C /home/user/banodoco/reigh-app rev-parse <commit>^{tree}`, `/home/user/banodoco/banodoco-workspace-runtime`, `/home/user/peteromallet/timeline-composition`, and the Agent checkout — PASS for every current, last-pass, author-run, service, activation, and layout tuple emitted by `source-manifest.json`.
- `git -C /home/user/banodoco/reigh-app rev-parse <commit>:<path>` — PASS for the popup spec blob, readiness spec blob, five canonical caller/renderer blobs, and ten changed activation/layout blob values. The popup spec blob is the full Git object retained as `d7da4c234fb921c448bc18e9ac174b1a11dbc4a6`.
- `sha256sum` of the Git-rendered popup and readiness specs — PASS; popup `09f5e2c2ea2a207575534a88adf2847d68cdd389caa5d145580100f21302b2b9`, readiness `2b9723db262978ebbb410d5925163fe61c4a83f05f3b44fbbd524bc9df301593`.
- `tar -xOf /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-pin-96d4754b-d73-p2-96d4754b-submit-1025100712-15203/d66.tgz d66/manifest.json | jq` — PASS; retained 15203 manifest agrees with the corrected four-way tuple. Archive SHA-256: `8d655157f6e1040c9c2d35fed9a604d2887158d28baf2fa9504233ce6e3020d7`.
- `sha256sum` of retained actual 1368 `manifest.json`, `p2-popup-add.xml`, and `readiness.xml` — PASS; hashes are recorded in the corrected source manifest.
- `jq empty` on the two emitted JSON files — PASS.
- All emitted corrected Git IDs have 40 hexadecimal characters; all emitted SHA-256 values have 64 hexadecimal characters. No nonexistent Agent `...fbd3` value remains in the corrected source manifest; the old value is retained only as an explicitly named `old` value in `correction.json`.
- Hashes of the six original 0232 files were read after generation and remain available in the worker log; no original file was opened for write.

The task brief stated an Agent value ending in `...fbd3` as the expected result, but the exact Git checkout and retained 15203/19078 manifests resolve `070dfc5e` to `...fbd2`. The derivative follows the independently validated Git object and records this discrepancy rather than emitting the nonexistent object.

Not run by instruction: product tests, imports, tsc, lint, browser/live-socket runs, collectors, retries, source investigation, or any product/test/fixture/schema/pin/registry/queue/hub/Git metadata change.
