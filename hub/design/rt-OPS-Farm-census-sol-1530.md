# rt-OPS-Farm-census-sol-1530

Actual Farm census: **EXACTMISSING**. Diagnostic fitness: **partial source diagnostic, independent review required**. This supersedes neither original review nor its evidence. It does not establish a complete refusal set, authorize a narrow fix, or authorize a build/reissue/body.

The installed sources remain pinned to:

| Source | SHA-256 |
| --- | --- |
| make-child-venv | e62f89eaf226897a36bd4c7f715d43a7a1d4206ff371432296c01de6bdd52dc3 |
| bench_store.py | 7d5870433a76b7a611703f47a385cba9584f7213fe4b8a27005317f27bf26495 |
| verify_dependency_seed.py | 116b4e6bcb791d08e6c3c548f7fb52c52e9225b9428d7e201c09b02160d7bfe2 |

`rt-OPS-Farm-census-sol-1530.py` captures and verifies those bytes before execution and checks the files again at completion. It never edits the maker. A subsequently installed retention variant must not be silently accepted as e62f. Use the preserved, exact authenticated preimage as the diagnostic's `--maker`, with the matching Store/dependency source files beside it; source mismatch refuses the run.

## Source-backed reachable call graph

These are source locations in the exact pinned files, not regex matches or claims of executed coverage.

1. Maker `STORE_PY` (211–312) authenticates the dependency helper through `bootstrap_key()`/`seed_module()`. For Farm, `farm_inputs(schema_source, bootstrap_archive)` validates the selected schema and original wheels before `Store(...)`, binding `bootstrap_authority` and `farm_authority` into the child identity. `farm_inputs` (dependency 389) calls the authenticated Farm component and extracts original wheels into a temporary directory. This is an actual prerequisite, not an unrelated preparation API.
2. Normal maker calls `Store.ensure('child', identity, registration, build, verify, seal=...)` (444). `ensure` (Store 650) enters `mutex`, `_load` → `_validate_index` → `_validate_entry`/`_owned_dir`, `_verify_projection`, eviction/reserve/journal handling, and build or reuse. The full Store file's 121 static checks are not all registration-verifier checks.
3. During the seeded build, `STAGING_INVENTORY` (maker 672–699) authenticates the helper. With Farm authority, `retained_farm(stage, authority)` runs **before** embedded verification. Then it runs exact `STORE_VERIFY` with `--staging` and the receipt's schema source, captures its JSON inventory, and invokes dependency `main(local_inventory=...)` with the retained seed, committed lock, maker interpreter, bootstrap root, and installed root.
4. Embedded `STORE_VERIFY` (maker 772–1078) checks physical ownership/traversal/interpreter/layout/origins, commits' archived source, distribution identity, source carrier/archive hash, every local RECORD row's digest/size/ownership, authenticated `licenses/LICENSE`, source modules/bytecode/console wrappers, overlapping ownership, canonical client bytes, installed package files, closed retained source directories/files, source/client markers, metadata and the exact report. Its schema argument is **`242f9c4306bf3b501222cb041a9eb246ef47bc85:packages/timeline-schema/python`**, including the subtree. `committed_files()` and archive comparisons preserve that argument exactly.
5. Dependency `main` (868) authenticates the committed lock, exact wheel set/tags/hashes/archive identity and retained bootstrap, then calls `installed_integrity` (561) with the **in-memory authenticated local inventory**, never an on-disk allowlist. That function reaches retained Farm authority/schema archive/test-wheel binding, venv source files, `store_metadata` (529), exact dependency distribution/RECORD/metadata/installed bytes and closed whole-root ownership. These paths cannot be credited when the embedded inventory or Farm/bootstrap authority is unavailable.
6. On normal publication/reuse, maker `verify` (372) runs retained Farm verification, the same embedded verifier without `--staging`, marker comparisons, seeded installed verification, `report_bytes`, and the child-Python `IDENTITY_SCRIPT`. The registration callback (425) then binds the verified report and suite; Store `_registration` (626) checks dependency references/report/name/hash and projection invariants before mutation. The diagnostic never invokes child Python or registration.

The reviewed retention-mode candidate is owned separately by 1521. Its source shows staging retained at `bench-store/staging/<key>`, with a sibling `<key>.diagnostic-retention.json`; it intentionally does not publish/index that stage. Therefore **a stage must not be required to appear as exactly one indexed final entry**, as 1516 did. The stage's owner/key/bootstrap binding belongs to dependency `store_metadata`, after its real authority prerequisites. An index entry or inode synthesized from current filesystem state would invent authority. The retention receipt alone is not that missing authority.

## What this diagnostic actually executes

