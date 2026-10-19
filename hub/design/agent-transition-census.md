# Agent transition census

Date: 2026-10-19 UTC  
Scope: Agent `tl/integration` (`fec45b08a1a97fc4e98a7aaa29374394bfae1cc0`), frozen Agent R4 candidate `origin/codex/handover-timeline-r4-20261019-candidate-sdk` (`11caf1d9de291d76f491cf69f7942606b7471d7a`), the Runtime film fixture source, and bounded ORCH pytest temp paths.

## Result

**Scoped count of canonical data with both proven Agent authorship and proven outgoing meaning: 0.** This is a scoped zero, not a claim about every historical realm.

The inspected corpus does contain Agent code that relies on outgoing semantics, but I found no persisted canonical parent/internal-timeline publication that can be attributed to that Agent outgoing authoring path. The canonical records with transition fields are either explicitly incoming (the synthetic film fixture), retained App input, or compiled/native/viewing fixtures without producer attribution.

## Datasets and counts

| Dataset | Exact result | Attribution / meaning decision |
| --- | ---: | --- |
| Runtime synthetic film fixture, `/home/user/work/runtime/tests/timeline_commit_film_fixture.py` | 1 canonical internal transition declaration | Incoming by fixture contract: `film-internal-2` / `clip-2`, `{type: crossfade, duration: 0.2}`. It is built and published by `RuntimeService`, not Agent. Parent head is `film-parent-v1`; linked shot revision is `film-shot-revision-2`. Excluded from outgoing count. |
| Frozen R4 `tests/fixtures/timeline_editing/w29_transition_history.json` | 21 literal `transition` keys; 4 transition-bearing canonical snapshot occurrences; 2 unique transition-bearing parent payload states | The transition is on `parent/clip:after`; the forward request names `from_clip=parent/clip:before`. However `tests/sdk/test_timeline_transition_history_receipts.py:1` explicitly identifies this as “Retained W29 App requests through SDK; synthetic declaration/acceptance only.” It is not evidence of Agent authorship or outgoing intent, so excluded. The fixture's source SHA is `f2a4f0f100dd9681b89f90bc1c3e0044797974612657451ee5fbb5ee59c04e7d`; accepted IDs are `parent-r2` and `parent-r3` in the retained results. |
| Agent current JSON data fixtures | 12 transition-key occurrences across the bounded scan | 1 in `examples/hype.timeline.full.json`, 1 in `astrid/core/rendering/fixtures/renderer_parity/transition-windows.timeline.json`, 8 in `tests/fixtures/timeline_visualize/compositor_parity/F7_transition_bounds.json`, 1 in `F10_transition-last-clip-ignored.json`, and 1 invalid vector in `tests/fixtures/visual-boundary-v1.json`. These are compiled/native or visualization test fixtures, not Agent-authored canonical realm publications; the invalid vector is not data. Excluded. |
| Frozen R4 direct Agent authoring behavior | 1 synthetic SDK authoring family | `tests/sdk/test_transition_admission.py:35-60` creates `transition-a` before `transition-b` and calls `tl.clip('transition-a').look.set(...)`; the same test accepts touching/gaps and refuses overlap with the next clip. `tests/transition-admission.md:13-18` calls changed builtin look transitions “outgoing declarations.” This is real evidence of historical Agent outgoing reliance in the authoring behavior, but it produces no persisted canonical realm record in the inspected corpus. |

The W29 `transition` count intentionally is not reported as 21 outgoing records: most occurrences are request arguments, guards, inverse consequences, or duplicate retained snapshots. Counting literal keys would overstate data, and the test's explicit App provenance prevents attributing it to Agent.

## Synthetic film source and revision IDs

The film fixture's source constructs three internal revisions at lines 89–119 and adds the transition only for `index == 2` (line 106). It publishes the resulting parent with `parent_revision_id: "film-parent-v1"` (lines 165–170, 251–265). The direct fixture assertion reads `internal_timeline_revisions` row `film-internal-2` and checks `clips[0].transition.type == "crossfade"` (Runtime test lines 49–53); the corresponding shot revision is `film-shot-revision-2` (lines 83–84, 126–130). No Agent request, Agent author field, or outgoing declaration is present.

The fixture is intentionally a real API-built source realm copied to a duplicate after service close (lines 203–269). At census time no matching `film-source-realm` or `film-duplicate-realm` remained under the bounded `/tmp/pytest-of-root` ORCH test area, and the Agent repository contained no SQLite/DB realm fixture. Therefore I did not open a database. No credentials or credential files were read.

## Method and attribution limits

I read the settled PLAN, the latest Agent inbox, and the ORCH copy of `design/viewing-incoming-policy.md`. I then:

1. Enumerated transition-bearing JSON under bounded Agent `tests/`, `astrid/`, `examples/`, and `evals/` paths and recursively counted `transition` keys.
2. Read the frozen W29 fixture and recursively distinguished canonical snapshot payloads from request/guard/receipt duplication.
3. Read the Runtime film fixture source and its direct readback assertions, without executing its builder or mutating any realm.
4. Read the frozen Agent authoring test and transition-admission note to separate outgoing behavior evidence from data provenance.
5. Checked only the named ORCH pytest temp area for surviving film realms and checked the Agent repository for database fixtures.

A transition field, a `direct` authorship entry in a retained receipt, a caller label, a clip shape, occurrence membership, or a republished App request does not establish Agent outgoing intent. The policy document also states that canonical pins identify immutable bytes, not transition convention, and that no existing selector is safe. Those limits are why the result is zero rather than a heuristic classification of W29 or the compiled fixtures.

## Smallest guarded migration if a real outgoing publication is later found

No migration is proposed for the scoped corpus because the proven-outgoing canonical count is zero. If a separately verified realm supplies one, the smallest safe recorded operation is a one-purpose ownership migration that:

- targets the exact parent/shot/internal revision IDs and clip IDs, with the source revision/content digest and transition payload digest/value as guards;
- records `from_ownership=outgoing`, `to_ownership=incoming`, the predecessor and successor IDs, and requires same-track adjacency plus destination-transition absence;
- writes a new canonical revision moving the unchanged transition bytes from the old outgoing owner to the incoming clip, while retaining the old immutable revision/CAS bytes unchanged;
- refuses stale, ambiguous, unsupported, or already-diverged shapes; it does not infer ownership from spelling, timing, occurrence, caller, or registry identity.

The migration receipt/event should identify the source revision and exact field move so later rendering can select the incoming policy from a recorded fact. This is a recommendation only; no implementation or data rewrite was performed.

## Verification

No tests, installs, full suites, renderer/browser runs, or live services were run. This task was read-only; no product files, repository refs, realms, immutable bytes, or credentials were modified.
