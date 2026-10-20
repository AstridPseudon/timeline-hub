# Native word-anchor review

Reviewed `caea687ee05632738bac7fb9683b5bb1933b83c0` against the approved
`m2-word-binding-contract.md`, the authored-identity decision, and the kernel now
integrated at `43d567f9`. **Changes required before native acceptance is qualified:**
two source-boundary checks are missing, and the outgoing schema still needs the
complete frozen S2 union. The authored-identity decision remains sound.

The review changes no product code, schema, pin, tests, integration tree or process
document. Diagnostics and the detailed command/result report live outside this
repository in the assigned worker's `notes/` directory.

## Findings

1. **Occurrence visibility is not checked for the selected word.** Through normal
   Runtime acceptance, an occurrence starting at 2 seconds with `duration_ms=100`
   accepts a word-anchor start of `3.4701333333333335` seconds. The source clip's
   own from/to interval still contains the word, but the occurrence ends at 2.1
   seconds. `_timing_evaluators.evaluate` records occurrence ends for film-end
   evaluation; its bound-word checks compare only with the source clip interval.
   `native_word_anchor.binding` also omits this visibility check. Validate the
   selected phrase against the supported occurrence's visible half-open interval
   on first selection, replay, source changes, inverse and restore. A word ending
   exactly at the boundary may remain valid; an onset there cannot be selected.
   Neighboring `native_placement_commands.placement_move` already enforces an
   occurrence extent for its own operation.
2. **A raw source clip's `source_window` is silently ignored.** A historical film
   seeded through the public publication API with
   `voice.source_window={"from":20,"to":30}` accepts the same word at
   `3.4701333333333335`. The adapter checks `source_window` on the internal timeline
   and registry asset, while the kernel's `_maps` omits that key on the raw clip.
   This is outside the advertised literal-source codec. Refuse the unsupported
   raw clip map instead of treating it as ordinary from/to timing. No claim about
   renderer interpretation of this unsupported field is needed for this finding.
3. **This schema is not an outgoing freeze.** Full containment of frozen S2
   `26ef2bbb31b4892fdd7c15ee5b20700bd40cb933`, raw SHA256
   `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`, fails at
   seven paths: the missing optional `ClipSetElementArgs.schema_source`, missing
   `producer.guard`, and missing `ProducerAdmittedTarget`, `ProducerAttemptPin`,
   `ProducerGuardArgs`, `ProducerIdentity`, `SettledProducerProposal`. The worker's
   comparison with its narrower parent is insufficient for release containment.

The two acceptance reproducers use real CAS, main-v1 transcript creation, normal
Agent provider registration, and the actual regenerated Runtime. Initial fixture
data is published through historical public APIs. There is no PreparedProvider,
SQL history seed, raw schema override, test-local operation or fabricated receipt
in those reproducers. Normal `occurrence.delete` correctly refuses source removal
with an unchanged head after the baseline anchor is accepted.

## What is proven

The stored `app.astrid.word_anchors.{on,until}` contains the raw occurrence/clip,
exact existing DocumentPin, ordered stable main-v1 word IDs, edge and offsets.
The echo remains human text. Same-echo A/B selections produce different authored
revisions and content digests; revision-only restore recovers each choice across
restart. Fresh-process compilation receives only canonical JSON and verified
transcript JSON. No accepted-history fold supplies meaning.

The adapter constructs a private declaration from the selected IDs. The kernel
checks those exact IDs, exact scoped pin/digest, transcript/media identity,
consecutive same-segment phrase, clip source window and derived clip interval.
Its bound-word resolver never calls text selection; a tripwire tests this with
stale, invalid and absent echoes. Missing inputs refuse without latest-version,
ordinal, alternate-clip or text fallback. Repeated legacy text, even with an
ordinal, refuses `ambiguous anchor; choose occurrence` at the pure adapter boundary;
the unique-text positive still compiles without authoring a reference.

