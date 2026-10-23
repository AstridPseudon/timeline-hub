# agt-G5-sdk-bootstrap-sol-1604 — G5 SDK fixture authority audit

**BLOCKED on a faithful historical test carrier; no repository changes.**
The permitted fallback is a precise Runtime test-fixture ownership request.
No product API, importer, schema, guard change, or revision-name override is requested.
No four-body integration request was submitted because no faithful setup was found.

## Correction to retained 1552 findings

Read PLAN §3 G5/R2, C0 §5, retained 1552 report/design and its actual preflight,
semantic failure, source hashes and original report in worker log lines 18444–19247,
24790–24890 and 24950–25065. The on-disk 1552 report is now a shorter final summary;
the original detailed report survives in that log.

1552's claim that the four bodies require the literal `m1-journey-baseline` ID
is incorrect. None references it. All four take their actual current basis from
the opened film; the restore body uses `original['base_parent']`, and the catalog
body retains `before_revision` and its actual digest. Only the imported shared
fixture (and unrelated `auto_film`) hardcodes that name. Any authentic retained
revision/publication pair with the exact original payload would suffice.

The actual obstacle is the **payload**, not its revision spelling:

- Default capture lacks the second `music-other` track/clip and the required app declarations.
- `music-documents` has a second clip, but its track is `music-2`, not `music-other`,
  and the original music-bed app declarations are absent. Treating it as equivalent loses behavior.
- `anchor` retains `on: word:word-1`, but uses `at: 0.25`, lacks the second track/clip,
  and lacks the original explicit null `until`, `until_film_end: true`, and nested opaque array.
- `raw` additionally changes output/null/opaque data and physical child pins.

All 28 retained parent images across the 12 existing Runtime 9ce archives were
read from temporary byte copies with SQLite `mode=ro`; none matches the required
parent payload. This bounds the search to the existing 9ce fixture catalog;
unlisted operator backups elsewhere were not searched.

## Why the current semantic path cannot supply this setup faithfully

`_commit_timing_validation.py:245–265` retains an unresolved legacy declaration
only when its original declaration and complete `_reference_basis` are unchanged.
That basis includes sibling clips and reference/timing inputs. The exact original
candidate has **zero legacy exemptions** against each of the four authenticated
carriers; the anchor carrier's added sibling and timing/app differences change
its reference basis. Removing/readding the declaration would create a new invalid
anchor, and altering sources would change the required fixture authority.

`native_word_anchor.py:134–170` parses this legacy spelling as **text lookup**.
The real transcript's word ID `word-1` has text `Open`, and word ID `word-2` has
text `on the river`; `word:word-1` does not mean an exact word-ID binding.
No alternative transcript or typed binding was manufactured. The retained 1552
registered-provider attempt already fails with `candidate.timing: legacy word
anchor is missing`. I did not repeat it or submit an invalid candidate.

## Minimal request to Runtime test-fixture owner

Provide an **existing authenticated pre-cut capture/backup**, through the existing
test restore helper, retaining the original film state and provenance, or identify
an already captured matching carrier outside the inspected catalog. It must:

1. Preserve the original parent JSON exactly, including all labels, registry,
   clips, track IDs, legacy declarations, opaque fields, absence versus explicit
   null, and config mirrors. Required canonical parent payload digest:
   **`sha256:b6069d1ddccc0279e871b142773b63b73b107ebf9d0adc11ab73832b69097afb`**.
2. Preserve the original three shot and three internal immutable images, all
   physical sharing/occurrences, media/CAS bodies, reference and text-binding
   authority listed below. No rewriting/stripping/normalization of the legacy fields.
3. Retain a genuine publication event/idempotency receipt and predecessor ancestry,
   so `verify_baseline` and `install_verified_baseline` recover the exact **actual**
   head revision/publication pair. Its spelling need not be `m1-journey-baseline`.
4. Remain historical restoration data: no new invalid orphan-anchor publication,
   invented receipt/history/cache, row insertion, or prepared-provider acceptance.

Required detached JSON (expectation only, **never persisted as an accepted image**):
[/tmp/w-d0a799f7dd/audit2/required-parent-payload.json](/tmp/w-d0a799f7dd/audit2/required-parent-payload.json).
Original canonical source closure:
[/tmp/w-d0a799f7dd/audit2/canonical-original.json](/tmp/w-d0a799f7dd/audit2/canonical-original.json).
This JSON was obtained by copying the original verified parent and applying exactly
the four original fixture mutations; its children and media remain the original sources.

