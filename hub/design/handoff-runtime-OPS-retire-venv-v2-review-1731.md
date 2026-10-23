# Runtime OPS-retire-venv-v2 review handoff

Status: **FAIL — evidence-only; do not install or merge.**

Independent review of the staged kit from `rt-OPS-retire-venv-v2-1722` found
that `.child-venv-source-venv-agent-child-fixture-EVIL` is accepted and
retired when a unique completed base exists. The actual maker emits only
`.child-venv-source-N-$RUN_ID.XXXXXX`, with `$RUN_ID=YYYYMMDDTHHMMSSZ-$PID`.

The staged handler broad fallback is at lines 41-49, and the staged request
writer broad validation is at line 14. Both must refuse the counterexample.
The private run returned handler exit 0 and removed the malformed source; the
request writer returned exit 0 and queued it.

Required private evidence otherwise passed: bash syntax 3/3, prior guard
37/37, prior unit 7/7, new matrix 13/13, and request-to-dispatcher-to-handler
smoke 3/3. Runtime `git diff --check` passed and the Runtime worktree stayed
clean. Installed hashes were observed as `f18bc20b`, `4713b456`, and
`48cac6c7`; no installed or production path was modified or invoked.

No reviewed handler/request exports are supplied because the packet failed the
settled acceptance gate. Next action is a worker repair plus a new independent
review; no host installation, publication, cleanup, retry, chmod, or daemon
execution is authorized by this handoff.
