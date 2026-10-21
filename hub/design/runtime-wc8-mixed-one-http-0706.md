# Runtime WC8 mixed one-HTTP case

Date: 2026-10-21  
Result: bounded new combined retained-sheet HTTP case passed.

## Scope

The Agent test branch is based at `8abeae34414d9399b5d9d94150ba1f28519c89d7`
(tree `a986c13718d94287ace384823c3fb5c0f4693552`). The Runtime was unchanged:
`b92d3e7a05eec65c142294ef4873edd059e9b31d`, tree
`6abc2f117391de8e7e35c0283f575a002199894d`. The only source diff is one new
test node in the existing Agent conformance file. No schema, generated client,
lock, Runtime, fixture, or product path changed.

## Qualified behavior

`test_current014_detached_mixed_text_duration_uses_one_native_http_batch_and_guarded_inverse[detached-historical]`
uses the real current014 historical fixture and retained original export
target/basis. It edits both the type card's literal text and static duration,
asserts the exact two native commands and original basis in one HTTP request,
preserves opaque data and the other video row, and verifies restart readback,
inverse, redo, and guarded inverse refusal.

Central service snapshot tree:
`d8dae6b06ba1cd1ef163b5b48c7e237c86007942`.

Run ID:
`rt-m2-wc8-mixed-one-http-0706-rt-wc8-current14-integration-1021070813-7975`.
The exact named suite selected one node and passed with exit `0`, count `1
passed`, pytest time `5.27s`, service time `7s`, requested at
`2026-10-21T07:08:13Z`.

## Not claimed

This is not a full WC8 result, deletion claim, source-safety verdict, merge,
pin, renderer/browser result, or repeat of the prior literal/text or duration
passing cases. The local sandbox's socket bind preflight failed with
`PermissionError: [Errno 1] Operation not permitted`; the central service was
used for the authorized live HTTP proof. No full, browser, render, install,
old passing proof, or retry chain was run.
