# D140 final source review

Verdict: `FAIL_SOURCE`.

Six of the seven prior findings are closed at source level, with private
subprocess controls for phase ordering, import-stop sequencing, durable argv
and output retention, and positive/poison call accounting. The remaining
blocking seam is receipt authenticity.

## Remaining finding

### D140-RECEIPT-005 — forged producer-free receipts are accepted

`ops-d140-farm/receive-farm.sh:238-293` parses a source receipt as arbitrary
JSON, permits any status in a broad allowlist, requires only a `timeline.*`
schema prefix, searches recursively for a matching commit/tree/repository
string, and then verifies the local checkout independently. It does not require
the known normal receipt schema, producer identity, receipt digest, source
path closure, or an authenticated receipt envelope. The same pattern is
loosened further for the child and kit parsers at lines 296-417.

Independent private control: a temporary executable `git` reported the pinned
Agent commit/tree and origin for a temporary physical checkout; a synthetic
receipt containing only `schema=timeline.synthetic-forged/v1`, `status=passed`,
`producer=untrusted`, tuple strings, and `repo` then passed
`receipt.FARM_CURRENT_AGENT_RECEIPT`. The receiver still returned its expected
overall `NOT_READY` exit because other bindings were absent, but the receipt
check itself was `PASS`. This directly violates the requirement that opaque or
forged JSON references be refused and that the real queue/checkouts/kit/
provision/D73 receipt formats be used.

Required closure: bind each receipt to its actual known normal format and
producer/digest/source-tree closure, with no generic recursive key search and
no synthetic fallback. Keep the current checkout/tree check as supporting
evidence, not as a substitute for receipt authentication.

## Closed source findings and limits

- ORDER is separated by `D140_PHASE`; the real receiver subprocess does not
  invoke the normal request route and pre-child has no child/post-output IDs.
- DURABILITY now has an executable command block. A private route run produced
  the exact JUnit, raw, start/stop, disk, manifest and runmanifest files and
  verified the 36-argument call including `--junitxml=...`. This is mechanics
  only: no Farm route or real service result was run.
- C0 names were checked against Runtime f103’s actual schema. The handoff uses
  `reads`, `canonical_document`, explicit base/previous/accepted IDs,
  `rebased_onto`, nested `records`/`receipt`, `current`/`conflicts`, and the
  separate history shape.
- GATE’s failing checker subprocess returned nonzero and did not touch the
  private dry/core markers.
- POISON’s actual private control block called the positive route once with
  exit 17 and called the poison route zero times with a nonzero exit.
- SCHEMA path swapping is refused by a real receiver subprocess; source lines
  bind RECORD/direct_url directly beneath the physical pinned dist-info and
  compare the fixed 18-row/12-hashed/six-unhashed and direct-url/manifest
  closures.

The current Farm venue remains `UNKNOWN` until a Farm census supplies the
installed schema and genuine current receipts. Agent `547e...` and Runtime
`0ca...` were not treated as the requested `41ad/f103` tuple.
