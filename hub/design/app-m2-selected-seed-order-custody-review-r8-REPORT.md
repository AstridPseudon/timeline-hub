# App M2 selected seed order custody review r8

Verdict: **APPROVE** for the committed r7 harness-only order correction.

Source reviewed: `74bfb99ea6a3357794285735040fb3dd0265cf4f`, tree
`f1b7b67050b754c105e30a9a565fbf228b289a09`.

The only changed path versus the parent is
`tests/e2e/local/support/harness.ts`. The selected clips/publication block is
byte-identical to the pre-move source: same `compositionPublication` call,
raw output/config/tracks/clips/registry, `draft-1` carrier, and publication
status check. The order is publication -> authoring restart -> selected actor
credential provisioning -> discovery/eval context capture. The Agent command
still receives exactly `published.body.data.new_head` as `--expected-head`.

The original selected spec and assertions are unchanged. No private/native
genesis writer, fake P1 revision/pin, grant/guard/schema/DTO change, or product
source change is present. The normal ephemeral `DirectHarness` pre-authoring
publication phase is preserved; the selected actor/discovery context remains
post-restart.

Checks:

- `node --import tsx --test tests/e2e/local/support/selected-param-credential.test.ts` — PASS (1 file, 1 test).
- ESLint with `--no-cache --max-warnings 0` on `harness.ts`, the selected credential controls, and the selected spec — PASS.
- `git diff --check HEAD^ HEAD` — PASS.
- Independent source-order/payload identity probe — PASS.

Not run by instruction: selected actual/browser journey, localhost/live sockets,
full suite, build/install, new graph, or P1/P2 qualification. Completion marker
and commit message are in the worker handoff directory.
