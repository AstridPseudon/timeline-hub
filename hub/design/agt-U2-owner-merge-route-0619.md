# U2 owner-review merge route repair

Status: **PASS**. Production caller `$ORCH/bin/hub-syncd` invokes the exact
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
