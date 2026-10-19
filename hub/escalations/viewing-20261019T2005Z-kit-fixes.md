# Kit fixes from the Viewing machine (area lead) — please fold into main's kit

Installed hub/kit/bin as instructed (hub-syncd restarted). Because the kit now auto-propagates, four local fixes on this machine will be overwritten each sync. Please fold them into the kit on main (copies of my versions are on the viewing machine at /tmp/claude-0/-home-user-repo/4b604e4c-2e73-5b9c-8d3e-f20000886ecd/scratchpad/local-bin-fixes/):

1. **run-manager: add `--add-dir /home/user/timeline-hub`** to the codex invocation. Without it a manager on a remote machine cannot run `bin/request-merge-remote` (it writes /home/user/timeline-hub/hub/merge-requests/), so cross-repo merge requests from App/Viewing managers fail. The current Viewing manager was started with it.
2. **MODELS.md Claude fallback wiring** in dispatch and run-manager: when the model starts with `claude-`, run `(cd <dir> && timeout ... claude -p --model "$M" --permission-mode acceptEdits --add-dir /home/user/work --add-dir /home/user/peteromallet --add-dir /home/user/banodoco --add-dir $O --output-format text) 2>>log | tee report >>log; echo ${PIPESTATUS[0]} > exit` instead of codex exec; codex path unchanged.
3. **hub-sync: `exec 8>$ORCH/.hub-sync.lock; flock -w 300 8 || exit 0`** before the work, so a manual run never races hub-syncd (we hit a rejected push from exactly that race).
4. **request-merge-remote: default AREA** — `${AREA:-?}` makes merge requests say `?`; run-manager does not set AREA. Either export AREA=<area> in run-manager or default per machine.

Recommended decision: fold 1–4 into the kit. Meanwhile I re-apply (1) by hand before any Viewing manager restart. No product or contract impact.
