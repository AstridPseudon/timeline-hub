# U4a / U2 D141 final provenance validation

Status: `PASS_SOURCE_TOOLS`

## Exact source receipt

The normal queue/done receipt names `/home/user/work/wt/rt-pin-6a011d58`.
The checkout was verified clean at Runtime commit
`6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d`, tree
`ac5b862744bece65b2e30565db1777bacd60da28`. The Runtime board records
independent reviewed tree `24107e83b0`, 119 targeted passes, and frozen
`fa9cd5464a8b37b02f971de375e56be846cd69e2` ancestry.

## Commands

| Command | Exit | Result |
|---|---:|---|
| `PYTHONDONTWRITEBYTECODE=1 python scripts/refresh_runtime_client.py --producer /home/user/work/wt/rt-pin-6a011d58` | 0 | Normal producer selection and staged re-vendor completed. |
| `PYTHONDONTWRITEBYTECODE=1 python scripts/vendor_lock.py update runtime.lock.json --producer /home/user/work/wt/rt-pin-6a011d58` | 0 | Direct requested normal update completed. |
| `PYTHONDONTWRITEBYTECODE=1 python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-6a011d58` | 0 | Vendored bytes match the exact producer manifest. |
| `PYTHONDONTWRITEBYTECODE=1 python scripts/vendor_lock.py check runtime.lock.json` | 0 | Local consumer lock check passes. |
| `PYTHONDONTWRITEBYTECODE=1 python scripts/artifact_manifest.py --check` | 0 | Agent artifact manifest is current. |
| `git diff --check` | 0 | No whitespace errors. |
| `python -m json.tool runtime.lock.json` | 0 | Lock JSON parses. |
| `python -m json.tool artifacts.json` | 0 | Artifact JSON parses. |

## Scope and preservation

The cumulative working-tree diff versus `aa5a91a618f4d28308772169bc08e8e79274cd6a`
contains exactly `artifacts.json` and `runtime.lock.json`. The only generated
artifact change is the approved `am-footage/component.tsx` digest and derived
Agent manifest version. The Runtime lock changes only producer provenance;
all 15 canonical mappings, hashes, consumer bytes, and modes are unchanged.
No product, test, fixture, client, schema, chat bundle, source producer,
shared dependency, or hub file was changed.

The prior independent review `agt-U2-D141-final-review-2357` remains retained
as a failed record: its stale `fa9cd` producer check, stale artifact check,
incomplete Python lane, and environment/incomplete chat findings are not
rewritten or reclassified here. This validation proves only the requested
source/provenance gates; it makes no full-suite, provider-cohort, or ship claim.
