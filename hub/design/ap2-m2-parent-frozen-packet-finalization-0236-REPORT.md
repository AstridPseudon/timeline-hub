# Parent frozen packet finalization 0236

## Result

Final parent source identity is closed to the committed author source:

- commit: `da6d910f7ab3dfc71142ece7f632d43341238882`
- tree: `6809757f93ca5e166b24b8bc0160ca09005e984a`
- parent: `7e85d89120227f336a2a8dbf8e0ea44d98311da0`

I read the final branch with `git show` after the harness commit. The final
bytes contain the exact mounted negative assertion: HTTP `404`, code
`not_found`, and message `selected media is not a managed project
generation/variant/object`. The original valid ADD/recovery/opaque/raw,
undo/retry/reload, and zero-legacy assertions remain in the final commit.

The only source change was the existing closed `final95:parent` selector in
`normal014-source-common.sh`:

```text
APP_ROOT_SHA=da6d910f7ab3dfc71142ece7f632d43341238882
APP_ROOT_TREE=6809757f93ca5e166b24b8bc0160ca09005e984a
```

The bootstrap selector remains unchanged:
`dfdbef10f9d8ccf1a630f000cd076023918ead8a` /
`33674ef4bbaa4b043baed77492621095cccc28f7`.

## Guards and callers

The existing ancestry, exact tree, clean-state, four App pin bytes, Agent
`6efc81500a0e0688c2bb41e736503f0fc3e04abb` / tree
`2ed2b8a12b5b3391ca221ba6ff05390f71a73556`, Runtime and producer
`95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` / tree
`d3a290b407fa61e6ab2d476f50c068073f70df00`, artifact, schema, import, locked
graph, and postflight guards remain intact. The producer still requires its
exact real HEAD.

Live callers are the existing `normal014-parent-media-central.sh` and
`normal014-app-central.sh` wrappers. The finalized parent evidence driver
`tests/e2e/local/support/run-parent-manual-drop-evidence.sh` selects
`NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent` and is bound to the
same source helper.

Helper SHA-256 values after this change:

```text
normal014-source-common.sh        3dc9034586bf8c6fe2ff877b44fd1cbbabfb4eeeb1472fe009bad6d677811014
normal014-parent-media-central.sh 1d2ebce742bab9a20a911baedab8e7e318e82d6f1043f7f554949855acf646fd
normal014-app-central.sh          8f70ed7adafa42d90b3053f5972bd763a653ae690c1b2dfda352e3704615686e
```

## Evidence

- `sh -n design/normal014-source-common.sh design/normal014-parent-media-central.sh design/normal014-app-central.sh` — PASS.
- Source-only exact-parent preflight, using the private checkout at the final commit and the existing `normal014-parent-media-central.sh preflight` command — PASS. It verified 76 artifacts, manifest `a902387c...`, and schema `6ba7b51e...`; no browser, socket, or real case ran.
- Negative source-identity probes — PASS: wrong tree refused, dirty source refused, wrong pin refused, and missing provenance refused.
- Bootstrap selector smoke — PASS and unchanged.
- Assigned App worktree remained clean; no product files were edited.

The first cause of the prior stale review was source timing: reviewer0230
inspected the provisional pre-harness source while the old helper still
expected author tree `972d2ed2e4f85f334eb9f2e6ca40d9bfbce9eac7`. The harness
then committed the exact negative and produced the new committed tree
`6809757f...`; the selector now names that final commit/tree.

## Handoff

Independent code/custody review is ready against the exact final commit and
the helper hashes above. The existing source-only command is:

```sh
env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent \
  bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-parent-media-central.sh \
  preflight "$PWD"
```

No browser/socket/full/real-case gate was run, as required. The next step is
independent code and custody review, followed separately by the authorized
existing parent gate if that review accepts this packet.