The recorded recipe guards target identity and writes, source raw clip/occurrence/
shot ownership, active source/track selection and registry asset identity. It
retains an exact transcript dependency and a follow binding. Source position,
order and supported windows are recomputed rather than frozen read guards, so a
disjoint native source move rebases while retaining the chosen raw clip and IDs.
The clock uses exact rational canvas FPS; six-decimal second offsets and frame
offsets retain their tested precision. Clear removes both echo and reference,
including a legacy flat echo that would otherwise reappear, and preserves the
other field and opaque siblings.

Native inverse restores A after B, including unchanged echo writes, and inverse
of inverse restores B. First-anchor inverse restores the complete prior clip and
exact absence. The last-reference literal cache is restored from authenticated
ordinary inverse provenance; live references always recompile. That cache recovery
does not make the film depend on accepted-history interpretation. Competing
target writes and later equal writes prevent unsafe inverse.

First use hydrates through `transcript_source` and retains V1 in the normal
dependency manifest. After a normal V2 update removes the chosen words, restart,
exact retry and an unrelated later native commit keep using V1. Missing version,
wrong digest, foreign document and authorization revocation refuse atomically.
V2 word removal is not document deletion: no public document-deletion route was
tested. The original raw source removal/media-change and source-trim probes use
test-local operations; this review separately verified native occurrence removal.

The default hook is bounded to parent clips carrying the new reference namespace
and their exact source dependency slice. A tested unrelated legacy clip retaining
`until_film_end` and `sequence` survives unchanged. Films with no new references
retain their existing default path. This is not broad compiler migration or proof
that Checkout retime/resolve, CLI, sheet, App picker, preview/export or other
consumers honor the new references. Those remain explicit qualification work.

## Required composition and evidence

Start from **complete frozen S2**, preserving every definition and operation.
Add exactly `WordAnchor`, `ClipAnchorArgs`, and the `clip.anchor` conditional from
this worker. The in-memory result has **50 definitions / 23 operation conditions**;
full containment of both S2 and the word candidate returns `[]`. Preserve S2's
producer registry/verified-producer plumbing and element first-use hydration while
adding this worker's declaration, guard, final compile hook and transcript-pin
hydration. Port the native module and its conformance fixtures/tests additively;
do not replace current shared command/provider files with the partial worker files.
Normally regenerate that complete successor before any coordinated consumer pin.

For the kernel, `_timing_evaluators.py` is byte-identical to `43d567f9`.
`compiler.py` differs only in its module docstring; executable ASTs are equal.
Use the integrated kernel files and its current documentation/tests rather than
reverting them to the worker's testing port. No executable kernel backport is
needed for this candidate. The source-window findings above still need narrow fixes.

Independent targeted results on Linux:

| Check | Result |
| --- | --- |
| Native main-suite Runtime file | 50 passed, 104.59 s |
| Portable file plus six command/provider neighbor files | 453 passed, 37.48 s (12 portable + 441 neighbors) |
| Current kernel's compiler/cycle files, copied unchanged from `43d567f9` to a private test folder | 51 passed, 19.31 s |
| Full S2/word containment diagnostic | Seven candidate failures; both union comparisons pass |
| Ordinary Runtime generator and `--check` | Exit 0 |
| Ruff on the reviewed product/test files | Passed |

Runtime evidence uses an **unpublished private normal-generation candidate**, not
the current public pair: base `c0dcd3871d78c405184506eb6735565592498c77`, base tree
`5f86f0ef9ad6c4c5bec21f41a8a1781c6a687c6d`, with this worker's schema SHA256
`a058aa6ec55d86f84b74360f4e9c01d207ec1db86434170c5d5658b5c809130a` copied as the
canonical generator input. Generated source fingerprint:
`a3aa854ce26583e9197f572ef75fed8b41d092d4f1b31c8cd3c6e7d7ec9c8883` (SHA256 over
sorted relative paths and bytes, with 4-byte path and 8-byte content lengths).
The historical seed Runtime is `80973d34ae10e498d7213c30287012c9876f4b1a`.
Normal generation's older published floor passing does not establish S2 containment.
No full suite, localhost/browser/socket lane or public release pair was tested.
