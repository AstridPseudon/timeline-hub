# App2 M2 selected final95 custody review

## Verdict

**HOLD.** The selected App source and final95 pins are internally consistent,
but the owned runner's later `SELECTED_FINAL95_MODE=run` path is not closed for
one immutable central actual. No App source or driver fix was made in this
review.

## Recomputed source and pin evidence

All identities below were recomputed from Git objects or the referenced files,
not copied from the owned-driver report.

- App `HEAD` is `ba02c8f246ec61cd65d178a1ada686788df3fdab`; its tree is
  `7fe8c15b56da9944ae31e8273d41d3ceb21b3677`.
- HOME base is `42b0c6c8434e2c491f8dbdf00a210ed755e41a95`; its tree is
  `fa887b5689d7ad44957021080f74d13a9d0c4e30`. The only base-to-HEAD product
  change is `tests/e2e/local/three-products.selected-param-dev.spec.ts`,
  `27` insertions and `5` deletions.
- The selected spec SHA-256 is
  `10250fa44db4e2d4423f8d06258105df267e3ba4e29700d700bb1d3182a6def1`, and
  it is byte-identical to approved commit
  `8e9975005d18c6278000ab4c8cc8b18291d03e12` (tree
  `87d2350417a876e14b81c58b64da29f1a30b35b6`). The approved real-scope
  semantics are therefore reused exactly: real mount, timeline combobox and
  URL identity, clip/P1 surface, P1/P2 admission and source removal, retained
  P1 refusal with draft preserved, lost acknowledgement, reload/recovery,
  exact retry body and idempotency key, inverse, and zero legacy POSTs.
- Unchanged App controls recompute to: `harness.ts`
  `af61e605e1930ae061506a317008d670c7c1be01511c7c1a57188a6a91cc0465`, Vite
  config `5f26c8fa9beae5691c7c94ae11d008eb6c548eb28aaa2b66887b7512efe6c70d`,
  discovery proxy `93989e634008d1c9a6aaeddbca7b0aa0f97c40a7ce232860157d04bc6b2155c0`.
- Agent `6efc81500a0e0688c2bb41e736503f0fc3e04abb` has tree
  `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`; Runtime/producer
  `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` has tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`.
- Runtime `contract/artifacts.json` recomputes to manifest SHA
  `a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`,
  76 entries, and version/artifact SHA
  `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`.
  Every listed artifact matches its committed bytes and producer checkout.
  The Runtime and Agent edit-command schemas are byte-identical at
  `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.
- App normal lock is `770352eaf1d015e90fca0ed2f1893749b73b69356ca82a7223b2573276fe485e`;
  generated metadata, generated client, timeline types, and vendored schema
  recompute to `4cd934d868eafd5ab82578da2232f1ee13f04d83c9314b3473b75bd951570044`,
  `c575f183b6486dd07e8ec798f5a46bff4c9ffc0918892b189c1a433b9f80762d`,
  `f8cbbbbc48713a308c2ac2e2e977d08525c4280ef4dc93cd3e8d842245394564`, and
  `f52b82024ecd44a5e6c9c68d5cb326d50d70efe9aaad6f8ac6352ea1c87b97b1`.
- The locked graph archive recomputes to
  `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`;
  its nested Composition `0.0.13` tarball has 77 members and SHA
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
  The graph resolves Node `v22.22.0`, Vite `5.4.21`, Vitest `4.1.5`, and
  Playwright `1.60.0` in the offline witness.
- Owned driver SHA is
  `159c1fa4ba6ed4d8b13d33d8230319b923d930a5b61dddb543a0bbe3d93c061a`.
  The protected old driver/helper hashes recompute to
  `a959de6e0041f0d8ee28b949a19f5add97d7fb5de27714da6beaad15abd6ce4f`,
  `d9a691dcaafd7d544a467445a3a020a9ad3d02afc1d527870f00be6948fea848`, and
  `1d2ebce742bab9a20a911baedab8e7e318e82d6f1043f7f554949855acf646fd`.

