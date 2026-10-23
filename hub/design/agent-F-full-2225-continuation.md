Qualification passed. **The single authorized full run is still running; continuation is required.**

Only the durable harness and two new suite rows were added. Existing rows remain byte-exact. Product, tests, guards, generated files, profiles and pins were unchanged.

- All **76 preflight checks passed**, including private generator/source-binding reproduction, the exact four registry hashes/state hash, 21,501 read-only non-registry files, 33 internal links, and 80 archive-installed package files.
- Exact positive qualification passed. Wrong registry hash, missing registry, fifth file, writable non-registry file, foreign symlink, stale TMPDIR, bad launcher hash and wrong executable controls all failed as required.
- Full-body SHA256 remains `5ebb51b8d7100a60658595176fac538d8248e9e2a85e082dc7c7feffd16bec71`; execution remains `pytest -q -n3`. Six boot probes were not repeated.

With `$O` denoting the supplied orchestrator directory and `$W=$O/workers/agt-F-qualified-full-sol-2225`, commands included:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$W" python3 -P "$W/profile_controls.py"
PYTHONDONTWRITEBYTECODE=1 python3 "$W/controls.py"
/bin/sh -n "$W/launch.sh"
/bin/sh -n "$W/full-body.sh"
"$O/bin/request-test" integration:agent preflight-post-g5-2225 --no-cache
"$O/bin/request-test" integration:agent full-post-g5-2225 --no-cache
```

Preflight **`agent-preflight-post-g5-2225-1023222735-20917` passed**, exit 0, in 17 seconds. Full **`agent-full-post-g5-2225-1023222822-25691`** was recorded durably before waiting.

At **22:54:03Z**, full progress was **71%**, with **169 observed failed phases across 169 nodes**:

| Observed diagnostic | Count |
|---|---:|
| Missing child `runtime_protocol` import | 63 |
| Other assertions/exceptions; cause unconfirmed | 70 |
| Retained tests invoking retired `--native` | 18 |
| Missing files/outputs; cause unconfirmed | 6 |
| Isolated child missing `astrid` | 9 |
| `FakeCheckout` missing `path` | 3 |

[Every observed failure and traceback](../../../tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-qualified-full-sol-2225/failure-inventory-current.json.gz) is retained alongside compressed logs, manifests and origins; durable storage is approximately **25 MB**. These are interim counts, not terminal suite counts.

Controller and three worker **before origins passed**. After origins, whole-profile/source comparisons and final failure classification remain pending. Historical creator and original complete-byte identity remain **UNKNOWN**. D14/D23/H9 remain unchanged and unskipped; no full PASS or extra deferral is claimed.

Resume **the same ID**, without resubmitting:

```bash
"$O/bin/wait-test" agent-full-post-g5-2225-1023222822-25691 1
```

[Continuation state](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-qualified-full-sol-2225/continuation.json) lists outstanding checks. Commit message written; `DONE` withheld because the full run remains active.