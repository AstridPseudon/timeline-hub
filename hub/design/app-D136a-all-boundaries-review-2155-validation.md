# D136a independent review validation

## Read-only checks

| Check | Result |
|---|---|
| `python3 -m json.tool` on input `review.json`, `table.json`, `source-manifest.json` | PASS |
| `table.json` summary count and boundary array length | PASS: 45 |
| final-row count and selector mapping | PASS: 9 final rows; 3 standalone plus 6 parametrized values |
| SHA-256 of all manifest-listed Agent files | PASS |
| SHA-256 of all manifest-listed Runtime pin files | PASS |
| assigned worktree `git status --short` | PASS: clean |
| assigned HEAD/source identity | PASS: HEAD `8b13a9829989150ac0387c31559c5d54d386cc57`; tree `897c318f237fbb78bebb3185c133f43ffc4fa38e` |
| Runtime pin identity | PASS: `ab1e4f6141987706132916e2da16477f5a019464`; tree `7d8e77b2f5a4af79305c9212ce5174d3ea9fd657` |
| focused Python AST parse of cited Agent/Runtime Python files | PASS; parse-only, no imports or execution |
| source diff | PASS: no source changes made by this worker |

## Custody observations

The supplied input manifest records joined source tree `0b66c7a0c1b1af0400055cce16827e42a2908dd9` under the review head `8b13a9829989150ac0387c31559c5d54d386cc57`. The actual review-head tree is `897c318f237fbb78bebb3185c133f43ffc4fa38e`; `0b66c7a0...` is the joined-source commit tree. The corrected worker manifest records both values. Listed file hashes match.

At pristine `886a3183bd4a4a44f0a2c08fabec4e8edcbf7b55`, `astrid/core/timeline/authoring_bundle.py` is present, while the joined D136 test and authoring-commit files are absent. This is source absence only and is not used as an upstream behavioral result.

## Reused dynamic evidence

The exact final20db original9 result is reused: 9 collected, 9 setup errors, 0 failures, 0 passes, 0 skips, exit 1; common refusal at Runtime `timeline_commit_auth.py:2209`. No rerun or raw XML/log/payload export was performed.
