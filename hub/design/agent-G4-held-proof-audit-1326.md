# G4 held-image proof audit — 1326

## Finding

**PASS for the bounded qualification evidence.** The completed 1320 run is
anchored to Agent `f6116e1b658514021cbbf08d5a6f16a240523f1a` / tree
`26f260e0674161f9f786bf93b15a1477a5e63a86` and Runtime
`8592822fd11275540f596562f43c715676f2bc0f` / tree
`ed9856f43a4e44a058bf2230badea2c4c7080050`. The current Agent and pinned
Runtime worktrees are clean. No material misload or guard gap was found.

The exact target test blob is Git blob
`94de6273cb814b77f9963418da59a8af6e2668d1` and SHA-256
`8ed89876247cdf08f167b750d1bc2b9047917a04cf27b5cb6f476027add9fe15`.
Collection produced exactly four cases: image ADD, image SWAP, and the two
parameterized video-hold refusal controls.

## Evidence audit

The durable captures are unchanged:

| Case | JSON SHA-256 | Result | History | Bindings/effects |
| --- | --- | --- | --- | --- |
| ADD | `05b291c550fd9b3dd4e78032095d7500b1f021462f96b2b94ec7e01d72e3fcea` | accepted `occurrence.add-media` | 2 → 3 | 13 / 5 |
| SWAP | `86c684dd49bf2de05d7421040d5e8f76ca85e32879a103ca82e716f0b6ec53d9` | accepted `occurrence.swap-media` | 2 → 3 | 13 / 5 |

Offline checks confirm, per case, the full v2 request shape and base pair,
command/step preservation, nested complete receipt/result, canonical output
equality, history append/head, stored bindings/effects, and dependency
manifest. The canonical rows retain literal `clipType: hold`, `hold: 2`,
`params: null`, and opaque `[null, false, {"keep": null}]`; SWAP retains old
and new physical image assets. The common 68-byte PNG digest is
`431ced6916a2a21a156e38701afe55bbd7f88969fbbfc56d7fe099d47f265460`.

The qualification's reported commands were **4 passed in 11.05s**, followed by
the unchanged evidence-producing rerun **4 passed in 12.08s** with only
`ORCH` supplied. Those two runs are disclosed and not double-credited.

The test source asserts dry-run `receipt is None` and unchanged database dump;
the two video controls assert Runtime 422 plus unchanged history and database
dump. These negative claims are supported by the source and durable run
log/report rather than by positive-case JSON files. The report does not invent
`preview.would_status`: it was not serialized; only null receipt and no-write
were observed.

## Provenance boundary

The captured per-case JSON records the Agent module origins for `commit.py` and
`native_occurrence_media_commands.py`. Runtime module origins are recorded in
the qualification preflight table and resolve offline from the pinned Runtime
to these exact SHA-256 values:

- `service.py` `267bec1aee551e7ea1f92f987adb24268be11c6dd165ee56f24aa68ff2b6a692`;
- `store.py` `578dd8f075a9d0ab05554e30b48434444c9777ede09379b9e2814a5fbd61c30c`;
- `timeline_commit_port.py` `d78dd313220634baaf37c9a6cb7a578b4453c3c94060eb13c02778834eeac867`;
- `timeline_commit_provider.py` `2dff389a11475420395a812d036888ad91c01e16df1170bb77917cc3cf128faf`.

The producer worktree path embedded in the JSON has since been cleaned up, so
the historical Agent origin paths cannot be re-resolved directly. The clean
f611 source files match the recorded hashes. This is an ordinary custody and
granularity limitation, not a material execution misload.

The local authenticated inverse restoration remains distinct from public
Runtime whole-commit undo; neither is conflated here. Broader G4/P2/P3,
whole-undo, leaf inverse, full/browser/HTTP/P1/P4/native14/58/D17 reruns remain
outside this finding.

## Checks

- Offline JSON/hash/source audit: **PASS**.
- Offline module-origin/hash audit: **PASS**.
- Exact target collection: **4 tests collected in 0.24s**.
- Reused prior independent evidence: 66 recipe cases, Ruff `2149/2149`,
  private mypy `1912/1912`, and current 83-case integrated evidence.
- No product/test/config/schema/generated/pin/dependency/evidence changes.

Recommended next step: consume this as bounded current-Runtime held-image
readiness evidence while retaining the explicit Runtime whole-undo/local-
inverse and broader P1/P2/P3 boundaries.
