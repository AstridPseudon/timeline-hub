# WC8 mixed current-forward landing

## Result

The uncommitted resolved worktree is based on Agent commit
`970a662af444b00e437507a4f08d8a0aa53ce521`, tree
`d8dae6b06ba1cd1ef163b5b48c7e237c86007942`. Its intended true merge parent
is hub Agent commit `b79fec587dc7bab3fcb0624785d38faa519b3c93`, tree
`02c9f56468f676bbc53a548c9295cf5e3a31ea89`; the harness will create the
commit. The common ancestor is `345085a511d05bc136672de1ff7236f2284bfb84`,
tree `e958a5def5fd3874eef83a68f95595dc7e6a9db8`.

This is a current-preserving WC8 packet. The base's retained literal and
mixed-sheet behavior remains intact, including the reviewed unsupported-edit
refusal tests and the new combined-field HTTP test. The hub's two unrelated
Agent changes were applied exactly:

```text
astrid/core/timeline/scene_roles.py
astrid/sdk/timeline/checkout.py
```

No new behavior was added by this worker.

## Three-way/path audit

The hub delta from the base names five paths:

```text
astrid/core/timeline/scene_roles.py
astrid/sdk/timeline/checkout.py
astrid/sdk/timeline_sheet.py
tests/editing_conformance/test_native_sheet_ordinary_runtime.py
tests/sdk/test_timeline_sheet_native.py
```

The hub has no delta on the three WC8 paths relative to the common ancestor,
so they were preserved byte-for-byte from the base. Their final/worktree
blobs are:

```text
astrid/sdk/timeline_sheet.py
  9dbf5945df16a5baae39b44907d73390c70c1e66
tests/sdk/test_timeline_sheet_native.py
  f2aad63fc756e708669567da5d4a4321dc883fcc
tests/editing_conformance/test_native_sheet_ordinary_runtime.py
  fe4b888f25c0b930f44e0b09c7228550666b2ccb
```

For the three allowed overlaps, `base == worktree`; independently,
`common ancestor == hub` for each path. Thus there was no unsafe source
overlap to resolve and no assertion was dropped. The literal escaping callback,
original target/basis/key/body/source guards, mixed local grammar, both
retained mixed/refusal tests, and the actual combined-field node all remain in
the preserved blobs.

The outside-path audit is exact: `git diff b79fec... --` reports only the
three allowed WC8 paths, and `git diff 970a... --` reports only the two hub
paths above. No tracked mode changed. No provider harness changed, so no
provider test lane was needed.

## Tuple/artifact preservation

The following Agent repository bytes are identical in base, worktree, and hub:

```text
runtime.lock.json       717d1c8ca0c1f0ef36653a96f6e9b7318b1ebfa8
artifacts.json          1425518b188e638218b1bcc73f0e506663a83833
remotion/package.json   8057a6d6b7cd63409bbaacc83d5408bc36f6aa2c
remotion/package-lock.json
                        2b3bc9c1f881ff22426d216b324ca162146e6322
```

No generated file, lock, source pin, caption/later source, or artifact was
generated or edited. The previously qualified shared tuple remains the normal
published95/all76/ordinary6ba/C13 tuple; the prior C13 artifact hash was
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.

## Reused evidence

The preserved base tree is exactly the snapshot tree used by central service
run `rt-m2-wc8-mixed-one-http-0706-rt-wc8-current14-integration-1021070813-7975`.
Its bounded result was:

```text
test_current014_detached_mixed_text_duration_uses_one_native_http_batch_and_guarded_inverse[detached-historical]
1 passed in 5.27s; service result exit 0
```

That run used Agent base `8abeae344...` before the test-only `970a...` node;
the combined-field test is the exact node added by `970a...`, and its snapshot
tree is the current base tree `d8dae6b06ba1cd1ef163b5b48c7e237c86007942`.
The compatible Runtime was b92 with the normal published95 client. Existing
literal and duration evidence remains prior evidence and was not replayed.

No full, socket, browser, render, install, schema, generator, pin, or release
lane was run. `git diff --check` passed.
