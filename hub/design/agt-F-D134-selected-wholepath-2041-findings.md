# D134 selected wholepath source review

## Verdict: PASS_SOURCE

This review is source-only. No behavior pass is claimed and no test body or provider rerun was performed.

The immutable first-return commit `4073fb0f84a9d0afbcba61b9406744d749c34d9` restores the three original ABI-1/native request bodies, restores the original `rebased` assertions, and repairs the retired HTTP setup to use the registered commit route with the original parent shape (`config.clips` absent). The independent review’s four source findings are therefore resolved at source level, and all seven UNKNOWN cases remain conserved.

## Normative request classification

The three moved-head requests are newly constructed with fresh keys (`rebase-after-v2` and `authority-retry`). Their bodies contain `api_version: 1`, command `schema_version: 1`, and omit `label` and `steps`; C0 explicitly permits that compatibility form. They do not identify a prior durable receipt.

The Agent provider normalizes omitted controls to `Timeline edit` plus a synthesized step. Its prepared recorder carries those authoritative steps. Runtime’s accept path classifies the resulting prepared record as modern and emits `merged` when the landing head differs from the requested base. Therefore the current `merged` observation is normative for these fresh requests. The preserved `rebased` assertions are an expectation/compatibility issue, not evidence of a product fault. Sol disposition: authorize a routine expectation correction only if the manager chooses to update these test expectations; do not change the request bodies, production classifier, or historical records in this task.

Exact retries are different: the same key/body after durable acceptance or restart must replay the stored envelope without provider execution or a new history row. The selected test’s later `authority-retry` call is such a replay, but the first call is not.

The genuine archive record `selected-param-legacy/accepted.zip` has key `legacy-params` and status `accepted` with `rebased_onto: null`; it is an old base receipt, not a historical `rebased` receipt. No selected-cohort record justifies changing a fresh request’s class.

## Cumulative source checks

- HTTP setup preserves the authored parent shape with `config: {tracks: []}`, `registry: {}`, `clips: []`, and `occurrences: []`; `config.clips` is absent.
- The HTTP path keeps the original pin in the pending outbox, checks history before submission, changes the current admission, removes source/artifact inputs, simulates a lost ACK, restarts, replays with the same key/body, checks refusal of seed 16 against the retained source, and undoes the accepted publication.
- The seven UNKNOWN function bodies are byte/source-hash identical to pristine base, with original assertion counts preserved.
- No production, provider, core, collection, profile, collector, Store, child, acquisition, browser, render, ZIP, fixture, test, pin, generated, kit, schema, Git, or permission changes were made in this worktree.

The HTTP body remains unverified because the central targeted route previously deselected it. No retry is authorized.
