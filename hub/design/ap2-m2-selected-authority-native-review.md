# ap2-m2 selected-authority native review

## Verdict

**REQUEST CHANGES for the pure App resolver.** The exact accepted-history fixture parity is good, but the helper does not yet match native authority scoping and ordering. Keep the source private; do not wire it into the mounted panel or claim the row qualified.

Native source approval and App integration approval are separate:

- **Native direct-triple compatibility: PASS for the exercised fixture.** The resolver returned exactly the same P as Agent WC4 for both opposite-selection histories.
- **App source: HOLD.** Reversed history ordering and a parent structural reorientation are accepted by the helper although native authority must refuse them.
- **Mounted UI/shared seam: HOLD.** `PropertiesPanel` still passes none of `retainedDocumentPin`, `timelineOps`, or `commandState` to its `ClipPanel` invocation. The supplied shared proposal is not an applicable patch.

## Reviewed inputs

- App source: `055d69c2a1f63602470e04d40e86fb4e4c251826`, exactly the helper branch over `89bb044627a30cfd1f055804f6393014a834b25b`.
- Agent native source: frozen WC4 `30fc8dd154015a7c58cf4ce7b065ccc46f470ee`. It was extracted with `git archive` into a private worker directory and was not modified. The supplied R4 `docs/projects/timeline-r4/PLAN2.md`, `PLAN3.md`, and `PLAN6.md` paths do not exist in the supplied archive; the current `/tmp/.../scratchpad/orch/PLAN.md`, row handoff, and explicit brief were used as the settled guidance.
- Rule and handoff: `app2-selected-original-pin-review.md`, `selected-param-original-pin-rule.md`, `handoff-app-to-app2-selected-param.md`, and `agent-review-selected-param-authority.md`.

## Findings

### F1 — history array order is not checked

`orderedEntries` indexes entries by publication and walks predecessor links, then returns `result.reverse()` (`selectedParamAuthority.ts:75-105`). It never checks that the supplied `HistoryPage.items` arrived in the authenticated predecessor order. Reversing the exact accepted WC4 history still returns P; the native `_history` carrier checks each page item against the expected previous pair and refuses an out-of-order page.

Reproduction against the exact native-parity fixture:

```text
node --import tsx --input-type=module -e '...HistoryPage.items.reverse()...'
=> {"reversedOrder":"accepted", "pin": P}
```

This violates the handoff requirement that incomplete/order-corrupt history refuse visibly. Preserve predecessor validation, but also require the existing carrier's item order to be the verified chain order (or reject the page before the resolver sees it). Do not sort client-side to repair an authenticated history error.

### F2 — structural reorientation is outside `touchesRow`

`touchesRow` (`selectedParamAuthority.ts:193-200`) only recognizes the exact clip reference and its `params`/`elementRef` paths. It misses the native resolver's scoped structural effects: `timeline`, owner clip/shot/source changes, parent `config.clips`, and the concrete `shot:<id>` materialization. Therefore a synthetic accepted record writing `{ref: "parent", path: ["config", "clips"]}` after a valid selection leaves P available in TS. Agent's `relevant()` marks this parent reorientation relevant, clears authority, and the next PARAM refuses. The same gap exists for occurrence source/shot reorientation unless the existing graph/materialization carrier is consulted.

Do not add a wire DTO, authority store, or new framework. Reuse the existing canonical command basis/graph and captured raw target; if the existing carrier cannot establish the concrete occurrence shot identity, fail closed rather than accepting a stale P.

### F3 — supplied shared proposal is corrupt; valid replacement hunk is known

`handoff-ap2-m2-selected-authority-helper-shared.patch` fails:

```text
git apply --check .../handoff-ap2-m2-selected-authority-helper-shared.patch
=> error: corrupt patch at line 34
```

The failure is the literal `@@` without a range, plus prose appended to what is presented as a patch. The accessor agreement below it is useful design text, but is not an applicable patch and does not qualify pagination or mounted wiring.

