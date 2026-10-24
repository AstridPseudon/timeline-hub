Implemented A2/U4p/U3b caller repair in three files. The existing compatibility boundary now admits both source-qualified full-v2 digests with matching generated protocol, version, component identity and commit operations. Unsupported document saves remain blocked before POST.

Both qualified Runtime versions have byte-identical commit schemas and DTOs. Request fields, persisted steps/reads/merge, created IDs and `Idempotency-Key` are preserved; reply handling is unchanged. Generated/vendor/lock/provenance bytes, protected paths and existing tests remain untouched.

Validation used:

```bash
V=(/opt/node20/bin/node node_modules/vitest/vitest.mjs run
   --config config/testing/vitest.config.ts --configLoader runner
   --no-cache --maxWorkers=1 --no-file-parallelism)
export NODE_OPTIONS="--import=$TMPDIR/preload.mjs"
```

| Command / selection | Result |
|---|---|
| `"${V[@]}" $(cat "$TMPDIR/union-files.txt")` — frozen 27 files plus five D39 neighbors | **772 passed; all 43 prior failures cleared** |
| `"${V[@]}"` selecting `localSaveSession.contract`, `.test` and `.v2` tests | **29 passed** |
| `"${V[@]}"` selecting lifecycle, ownerRecovery, trackLabelRefusal, documentPatchIntent, commitOutbox and genericPatch tests | **75 passed; one collection failure below** |
| `TSX_DISABLE_CACHE=1 /opt/node20/bin/node --import tsx --test tests/e2e/local/support/{gate5-reset-precondition,p2-document-oracle,p2-original-owner-ready,p2-parent-oracle,p2-transition-oracle}.test.mjs` | **30 passed**, including 20 Gate5 controls |
| Vitest with `$TMPDIR/vitest.semantic.config.ts` | **7 passed** |
| Vitest renderer config with `ASTRID_CHECKOUT=/home/user/work/agent` | **2 passed** |
| Serialized `flock -w600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 /opt/node20/bin/node node_modules/typescript/bin/tsc -p CONFIG --noEmit --pretty false --incremental false`, for root/app/node configs | **All passed** |
| Scoped ESLint `--max-warnings 0`; `git diff --check HEAD` | **Passed** |
| Runtime `generators/generate.py --check`; `scripts/artifact_manifest.py --check` | **Passed** |
| Both vendor-lock checks; `verify-astrid-vendor-sources.mjs`; public-boundary tests | **Passed; 9 tests** |

Read-only checks confirmed **79 producer artifacts** and **14 consumer artifacts** match exact pinned committed bytes/hashes.

Remaining failure: unchanged `commitSession.genericPatch.test.ts:7` strictly expects the old digest and fails collection against D39. It was neither weakened nor skipped.

Identity:

- Base HEAD: `a16645c69c629fd5293e7b811140e2c253c8b568`
- Base tree: `dc3f7fdedf4cd9eeb83a6dffd67a56b438089b19`
- Base parents: `cd29ff2642ab8241850a2ed3490970771a9c02eb`, `82cb5c0005df7abe0fcb8673f7be192a6c9e9183`
- Final working tree, computed read-only: `9079ec3710f21676ec6f3b3b9d5eecb67b69babb`
- New commit SHA is harness-owned; expected parent is the base HEAD above.

`commit-msg` and `DONE` are written. No integration merge or full/browser/HTTP/build/service run occurred. Next: independently review this repair, then let the manager request the full checkpoint after PASS.