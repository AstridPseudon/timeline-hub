# Isolated Runtime fixture — journey finished, recyclable

Use `ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-m0-journey-runtime-env` for the App journey. Its `.venv/bin/python` points to `/home/user/work/venv-runtime` and imports Runtime source from this worktree; manager independently verified runtime_protocol and astrid_runtime module paths. No installs or product-source changes occurred.

Fixture branch HEAD: `8345656`. Product-source base: Runtime integration `8c1830d1ca64a3934c37611a28ffe8db7df879ea`, package source version `0.1.0`. The fixture's only two committed files beyond that base are `.venv` symlink and a local environment note. Contrary to the worker's initial note, `.venv/` does not ignore a symlink: the harness committed it. This is a disposable local fixture branch, **not for merge/delivery**, not a change to Runtime's canonical environment contract. Integration is untouched. Record fixture HEAD plus product-source base honestly in journey results.

Shared environment remains dependencies-only, without installed astrid-runtime distribution metadata. Module imports work from this source checkout; the existing App fixture launches Runtime programmatically, not via a newly installed package. No actual Runtime start or journey pass is implied by these import probes.

rt-m0-journeys finished: direct39/39 and three-products3/3 passed, suites ended and door port17340 was verified free. This fixture is now recyclable. No live process currently belongs to this setup worker. The heavy App worker uses its own App worktree/build and the existing generated clients; actual suites run with --net, serially, at most one attempt each.
