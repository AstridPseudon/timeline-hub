Completed the permitted measurement handback. **No production fix was made:** the evidence does not establish one cause for ten-note and element, and a bounded repair preserving every fresh authority check was not identified.

- Preserved all **13 prior artifacts byte-for-byte**, including private stacks. The prior worker was checkpoint-stopped to receive expanded scope.
- Original XML: **1 failure, testcase 45.182s**, timeout `>45.0s`; suite 47.052s. Separately recorded process wall/main CPU: **46.2196s / 43.8582s**. No original rerun or new cProfile.
- Actual 15/30/44s samples occurred at request ordinals **60/66/68**. Request 66 spent **12.723s**, with **1,072 accepted-record checks versus eight deterministic replay checks**. Request 68 was interrupted; its counts are partial.
- Of 428 safe stack samples, 351 included accepted-record verification, 304 `_ancestor`, and 234 `_inverse_stage_history`. These overlapping observations identify recursive fresh-history work before the replay-proof lookup.

The D78 packet contains **one command, one step and 11 reads**, contrary to the multi-command premise. The final local loop used the genuine supported film fixture, real provider and Runtime source paths:

| Commands | Wall / CPU | Accepted checks | Result |
|---:|---:|---:|---|
| 1 | 0.315 / 0.307s | 1 | Accepted |
| 2 | 0.358 / 0.347s | 11 | `invalid_records` |
| 3 | 0.485 / 0.473s | 11 | `invalid_records` |

The extensions failed at `timeline_commit_auth.py:2131 command_output`: command 0 had two writes resolving to one normalized site. No validation was weakened. Earlier harness read-declaration errors and their refusals were retained. Schema-validation calls totalled **10–19ms per command ordinal** in the final loop.

Consumed App 7131 safe facts: ordinal 3 has **no observed Runtime accept, receipt or response**, and the retained frame is Agent `commands.py:137 validate_command`. Its body is unavailable. The historical realm/base is also unavailable; the local comparison is **not exact replay or gate credit**.

Validation: **169 passed in 46.86s**, exit 0:

```bash
PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/agent \
PYTHONPATH="$PWD:/home/user/work/agent:/home/user/work/venv-agent/lib/python3.13/site-packages" \
/home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
--junitxml=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-P4-element-D84a-return-sol-2231/evidence/targeted.xml \
tests/test_timeline_request_verification.py \
tests/test_timeline_history_authenticated_read.py \
tests/test_timeline_inverse_stage_authentication.py
```

`git diff --check` passed; worktree remains clean. No full suite or browser run. No source change, security review, or old-RED/new-GREEN repair is claimed.

Runtime SHA: `732c48c6f5a9441a65c61b24595d454a1cd3e180`. Local Agent SHA: `7c485e5b612a31a9b4f6e9a67163612a4a3313d4`; App 7131 used Agent `039ff2c2187d02b723074a8a6dfcbc6a70544c19`.

All durable artifacts, exact commands and complete identities are in [this worker’s evidence directory](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-P4-element-D84a-return-sol-2231/evidence).

Recommended next seams: Runtime’s recursive input assembly at `_accepted_replay:342–358`; separately, Agent’s retained `validate_command:137` frame. Further original timing remains pending meaningful reviewed source. Commit message and `DONE` written.