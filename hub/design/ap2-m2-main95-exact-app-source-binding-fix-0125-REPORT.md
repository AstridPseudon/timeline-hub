# App2 current95 exact App source binding

## Result

Closed the profile-review0111 custody gap in the existing normal014 helpers.
The final95 profile now selects one of two reviewed, frozen App source tuples:

| source role | App commit | App tree |
| --- | --- | --- |
| parent | `25155ccb22728780a3ecd6379a929cad75cc1400` | `972d2ed2e4f85f334eb9f2e6ca40d9bfbce9eac7` |
| bootstrap | `dfdbef10f9d8ccf1a630f000cd076023918ead8a` | `33674ef4bbaa4b043baed77492621095cccc28f7` |

The parent tuple is the completed stage0125 source root. The bootstrap tuple
is the exact source approved by the independent bootstrap bridge-base review
0125. The suite entries select `parent` and `bootstrap` explicitly; an
unknown final95 source role fails before source preparation.

`verify_app_source` now checks the supplied App root's package marker, real
repository root, exact HEAD, exact `HEAD^{tree}`, clean tracked and untracked
status, and four pin files byte-for-byte against approved App pin commit
`10fa2ff9a8216604aa39e3584f89dc9e7a09080a`. The App root is checked before
and after the normal private overlay/updater preparation. The old202 default
profile bypasses this new final95-only guard and retains its old source tuple
and behavior. No App repository source-identity hash was added.

## Changed orchestration artifacts

These are the explicit before/after SHA-256 values. No product source,
dependency, lock, generated client, or shared install was changed.

| artifact | before | after |
| --- | --- | --- |
| `design/normal014-source-common.sh` | `1e3708e5dff0b0acc251e9c97d802aa39383fe52435d229448e3517ebbe9a101` | `3b2018de1fbc123135590c37d4b17e995fd194fc39089b793e3f1b82e742bd56` |
| `design/normal014-app-central.sh` | `766e0b6a38a5d450a92aee8424d181041c54d523a8ea1427316cf02f3809d68c` | `65ea14c97c8bafccb53ae3ccc7054c380f409f211281ca46afbcaeed23e7f30f` |
| `design/normal014-parent-media-central.sh` | `69507020c13b7351fd8350e39e481a186f21d4d4c4a98300102a4625f1142ffb` | `1d2ebce742bab9a20a911baedab8e7e318e82d6f1043f7f554949855acf646fd` |
| `tests/suites.conf` | `f4f2dbffaee51a9213b87ff449fd432cff4dfbab5bc7adb3a35849ae79da14e4` | `9bb3b11d4e7292adb4ca9ca40203a86eeb815911a5896c1a23ccca2a3f39fbc7` |

The four App pin bytes match the 10fa reference in both reviewed commits:

```text
runtime.lock.json                                      770352eaf1d015e90fca0ed2f1893749b73b69356ca82a7223b2573276fe485e
src/integrations/runtime/generated-contract-metadata.ts 4cd934d868eafd5ab82578da2232f1ee13f04d83c9314b3473b75bd951570044
src/integrations/runtime/generated.ts                  c575f183b6486dd07e8ec798f5a46bff4c9ffc0918892b189c1a433b9f80762d
src/integrations/runtime/timeline-commit-types.ts      f8cbbbbc48713a308c2ac2e2e977d08525c4280ef4dc93cd3e8d842245394564
```

## Verification

Passed, offline:

- `sh -n` on all three normal014 helper scripts.
- Exact object and tree checks for both reviewed App tuples.
- final95 role-to-tuple selection for `parent` and `bootstrap`.
- old202 source-constant and compatibility probe.
- unknown source-role refusal.
- missing App root refusal.
- foreign/dirty current App root refusal.
- both runner preflight entry points refused the foreign App root before
  preparation, installation, browser, or network work.
- all four pin bytes matched 10fa in both reviewed App commits.

Not run by instruction: normal014 real gates, browser, localhost/live socket,
full suite, install, new venv, network, or mutable-source approval. A positive
guard invocation against a clean checked-out frozen App root was not possible
after the prerequisite worker worktrees were recycled; the exact reviewed
commit/tree objects and four pin bytes were verified read-only instead. No
Git worktree was created because the task forbids Git metadata mutations.

## Decisions and next steps

The existing profile mechanism was extended with a closed source-role enum;
no wrapper, new framework, caller-controlled source identity, or App self-hash
was introduced. The orchestrator must run any later gate only from a clean
App root matching the selected tuple and must obtain independent custody
approval of these helper hashes first. The prior `4657` result remains
unqualified.
