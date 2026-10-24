## Report — FAIL/HOLD

Reviewed `c5525bffa62fc36adcb21c93adb401e0fb28b827`  
Tree: `c34a88bfef75c57e2ab9fe9a5444044a618af375`  
Parent: `10223c129093df18ee4dcf0c5094407ab212f379`

No product changes made. Worktree clean.

### Source preflight

Exact command:

```text
env TMPDIR=/tmp/app-F-current-caller-review-1302.asL9iX PYTHONDONTWRITEBYTECODE=1 python3 caller-publication.py
```

Result: `PREPARED`, `NOT_GRANTED`, `NOT_RUN`; total 1.466s.

- P2 source guard: PASS, 0.177s
- P3 source guard: PASS, 0.168s
- Child/import/native/backend/browser/HTTP/original stages: not run

Current normal tuple matched exactly:

- App `0971c645…`, tree `60cdf06f…`, parents `450f3080… 52f1ee51…`
- Agent `cba425b6…`, tree `d19ce2e5…`, parents `de2d1aad… 9746c925…`
- Runtime `becfe6db…`, tree `7edc08e3…`, parents `46eb068c… c021f13a…`

All were clean `tl/integration` checkouts.

### Guard results

Registry checks PASS:

- Full registry: 249 lines, 569825 bytes, SHA256 `52f556f8…`
- Outside selected rows: 247 lines, SHA256 `9acf76fa…`
- P2 row/body/tail: `6a45d056… / f6042b33… / 0839e6b5…`
- P3 row/body/tail: `1b7c7996… / 6366048b… / 47deb73f…`
- Duplicate and concurrent-change negatives refused correctly.

All 13 negatives passed under both normal and `python3 -O`:

`wrong-source`, `stale`, `app`, `agent`, `runtime`, `tree`, `target`, `path`, `body`, `receipt`, `registry`, `duplicate`, `concurrency`.

Wrapper checks also passed under both modes: one `bash -c` argument, export markers, eval suffix, and safe missing-custody failure (`rc=2`).

Static checks passed:

```text
python3 -m py_compile caller-publication.py caller-dry-preflight.py
python3 -O -m py_compile caller-publication.py caller-dry-preflight.py
python3 -m json.tool caller-custody.json
git diff --check
```

### Remaining findings

1. Candidate post-rebind source/body/tail/native-stage digests are recorded but not authenticated against expected protected values. `SOURCE_PATHS` is unused; guard refreshes use broad dynamic replacement. Computed candidate hashes were:

   - P2 body `7bab4028…`, tail `0839e6b5…`, native stage `1a4eb8ac…`
   - P3 body `f3ea3ede…`, tail `027cd2c9…`, native stage `1a4eb8ac…`

   No expected candidate/native-stage digest comparison exists.

2. The declared `REPLY_FIELDS` inventory is not complete against C0 §4. Missing fields include `receipt_id`, `idempotency_key`, `rebased_onto`, `provider_version`, `compiler_version`, `evaluated_head`, `message`, `details`, `conflicts`, `theirs`, `ours`, and `choices`. This prevents certifying the complete `{data,receipt}` envelopes and D58’s authoritative receipt/idempotency distinction.

3. `check_runtime_lock()` verifies Agent files against Agent’s lock but does not itself compare all Agent `from` blobs against Runtime. An independent comparison found all 15 current Agent bindings match Runtime blobs, so the current tuple passes, but the caller guard is incomplete.

4. Custody remains source-prepared only. Genuine coordinator admission, current child/client import, backend, Remotion, graph, post-request service snapshot, and terminal current-tuple run receipts remain absent. Historical inputs were not relabeled.

No browser, backend, native, HTTP, service, original journey, full suite, install, or Git mutation was performed. `DONE` and the conventional commit message were written.