# D100 six-node receipt — finite custody disposition

## Ask

Record one finite source/result custody disposition for the six corrected D100
shared-item setup controls. Apply D120: the existing Runtime receiving owner
consumes one fixture-only Agent correction, gets one protected review, and then
merges normally. No new body, approval gate, collector, native route, or
product-release claim is created.

## Owner / By

- Owner: existing Runtime receiving owner.
- Agent source: `3aaf24388f0a3f5f2268bea3836f052feb735973`
  (`tl/agt-R1-D100-duplicate-seed-1100`), fixture only.
- Protected review: `agt-R1-D100-seed-review-1104`.
- Runtime: genuine `1daca2a33f6d7b10053e07c539a54843e3984e19`, tree
  `a522511414947e48e317a5e5c2103483b121a750`.

## Result

The author result is six PASS in 3.42 s; the protected result is six PASS in
4.00 s. The six selectors are exactly the former duplicate-`chapter-1` setup
nodes in the companion evidence packet. The correction consumes already
registered roots and creates only missing roots through the normal timeline API.
The earlier `dd2fc26` actual remains recorded as 20 PASS / 6 FAIL with one
duplicate-chapter setup group. This receipt closes only those six setup nodes;
it does not reinterpret the old result or expand membership.

## Evidence boundary

The author/protected XML result identities are retained privately; this packet
exports no raw XML, logs, credentials, URLs, bodies, or media. Source, JSON,
hash-lineage and AST checks pass. The four reviewed Agent product/test blobs
are unchanged across the correction; the only changed path is
`tests/sdk/test_sequential_shared_item_provenance.py`. Runtime’s store guard and
the product/source contract remain unchanged.

The exact20 and original TEN are disjoint and conserved. Original TEN/inverse,
product-batch, and full-chain acceptance remain held and distinct. A private
custody receipt is not product release; production still uses genuine
Agent-captured shared items.

## C0 v2 shape check

The receipt records the required request fields (`api_version`, project/timeline
and base IDs, commands, label, steps, merge, reads, dry-run and the
`Idempotency-Key`), step fields (`id`, label, intent, tags, command ordinals,
patch, reads), accepted/merged result fields (canonical document, receipt, head,
effects, bindings and dependencies), conflict head/reason, invalid code/path/
hint, and dry-run no-write/unchanged semantics. This is a shape check only; no
commit request was issued.

## Not run

No 20/TEN/26/old60/P4/full rerun, test service, browser, socket, collector,
native route, upstream write, hub write, credential action, retry or alternate
was performed.
