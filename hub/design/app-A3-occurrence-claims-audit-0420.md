# A3 audit report

Result: **FAIL — no App-side augmentation exists.**

- Popup ADD emits `occurrence.add-media` without `created`: [shotTimelineDataProvider.ts:829-842](/home/user/work/wt/app-A3-occurrence-claims-audit-0420/src/tools/travel-between-images/components/shotTimelineDataProvider.ts:829).
- `localSaveSession` persists those commands unchanged: [shotTimelineDataProvider.ts:1078-1084](/home/user/work/wt/app-A3-occurrence-claims-audit-0420/src/tools/travel-between-images/components/shotTimelineDataProvider.ts:1078), [localSaveSession.ts:165-188](/home/user/work/wt/app-A3-occurrence-claims-audit-0420/src/tools/video-editor/commands/localSaveSession.ts:165).
- Outbox stores the built request body verbatim: [commitOutbox.ts:477-483](/home/user/work/wt/app-A3-occurrence-claims-audit-0420/src/tools/video-editor/commands/commitOutbox.ts:477).
- Runtime provider forwards the request without rebuilding claims: [dataProvider.ts:745-766](/home/user/work/wt/app-A3-occurrence-claims-audit-0420/src/integrations/runtime/dataProvider.ts:745).
- Runtime validates submitted `created` against captured `command.created`; the inverse omission exception applies only to `timeline.inverse`: [timeline_commit_auth.py:255-299](/home/user/work/runtime/runtime_protocol/timeline_commit_auth.py:255).
- Agent ADD always creates the clip and creates the asset when absent, producing nonempty creation claims: [native_occurrence_media_commands.py:204-218](/home/user/work/agent/astrid/sdk/timeline/native_occurrence_media_commands.py:204), [_recording.py:155-180](/home/user/work/agent/astrid/sdk/timeline/_recording.py:155), [_recording.py:210-220](/home/user/work/agent/astrid/sdk/timeline/_recording.py:210).

The inherited shared ADD had the same omission at 6efdb; the current own unshared ADD introduced by 561a792a51 also omits claims. The shared fork’s `created` only covers the forked shot, not the subsequent ADD.

Bounded pure control:

```text
missing-created REFUSED CommitRejected provider executed a different command
matching-created ACCEPTED
```

Command: `PYTHONPATH=/home/user/work/runtime python - <<'PY' ... validate_claims ... PY`

No product files changed. `git status` clean; `git diff --check` passed. No HTTP, daemon, browser, full suite, or duplicate App suite run. Expected prior-report directory was absent, so no live/report evidence was substituted. Markers and commit message were written.