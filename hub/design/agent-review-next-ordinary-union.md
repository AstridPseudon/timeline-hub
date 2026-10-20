# Bounded review: next ordinary Agent source union

**APPROVE bounded additive union for the new source joins, with final ports
and gates below.** This is not approval to publish, freeze, merge, or claim
final core proof.

Reviewed candidate commit `ce3e647f10f6b7950de19e4219da6d55af4d3939`
(`feat(timeline): prepare complete next ordinary command union`), based on
`4ef1391c2c104d5d11b3a27265035c51be296045`. Its content tree is
`260f2615b869b5e0d8ab236d6c1fbc952c0f6186`, matching the handoff. The review
worktree remained at `8e3107853d17453758a933d1f47215cc1c002660`; no product,
test, integration, branch, or shared-dependency files were changed.

## Scope and result

I read PLAN, the source-union design/report, and the reviewed source tips
`537c2ecd` (S3), `09ca873c` (native text), and `0937d6fd` (parent-auto
completion). I did not re-review unchanged generator bulk. The new overlap is
bounded to keyed text-binding collection/state/recording, inverse coalescing
and staged cache replay, authenticated root-birth replay in reservation and
media-inverse paths, exact source hydration, the parent-auto completion
follow-up, and their tests.

The two new join repairs are sound in the inspected paths:

- A born occurrence/shot is replayed through `Recording.create_entity` only
  when the exact root identity is present in the accepted record's `created`
  facts. This preserves the source-free creation proof without a guessed
  owner, cache blanket exemption, or opaque rewrite.
- Keyed text rows use `binding_key`, preserve recorded insertion order, and
  retain EMPTY versus ABSENT. `text-binding.owners` records an empty
  membership/boundary when its occurrence is absent, allowing grouped redo
  after root removal while retaining the normal ownership guard when present.
- Staged cache writes remain separately guarded and are replayed with the
  root's authored writes. Parent raw/config mirrors and asset dependents are
  still checked through their authoritative structures.
- Source hydration accepts a restored transcript pin only when the exact pin
  and media pair occur in the authenticated inverse closure. Normal hydration
  still reads the requested exact pin through the Runtime port and verifies
  project, version, content digest, transcript identity, and media identity;
  it does not use caller/latest state.

No new root-cache blanket ignore, numeric normalization, opaque rewrite,
schema override, fake history/SQL/Prepared provider, or lost operation/type
was found. The candidate preserves **55 definitions / 29 operations** and
the full S2 floor of **48 / 22**; the candidate's canonical schema has raw
SHA256 `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`
and canonical JSON SHA256
`63ac77b3c3e2c582f76ab4b2499be5011ea4836e8c92264b1938632b3bfacba7`.

The parent-auto original guards, saved policy/defaults, and consumed reads
remain covered by the candidate's retained tests. The current public
schema/client/lock is not changed by this candidate.

## Independent evidence

All commands ran against a private archive of the candidate with
`PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH` set to that archive, private
pytest basetemps, and no full/full* suite.

Normal private Runtime generation used committed Runtime `b748ae723b51c6d578ba7a393209ce37d6e2b0c3`, with only the candidate schema
supplied as the ordinary schema input. Generator check, TypeScript
conformance generation/check, and artifact manifest/check all passed. The
normal private Runtime output had 13 generated changes and artifact identity
`sha256:7e8fe2e485f036741369eed62ccc7a389e27719a166fd70b0009a161c9c7240d`.

Source/schema/pristine/native-portable lane:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$CANDIDATE \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= \
  -p no:cacheprovider --basetemp=$PRIVATE/tmp-schema \
  tests/sdk/test_timeline_current_union_schema.py \
  tests/editing_conformance/test_pristine_initialize.py \
  tests/editing_conformance/test_recipe_text_binding_native.py \
  tests/editing_conformance/test_recipe_parent_auto_completion.py
```

**184 passed in 202.29s; exit 0.** This covers current S2/schema floors,
pristine stripping, native text semantics, and parent-auto portable cases.

Native Runtime lane against the normally generated private pair:

```sh
ASTRID_RUNTIME_CHECKOUT=$PRIVATE/runtime-private \
ASTRID_WORD_ANCHOR_SEED_RUNTIME=$PRIVATE/historical-word \
ASTRID_PARENT_MEDIA_SEED_RUNTIME=$PRIVATE/historical-parent \
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$CANDIDATE \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= \
  -p no:cacheprovider -m integration --basetemp=$PRIVATE/tmp-integration \
  tests/editing_conformance/test_next_ordinary_union_runtime.py \
  tests/editing_conformance/test_commit_runtime_text_binding.py \
  tests/editing_conformance/test_commit_runtime_parent_auto_completion.py \
  tests/sdk/test_timeline_selected_schema_runtime.py
```

**57 passed in 83.76s; exit 0.** This includes first initialization,
occurrence birth plus media/text, clear and grouped inverse, exact order,
redo, restart, exact idempotent retry, text source/MIME and stale/atomic
negative cases, parent-auto stale guards, and selected-schema Runtime
coverage.

`git diff --check 4ef1391c..ce3e647f` also passed with no output. No full,
browser, live socket/HTTP, renderer/audio/pixel, App, macOS, or public-client
qualification was run or requested.

## Required final ports and remaining gates

These are required before public freeze; they are not defects found in this
bounded review:

1. Port current core F1 fix `8e3107853d17453758a933d1f47215cc1c002660`
   into the final candidate. It adds staged-record intervening-write guards
   in `inverse.apply_inverse` plus the command/inverse/conformance coverage.
   The reviewed candidate has no `staged_records` implementation. Registry
   and schema remain unchanged by F1. Do not claim final core proof until
   this port is tested on the composed candidate.
2. Port the separately approved media-fixture migration
   `134f1c276a11b4703c7a76f25cbf13158e4a4416`; this source union still has
   the two old fixture-import failures reported by the preparation worker.
   They are migration residue, not a failure of the new birth/text joins.
3. Keep the four existing renderer-request strict-xfail holds visible and
   keep the parent follow-up/manager gates and fresh-version Runtime
   generation/publication separate. Do not republish the existing 0.2.13
   artifact or treat the private generated pair as a public tuple.

No blocker defect remains in the reviewed new overlap. This bounded approval
does not claim destructive GC, producer admission, App cutover/outbox,
transport, renderer parity, or owner-film qualification.
