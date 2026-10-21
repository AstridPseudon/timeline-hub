# M2 current-ops producer custody proof review

## Verdict

**Approve the bounded source-only custody proof; do not claim route acceptance or writer closure.**

Reviewed exact source0306 commit `36dd91257fd13dcad0d58b48c790caa5063b4c8c` (tree `d908845dbc8e5ebf96698d08621557e904f20c52`) on the App source branch, after the frozen wait. The source adds only:

- `tests/e2e/local/producer-ownership-current-pin.spec.ts`
- `tests/e2e/local/support/producer-ownership-current-pin.ts`

No production, shared writer, three-products, future-fresh, DTO, authority, or carrier implementation changed.

## What the source proves when the later route gate runs

- It opens the existing `/tools/video-editor` route with the exact project/timeline query parameters and drives the existing Transcript actions menu and Scene “Move existing shots to markers” button. It does not call producer builders or force a disabled control.
- The fixture publishes a new dedicated timeline with `expected_head: null` through the existing isolated Runtime harness, uses the harness’s existing video object, and supplies valid source intervals and a real media carrier. The stale transcript output and Scene output are existing deterministic IDs derived through the production `transcriptCaptionClipId` and `scenePhaseShotId` functions.
- The transcript accepted branch requires exactly one native `clip.delete` for the stale owned output. The Scene accepted branch requires only native `clip.move` plus the native hold-setting `clip.set` for the existing owned output. No fresh `clip.add` path is asserted or claimed.
- Four protected foreign/user rows are required present. Their complete raw clip objects and list-order indices are compared against the initial state after accepted operations, reload, the accepted real commit whose acknowledgement is dropped, exact idempotency-key/body retry, and undo. The accepted Scene request is also checked not to target protected rows by its exact command assertions.
- The refusal branch recognizes the visible `Native patch refused` alert, requires no commit request and unchanged head, then repeats the refusal after reload and checks the protected rows again. It records `no-accepted-ownership-proof`; it does not relabel refusal as acceptance.
- The lost-ack helper first obtains a real accepted Runtime response via `route.fetch`, aborts only the browser acknowledgement, and later requires the retry body and idempotency key to match exactly. Undo requires a `timeline.inverse` command and the original owned Scene values.

The source intentionally leaves the fresh-creation carrier missing. This is existing-output custody evidence only, not proof that fresh producer output can be created or carried through the current generic writer.

## Read-only checks

All checks used the exact source0306 tree, extracted into a private temporary directory. The shared App `node_modules` was only referenced through a read-only symlink; its `realpath` was verified.

```text
eslint tests/e2e/local/producer-ownership-current-pin.spec.ts tests/e2e/local/support/producer-ownership-current-pin.ts --ext ts --max-warnings 0
PASS

tsc --noEmit --pretty false
PASS

private no-webserver Playwright collection config; one-case --list
1 test in 1 file
PASS: removes only stale owned transcript output and moves only owned scene output

git diff --check 36dd91257^ 36dd91257
PASS
```

The repository’s default Playwright config was not used for collection: it allocates live isolated ports and ignores local journeys. No browser, localhost service, Runtime socket, actual gate, or full suite was run.

## Limits and next step

This is source-only approval of the custody journey and its refusal boundary. It does not establish that the current mounted route accepts transcript removal or Scene MOVE/HOLD; current generic mixed producer capture remains a known prerequisite. Run the single collected journey later in the approved browser/Runtime gate. If it refuses, retain the refusal annotation and report that limit. If it accepts, retain the exact command, retry, protected-row, reload, and undo evidence. Do not close the writer or fresh-creation carrier rows from this source review.
