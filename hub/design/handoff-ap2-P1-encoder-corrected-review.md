# P1 corrected encoder corpus review

## Verdict

**PASS for the new encoder corpus test only; not H3 GO and not completion of full P1.**

Source under review:

- HEAD: `d3e141fa5bb544db6eb083d0e08a564f92df67ad`
- Tree: `991c6720b89302e5a375845542ae03a9af4bb666`
- Added test SHA-256: `198a22068c6c99b2ece932273a4728068a559e97da94586037b893f9130a946b`
- App integration comparison: `794d365ae03725453c3359d21c791b1ffe7ccee9`

## Review findings

The cumulative product diff from App integration contains only
`src/tools/video-editor/commands/p1EncoderCorpus.test.ts`. The existing
`p1FeasibilityCorpus.test.ts` is unchanged. Its corpus still contains the same
8 pinned source cases: 7 exact current-source checks and 8 historical
`git show`/SHA-256 checks.

The corrected split assertion is complete and exact. It covers:

- the parent physical root (`revisionId` and `contentDigest`);
- the entire inserted `right` payload, including unknown/opaque/null/false/zero
  values;
- absent insertion guard, stable created ID, original order, and insertion
  anchor;
- all three intended `clip-a` updates with their original previous values;
- exact before/after clip arrays and the mirrored `config.clips` array;
- preserved registry, name, unknown, output, opaque, and params fields; and
- input, output, and constructed-after immutability.

The complete `changes` array uses `toEqual`, so omitted or unexpected changes
fail. The existing trim case remains complete, including tagged present guards,
explicit removes for `for` and `until`, root, mirrors, and preservation checks.

Actual import callers of `documentPatchIntent` are:

1. `src/tools/video-editor/commands/documentPatchIntent.ts` (the definition);
2. `src/tools/video-editor/commands/documentPatchIntent.test.ts`; and
3. `src/tools/video-editor/commands/p1EncoderCorpus.test.ts`.

There is no production encoder caller or mounted encoder path. This is interim
isolated test coverage; it does not satisfy “the production caller uses it.”
The split→trim of the created clip, intervening Agent edit, lost
acknowledgement, and restart/mounted caller chain remains explicit
`authored-not-go` and unexecuted.

## Exact checks

```text
$ node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/commands/p1FeasibilityCorpus.test.ts src/tools/video-editor/commands/p1EncoderCorpus.test.ts
 RUN  v4.1.5 /home/user/work/wt/ap2-P1-encoder-corrected-review
 Test Files  2 passed (2)
 Tests       14 passed (14)
 exit 0

$ node node_modules/typescript/bin/tsc --noEmit
 exit 0

$ node node_modules/eslint/bin/eslint.js src/tools/video-editor/commands/p1EncoderCorpus.test.ts --max-warnings 0
 exit 0

$ git diff --check
 exit 0
```

The combined run included the existing provenance checks and did not reproduce
the prior sandbox-only `spawnSync git EPERM` failure.

## Explicit limits

No full, browser, live-socket, heavy, install, or central-service run was
performed. H3 GO is not claimed. The production split capture/submit mount,
dependent trim against the created ID, intervening Agent edit, lost-ack/restart
chain, and full v2 request/reply ABI remain separately required.

In particular, unverified v2 evidence still includes ABI 1 scope/base/commands,
label, step metadata and patches, optional reads, `fields|atomic`, dry-run and
`Idempotency-Key`; accepted/merged canonical closure/digest/heads and
`rebased_onto`, authentic receipt, commands, authoritative steps/dependencies
and merge mode; conflict reason/head; invalid code/path/hint/suggestion; and
dry-run/history behavior.
