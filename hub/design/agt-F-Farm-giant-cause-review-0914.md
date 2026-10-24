## PASS — F-Farm-giant causal delta review

Read PLAN §3, commit contract §§1–5, BOARD-HEADER, and reused the authoritative 0904 qualification without repeating its source/rationale/test/JUnit checks.

Source: `astrid/core/execution/generic_host.py`

| Scope | Full commit SHA | Lines | Source blob SHA-256 | Attribution |
|---|---|---:|---|---|
| Last passing | `03ef36fd89c163ba9ec92d3667b895d1fb760546` | 13,998 | `3f00a66bd6104fc2096d27f677343951d384cd17b3be9cf2d54a6921ffa39e07` | baseline |
| Inherited span endpoint | `fb4fd94c1fead8715baea5ca3098ddb2e770efef` | 14,029 | `fc020cc2f6256642203fc4d36a9bb661265fa9a9589d386a46963528d11791d3` | exact span `+242/-211 = +31`; not D40-owned |
| D40 | `f93c69bd70077e52b27b2fb70d04f7be6f19c3d3` | 14,138 | `4cffb180a9e1702ca79d04e152fda09f3b7d13bd0b78203ec44fd33d9febfdcf` | own `+109` |
| D40 | `d367a45c3f74cadd45d437585bc59ee60f60f683` | 14,233 | `189ab8b3798fd487600fc179e12527c3b512f68ea63467075eec8ca297d2c003` | own `+117/-22 = +95` |
| D40 | `429c3e80062c59206fb1078c11ca2acc6b5fc17e` | 14,313 | `b5ad2c6494064ecb5e1c1c1c251b411a39f8b59de3358ddc783a1b1ec6765fd6` | own `+114/-34 = +80` |
| Frozen | `9cd3dbe865a941c052bda04ae0d61306d18f8f26` | 14,313 | same as above | no source delta |
| Inherited U2 | `cb6ce42cc2c0a071554353032a95073f04f72832` | 14,330 | `9a0d3f8e987c043e4dfdb7912e63b228fc6dfeec41d573d92ff31bf4ec8cd11b` | own `+20/-3 = +17` |

Arithmetic verified:

- `31 + 109 + 95 + 80 = 315` → 13,998 to frozen 14,313.
- `315 + 17 = 332` → current 14,330.
- D40-owned total is `109 + 95 + 80 = 284`; the missing 31 lines are inherited history, not a single cause.

Parent checks confirmed merge-parent source blobs: `fb4…` both parents at 14,029; `9cd…` first parent at 14,313 and second at 14,233; `cb6…` first parent at 14,313 and second at 14,114.

Commands used were read-only `git show`, `wc -l`, `sha256sum`, `git diff --numstat`, and `git status`. No tests, probes, lint, typecheck, census, or product edits were performed. Worktree is clean. Commit message written and `DONE` created.