## Exact sources and authenticated preflight

- Agent HEAD: `e8a29acc0c896b2c3c0b78fd6c258b6f809ae721`; worktree remains byte-identical to HEAD.
- Runtime: `9ce4242bc01f100bab9efc51032a73985cefb2b2`, tree `92ab1f5f739ffdfedf7b25fbd2a7b46ae42c5d1a`,
  clean at `/home/user/work/wt/rt-pin-9ce4242b`.
  `/home/user/work/runtime` has advanced to `2593942dfbbbe1d70bb6e776f811285deb2ab18b`;
  it was not used as the executing Runtime.
- All 29 loaded Runtime module origins checked beneath exact 9ce:
  [runtime-origins.json](/tmp/w-d0a799f7dd/runtime-origins.json).
- Client/Runtime schema digest matches: `sha256:35c2d9c5e0b51ab8d8b7a4f4dbafbdfcb13d232d7bd22fff21cf73e250398d4c`.
  Declared producer lock stays `34eac0041b0891e9011966b39bcbd26053fde5bc`.
- The historical `CATALOG_RUNTIME=3b900c377e7126e14eeb92dc2ce73114cbda5a0e`
  is still source data. Its literal is not evidence of the running module origin;
  all executed preflight/boundary modules came from explicit 9ce.
- Existing read-only profile `/home/user/work/runtimes/agent-remotion-composition14-255b6856`:
  lock SHA256 `b7c4ab2e3c3f466d9d1c0c8d7472a40101d37b6288d52b930067dc663a17feb0`;
  archive SHA256 `21fde4d2a5d62a83f97a85d4b8d9f9d3f707a6489c07eb421c6331eccf893e6e`;
  Composition `0.0.14`, Node `v20.19.4`.
  No provisioning, links, installs, or shared-cache writes.

The four relevant committed archives were HMAC verified and restored with existing
`load_precut_realm_fixture`. On the duplicate only, existing
`install_verified_baseline` returned its verified pair, preserved the complete
canonical closure, and was idempotent with zero additional DB changes on its
second call. `verify_baseline` itself made zero writes. Backup/source copies and
all media bodies kept their original hashes. No RealmStore/SQL mutation was authored.

| Carrier | Actual verified revision | Actual publication | Archive SHA256 |
| --- | --- | --- | --- |
| anchor | `input-anchor-baseline` | `txn-09ed822514ac41f093f4a570556dfc97` | `19033fe2d2f33edbf6ff0b965f68aa88323859802d165f963563c6d8acc16d47` |
| music-documents | `film-move-baseline` | `txn-3362692b9f4b4d3394779d4b5c4de42e` | `f955ea28ae66b0161b7af8eb3a83a8e97e44749bd4c6569b36bedf6d40a094db` |
| original | `film-parent-v1` | `txn-55c0651b2cd64255ae06e73f9708220a` | `e304773208ff96cea0dca545c69cfa3fcb7ef605c01c306017ed8bcfc654a6b5` |
| raw | `raw-parent` | `txn-e324321a36644bf6983e0e2dda0f7f9b` | `e5eb4b5c740b055dcc0eb938ada6931ccb8f2dc432def915dc1f88cb8b93cdb5` |

Immutable child source payload digests:

- `film-shot-revision-1`: `sha256:b97de3b8da2c0f0d66302fe690e82049ba3ef1d635bbea53cf8de64a8b894a2d`.
- `film-shot-revision-2`: `sha256:a59a980cb7d9b78b605a946761fb801885340d05a1fc9ee7d2353106ec7e2c6a`.
- `film-shot-revision-3`: `sha256:d621270cdb1ac3de14d109f0586cd26853d036eb88f106ad2b0f1ac3c18e3fb7`.
- `film-internal-1`: `sha256:1264224ee99eabe4b5ff1b4cb970047c389930403db8bdb32ad4e26ae9b3287c`.
- `film-internal-2`: `sha256:848e75dfcb471007dfccf5b489ebe76e98b8efec11c5ecf9740a013946e6153a`.
- `film-internal-3`: `sha256:9fb7e21a3b19633f5b6cd9e3a17795a25025fdf1e8b512c2bec2df4135806192`.

Original managed media body digests (verified against actual CAS bytes):