The pagination portion can be represented by this exact applicable hunk against the current App tree; it passed `git apply --check` in this review:

```diff
@@ -786,7 +786,23 @@
 
   /** Public verified history pins plus scoped immutable reads, never projected rows. */
   async loadTimelineCommandBasis(timelineId: string): Promise<TimelineCommandBasis> {
-    const history = await this.listTimelineCommits(timelineId);
+    const firstHistory = await this.listTimelineCommits(timelineId);
+    const pages = [firstHistory];
+    const seenCursors = new Set<string>();
+    while (pages.at(-1)!.next_cursor !== null) {
+      const cursor = pages.at(-1)!.next_cursor!;
+      if (seenCursors.has(cursor)) {
+        throw new TimelineSchemaIncompatibleError('Workspace Runtime returned a cyclic timeline history cursor');
+      }
+      seenCursors.add(cursor);
+      const next = await this.listTimelineCommits(timelineId, cursor);
+      if (next.head.revision_id !== firstHistory.head.revision_id
+        || next.head.publication_id !== firstHistory.head.publication_id) {
+        throw new TimelineSchemaIncompatibleError('Workspace Runtime changed the captured timeline history head');
+      }
+      pages.push(next);
+    }
+    const history: HistoryPage = { ...firstHistory, items: pages.flatMap((page) => page.items), next_cursor: null };
     const head = history.head;
```

This is only the shared pagination seam. It does not approve the resolver or mounted UI.

## Exact evidence

App focused resolver/control tests, using private Vitest temp state:

```text
TMPDIR=/tmp/ap2-m2-selected-authority-native-review-vitest \
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/selectedParamAuthority.test.ts \
  src/integrations/runtime/retainedParamInputs.test.ts \
  src/tools/video-editor/components/PropertiesPanel/AstridElementParams.selected.test.tsx \
  src/tools/video-editor/components/PropertiesPanel/AstridElementParams.lifecycle.test.tsx \
  src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted-batched.test.tsx
=> 5 files, 105 passed
```

Native selected-authority suite:

```text
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=<private agent-30fc archive> \
/home/user/work/venv-app2-native/bin/python -m pytest -q -c /dev/null -p no:cacheprovider \
  <private agent-30fc archive>/tests/sdk/test_timeline_selected_param_authority.py
=> 27 passed in 10.13s
```

Exact same accepted-history fixture and raw stable target/head parity:

```text
native fixture generation from the existing Agent test:
  test_equal_json_opposite_pin_order_has_distinct_accepted_authority
  => 1 passed
native resolver replay on the generated fixture
  => 2 cases, native returned two exact P pins
TS resolver over the emitted accepted HistoryPage and raw clips
  => {"cases":2,"exactParity":true}
```

The same parity fixture probes exposed both source holds:

```text
reversed-history-order              => accepted (must refuse)
parent-config-clips-reorientation  => accepted (must refuse)
```

Static checks:

```text
eslint selectedParamAuthority.ts selectedParamAuthority.test.ts => pass
git diff --check => pass
tsc --noEmit -p tsconfig.app.json => baseline failure; no new resolver error.
```

The full typecheck reports existing Composition export/type errors and existing `Object.hasOwn` target errors in `SelectedElementParamFields.tsx`; it was not treated as green evidence. No full, browser, localhost, socket, Runtime HTTP, or end-to-end suite was run.

## Next steps

1. Repair F1 and F2 using existing authenticated history/basis carriers; add focused refusal coverage without weakening any existing positive behavior.
2. Replace the corrupt shared proposal with the applicable pagination hunk and a separately reviewed, real consumer seam.
3. Wire the existing `PropertiesPanel` props only after the accessor can retain the exact P across capture/retry/restart and preserve draft-visible refusal.
4. Obtain mounted App/browser evidence for V1B through HA/V2/removal/restart, pending/raw16 refusal, and zero legacy traffic. This review supplies none of that integration evidence.

