Ask: Runtime and App author the D42 fixes now, in parallel; App confirms from the 3362 trace / Owner: Runtime (primary), App (secondary + diagnostic), Proof (one run) / By: Runtime and App fixes reviewed by 05:00Z

**Root cause (independent read-only analysis, file:line evidence)**
- The P2/P3 basis read never reaches basis-ready: the promise is still pending, not failed. useTimelineSave.ts:193-205 shows neither basis-ready nor basis-error. The outbox DB is created only later (useTimelineSave.ts:225), so "outbox unknown" is a downstream symptom.
- The Runtime history GET runs under the single global `store._mutex` (server.py:1204-1206). Inside it, service.list_timeline_commits -> _read_history -> history_entry -> _verify_accepted **replays and schema-validates the whole accepted seed commit on every read** (timeline_commit_store.py:202-310, :520).
- Measured per GET:

  | Seed | 2a9 | 37eb/45c3 |
  |---|---:|---:|
  | native21 (P2/P3) | 6.28 s | 2.01 s |
  | P1 | 1.06 s | 0.33 s |

- The GET queues behind every other locked request during mount. P2's effect restart issues a **second** history GET, because client.ts:702 uses withSession, not coalescedRead. Shot, internal, identity and the IndexedDB claim still have to follow, all inside the fixed 5000 ms poll. P1 passes because its seed check is cheap.

**D42 decisions**
1. **Runtime (primary, HARD Sol + independent review):** stop re-verifying an immutable accepted publication on every read while holding `store._mutex`.
   - **Approved:** an in-memory, per-daemon-process verification memo keyed by the SHA-256 of the exact accepted record bytes plus the schema/validator version.
     - It isn't persisted; a miss, or any byte difference, does the full _verify_accepted.
     - A negative test must show that a single byte change re-verifies and still refuses.
   - Also move the verification outside the global mutex, on a read snapshot, where that is provably safe; if not, keep it inside.
   - This is not trust of a prior result: the key is the content itself. All existing refusal tests must still pass.
   - Then, under D41, backport it onto the 37eb proof pin with client bytes identical.
2. **App (secondary, Luna + review):** in useTimelineSave.ts:154-317, when the effect restarts on the SAME head, reuse or coalesce the in-flight original basis read instead of issuing a second history GET. Also find what changes the effect's dependencies and triggers P2's lifecycle-cancel. Fix it if it's spurious.
3. **App (diagnostic, now, no new run):** from the existing 3362 and 12221 trace.zip, extract each /commits request's start, end or -1, plus the page-close time, against basis-read. One line to the orchestrator: does the timing confirm or refute this cause?
4. **Never** raise the 5000 ms wait, or change any test body or guard.
5. **Proof:** ONE P2 and ONE P3 run once (1) is on the pin, plus (2) if it's ready by then.
