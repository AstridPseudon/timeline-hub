# App2 M2 producer ownership live-proof preparation

## Result

Prepared one new focused Playwright route proof and one support adapter:

- `tests/e2e/local/producer-ownership-live.spec.ts`
- `tests/e2e/local/support/producer-ownership.ts`

No existing spec, shared three-products journey, production source, DTO, authority, API, suite wrapper, or source-repair file was changed.

The adapter seeds a dedicated timeline through the existing Runtime publication helper. It includes transcript data, a media carrier, Scene markers, one foreign-owned and one user-authored transcript clip, and one foreign-owned and one user-authored Scene clip. The spec drives the mounted transcript Regenerate and Scene Create/Move controls, observes the normal `/commit` request body, and compares the protected clips' complete raw values and list order after each action and reload.

If the active native route accepts the producer batches, the case checks:

- fresh transcript and Scene output carries the existing `app.managedBy` carrier after acceptance and reload;
- a lost-ack Scene submission is retried with the identical request body after reload;
- a second transcript action and Scene alignment do not target either protected ID;
- protected clips remain byte-for-byte equal, including payload/app data and order.

If the current route refuses the mixed producer batch, the case retains that visible `Native patch refused` atomic refusal, retries the transcript action after reload, runs the Scene action, and verifies that no commit targets a protected ID and no protected clip changes. It does not manufacture accepted output or claim the success path.

## Pinned contract decision

The safety review and active source agree that producer batches contain structural `clip.add` members plus non-scalar/app-bearing `clip.update` members. `useTimelineOps` routes a mixed batch to generic capture. The generic native family supports ordinary scalar/hold, same-track absolute move, trim, label, and structural members, but refuses these mixed app-bearing producer updates atomically. The proof therefore keeps the refusal branch visible. The exact prerequisite for the accepted branch is an approved native capture member/carrier that preserves the existing producer ownership app fields through the normal command/session path.

The source-repair worker's ownership-carrier changes were not edited or copied. This worker only prepares the consumer route proof for the repaired source to run later.

## Checks

Passed:

```text
git diff --check
```

```text
node_modules/.bin/eslint --no-cache --no-warn-ignored --max-warnings 0 tests/e2e/local/producer-ownership-live.spec.ts tests/e2e/local/support/producer-ownership.ts
```

Passed exact case collection using a private one-file Playwright collection config, removed immediately afterward:

```text
TMPDIR="$PWD/.tmp-producer-ownership" node_modules/.bin/playwright test --config .producer-ownership-collection.config.ts --list
# Total: 1 test in 1 file
```

No browser, localhost, Runtime socket, live door, full suite, or gate run was performed.

## Blocked and next step

The accepted/reloaded success branch is unverified by design because the current pinned generic route atomically refuses the mixed producer members. Run this one case centrally after the source repair is integrated with the normal Runtime/door/outbox cohort. Record whether the native prerequisite has landed; if refusal remains, retain the refusal result and do not claim fresh ownership acceptance. If acceptance is enabled, the case's reload, exact retry, derived ownership, protected-clip preservation, and target checks are the required evidence.