- `sha256:beec97efbe7637ec4c5468a08f39fd3263dd3762483d66318d13093c22645beb` — 19 bytes.
- `sha256:bfa95bbc854e387c08f73177c2a48719d9a928c3f2c94eca0e693f3f970014e5` — 19 bytes.
- `sha256:e29d6131553bfda749080174ccc5fb5f1be8eb27f2775323cb0293fcb6933a65` — 19 bytes.
- `sha256:f39a4fd033486fb1e77eed03a6787fa83a5860d280e4b5ee47f7f8372eed95a2` — 19 bytes.
- `sha256:fef50eab9e9b23b75133cf7553faee605c3ff14d993599c8d2c551030f0bcb3d` — 17 bytes.

Repository source SHA256 (all unchanged from HEAD):

- `astrid/sdk/timeline/_commit_timing_validation.py`: `871a4b140be60863a8238ac60acf1ab12f56d7a71d4a59bc4f3f3792de46f58f` (Git blob `29d32035ea352ed444a6c9dd7b5baabbb1b3ba4e`).
- `astrid/sdk/timeline/native_word_anchor.py`: `771d833188de33556a1853e95e84703e7ce5b36e2a6b2d2c55cb975f93f36744` (Git blob `4c8dec68dcd42008158193df195d44b6838335b0`).
- `tests/editing_conformance/test_commit_runtime_m1.py`: `a95ee868774b20b093c015eef40b48a12f695ddaa9c06d6f1a8b8329b2092776` (Git blob `4ceee9aea278f206c6416b2d51e7d054212682c8`).
- `tests/sdk/test_timeline_checkout_history_boundaries.py`: `b7478f50b80fa73ce8546f7017c3fb0b52f4c722c8e2f74088e8fc8c4cc6446b` (Git blob `d2ee3d0e928896fb8b127b2f3dd556c3d5ebe078`).
- `tests/sdk/test_timeline_checkout_history_runtime.py`: `2575cb71554a104a48eba75bc5edb0998901e1014dca865a42088844a966db2a` (Git blob `73092f1a333e10be6d7966213ccc0a82a7ec7106`).
- Runtime `tests/precut_realm_fixture.py`: `c7fed3953a0de5147260a6e4fd1cb4a3d28b4fb87b04f8bacba928bf1397fff1`.
- Runtime `tests/timeline_commit_film_fixture.py`: `7fa6dd0212dae2a8c5157a297c30c3369ec3d68f123bab43ca3552978a123398`.

## Commands and results

Environment `E` below expands exactly to:

```sh
env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/w-d0a799f7dd \
PYTHONPATH=/home/user/work/wt/agt-G5-sdk-bootstrap-sol-1604:/home/user/work/wt/rt-pin-9ce4242b \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-9ce4242b \
ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-composition14-255b6856 \
ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-composition14-255b6856/node_modules \
ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages
```

1. `E /home/user/work/venv-agent/bin/python -P /tmp/w-d0a799f7dd/inspect_carriers.py > /tmp/w-d0a799f7dd/carrier-preflight-2.log 2>&1` — **PASS** (4 authenticated restores/baseline installs; no matching payload in 12 archives / 28 parent rows; four AST and full-function source hashes unchanged).
2. `env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-G5-sdk-bootstrap-sol-1604:/home/user/work/wt/rt-pin-9ce4242b /home/user/work/venv-agent/bin/python -P /tmp/w-d0a799f7dd/check_origins.py > /tmp/w-d0a799f7dd/origins.log 2>&1` — **PASS**, 29 actual Runtime origins and matching schema.
3. `E /home/user/work/venv-agent/bin/python -P -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/w-d0a799f7dd/boundaries tests/sdk/test_timeline_checkout_history_boundaries.py > /tmp/w-d0a799f7dd/boundaries.log 2>&1` — **9 passed in 1.40s**.
4. `/home/user/work/venv-agent/bin/ruff check --no-cache --output-format json --config 'include=["**/*.py"]' tests/sdk/test_timeline_checkout_history_runtime.py tests/editing_conformance/test_commit_runtime_m1.py > /tmp/w-d0a799f7dd/ruff-corrected.json` — exit **1**, **11 existing diagnostics / zero added** (I001 2, F401 2, E402 1, F811 6). Both sources exactly match HEAD; no lint suppression or edits.
5. `env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-G5-sdk-bootstrap-sol-1604:/home/user/work/wt/rt-pin-9ce4242b /home/user/work/venv-agent/bin/python -m mypy --cache-dir /tmp/w-d0a799f7dd/mypy-cache --follow-imports skip --ignore-missing-imports tests/sdk/test_timeline_checkout_history_runtime.py tests/editing_conformance/test_commit_runtime_m1.py > /tmp/w-d0a799f7dd/mypy.log 2>&1` — **PASS**, no issues in 2 source files, private cache.
6. `env PYTHONPYCACHEPREFIX=/tmp/w-d0a799f7dd/compile-cache /home/user/work/venv-agent/bin/python -m py_compile tests/sdk/test_timeline_checkout_history_runtime.py tests/editing_conformance/test_commit_runtime_m1.py` — **PASS**, private output.
7. `git diff --check` and `git status --short` — **PASS**, empty diff/status.
8. `bash -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-sdk-bootstrap-sol-1604/run-qualified-four.sh` — **PASS**. Runner written but **not executed or registered**. It fixes missing PYTHONPATH using the existing named qualified-suite pattern, pins exact 9ce, preloads/checks Runtime origins before collection, and selects exactly the original four nodes with `-o addopts= -m integration`. Manager may register it with the central service **after** faithful fixture setup exists. No extra review gate is proposed.

