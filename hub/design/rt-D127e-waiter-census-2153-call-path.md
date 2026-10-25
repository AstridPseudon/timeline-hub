# D127e historical call path

The source tuple is Runtime `ab1e4f6141987706132916e2da16477f5a019464` and Agent `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2`. Current integration was not used as behavioral evidence.

```text
Runtime server._timeline_commit (server.py:300)
  -> RuntimeService.commit_timeline (service.py:2469)
  -> _execute_timeline_commit (service.py:2486)
     -> _timeline_authorize / store.get_project (service.py:2464 / store.py:1516)
     -> _timeline_commits (service.py:2438)
     -> coordinator.execute (timeline_commit_execution.py:365)
     -> _execution: coordinator guard and same-key entry lock (lines 328, 341)
     -> port_factory (service.py:2541)
        -> require_active / baseline (service.py:2517, 2625)
        -> RequestCommitPort
     -> provider.commit (timeline_commit_execution.py:395)
        -> Agent RuntimeCommitService.commit (commit.py:1160)
           -> validate_command (commit.py:1187)
           -> capture_media_admissions / capture_producer (commit.py:1188-1189)
           -> port media/history reads (commit.py:1191-1230)
           -> commands.execute (commit.py:1331)
           -> bounded StaleHead loop, max 3 (commit.py:1336-1452)
              -> port.preview or port.accept (commit.py:1443-1444)
                 -> TimelineCommitStore.preview/accept (store.py:1792 / 1834)
                    -> history read scopes and RequestCommitPort._read (port.py:217-228)
                    -> _store_version (timeline_commit_store.py:349-365)
                       -> conditional D112 _reestablish_connection (lines 307-347)
                    -> accept _accepting / BEGIN IMMEDIATE (lines 1837 / 455; store.py:933)
     -> verify_outcome and port.close (timeline_commit_execution.py:400-408)
  -> Runtime server return/_send
```

The D112 test is answered statically: yes, the recovery path can wait on the actual element route. A provider history read enters `RequestCommitPort._read:217`, then `history_read_scope:517`, `_read_transaction:381`, and `_store_version:349`. A changed DB/WAL identity at `_store_version:353-357` calls `_reestablish_connection:307`, whose first operation is a blocking `with self.store._mutex:315`; its same-connection branch closes and reopens through `store._open:333-338`, where `sqlite3.connect(... timeout=10)` and `PRAGMA busy_timeout=10000` are configured at `store.py:1230-1246`. This identifies the held D130 SWAP/WAL path. No authoring, test, retry, alternate route, or qualification was performed after that identification.

The provider's roughly 12-second interval is a synchronous blocking call at `timeline_commit_execution.py:395`, not a proof that the provider spent that time waiting. Agent's retry loop is bounded and has no sleep. The provider source and invoked admission/producer helper source contain no subprocess, Event/Condition, or lock wait primitive.

Several Runtime subprocess/sleep/Event paths exist elsewhere in the repository, but static call-map inspection shows they belong to media import, task/worker, or lifecycle paths and are not reachable from this timeline commit provider route. The HTTP server's `selectors.select` seen in a non-element retained 10721 stack is likewise not evidence for 32016/15200.