## HOLD findings in the actual path

1. **The actual launch input is not source-preflighted.** `run` dispatches
   directly to `run_actual` at runner lines 361–365. `run_actual` sources the
   common helper at line 323 and copies `$APP_ROOT` at line 346, but never calls
   the owned exact App verifier (lines 95–108), the normal-lock verifier
   (110–122), or the selected-contract verifier (208–229). Thus a central
   service synthetic/wrong/dirty App tree can be copied into the actual overlay
   after only the initial `package.json` check at lines 10–15. The helper's
   synthetic-tree-aware `verify_app_source` is also only a function definition;
   it is not called by `run_actual`. Moreover, `NORMAL014_APP_SOURCE=bootstrap`
   at line 323 selects helper App identity `dfdbef10…`/tree `33674ef4…`, not the
   required selected App `ba02c8f2…`/tree `7fe8c15b…`.

2. **The actual path does not enforce list-1.** The offline preflight calls
   `verify_private_list`, whose exact title/count checks are lines 312–316.
   The actual path only executes the raw `--list` command at line 355 and does
   not assert one matching test in one file. A zero/multiple collection can
   therefore reach build/actual execution.

3. **Node graph and inherited environment are not fully controlled for the
   actual children.** The owned preflight checks Node/Vite/Vitest/Playwright
   versions at lines 174–191, but `run_actual` only calls the common
   `verify_locked_graph` at line 336; that helper verifies the archive and
   Composition tarball, not those package resolutions. Line 352 pins
   `NODE_OPTIONS`, but no actual-path assignment or unset controls inherited
   `NODE_PATH`; the private `NODE_PATH` assignment exists only on the preflight
   list command at line 313. The Node/Vite/ESM graph can therefore be affected
   by the central caller's inherited `NODE_PATH`.

4. **The actual path leaks its outer temporary root.** The runner creates
   uppercase `RUN_ROOT` at line 61 and installs its cleanup trap at lines 68–74.
   `run_actual` then calls `normal014_start_run` at line 324; the sourced helper
   replaces the EXIT trap at `normal014-source-common.sh:105–119` and cleans only
   lowercase `run_root` at lines 89–94. The uppercase runner root is not used by
   the actual work and is not removed on success or failure. This violates the
   requested cleanup/resource custody.

These are runner-artifact mismatches, not evidence that the selected source or
the final95 object pins are wrong. Per the task, no fix is proposed or applied
here.

## Bounded checks run

Passed:

```text
git diff --numstat 42b0c6c8434e2c491f8dbdf00a210ed755e41a95..HEAD -- tests/e2e/local/three-products.selected-param-dev.spec.ts
  27  5
cmp approved 8e997... selected spec
  byte-identical; SHA-256 10250fa4...
offline committed-object manifest/schema/artifact recomputation
  PASS: 76 artifacts, producer bytes, schema6ba, Agent/Runtime trees
offline locked-graph tarball/package/version witness
  PASS: archive895c, Composition13/9412, 77 nested members, Node/Vite/Vitest/Playwright
sh -n owned runner; sh -n normal014-source-common.sh; node --check scripts/runtime-discovery-proxy.mjs
  PASS
git diff --check
  PASS
```

Not run: the owned runner preflight (it performs the App overlay/list
operation), browser, Vite/build, daemon, localhost/live sockets, central
actual, full suite, dependency installation, or any shared-source/graph/helper
mutation. The worker App worktree remained clean.

## Required next step

Return the owned runner to its owner for a role-only custody correction that
validates the exact selected App input immediately before overlay copy, enforces
the one-test list on the actual path, controls `NODE_PATH`/`NODE_OPTIONS`, and
uses one cleanup root/trap. Then perform one central actual on the exact
immutable selected registration. Do not claim behavioral qualification from
this review.
