# R2r sequential causal recovery — Runtime-owned failure reproduced offline

Runtime base: `85b2feeb58bc54174ac7b89fda4805883865d3b2`. Agent: `67ba416bca813f4931b557f6f2ca2abf935d7d35`. No product edits or new service writes/body runs.

Both moved captures (12, 17) pass the unchanged test's binding digest comparisons using actual Agent `execute` on retained `source_closure`; current captures (03, 07) pass too. Repeated `commit.read` entries are not the cause.

The captured merged result is accepted at the private port, but subsequent durable history verification calls `timeline_commit_store.py:255` → `timeline_commit_auth.validate` without `base` or `sequential`. The stored submitted second-step patch/read still names its original unlanded intermediate image. The accepted-history continuation map has only the genuine peer edge, so it cannot resolve that original intermediate image at the landed command input.

Offline history-validation reproduction: both moved cases raise `CommitRejected('provider alias is outside its authenticated boundary')` at `timeline_commit_auth.py:173`. Capture 12 reaches this through `validate_step:399` (submitted patch); capture 17 through `validate_step:329` (submitted declared read). `_verify_accepted` catches it at store line 296 and raises `ProtocolError('accepted commit record is corrupt')`. Current captures pass this validation.

The original pytest longrepr and post-acceptance document/history/retry reads were not captured. Therefore this is a reproduced deterministic source-path failure, not a recovered historical pytest traceback. Exact original first-failing test line remains to be established from source-path execution; no missing database/head state is invented.

The task prohibits history-authority edits. A safe correction must preserve independent reconstruction of original and landing inputs on historical verification. Merely retargeting submitted refs, dropping claims, trusting provider snapshots, or adding an accepted edge for the original unlanded intermediate is disallowed. No original-nine retry is authorized without a meaningful safe source correction.

Complete twenty captures are exported losslessly as flat hash-named JSON files next to this report. Source/log snapshots are included. A manifest, credential scan, and detailed per-assertion comparisons follow in this worker's final update. Retained 1512 evidence remains untouched. Retained qualification was 353 Runtime tests/44 verifier tests, Ruff22/Pyright80 baseline identities with 0 added; not rerun and not a 9-PASS claim.
