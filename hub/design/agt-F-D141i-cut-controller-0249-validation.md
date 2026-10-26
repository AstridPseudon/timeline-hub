# D141i cut measurement validation

- Independent 0246 command review: `PASS_COMMAND`, terminal exit `0`, exact 0238 wrapper/row/manifest hashes.
- Suite registration: exactly one `agent agent-core-full` row; one line changed; all other bytes/rows preserved. Preimage SHA `f790bcbbcae42eec97eb87734dfa27058c6ff24dc2d4755879002c2f384ab54f`; postimage SHA `8871cb8218c828f74e2ad4a15f385df497f45ff860788b25f98a8fb111cb257d`.
- Normal submission: `request-test integration:agent agent-core-full --no-cache`, request exit `0`; returned service ID `agent-agent-core-full-1026025151-24049` recorded immediately.
- Terminal poll: `wait-test agent-agent-core-full-1026025151-24049` => exit `78`; status `fail`.
- Terminal log: `REFUSED: controller admission disk floor not met: 4687142912 < 4700000000`
- Source/command/row/positive/poison hashes are retained in `receiving.json` and `result.json`.
- No local pytest, collection, body execution, install, retry, or alternative environment was run.
- No REG/nonREG conclusion; no ship credit.
