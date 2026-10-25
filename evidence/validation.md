# D141 independent review validation

## Commands and results

- `git show 1de87d66097b3e17c684f18674870e556cfcbc99:evidence/recipe.sh | bash -n` — PASS, exit 0.
- `git show 1de87d66097b3e17c684f18674870e556cfcbc99:evidence/preflight-inventory.json | python3 -m json.tool` — PASS, exit 0.
- `git show 1de87d66097b3e17c684f18674870e556cfcbc99:evidence/source-manifest.json | python3 -m json.tool` — PASS, exit 0.
- `git diff --check c585cb2aa73c5298d474e614cb2144f58f27e605 1de87d66097b3e17c684f18674870e556cfcbc99` — FAIL, exit 2: `evidence/notes-input.md:244: new blank line at EOF.`
- Read-only `git show -s --format=%H/%T` for all four frozen tips and `git remote get-url origin` — PASS for all four exact commit/tree/origin tuples.
- Read-only `git cat-file -e <frozen-agent>:<path>` — PASS for the five named absent roots and D73 source absence; additionally confirms the three original P4 source paths are absent.
- Read-only current launcher inspection — confirms self-location guard and `original_p4_test_hash` guard; launcher SHA-256 `9f668e398b1ea4cce48a6c610102723e0a3dab27a764be4191015aa7fc4110cd`, Git blob `f1bde17ea107a8b669cb6924fbdbd2f3979da988`.
- Read-only Python set comparison of controlling D134 root JSON/TSV versus prep notes — PASS: 52 groups, 370 ID tokens, 370 unique IDs, no missing/extra/duplicate IDs; all group metadata matches.
- Read-only exact slice comparison — PASS: managed105/root-019 = 105, media48 = 48 and is a subset, CLI22 = 22, fork18 = 18, identity16 = 16, selectedPARAM14 = 14, legacyword35 = 35.
- `sha256sum` checks for D134 root census, per-ID TSV, root-review-2029 inputs, D134 command1848, D141 cut docs, current launcher/maker, and retained stub — PASS; values are recorded in `source-manifest.json`.

## Not run

No pytest, import, provider, collection, control, suite, body, acquisition,
checkout creation, installation, Store/Git write, browser, socket, or live
request was run. The review does not claim a pristine comparator result.

## Disposition

`FAIL`: documentary conservation is largely sound, but the exact prep commit
has a whitespace failure and its advertised operational controls/guards are
incomplete. `NOT_READY` remains fail-closed; no proof, REG, core, or ship
credit is retained.
