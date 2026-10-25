# F-D86 later exact input receiving continuation (source/static only)

This is a durable private LATER packet for the existing MAIN affected-node route. It claims no test, service, behavior, core, or final-gate credit. It is based on Runtime `6634a17f3ffd885567ba3c91b6c7a560df7375a4` and excludes the current161 packet/body.

## Exact set accounting

- The received Agent69 continuation and current161 source packets were verified as a lossless disjoint union: `161 + 69 = 230` selectors across 18 family keys.
- The inherited packet is `SETUNION(Agent69, netzero1, D87six, CLI8, WC6eleven) MINUS current161`: 95 unique selectors across 7 family keys. This continuation is `SETUNION(inherited95, pool6, core-element-reply-literal)`: 102 unique selectors. It never uses count-summing or guessed membership.
- The 26 additions beyond the verified 230 are disjoint: netzero 1, D87 live frontends 6, CLI first bodies 8, and WC6 first bodies 11.
- The continuation adds exactly six `F-M2-pool6` rows after the reviewed `occ-a` setup dependency and one core-element reply-literal row after the reviewed normal seam. The resulting actual10077 remainder is 86 rows; the historical core-element lost-ACK row is not removed.
- The 19 CLI/WC6 rows are promoted from the exact actual23 TSV. No marker or assertion was edited. The existing route below has no `-m integration` marker filter.
- All 550 historical rows/dispositions are preserved. D87’s exact 24 retired mappings plus separate checkout mapping remain copied as source inputs; the six D87 live selectors are not retirement credit.
- D91’s exact ten shared-inverse selectors are recorded in `inputs/scheduled-elsewhere.tsv` with no actual result and are not included in this receiving set. The original `current161` captured tuple is copied under `inputs/current161-captured-cef8-*`; it is a boundary reference owned by task 0254 and is never rebound here.

`inputs/membership.tsv` and `inputs/selector-argv.txt` are the canonical packet inputs. `inputs/combined230-*-reference.tsv` retains the received 230-set authorities for audit. `inputs/source-map.tsv`, `inputs/held.tsv`, `inputs/remainder.tsv`, and `inputs/source-profile-PENDING.json` are the corresponding source/static maps.

## Included source scopes

- Agent69: current-sheet13, M1-baseline10, and word-bootstrap46, copied from the received continuation membership/map and rechecked against current Agent source hashes.
- Net-zero: the exact `[net-zero]` selector only; source `f32a890e3b`, normal Agent home `cef8a5be53`, protected review `agt-F-netzero-review-0215.md`. `replace-existing` remains separate and held.
- D87: the six exact live frontend selectors; source `7e0ac7b242`, normal home `8d93889e01`, protected review `rt-D87-live-review-0202.md`.
- CLI8/WC6eleven: exact rows from `handoff-rt-D86-10077-unexecuted-23.tsv`, with their received source/review/home correspondences. They remain first-body-pending and must use the existing targeted route without `-m integration`.
- Pool6: six exact `F-M2-pool` rows from the immutable actual10077 outcome set. The reviewed shared helper now creates and reloads `occ-a`; this is source eligibility only, not behavior credit.
- Core element: exactly `test_public_helper_optional_session_rebases_over_disjoint_edit`; protected review `rt-D86-core-element-review-0222.md` and normal Agent `a836baa3…` establish the reply-literal seam. The lost-ACK metadata original remains held.

Original P4, four R2, unchanged245/268/298, full-suite, and current161 body work are not in this packet. `replace-existing`, inverse7, D92, and other pending exact nodes remain held.

## Fresh receiving boundary

The receiving source profile records Agent `tl/integration` commit `a836baa3b11208d66bf8d23d6abfb1c8e59257e2` and tree `9643ec2c3ac752b0d9925ee7e7f287da9a806f86`; all 12 relevant source files match their captured SHA-256 values, all selected function names exist under AST inspection/in-memory compilation, and all reviewed source commits are ancestors of `a836`. The inherited `source-profile-PENDING.json` remains the prior 95-selector provenance; `inputs/receiving-source-profile.json` is the fresh receiving record.

Fresh four-repo custody, imports, path-sensitive hashes, normal profile, parsed preflight, owned-row CAS, and actual body receipts remain `PENDING`. Old receipts/profile data are provenance only and are not borrowed. Stop on any source/origin, classifier, safety, permission, or route refusal; do not retry a denied route.

## Existing MAIN recipe parameters

`route/main-affected-batch-recipe.sh` is copied from the existing D86/D88 route; no new runner framework was added. A receiving worker must supply fresh values and invoke it with the packet’s selector file, for example:

```bash
MAIN_BATCH_SELECTOR_FILE=<packet>/inputs/selector-argv.txt \
MAIN_BATCH_EXPECTED_SELECTOR_COUNT=102 \
P4_LAUNCHER=<fresh-agent>/tools/p4-d73-pinned-launch.sh \
P4_D73_MANIFEST=<fresh-four-repo-manifest> \
P4_D73_EVIDENCE=<fresh-main-evidence-directory> \
P4_D73_REQUEST_ID=<fresh-request-id> \
bash <packet>/route/main-affected-batch-recipe.sh
```

The recipe retains the original 45-second timeout, cache-off mode, `-n 3`, JUnit output, and existing launcher. No command above was executed here; only static JSON/TSV/set checks, SHA-256, AST/in-memory compilation, and `bash -n` were used. The manager must supply fresh four-repo custody, parsed preflight, owned-row CAS, and body receipts; none are implied by this packet.
