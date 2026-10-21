# Gate7 current extras actual-tree dryrun report

The single central `delivery-owner-extras-actual` request
`rt-m4-gate7-current-extras-actual-tree-delivery-owner-extras-actual-1021013933-28953`
ran the installed reviewed carrier with both required guarded `--extra`
arguments. It finished exit 1 after 184 seconds. The builder retained
`delivery/build-20261021T013934Z` with 12 files and wrote no ZIP.

The tuple printed immediately before the request was:

| repo | commit | tree |
|---|---|---|
| Agent | `57d6635616f2982b814cfcc059b670ea1a7c9f2c` | `0174fd49bd175a726a44542d1d6e31bca13c0f02` |
| Runtime | `9d1c43c647301da48a6e86ad82e466b501bd2418` | `50e74e3243c5da4cf77b6e6cc76605fae8aeb649` |
| App | `813a85106ecb4abbaf224081abe6c33b8dab0df7` | `2a19a78bb1bdfb3fd779f568a1b513b094318982` |
| Composition | `4788e107f183e0523a740b691a20eb8261d7183c` | `585e8c4784ee78ccbfbff4b6ce26f577b8eda05e` |

Builder verification passed Agent, Runtime, and Composition patch/bundle/tree
equality. App patch/bundle/applied equality also passed for frozen tree
`2a19a78bb1bd`, but the builder’s required source identity recheck failed:
App moved from `813a85106ecb4abbaf224081abe6c33b8dab0df7` to
`692765846fef511047445fecef3e55ec8bb6a5bf` during the run. The staged
`SHA256SUMS` verification passed for all 11 non-self members, and the extras
retain hashes `204a7aac...c93ee` and `969fe303...da220`.

The remaining gap is therefore a concurrent source-ref mutation, not an
extra-carrier or tree-equality failure. Post-run inspection also found Agent
advanced to `859d662f6f0cbe4a75b3d56c712b4f99edaad741`, so no repeat is honest
without a new source freeze. No retry, final ZIP, owner-film scan, browser or
render run, macOS check, physical parity check, or Gate7-complete assertion was
made.
