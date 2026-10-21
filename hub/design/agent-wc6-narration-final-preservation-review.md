# WC6 narration preservation review

## Decision

**REQUEST CHANGES — exact authoritative narration carrier is still missing.**

Reviewed commit `a3a694312a220d34bc0f0ac49d885c5ff82d7cf6`, tree
`06e3f9b3ab238ab8cd34b934b157d45854358ff5`, on
`tl/agt-m2-wc6-current-published14-final-forward`.

This is the correction review of the prior independent finding, not a new WC6
audit. The new native proof is materially stronger and does preserve a real
text binding, but it does not preserve the same authoritative narration
descriptor/text carrier as the original positive.

## Exact missing carrier

The original `test_real_runtime_import_and_parent_publication_roundtrip`
created an authoritative Runtime binding with:

- `kind: "voiceover_script"`;
- `slot: None`;
- text bytes `b"hello"` (and the Runtime-returned content hash/byte size);
- the returned authoritative binding identity and media descriptor, then
  placed that descriptor plus `text: "hello"` in the shot snapshot.

That setup was removed at commit `25d4b9040` and replaced with
`shots[0]["payload"]["text_bindings"] = []` at
`tests/timeline/test_authoring_media.py:331-333`.

The native proof now asserts non-empty narration and exact equality at
publication and reload (`:607-608`, `:649`, `:666`), which fixes the empty
binding regression for its own fixture. However, its source closure is the
pre-cut film fixture. A direct read of that authoritative fixture gives the
different descriptor `kind: "transcript"`, text `"Open on the river"`,
17-byte content hash `sha256:fef50eab9e9b23b75133cf7553faee605c3ff14d993599c8d2c551030f0bcb3d`,
and the corresponding transcript binding identity. The proof does not create
or independently read a `voiceover_script` binding, nor assert the original
`hello` bytes/descriptor. Equality to a non-empty checkout value is therefore
not a one-to-one proof of the original authoritative narration behavior.

Required correction: retain the native command proof, but give it a supported
Runtime-authoritative `voiceover_script` carrier equivalent to the original
binding (or an existing fixture with that exact carrier). Assert the exact
descriptor identity/kind/slot, text bytes, content hash and byte size at
checkout, then assert the same authoritative descriptor/text on accepted
publication and a fresh checkout after reload. Do not restore the whole
legacy writer and do not convert this positive to skip/xfail.

## One-to-one ledger

| Original behavior | Current evidence | Review result |
|---|---|---|
| Authoritative `voiceover_script` descriptor and `hello` text binding | Old setup is emptied; native proof carries a `transcript` binding with different text | **Missing; REQUEST CHANGES** |
| Image/audio import and catalog reuse | Original test still retains the image+audio import/replay assertions at `:408-416`; native proof additionally exercises the native image import | Retained, but still on the legacy test’s setup path |
| Selected media and dependency closure | Native accepted document asserts the new media in the shot item/assets and exact command media pins (`:646-657`) | Preserved/strengthened |
| Local path is not published | Native document diff places the local path behind the native import; the inherited 233-pass evidence covers this path, but the new test does not assert `local_path` absence in the canonical document | Existing bounded evidence; not the narration blocker |
| Raw closure and opaque/order preservation | Exact alias order and opaque registry value, clip order, opaque namespace, source-window fields, and untouched `shot-2` are asserted (`:639-653`) | Preserved/strengthened |
| Receipt/history | Accepted publication and history receipt are asserted (`:626-629`, `:658-659`) | Preserved/strengthened |
| Lost-ack exact retry after restart | Outbox key/body, dropped response, restart, identical wire retry, accepted receipt/head/history are asserted (`:670-734`) | Preserved/strengthened |
| Inverse and A→B→A protection | Undo returns the baseline; disjoint rebase succeeds; changed opaque input is held; ABA inverse conflicts (`:720-787`) | Preserved/strengthened |
| Native path has no fallback publication | The document script emits exactly `occurrence.swap-media`, `clip.move`, `clip.set` and commits through `TimelineSession`; the legacy writer remains only in the retained old positive/setup paths | Bounded native proof has zero fallback; do not claim global legacy-writer removal |

## Evidence used

- Final-forward worker report: targeted **233 passed, 2 deselected**;
  Runtime95 HTTP proof **1 passed in 10.23s**; Ruff and `git diff --check`
  passed.
- Concrete local fixture inspection used the exact Runtime fixture and
  public binding read. It confirmed the native proof’s carrier is `transcript`
  / `Open on the river`, not the original `voiceover_script` / `hello`.
- This review ran `git diff --check` locally and did not rerun the already
  qualified direct/HTTP suites, per the task instruction. No full, browser,
  renderer, or repeated HTTP suite was run.

Once the exact authoritative voiceover carrier and byte-level publication /
reload assertions are added, the existing native lifecycle evidence is the
right bounded replacement evidence for this review.
