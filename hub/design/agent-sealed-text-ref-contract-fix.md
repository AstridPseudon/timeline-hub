# Agent sealed text reference contract fix

## Result

No Agent product or canonical-schema change is needed. The Agent capture is
already the correct sealed form, and the frozen Agent schema is already wide
enough for it. The minimal Agent-side change is a regression test that keeps
the exact authored key visible. The remaining integration seam is owned by
Runtime.

## Exact source and reproduction

- Frozen Agent source: `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3`
- Frozen Agent content tree: `c5a8a3ec7e9e01c61c5ae31834da53bed4be406a`
- Agent canonical schema: `astrid/core/timeline/schema/edit-command.schema.json`
- Agent schema SHA-256: `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`
- Frozen Runtime candidate: `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`
- Frozen Runtime tree: `4b7dd0fe44be973c344bab3de568eaf0bdd28476`

The Agent-native capture produces this key for the first occurrence-owned
voiceover binding:

```text
occurrence:occurrence-1/text-binding:voiceover_script::
```

`_recording.finish()` derives it from the whole text-binding entity write. The
key preserves occurrence identity, compound binding kind, and the empty
property path; it must not be rewritten to a shot/property key or omitted from
`expect`/`authorship`.

The direct Agent reproduction is:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-agent/bin/python -m pytest -q \
  -o addopts= -p no:cacheprovider \
  tests/editing_conformance/test_recipe_text_binding_native.py \
  -k 'exact_capture or authorship_key'
```

This reaches Agent `validate_command`; it does not use a schema override,
prepared history, SQL, or a fake provider.

## Cause classification

1. **Not an Agent codec error.** Agent capture and `_normalize` intentionally
   canonicalize whole-entity writes to `ref + '::' + spelling(path)`. For this
   write, `spelling([])` is empty, so the exact key above is generated. The
   frozen Agent `TargetKey` union admits the text-binding identity followed by
   the empty path.
2. **Runtime integration schema gap.** The current Runtime integration tree
   (`a51af88`, `runtime_protocol/schemas/timeline-commit-bundle.json`) has the
   older `TargetKey` union and rejects this text-binding identity before the
   provider. This is the narrow Runtime-owned gap.
3. **Frozen-candidate discrepancy.** The exact `a0dca169` source tree’s
   generated `runtime_protocol/schemas/timeline-commit-bundle.json` contains
   the same text-binding branch and direct validation of the key succeeds.
   Therefore the reported rejection against `a0dca169` cannot be reproduced
   from that committed candidate as inspected here; it indicates a stale or
   mismatched Runtime source/artifact in that run. This must be reconciled by
   Runtime before any landing or pin decision.

## Exact narrow Runtime proposal

Runtime should ensure its generated `TargetKey.anyOf` includes this additional
branch, byte-for-byte equivalent to the frozen Agent canonical branch:

```json
{
  "type": "string",
  "pattern": "^(?:(?:(?:parent|(?:(?:parent|shot:[^/]+|occurrence:[^/]+)/(?:clip|track|asset):[^/]+|shot:(?:(?!::)[^/])+|occurrence:[^/]+(?:/shot)?|cut:[^/:]+)|parent/shot-group:[A-Za-z0-9_-]+|occurrence:[^/]+/(?:source|registry)|occurrence:(?:(?!::)[^/])+/text-binding:(?:prompt|voiceover_script|transcript)(?::[a-z][a-z0-9-]{0,63})?))::)?(?:(?:[A-Za-z_][\\w-]*|\\[(?:(?:0|[1-9][0-9]*)|\"(?:[^\"\\\\\\x00-\\x1f]|\\\\(?:[\"\\\\/bfnrt]|u[0-9A-Fa-f]{4}))*\")\\])(?:\\.[A-Za-z_][\\w-]*|\\[(?:(?:0|[1-9][0-9]*)|\"(?:[^\"\\\\\\x00-\\x1f]|\\\\(?:[\"\\\\/bfnrt]|u[0-9A-Fa-f]{4}))*\")\\])*)?$"
}
```

This is an additive, closed union member only. It does not admit arbitrary
scope IDs, alter `ScopedId`, remove reads/selections/authorship, or change
text identity/order semantics. Runtime should add direct tests for both
`expect` and `authorship` property names, including the exact key above and a
prompt slot such as `.../text-binding:prompt:speaker::`; ordinary clip/track
keys must remain accepted and unrelated broad keys must remain refused.

The Runtime generator should regenerate its normal bundle only after peer
review. No Agent schema bytes, Runtime DTO, endpoint, lock, release, or frozen
artifact was changed by this worker.

## Peer request

Runtime manager: please verify the exact committed `a0dca169` bundle, its
installed validator/import path, and the source/artifact used by the failed
normal-pair run. If the candidate really rejects the key, apply the narrow
branch above through normal generation and return the new exact Runtime commit,
tree, schema/artifact digests, and targeted validator/native results. If it
accepts the key as the committed source does, correct the qualification command
or artifact selection instead of changing Agent.

The acceptance lane remains: sealed Agent capture -> normal Runtime validator
-> real provider first use with UTF-8 and EMPTY -> reload/retry/inverse/clear
and order preservation -> cross-project and changed-reference refusals before
writes. The Agent unit lane now proves only the capture/codec half; the Runtime
normal-pair lane is not claimed green until this source/artifact discrepancy is
resolved. Existing unsealed positive and history/retry/undo/redo tests remain
unchanged.

## Tests and gaps

Passed locally after the minimal test addition:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-agent/bin/python -m pytest -q \
  -o addopts= -p no:cacheprovider \
  tests/editing_conformance/test_recipe_text_binding_native.py \
  -k 'exact_capture or authorship_key'
```

Result: 2 passed.

Also directly validated the exact key with `Draft202012Validator` against the
frozen Agent schema and the frozen `a0dca169` Runtime generated bundle: both
accepted it. The current integration Runtime bundle omitted the branch and
rejected it. No full suite, HTTP/browser lane, Runtime edit, release, or
consumer pin was performed.