- For every bounded retained node, it evaluates the **unchanged AST predicates from pinned `readonly()`**, independently: owner/hardlink, the exact `lib64 -> lib` exception, then type/symlink/writable. This accumulates independent failing paths without changing `fail`, continuing a failed production verifier, or importing installed child code. `--staging` preserves the production staging mode's writable-mode rule.
- It attempts the complete, unchanged embedded verifier once, retaining its original first-refusal semantics. A trace records actual `fail()`/Store `check(False, ...)` calls and available caller paths. Trace function names/lines are observations, not branch coverage.
- Independently it executes exact pinned Store construction, `_load`/index/entry ownership and, only after successful index validation, `_verify_projection`. Those reads do not acquire a transactional consistency guarantee.
- The exact license policy is exercised against authentic/changed/extra metadata in private fixtures; that is **fixture evidence only**, not Farm license coverage.

Every blocked downstream scope is `SKIPPED` with a prerequisite reason. This task prohibits Git/subprocess helpers, live locks/writes and installed-code execution. The diagnostic accordingly stops an exact embedded attempt that reaches `committed_files` at its subprocess boundary; it does not substitute unauthenticated retained source bytes. Store mutex/lease ownership contexts require writable handles. Farm `retained_farm` reaches temporary extraction. Full dependency verification needs the successful embedded inventory plus Farm/bootstrap authority. Child freeze verification executes child Python. These scopes are explicitly incomplete. Mutation bodies (build, eviction, journals, publication, recovery and projection writes) are out of scope, not extra checks required to reach a static total.

**This is intentionally not certified as an all-refusal census.** A Farm run cannot turn these skips into COMPLETE merely by supplying a root. Further work would need an independently reviewed, authorized way to execute the actual source/Git, locking and temporary-extraction prerequisites read-only with bounded I/O. Do not replace those prerequisites with a parallel scanner, trust the local RECORD as authority, relax ownership, or patch identity. With this task's constraints and missing corpus, reporting that limitation is the sound result.

## Input and output contract

Use the exact root returned by Farm's reviewed retention mode, the original caller's client tuple, physical Agent `a4e016b6a9f91fbe372672bdcf382c630bf59186` and Runtime `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344` checkouts, and the selected schema checkout. Also retain the original Store owner/index/directories/mutex/lease metadata, `.bench-owner.json`, source snapshots/archive carriers, all RECORD/METADATA/WHEEL/direct_url and license files, marker/provision report files, original dependency wheelhouse and lock, `.dependency-wheelhouse`, `.bootstrap-input.tgz`, `.bootstrap-authority`, `.bootstrap-wheelhouse`, `.farm-receipt.json`, `.source-inputs/schema.tar` and `.farm-test-wheelhouse`. Do not reconstruct them or substitute the old 9ea/369 child.

Supported **partial diagnostic** invocation, after independent review (not run here on a Farm corpus):

```bash
python3.13 -I -B "$ORCH/design/rt-OPS-Farm-census-sol-1530.py" \
  --maker "$PINNED_E62F_KIT/make-child-venv" \
  --root "$EXACT_RETAINED_STAGE" --staging \
  --client "$ORIGINAL_CALLER_CLIENT_IDENTITY" \
  --agent-checkout "$PHYSICAL_A4E016_CHECKOUT" \
  --runtime-checkout "$PHYSICAL_5E9AD_CHECKOUT" \
  --farm-source "$PHYSICAL_SELECTED_SCHEMA_CHECKOUT" \
  --work-root /home/user/work --tests "$ORCH/tests" --python python3.13 \
  --output "$ORCH/workers/rt-OPS-Farm-census-sol-1530/evidence/farm-partial-new.json"
```

All variables must be the authentic original inputs, not placeholders passed literally. Client input is newline-separated `packages/python/astrid_runtime_client/<file>=<64-hex SHA256>`, unique by path; syntax validation does not authenticate those hashes. The output must be a **new** file, outside every input/source tree, with physical existing ancestors. Both ancestor and descendant overlap and existing files/hardlinks/symlink aliases are refused before output creation. Source directories include the maker kit, diagnostic source and trusted host libraries/interpreter.

Default deadline 180 s; allowed 1–900 s. SIGALRM bounds blocked reads/syscalls, tracing bounds execution, all opens/scans are audited, node iteration is budgeted, reads are capped at 32 MiB/file and 256 MiB charged total, execution at 10 million trace events, filesystem operations at 100,000, address space at 256 MiB, rows at 2048 and report at 1 MiB. No files are extracted or copied. Only the newly reserved output is written. A limit, exception, refusal or skip never produces COMPLETE. Exit 3 means EXACTMISSING; exit 2 means incomplete/refused. There is no success/COMPLETE exit.

## Evidence and next step

Focused tests and the absent-input probe are under `workers/rt-OPS-Farm-census-sol-1530/evidence/`. The absent-input probe is not a Farm run: the prior requested final key is only an absent-path witness; no actual retained stage or schema input is claimed. Original 1510/1516/1523 artifacts and 1521's maker remain untouched.

Manager action: independently review this partial diagnostic and its explicit gaps; do not treat it as a replacement completed census. Farm must supply the exact retained corpus through its existing supported path. No narrow ownership fix follows from the old flat `unowned retained source directory` message without the offending path and authenticated source/ownership state. No live kit/repository/provider/test-body changes were made; C0's request/reply/dry-run contract is unchanged.
