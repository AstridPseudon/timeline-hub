# G2 public command — PASS (bounded SDK/provider qualification)

Worker `agt-G2-public-command-0731`; branch `tl/agt-G2-public-command-0731`.
Base HEAD `d24da4af0f1ca83880b4b9ef57559e28ebe52a2a`; Runtime import checkout HEAD `a5d4258312c979024865ee704da2d632ca5b2730`.
Product and regression changes are uncommitted in `/home/user/work/wt/agt-G2-public-command-0731`. The harness owns the resulting commit SHA; no Git mutation, fetch, push or shared dependency mutation was performed.

## Result and decisions

Only `astrid/sdk/timeline/commit_session.py` and new `tests/sdk/test_timeline_public_command.py` changed. Product diff: 27 additions / 4 deletions. No contract decision changed.

`Timeline._execution_bundle` obtains canonical input through the existing `fetch_bundle(..., revision_id=self._basis["revision_id"], publication_id=self._basis["publication_id"], client=self.session.client)` reader. Hydration is lazy for patch execution or child emission; a verified cache is reused privately after acceptance. The current evaluation's pair is used, including conflict recomputation. The authenticated canonical document is attached only to copies used for local execution/emission. Public `.bundle` and `._command_bundle` stay portable, so hydration creates no authored diff. Both sides of child emission use matching private provenance. Earlier local commands, sequential previous values, declared reads and original request steps remain intact. Once hydrated, semantic execution also retains that private input.

The existing `_remote_timeline.open_bundle` reader was preserved byte-for-byte (including bd239 canonical image projection). It still verifies exact pair/scope, immutable digests, full closure/manifest equality and physical owner bindings. No document reconstruction, caller-fact invention, provider changes, alternate executor, test cache injection, schema/client/pin or other writer change.

The new **10-case** regression starts from real `RemoteTimelines.open_bundle` ordinary public reads with no private cache. It reuses the existing DetachedRealm/DetachedPort provider harness and ABI fixture. It covers two sequential public commands → accepted provider/history, unchanged full child closure, no staging outbox write, portable restart, child free-edit emission, refusal of a single shared alias broadcast, callback recomputation at a real provider conflict pair, preview `would_status` and unchanged base, and changed-pair/foreign-source/digest/outside/previous-value refusals. Test transport adaptation only normalizes the existing detached port's optional annotation and one-endpoint sequence range into the public receipt DTO; command meaning stays in the real existing provider. This is SDK/provider evidence, not live Runtime/HTTP qualification.

## Exact final commands and results

Executed from the assigned worktree:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_public_command.py tests/sdk/test_p4_commit_v2.py tests/sdk/test_p4_ten_note_provider.py tests/sdk/test_p4_note_rerun.py tests/sdk/test_timeline_open_commit.py tests/sdk/test_timeline_open_commit_v2.py tests/sdk/test_timeline_sync.py tests/sdk/test_remote_timeline_owner_scope.py
```

**151 passed in 29.26s**, exit 0.

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/commit_session.py tests/sdk/test_timeline_public_command.py
PYTHONDONTWRITEBYTECODE=1 make ruff PY=/home/user/work/venv-agent/bin/python
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy astrid/sdk/timeline/commit_session.py --follow-imports=skip --cache-dir=/tmp/w-bdf17e8d56/mypy-scoped
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-bdf17e8d56/mypy-baseline /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
git diff --check
```

All exit 0: scoped Ruff clean; normal Ruff **2149/2149**; scoped Mypy no issues (normal untyped-body notes); normal private Mypy **1912/1912**; vendor `ok runtime.lock.json`; whitespace clean. No baseline increase or dependency addition.

Import witness (same test environment prefix) printed:
- `astrid`: `/home/user/work/wt/agt-G2-public-command-0731/astrid/__init__.py`
- `astrid.sdk.timeline.commit_session`: `/home/user/work/wt/agt-G2-public-command-0731/astrid/sdk/timeline/commit_session.py`
- `runtime_protocol`: `/home/user/work/runtime/runtime_protocol/__init__.py`

Earlier development runs: first combined run had **2 failed / 18 passed** (new test adapter passed a raw receipt instead of CommandReceipt); the next had **2 failed / 66 passed** (existing detached port sequence range needed public DTO normalization). After adapter correction, new cases passed **6/6**, then expanded callback/preview/digest cases passed **9/9**. The final combined **151/151** includes the final shared-alias/staging-write assertions. No product behavior expectation was weakened, deleted or marked skip/xfail.

## Limits and next steps

No blockers. No full suite, localhost/browser/live socket suite, originalten/conflict HTTP node, native/crash suite, build, producer artifact check or diff was run. Full request/reply schema, merged/historical rebased receipts and guarded undo remain covered by existing neighboring suites; this task does not claim new integrated qualification of every contract field.

Next: independent review, harness commit, Agent home queue merge, then Proof's existing original public-command HTTP qualification against integrated heads. Proof received the callable source handoff while qualification was in progress. Integrated P4 remains owned by Proof and is not declared done here.

## Final source SHA-256
- `astrid/sdk/timeline/commit_session.py`: `72d1d68b69dd0efb63d4a1e4727f8d1f8861e509f98da3016e8265ef67cee4d7`
- `tests/sdk/test_timeline_public_command.py`: `4aef3b6e80337872e346b87769f3664a9d75019c76ab77baecb28c3effc00842`
- `astrid/sdk/_remote_timeline.py`: `05a00ba3af343eba2a5970f7ad047c0008d6f4c4bee745767dd3d71d7cc2ac67`
