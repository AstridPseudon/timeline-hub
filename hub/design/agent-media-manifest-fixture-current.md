# Agent media-manifest fixture migration

Assigned source: Agent `537c2ecd28f92b391c79e383e0e045fd71b3258f` (tree `d291cf421e837b33e88132c3ac0760ad6812eda3`), the reviewed whole S3 candidate. Only the two parameterized positives in `tests/editing_conformance/test_commit_runtime_media_manifest_inverse.py` are migrated. Product code, schemas, public generated artifacts and pins remain unchanged.

The test still qualifies **manifest-subset acceptance through a test-only recipe/provider ABI adapter**. It does not qualify a production popup command, requester lifecycle, or new timing behavior. Numeric 24 fps and the original legacy fixture window treatment are retained. Native add/swap acceptance is separate coverage.

## Setup and authority

1. Reuse `test_commit_runtime_parent_media_swap.editing` as the existing native parent-media fixture. Its subprocess invokes the existing occurrence-media fixture against historical Runtime `b2a1d9fd82121a5509769531a2e91aece97d78b9`: normal project/task admission, settlement, real decodable red/blue PNGs, shot/text-binding APIs and legacy publication. The historical interpreter closes before the current Runtime opens the realm. No SQL, fabricated legacy publication/event/receipt, prepared provider, or compatibility publisher is introduced.
2. Current Runtime imports the genuine legacy chain via normal history reads. Normal immutable parent GET and text-binding GET supply the saved source and its retained text descriptor. The fixture checks actual CAS bytes equal `A chapter` and match descriptor size/digest.
3. The approved `tests/helpers/trusted_seed.py::seed_trusted_parent` installs the explicitly labeled **trusted TEST SETUP** baseline. A fresh immutable shot revision carries exactly `kind`, `slot`, `media_id`, `content_hash`, `byte_size`, `mime_type` from the real binding; there is no inline text authority. All existing opaque/source fields survive. The original legacy revision stays unchanged. As in the original fixture, this is a text binding of kind `transcript`, not an added media.transcript Document/word-anchor proof; the documents manifest is empty.
4. Reopen the service before registering the custom recipe provider, respecting startup-only provider registration.

The approved trusted-seed adapter needed one metadata correction: its placeholder command now says `created: []`, matching its already-empty recorded creation list. Without this, the current identity-history scan refuses the later add operation with `semantic identity history is unavailable` / underlying `created identity history is unavailable`. This changes future test setup records only; no accepted record is edited and no creation/reservation is invented.

## Preserved proof

All **15 original assertion expressions** remain, checked by AST comparison to the assigned HEAD. No skip, xfail, refusal substitution, or assertion weakening was added. Additional assertions check the independently saved complete baseline, old managed-media membership, exact new-media manifest delta, retained binding/CAS facts and immutable original legacy GET.

Both add and swap must still introduce the exact new managed object; dry undo and accepted undo equal the entire baseline CanonicalDocument; undo admission reads the accepted target closure while its result omits new media; restart and exact retries return the original ledger results with semantic execution trapped; changed source under the same key returns 409; the managed selection stays retained; redo equals the entire created document; stored receipt/dependency and immutable GET manifest match exactly; store integrity is OK.

## Runtime provenance and limits

Private Runtime source is immutable `2c4ac180c2220bdad966bc01e95ad230e99ce26a`. Its ordinary schema input is replaced with the **complete** Agent S3 schema, raw SHA256 `8a55a9fd84d6fc188e48f63976dacc1c27ea25c7747ea88e7eba7589974dd85a` (54 definitions / 28 operations). Normal generator, generator check, artifact-manifest generator and manifest check all pass. The private file comparison contains only that ordinary input, normal generated outputs and manifest. Nothing is hand-generated and no validator/schema monkeypatch grants acceptance.

The custom command is accepted by the actual current validator/provider/port path. No new production operation or endpoint is required. Public 0.2.13 bytes, shared dependencies, shared caches and integration worktrees receive no writes. No full/full*, localhost, browser, App, released-pair, renderer, owner-film or macOS qualification is claimed.

Exact commands, final results, diagnostic iterations and reproduction script: [worker report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-tests-media-manifest-fixture-current/notes/report.md).
