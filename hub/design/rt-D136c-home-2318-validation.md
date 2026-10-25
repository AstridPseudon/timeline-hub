# D136c Runtime integrated-head receipt

Status: PASS.

## Authority and source identity

- Runtime actual integrated head: `0ca306dfd3cf4e21976271cc4b2e779b10e025b0`, tree `37cfcd4f6108c1fdda401e563e3674503bc328ef`.
- Security review: `rt-D136c-security-review-2312`, PASS, candidate `2f1fbb1fc2954dc54eda7f29656de8f15e38683a`, same tree.
- Queue terminal: `queue/done/merge-rt-D136c-safe-observation-diagnostics-2305`, merged into `tl/integration` as `0ca306dfd3`.
- `git diff HEAD 2f1fbb1fc2954dc54eda7f29656de8f15e38683a` is empty: the actual integrated entire tree equals the reviewed candidate tree.
- Reviewed blobs equal before/after/candidate: `runtime_protocol/timeline_commit_auth.py` (`b2b238a716b55276e63d23d2886ef8542a382faa`), `runtime_protocol/timeline_commit_store.py` (`3388fa923c7aaeec2980a8981280146eaa30cbc7`), and `tests/test_timeline_missing_observation_diagnostics.py` (`15c35c662480d98443b66210a823e3f00967d6db`).

The Runtime worktree was clean before and after. The pinned Agent checkout `/home/user/work/wt/agt-pin-4c4ee35d` was clean before and after at commit `4c4ee35d5687c4cd40a0e5395efda53aa56f939d`, tree `d50fd98f7d1bc6860de810f38e8a0b3a55ca224e`. Local `refs/remotes/origin/HEAD` was absent in both checkouts before and after; read-only remote HEAD observations after the run were Runtime `refs/heads/main` at `fa9cd5464a8b37b02f971de375e56be846cd69e` and Agent `refs/heads/main` at `8b6ed2116fd1803d24b2be5bc08bd9490407fe4a`.

The source-resolution check passed. Agent modules resolved only from the pinned checkout (`astrid`, `astrid.core.execution.generic_host`, `astrid.sdk.timeline.commands`, `astrid.sdk.timeline.commit`); Runtime modules resolved only from this worktree (`runtime_protocol.timeline_commit_auth`, `runtime_protocol.timeline_commit_store`). The direct generic-host import was not used because this environment lacks optional `PIL`; the mandated pytest run does not require that import.

## Targeted evidence

Exact command and durable artifacts are recorded in `result.json`. It returned `0` and reported `4 passed in 1.42s`. The JUnit XML contains exactly the three diagnostics cases plus the requested `[False-False]` native case. XML SHA-256: `8a9ce803297c6e0de66c0014203aad75f80c8b235e727df58cfbf8488a8bd397`. Raw output SHA-256: `d8a663a81cc181eb028d17573d86a44e87e9eb4782bc7ccdebd61962aeaf7d77`.

No broad or unrelated suite was run. No source or generated files changed during qualification.
