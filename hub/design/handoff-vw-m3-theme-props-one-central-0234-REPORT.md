# Agent owner handoff: normal imported-theme props central run

The one manager-authorized named central run reached the exact node but failed
before the fixture started its route. Runtime `8f105c26e3b62f9c2683f717a9773a12bc775a8e`
does not accept the existing test fixture's `production_worker_credentials`
keyword (`tests/integrations/test_generic_host_remotion_render.py:345`).

Offline evidence is sound: exact collection is 1 node with no skip; the
targeted normal-theme controls are 2 passed; Ruff and `git diff --check` pass;
the Runtime import, Node 20.19.4 (`43d6…`), Remotion 4.0.509 carrier, and
Composition 0.0.13 (`9412…d54738`, 77 members) were audited read-only.

No assertion, media import, Runtime admission, GenericPackHost materialization,
resolver, Root props, palette/default/forged-local case was reached centrally.
No retry, alternate Runtime, install, shared write, or source/product change was
made. See the worker `REPORT.md`, `COMMAND`, `testid`, `FILELIST`, and `PATCH`
for exact evidence.
