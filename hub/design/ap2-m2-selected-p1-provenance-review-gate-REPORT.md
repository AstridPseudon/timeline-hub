# AP2 M2 selected P1 provenance review gate

## Verdict

**HOLD / REQUEST CHANGES.** The source worker's DEV8e journey is not eligible
for a central positive gate. It admits a real project pack, but it does not
establish the claimed original P1 through a normal accepted `EditCommand`.
No central suite was added or launched, and no product/shared source was
changed.

## Evidence reviewed

- Source report: `design/ap2-m2-selected-composed-dev-journey-source-REPORT.md`.
- Source commit: `7db1752ca` (`test(app): add selected param dev journey source`),
  based on `92cb038f6`.
- Current selected packet311 controls: `design/peer-app2-to-app-20261020T2118-selected-packets.md`
  and `design/ap2-m2-selected-reviewed-current-shared-packet-REPORT.md`.
- Runtime carrier30 controls: `design/runtime-selected-catalog-existing-carrier.md`
  and `design/peer-runtime-to-app2-20261020T2050-selected-catalog-carrier.md`.
- Agent implementation on `/home/user/work/agent`, especially
  `astrid/sdk/timeline_elements.py:25-41,180-238` and
  `astrid/sdk/timeline/_selected_param_authority.py:14-62`.

The packet/runtime controls are coherent: the supported carrier is the
Agent-produced exact project-pack `DocumentPin`, the exact retained document
and snapshot-object reads, and an accepted record carrying `schema_source`.
The reported Runtime retention evidence is 30 passed for the two selected
pack-read suites. That does not repair the missing accepted P1 producer in
this App fixture.

## Blocking provenance finding

The source fixture does perform a genuine private setup up to pack admission:

1. `project-pack init` creates the throwaway pack realm.
2. `pack.yaml` and the max-10 element definition are written under that
   throwaway root.
3. `project-pack admit` computes the exact owner/id/kind/revision and stores
   the project-pack document/binding. The resolver then checks the returned
   binding against `projectPackDocumentId()` and a `sha256:` content digest.

However, `seedSelectedParamDev()` then directly publishes a composition at
`tests/e2e/local/support/harness.ts:649-654` whose clip already contains:

```ts
elementRef: { id: elementId, kind: 'effect', revision: p1.revision }
```

The following Agent call at `:655-657` passes that same P1 ref to
`timelines update-element`. This contradicts the adjacent comment claiming
that the carrier starts with an unowned draft ref (`:644-647`).

Agent's existing helper makes the consequence exact:

```python
same = equal(element, before.get('elementRef') or before.get('element_ref'))
calls = [] if same else [clip.set-element, ...]
```

With the source fixture's `before.elementRef === element === p1`, the helper
does not emit `clip.set-element`. With `params={amount: 4}`, it emits only
`clip.set-params`. Its capture path then enters the existing selected-authority
branch (`timeline_elements.py:204-220`), which requires an already accepted
history association containing the exact `params.schema`, `params.snapshot`,
and `params.element` records. The prior direct
`POST /v1/projects/.../composition-revisions` is the Runtime's
`parent.composition.publish` writer, not an accepted `clip.set-element`
EditCommand and does not supply that selected-PARAM proof.

Therefore the fixture has one of two invalid outcomes: the Agent call should
refuse because selected P1 authority is unavailable, or some legacy/direct
publication behavior makes it appear to succeed without the required native
history. Neither outcome can qualify a positive P1/P2 retention journey.
The source report's `--list` success proves collection only; it does not prove
the P1 setup.

This is also why the later `schema_source` equality checks are insufficient:
the test records the pin returned by a pack resolver, but it has not shown
that the pin is linked into accepted timeline history by the real product.
`p2DocumentPin` is captured at `harness.ts:673-674` but is not used to prove
the current scope/epoch or a real retained P1 read after P2/removal.

## Exact native producer alternative

Use the existing normal producer unchanged. Seed the initial hold-effect clip
with an unowned draft ref for the same `{kind: effect, id: elementId}` (for
example a draft revision and no `packId`), while keeping `clipType` equal to
the element id and retaining the existing hold/no-media shape. Then call the
existing Agent `timelines update-element` with the admitted P1 ref and the
exact captured head.

That is the branch already implemented in
`astrid/sdk/timeline_elements.py:221-238`: it reads the exact admitted pack
document and snapshot object, constructs the existing exact `DocumentPin`,
passes it as `schema_source`, and executes the native
`clip.set-element` + `clip.set-params` command batch. Runtime acceptance then
creates the genuine P1 history association and links the retained project-pack
input. The existing native coverage in
`tests/core/test_timeline_element_publication_runtime.py` exercises this
producer/retry/reload/inverse path. No new route, DTO, provider, catalog,
browser hash, or synthetic authority is needed.

Only after that accepted P1 exists can the journey admit P2, remove the
authored source, and verify the original P1 exact pin/object remains readable
and enforces the old schema while current scope/epoch and zero legacy gesture
traffic are checked.

## Tests and commands

Source-worker evidence, reviewed but not re-run as a positive qualification:

- `npx eslint --no-cache --max-warnings 0 tests/e2e/local/support/harness.ts tests/e2e/local/three-products.selected-param-dev.spec.ts playwright.three-products.config.ts` — passed in source report.
- `npx tsc --noEmit --pretty false` — passed in source report.
- `git diff --check` — passed in source report.
- `npx playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.selected-param-dev.spec.ts --list` — collected 1 test in source report; collection is not browser qualification.

Reviewer checks:

- `git diff 92cb038f6..HEAD --check` — passed.
- Static source inspection of the donor and Agent helper — confirmed the
  initial P1 ref is equal to the `update-element` target, so the native
  `clip.set-element` branch is not selected.
- Attempted a no-write `_calls` probe using
  `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/agent
  /home/user/work/venv-agent/bin/python`; the documented shared Agent venv was
  absent (`No such file or directory`), so no runtime probe result is claimed.

Not run: central browser/socket suite, local browser, full suite, dirty-source
run, neighboring Gate5, or any positive gate command. No commit-source changes
were made in this worktree.

## Required next step

Repair only the private fixture's initial clip to use the unowned draft-ref
producer path (or provide another existing native producer that emits the same
accepted `clip.set-element` history), then re-review the resulting source
before any central DEV launch. Do not mark the current source qualified.
