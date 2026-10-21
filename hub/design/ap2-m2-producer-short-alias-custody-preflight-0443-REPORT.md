# Producer short-alias custody preflight review

## Result

**BLOCKED: the exact short-alias source does not pass its preserved
`approved-delta` guard.** I did not weaken that guard, use an arbitrary
ancestry, submit a central run, or run a producer actual.

The requested immutable keeper is present and clean:

| Item | Value |
| --- | --- |
| Keeper | `/home/user/work/wt/app-pin-7fafee1f` |
| HEAD | `7fafee1f67aa7b42e3997d2c30b4ee8e1bad42c5` |
| tree | `9d5ba429c703da57203e01d13e5a5fe4cc7ee014` |
| HEAD parent | `97187ce3c1576559239f869067a9cef8ffb5f357` |
| wrapper SHA-256 | `95e5a901b599d3202788fb7ce5cbc6d0b6517d63a3a5c9e40e43a90979ce2983` |
| existing runner SHA-256 | `be59b3da5c01e0df22ec556cc84cd25a2a1a4304cf4542035829003eecb2e75b` |
| dependency setup | `node_modules -> /home/user/work/app/node_modules` only |

The keeper's only diff from the prior source `97187ce3` is
`scripts/testing/run-producer-public13-list.sh`; no product, body, graph,
package, origin, credential, browser, or test assertion file changed.

## Review evidence

The exact alias check passed:

```sh
ALIAS_ROOT=$(mktemp -d /tmp/tla-review-XXXXXX)
ln -s /home/user/work/wt/app-pin-7fafee1f "$ALIAS_ROOT/a"
test "$(realpath "$ALIAS_ROOT/a")" = /home/user/work/wt/app-pin-7fafee1f
test "$(git -C "$ALIAS_ROOT/a" rev-parse HEAD)" = 7fafee1f67aa7b42e3997d2c30b4ee8e1bad42c5
test "$(git -C "$ALIAS_ROOT/a" rev-parse HEAD^{tree})" = 9d5ba429c703da57203e01d13e5a5fe4cc7ee014
test -z "$(git -C "$ALIAS_ROOT/a" status --porcelain=v1 --untracked-files=all)"
find -P "$ALIAS_ROOT" -depth -delete
test ! -e "$ALIAS_ROOT"
```

Result: **PASS**. The wrapper's real-path alias and cleanup path were also
exercised by the negative and preflight invocations; no `/tmp/tla-*` alias
root remained. The existing ignored dependency symlink was retained and the
keeper stayed clean.

The unchanged body/config bytes match the wrapper's recorded guards:

```text
spec   d91d0c1cce22f68119cd30fcb0a288346474b0ad4b64c84dcee3b730fa468d89
helper 50cbe5341f24c9a1ecc999018e2c6d975380a3440570abce151f9173c9752016
config 5b880ceff883abce2575a3a85aaa4eda69d3bcb848768ff0e91f337d50cca4c0
```

The new diff has no non-comment changes to origin/credential authority,
Chromium binary/options, assertions, or timeouts. The runner hash is the
requested unchanged `be59…75b`. These are static custody findings; no
browser launch occurred in this review.

## Negative controls

Wrong wrapper hash, with invocation short-circuited before `sh`, returned
exit 1: **PASS**.

```sh
KEEP=/home/user/work/wt/app-pin-7fafee1f
test "$(sha256sum -- "$KEEP/scripts/testing/run-producer-public13-list.sh" | cut -d' ' -f1)" = 0000000000000000000000000000000000000000000000000000000000000000 \
  && sh "$KEEP/scripts/testing/run-producer-public13-list.sh" "$KEEP" preflight
```

Wrong source alias `/home/user/work/app` returned exit 1 with the expected
`app-clean`, `app-baseline`, `approved-body`, `approved-delta`,
`body-helper-config-hashes`, `isolation`, and `argv-and-test-path` refusals:
**PASS**. No source authority was accepted.

## Blocking preflight result

The exact approved command was attempted after the above checks:

```sh
cd /home/user/work/wt/app-pin-7fafee1f
test "$(sha256sum -- scripts/testing/run-producer-public13-list.sh | cut -d' ' -f1)" = 95e5a901b599d3202788fb7ce5cbc6d0b6517d63a3a5c9e40e43a90979ce2983
sh scripts/testing/run-producer-public13-list.sh /home/user/work/wt/app-pin-7fafee1f preflight
```

Result: **FAIL, exit 1**, with only:

```text
producer preflight FAIL
- approved-delta
```

All other original source/body/graph/cohort/disk/isolation/argv checks passed
through the short alias before the runner stopped. The failure is explained
by the preserved guard:

```sh
test "$(git -C "$APP_ROOT" rev-parse HEAD^1 2>/dev/null)" = "$APP_SOURCE_SHA" || return 1
```

The exact final HEAD is `7faf -> 97187 -> 00bbc`, while
`APP_SOURCE_SHA` is `00bbc`. Thus the new wrapper commit is not admitted by
the guard even though `git diff 00bbc 7faf` contains only the wrapper path.

## Central-run disposition

No central preflight or launch-smoke was requested. The current central
allow-list still binds the existing producer suites to the old worker
`/home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416` and old
wrapper hash `3069891c…1b48` (the three registrations in
`scratchpad/orch/tests/suites.conf`, producer lines 109–111). It therefore
cannot consume this exact keeper/hash unchanged. The previously recorded
Chromium launch diagnosis `30467` remains supporting evidence only; it does
not qualify this new binding.

Smallest missing seam: the source owner/orchestrator must provide an exact
source-7faf custody command that preserves the existing ancestry/body/graph
guards while explicitly admitting this wrapper-only successor, then register
one new central preflight and reuse the existing list-mode launch-smoke with
the exact keeper and wrapper hash. Until that seam exists, changing the
allow-list alone would still fail `approved-delta`, and bypassing that check
would violate this task.

Not run: central preflight, central launch-smoke, build, browser, producer
actual, repeated hosted build, full suite, install, or shared dependency/cache
mutation.

