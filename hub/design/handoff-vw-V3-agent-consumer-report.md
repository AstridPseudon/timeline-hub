DONE

Implemented V3 archive adoption:

- Added exact reviewed archive and SHA sidecar.
- Updated `remotion/package.json` and lock SRI/path.
- Updated stale pin assertions and public evaluation tests for required exports.
- Production caller resolution smoke passed.

Tests:

- Targeted pytest: `108 passed, 1 deselected`
- Installer pin test: `1 passed`
- Private overlay `npm run gen-types && npm run typecheck`: passed
- Archive `cmp`, SHA/SRI verification, and `git diff --check`: passed

Ruff reports only pre-existing findings. Capture-label broader tests were environment-blocked by missing provisioned Remotion peers.