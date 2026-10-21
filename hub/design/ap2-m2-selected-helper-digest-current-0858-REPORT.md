# AP2 M2 selected runner current helper digest 0858

## Result

Retained one new owned copy of the immutable 0852 selected final95 runner at:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-helper-digest-current-0858/artifacts/run-owned-selected-final95.sh
```

The empty `KEEP` marker is alongside it. The final whole-runner SHA-256 is:

```text
b3fb1336b36bd3703e3fc460ca9fe0932e9601b39c721215e07c5ca35bf535e5
```

The immutable 0852 runner remains unchanged at SHA-256
`266212583458c600bc3248401b40cb9cba5bc4c66068b3b5e65e0503b0405238`.

## Exact custody tuple

```text
App source HEAD:       a50ca4a0172cce9c73ce3c040290bf9479098b0f
App source tree:       92391f9a57dd38ce327b0a63990725053ea34601
HOME/base ancestor:    32b74fdea165816226b6f0727a16817a6a1a79c3
HOME/base tree:        a3ddc2997e6460bab77d1e4ef7c1ac98ee21ad65
selected spec SHA:     10250fa44db4e2d4423f8d06258105df267e3ba4e29700d700bb1d3182a6def1
harness SHA:           1585677bafef583110e86a04a4490a968a8db499b0e9d566c6b890eab228ce6c
current helper SHA:    96969ce9ff43b676abb4616009fd1112e93020065483b2a8ae0afac7245ba109
old helper SHA:        a0ed2bd7d6688799f22bc8f17f89631c603e4e692a8d5e71f3ee3b26437b27b3
```

The runner's owned keeper is:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-helper-digest-current-0858/artifacts/KEEP
```

Any later central run must provide a separate clean protected
`APP_KEEPER_ROOT` whose exact HEAD/tree are the App source tuple above. No
central keeper or actual run was materialized here.

Relevant retained toolpaths are:

```text
runner:       /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-helper-digest-current-0858/artifacts/run-owned-selected-final95.sh
helper:       /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-source-common.sh
old driver:   /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/run-central-selected-p1.sh
parent media: /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-parent-media-central.sh
locked graph: /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph
graph archive: /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph-source.tar
```

## Minimal delta and reverse proof

The only runner change is the one expected-helper digest in
`verify_scripts_and_scope`:

```diff
-test "$(sha256sum "$SOURCE_COMMON" | cut -d' ' -f1)" = a0ed2bd7d6688799f22bc8f17f89631c603e4e692a8d5e71f3ee3b26437b27b3
+test "$(sha256sum "$SOURCE_COMMON" | cut -d' ' -f1)" = 96969ce9ff43b676abb4616009fd1112e93020065483b2a8ae0afac7245ba109
```

`diff -u` showed exactly that one line. Replacing the new literal with the
old literal reproduced the old runner SHA exactly:

```text
reverse runner sha=266212583458c600bc3248401b40cb9cba5bc4c66068b3b5e65e0503b0405238
```

The shared helper was not edited by this worker. Reversing only its authorized
`final95:parent` App SHA/tree pair reproduced the prior helper exactly:

```text
reverse helper sha=a0ed2bd7d6688799f22bc8f17f89631c603e4e692a8d5e71f3ee3b26437b27b3
roles: final95:parent=1, final95:bootstrap=1, final95:selected=0
```

This reverse hash proves all other helper bytes, roles, pins, and guards are
unchanged from `a0ed2bd7`. The selected role remains absent.

## Checks and proposals

Passed directly here:

```text
sh -n <0858 owned runner>                                      PASS
bounded helper guard with wrong hash                           REFUSED (PASS)
bounded helper guard with 96969ce9... hash                     ACCEPTED (PASS)
literal central preflight proposal through sh -n               PASS
literal central run proposal through sh -n                     PASS
App worktree git status --short --untracked-files=all          clean
```

The existing 0852 eleven-check source preflight was reused as instructed,
not repeated. Its exact prior command and result remain:

```sh
SELECTED_FINAL95_MODE=preflight \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-existing-runner-current-bind-0852/artifacts/run-owned-selected-final95.sh \
  /home/user/work/wt/ap2-m2-selected-existing-runner-current-bind-0852
# PASS: all 11 aggregate checks, including exact one-test list1
```

Syntax-checked literal proposals for the new runner are:

```sh
# Central/source preflight proposal; not executed here.
RUNNER=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-helper-digest-current-0858/artifacts/run-owned-selected-final95.sh
test "$(sha256sum -- "$RUNNER" | cut -d' ' -f1)" = 'b3fb1336b36bd3703e3fc460ca9fe0932e9601b39c721215e07c5ca35bf535e5'
SELECTED_FINAL95_MODE=preflight "$RUNNER" /home/user/work/wt/ap2-m2-selected-existing-runner-current-bind-0852
```

```sh
# Central actual proposal; not executed here.
RUNNER=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-helper-digest-current-0858/artifacts/run-owned-selected-final95.sh
SERVICE_CAPTURED_APP_ROOT=/absolute/clean/service-captured-app-root
PROTECTED_APP_KEEPER=/absolute/clean/protected-app-keeper
test "$(sha256sum -- "$RUNNER" | cut -d' ' -f1)" = 'b3fb1336b36bd3703e3fc460ca9fe0932e9601b39c721215e07c5ca35bf535e5'
APP_KEEPER_ROOT="$PROTECTED_APP_KEEPER" SELECTED_FINAL95_MODE=run "$RUNNER" "$SERVICE_CAPTURED_APP_ROOT"
```

No source, spec, harness, helper, pin, role, dependency, private App copy,
browser, build, daemon, localhost/live socket, actual selected run, full
suite, install, or central service request was performed. The previous 0730
central result remains a HOLD at the Runtime handshake and is not relabeled.

Next: independent combined process-custody review, followed by the manager's
decision on whether to authorize one actual run.
