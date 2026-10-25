# D116/G3 verdict: exact unapplied source dependency

`SOURCE_DEPENDENCY`.

The current fixture’s authenticated initial source contains `parent/clip:card`’s `on` word anchor, with the exact choice source `occurrence:occ/clip:voice`. The required Gate3 authored topology ends with `parent['occurrences'] == []`. The existing registered public `occurrence.delete` command clears `occurrence:occ`; its recorder then recompiles the remaining card anchor and refuses at `native_word_anchor.py:71` because its bound occurrence/clip is missing.

There is no compliant caller-only correction in `native_checkout_current_fixture.py`: clearing/rebinding the anchor changes authored input, retaining the occurrence violates the exact Gate3 predicate, and generic membership/private history routes are forbidden. No product or compiler change is proposed.

Owner scope for the unapplied dependency is the Agent semantic-command/anchor integration owner (`native_occurrence_delete` plus the `native_word_anchor`/recorded-compilation interaction). The App fixture owner cannot proceed without an approved public semantic behavior or an independently proved equivalent initial source that preserves the complete authored anchor/card/word/occurrence purpose.

Static source checks pass; functional behavior and retirement credit are unverified/not claimed. No worktree source edit was made.
