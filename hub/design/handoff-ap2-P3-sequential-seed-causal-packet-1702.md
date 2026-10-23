# Runtime handoff: P3 sequential-binding refusal

Status: **FAIL with source-backed causal seam; Runtime owns the next bounded classification.**

Service `ap2-P1-P2-P3-current-OPS-sol-1653-ap2-P3-gate5-h6-0348-1023170008-20942` failed exit `2` after `85s` on App `4c4c9c77c96fab70c4efef09db9a3bc456b0d803` / tree `2652d85a0ab40bcf0e88443f721dc4b868eeb743`, Agent `bac094180aef38a77b86ab165962e6159f873c60`, Runtime `d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b`.

Observed refusal:

```text
validation_error / invalid_records / status refused
submitted assertion has no unique authenticated sequential binding
```

The public caller is unchanged App `commitNativeSeed` (`tests/e2e/local/support/harness.ts:670-824`), invoked by `seedThreeProducts` (`:1032-1073`). It opens the public SDK, emits native commands and guarded patches, and submits the unchanged v2 request with top-level and per-step `reads`, `steps`, command ordinals, patches, `merge: 'atomic'`, and `source: {'via': 'python'}`. It fails at the commit call before an accepted packet exists.

The exact Runtime consumer is `runtime_protocol/timeline_commit_auth.py:307-319`. `_sequential_assertion` compares a submitted claim against authenticated `binding_pairs`, constrained by command ordinal and claim kind, and requires exactly one match. Call sites are:

- `:2261-2267`: top-level request reads, `dependency`, ordinal `[0]`;
- `:327-328`: step reads, `dependency`, first step ordinal;
- `:367-369`: step patch assertions, `change`, step command ordinals.

Agent’s private producer path is `_commit_preview.py:25-80` and `_commit_patch.py:282-323`, `:455-462`, `:576-607`; Runtime’s private capture port is `timeline_commit_port.py:177`, validated through `validate_sequential_capture` at `:669-670`. This establishes the producer/consumer interface, but the failed seed tempdir was cleaned.

## Required next owner action

Runtime should perform a bounded offline classification using one retained/redacted capture packet if an approved diagnostic makes one available. Determine which claim kind and command ordinal reaches `_sequential_assertion`, then whether the match cardinality is zero or greater than one. Keep the public request and all auth/tamper/no-write/fixture guards unchanged. Do not infer the failing ordinal from this packet.

If the retained packet shows malformed Agent capture provenance, route that single exact producer defect to Agent. Until then, do not assign an Agent or App authoring defect.

Portable check shape:

```python
matches = authenticated_match(claim, ordinals, key, binding_pairs)
assert len(matches) == 1
```

Use only non-secret fields: claim kind, submitted ref/path, ordinal set, pair cardinality, and authenticated source/landing ref identity. Never export credentials, raw principals, bearer values, or signed tokens.

Evidence: summary SHA-256 `1177d7f38839bdca87ad755c3acf1a8ded131f19dfc99a59a6d7747aeff58f91`; service log SHA-256 `a89b6146689ae3fc899ce43ccc935152012d7f5b0e48891e4eaaeb8220156feb`; trivialboot SHA-256 `59d3bcaf53bed4d74277d1dad7ac261579575acca2a9229cf0c380ef6b986043`. No product files were modified and no rerun was performed.
