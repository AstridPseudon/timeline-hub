Ask: publish the answer as hub/design/farm-extensibility-minimal-codex-20261026T144554Z.md (labelled Sonnet fallback, independent third view); note it is PARTIAL / Owner: lead / By: next pass

F-extensibility-minimal: tf-extensibility-minimal-1450 finished (exit 0, KEEP). Answer file: workers/tf-extensibility-minimal-1450/evidence/farm-extensibility-minimal-codex-20261026T144554Z.md (first line carries the required label).
Verdict: yes, over-engineered. Minimal version about 9-10 senior-engineer days vs the assessment's 110-120.
- Commands: python fn(timeline, **args) run through the existing Timeline.commit(fn) (retry, undo, labels); op table stays closed.
- Views: make the hard-coded `--as` choices come from a registry.
- Overlays: reuse Layer/Check classes and directory-glob discovery in layers/base.py; generalise the discovery to also collect COMMANDS and VIEWS.
- Example pack astrid/packs/beatgrid/ (beat-snap command, beat-grid view, beat-tick overlay, tests); agent finds them via `timelines run`, `--list-commands`/`--list-views`, and MCP via the existing CLI-to-tool conversion.
- Cut/defer: elements and signals, markers, Runtime proposals, manifest/scaffold, conformance harness, unifying the two commit paths, sandbox, App panel host.
- Main risk: function-commands are Agent-side macros, not ops Runtime/App can replay; if App-visible commands are needed a real op registry is needed, where most of the 110 days come from.
PARTIAL: the worker did NOT read your job text, shot-layering-PLAN-v1 4.1-4.3, or astrid/core/pack/, and did not verify that MCP auto-picks up pack CLI additions or the App panel claims. Agent checkout stayed clean (ec0a9f5b). One compound read command was refused earlier; it stopped and resumed with dedicated tools.
Follow-up already dispatched by Farm: tf-extensibility-gaps-1500 (read-only, same Sonnet fallback) covers exactly those four gaps and says whether each changes the estimate; results next pass in workers/tf-extensibility-gaps-1500/evidence/farm-extensibility-gaps-<UTC>.md.
