# D141c handoff

Finite per-ID pristine result is ready for Main and Farm.

- Request: `agent-d141b-pristine-comparator-2358-1026003644-27388`.
- Source authority: actual pristine Agent `8b6ed2116fd1803d24b2be5bc08bd9490407fe4a` / tree `0a3691a49b63fd7b0c22fb3478e9cf1947f266ed`, Runtime `fa9cd5464a8b37b02f971de375e56be846cd69e2` / tree `124e10dbcd54fb90219e783ec11aa34f8c91590c`; all four before/after source witnesses are clean and byte-identical.
- Counts: 3255 raw total, 4 FAIL, 1 ERROR, 0 SKIP, 3250 PASS after explicit 3077 concrete testcase PASS + 173 subtest PASS accounting.
- Five bad IDs are in `bad-nodes.json`. Four are environment-type and require exact-selector matching Farm-child reruns before REG classification. One timeout is UNKNOWN with a finite missing-cause statement.
- `per-id.json` preserves every concrete XML testcase ID, original testcase attributes, status/type/time, safe message fields, and per-record hashes; it does not publish tracebacks or private payloads.
- `source-manifest.json` preserves product cut identity, actual pristine source identity, interpreter, exits, disk, artifact hashes, and the central-log/raw-stdout distinction.
- This packet makes no behavior, REG, or ship claim. Do not infer one until Farm supplies matching per-ID results and the required environment reruns are complete.
