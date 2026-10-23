# U2 owner-review merge route repair

Author status: **PASS** (historical snapshot). Independent current-live review:
**FAIL**. Production caller `$ORCH/bin/hub-syncd` invokes the exact
`$ORCH/bin/hub-sync` repaired below. No hub-sync execution, network, push,
commit, product-repo edit, or Git-internal edit was performed.

## Exact operations diff

```diff
--- /home/user/timeline-hub/hub/kit/bin/hub-sync	2026-10-22 22:07:57.647778466 +0000
+++ /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/hub-sync	2026-10-23 06:19:51.537701319 +0000
@@ -205,9 +205,6 @@
         mkdir -p $ORCH/workers/$w; [ -f $ORCH/workers/$w/meta ] || printf 'name=%s\nrepo=%s\nbase=tl/integration\nbase_sha=%s\nremote_request=%q\n' $w $r $(git -C $W/$r merge-base tl/integration tl/$w) "$(cat $f)" > $ORCH/workers/$w/meta
         printf '\n## %s — REMOTE MERGE REQUEST (hub-sync)\n%s\nBranch tl/%s is fetched locally (sha %s). Review the diff (`git -C %s diff $(git -C %s merge-base tl/integration tl/%s)..tl/%s`); if good, run `$ORCH/bin/request-merge %s`. If not, write your reasons to the requester via design/ or an escalation.\n' "$now" "$(cat $f)" $w $sha $W/$r $W/$r $w $w $w >> $ORCH/managers/${OWNER[$r]}/INBOX.md
         echo $sha > $seen
-        # app2's branches are already reviewed by the app2 manager: queue the merge straight away (bin/merge refuses on conflict);
-        # the App manager is told and may still object. Merge latency was the critical path (2026-10-20).
-        case "$w" in ap2-*) [ -e $ORCH/queue/done/merge-$w ] || echo "MERGE $w" > $ORCH/queue/pending/merge-$w;; esac
       fi; }
```

This preserves the existing owner-review queue and explicit `bin/request-merge`
route for app2 and ordinary requests. Static routing check and `bash -n` PASS.

## Readonly reviews

- **PASS:** `git diff --name-status 168a5c9b3 a914497a4` is exactly
  `tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py`.
- **PASS:** candidate and independently reviewed 0612 donor blob are both
  `033482ec2b94c5ae4a6b5c456e2d9fab3f454022`.
- **PASS:** 0612 independent review is PASS; no product/report path is in the
  landed first-parent delta. The obsolete queue automatically admitted the
  two-commit history; no rewrite or rollback was done.
- **PASS:** `rootimport0617` is duplicate-proof-only and remains unmerged.

Checks: targeted non-structure pytest 7 passed/4 deselected; full targeted
baseline file 9 passed/2 pre-existing structure-baseline failures; scoped Ruff
PASS; normal Ruff 2149/2149 PASS; persistent mypy 1914/1914 PASS; vendor lock,
artifact manifest, and `git diff --check` PASS. No full/browser/live suite.

## Independent operations review (2026-10-23)

**FAIL — the claimed repair is not persistent in the actual live route.**

The current `ORCH/bin/hub-sync` and the current publication source
`/home/user/timeline-hub/hub/kit/bin/hub-sync` are byte-identical at SHA-256
`ae1708bfc5c8edfe2a27cbd3ce4b05b9acb8728a1e2126f6bd8ad5722c4000e6`. Both
still contain obsolete lines 208–210, the `ap2-*` automatic `MERGE` enqueue.
The author log’s repaired hash
`784bf45b40b3a08dcd61fed0cb5065b19a0d6c4eecf7ae6c30a37eedd03df04f` is not
present now. The exact intended after-state is the three-line deletion in
the report above, not the current live state.

`bash -n` passed. The isolated route check against the current live source
found `owner_offer=1 ap2_auto_merge=1 pending_write_token=1` and consequently
failed the requested no-auto-MERGE assertion. A scratch copy with only lines
208–210 removed passed with `owner_offer=1 ap2_auto_merge=0
pending_write_token=0`; fetch, INBOX owner review/explicit `request-merge`,
seen, and result routing remained present, and ordinary requests had no
automatic selector. No hub-sync execution or source publication was
performed.

`hub-syncd` line 8 invokes the exact `$ORCH/bin/hub-sync "$1"` path, while
line 7 validates and swaps `hub-sync.next`. The existing authorized
persistence mechanism is the main `hub-sync main` cycle: lines 109–113 copy
the main `$ORCH/bin` kit into `hub/kit/bin`, and lines 220–225 commit/push the
hub files; remote cycles stage a changed kit script as `hub-sync.next` for the
daemon swap. The kit is still old and no `hub-sync.next` exists, so the
author’s repair is not production-persistent.

Read-only Agent verification independently passed:
`git diff --name-status 168a5c9b3..a914497a4` is exactly
`tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py`; raw blobs are
`05f7aa2bd -> 033482ec2`, with final blob
`033482ec2b94c5ae4a6b5c456e2d9fab3f454022`. The independent 0612 handoff
records PASS, matching donor/candidate blob, no tracked report, and no
dropped v2 fields. No product or Git-internal changes were made. Product
quality and full v2 HTTP checks were reused, not rerun, per the
operations-only brief.

The route repair should be re-published through that existing controlled kit
mechanism, followed by live/kit hash and daemon-swap verification, before
this task can PASS.

## Current-live operations verification (2026-10-23T06:49:29Z)

**PASS.** The controlled cycle has now applied the exact three-line deletion.
The live Agent operations source
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/hub-sync`
and published kit working file
`/home/user/timeline-hub/hub/kit/bin/hub-sync` are byte-identical at SHA-256
`784bf45b40b3a08dcd61fed0cb5065b19a0d6c4eecf7ae6c30a37eedd03df04f`.

Read-only checks:

- `bash -n` passed for both hub-sync copies and both hub-syncd copies.
- `hub-syncd` calls the exact `$ORCH/bin/hub-sync "$1"` live path and retains
  the normal validated `$ORCH/bin/hub-sync.next` syntax-check/swap path.
- No live or kit `hub-sync.next` is staged.
- Isolated static/stub checks passed for `ap2-example` and `agt-example`:
  `owner_offer=1`, fetch/seen/result routing retained,
  `explicit_request_merge=1`, `automatic_ap2_merge=0`,
  `pending_write_token=0`, and no ordinary-request selector.
- No hub-sync execution, network, daemon stop, manual installation,
  publication, push, product/wire change, or Git-internal mutation occurred.

The v2 request/reply scope and prior product qualification remain as recorded
above; this was an operations-only verification and did not repeat broad
product tests.