Initial diagnostic-only mistakes, corrected: first audit assumed `film.config`
existed in the default archive and stopped with `NotFoundError`; corrected to list
actual source documents and used fresh scratch roots. First Ruff command used
unsupported `--include` (exit 2); corrected to config override above. First extra
origin check used nonexistent `astrid_runtime_client._generated` (import error);
corrected to the actual `contract_metadata` module. None ran an integration body
or encountered a permission/classifier refusal.

## Four original body locks

AST body hash means SHA256 of `ast.dump(ast.Module(body=node.body,
type_ignores=[]), include_attributes=False)`. Full function source includes the
original declaration/body text. Both hashes match HEAD for each function.

| Original function | AST body SHA256 | Full-function source SHA256 |
| --- | --- | --- |
| `test_catalog_recover_uses_real_http_and_preserves_closure_before_revision_restore` | `96177bd02c8ead8461cc565c73b45bb403617ac1beec8d9a1f3bb0b01123fc97` | `dcbeca79c3ff4830a6535646edcd76f81646a05e024d17756769e11262140627` |
| `test_checkout_reload_undo_cli_redo_uses_retained_history` | `e1163f29661c3c824bdd63f22f6699ec59ef9d2d7cf6445bf6fb893d563832cf` | `1ea4f8c1a8342c049933e580f70282a9fef87fdc73f9f45366c854664b513056` |
| `test_open_bundle_keeps_http_rows_raw_and_round_trips_canonical_images` | `05b4cf4915ef9bb1220b1c9333f72bd9b2e456001fcb3bef72ca83503c98744c` | `0d9c76abdb1304c760cc667273f592c5ba7f987e84170aaa67b7ea2a6722a8d6` |
| `test_retained_restore_does_not_reopen_consumed_draft_steps` | `609dfdb23b5800ca07974af9214d859079894a6402d1bb7494826feab056b3f8` | `43a5cab36e8464974c86af04ed37e138ea7ec441c3d1180235587bba4b363b1f` |

## Evidence and limits

Complete report-all carrier packet, payload differences, actual source documents,
manifest/pins, archive inventory, source hashes, and origin/profile facts:
[carrier-evidence.json](/tmp/w-d0a799f7dd/audit2/carrier-evidence.json) (SHA256 `a6b2b59e0a0094afb3b9e7713f21ba84374fb7db3eb04cac532e7312eb47a212`).
Audit implementation: [inspect_carriers.py](/tmp/w-d0a799f7dd/inspect_carriers.py)
(SHA256 `91fd98d85e1d625d678eb08f23850fb1d68c6ae5f81874e516f3dabf9513e650`).
Ready central runner: [run-qualified-four.sh](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-sdk-bootstrap-sol-1604/run-qualified-four.sh)
(SHA256 `ce5304334f0999ab2c01836c38f744145a525ff0c08c7c2e7061dda345f87a8e`).

Only the existing baseline installer wrote its normal bookkeeping on disposable
restored duplicates. No accepted history was synthesized, and no new candidate
was submitted. No original behavior was weakened, removed, skipped or marked xfail.
All C0 request/reply/history/undo data paths and product files remain unchanged.
HTTP/restart/catalog/no-write behavior in the four original bodies is **unverified**
in this task. No full, G5 c271, R2 nested, P1–P4, native14, V4 or browser runs.
No Git writes, branches, refs, merges, pushes, or merge requests.

Next: Runtime fixture owner identifies the exact historical authority above;
then a fixture-only override can expose its actual verified base pair and the
manager can run the supplied four-node command once through the central service.
This is an authority handoff, not a request for a new product API or a decision change.
