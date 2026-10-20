# Minimal peer request for App2 build28265

The 28265 report says Rollup resolved
`@banodoco/timeline-composition/dist/evaluation.js` without `clipOpacity`.
Return the following from the exact retained 28265 source/graph/build
environment, read-only; do not rerun the journey or alter package, lockfile,
alias, fallback, cache, or graph state.

```text
source commit/tree: 48576cfa2783331f2c7c8309ff4069162a3afd11 / 126983e329d1ab85a59d7a62ebb96676f8aab622
run: ap2-m2-private392-current-postbuild-app-proof-ap2-m2-private392-real-app-door-consumer-gate-1020230652-28265
ROLLUP_RESOLVED_EVALUATION_REALPATH=<realpath -e of file Rollup opened>
ROLLUP_RESOLVED_EVALUATION_SHA256=<sha256sum of exact file>
ROLLUP_RESOLVED_INDEX_REALPATH=<realpath -e of package dist/index.js>
ROLLUP_RESOLVED_INDEX_SHA256=<sha256sum of exact file>
PACKAGE_ROOT_REALPATH=<realpath -e of package root>
PACKAGE_JSON_SHA256=<sha256sum of package.json>
PACKAGE_VERSION=<package.json version>
SELECTED_ARTIFACT_PATH=<artifact selected by exact graph/lock>
SELECTED_ARTIFACT_SHA256=<artifact SHA-256>
SELECTED_ARTIFACT_BYTES=<artifact byte count>
INSTALLED_MEMBER_COUNT=<regular-file count>
ARTIFACT_MEMBER_COUNT=<regular tar-member count>
MEMBER_NAMES_ONLY_INSTALLED=<count>
MEMBER_NAMES_ONLY_ARTIFACT=<count>
MEMBER_BYTES_DIFFERING=<count>
EVALUATION_EXPORT_PROBE=<typeof clipOpacity from exact resolved file>
ROOT_EXPORT_PROBE=<typeof clipOpacity from exact resolved root file>
```

Minimum probes:

```sh
realpath -e "$ROLLUP_RESOLVED_EVALUATION"
sha256sum "$ROLLUP_RESOLVED_EVALUATION"
realpath -e "$PACKAGE_ROOT/dist/index.js"
sha256sum "$PACKAGE_ROOT/dist/index.js" "$PACKAGE_ROOT/package.json"
node --input-type=module -e "import('$ROLLUP_RESOLVED_EVALUATION').then(m=>console.log(typeof m.clipOpacity))"
node --input-type=module -e "import('$PACKAGE_ROOT/dist/index.js').then(m=>console.log(typeof m.clipOpacity))"
```

If a tarball is selected, compare all 77 regular members and return the five
counts plus exact hashes for both JS and both declaration files. This is
sufficient to distinguish stale graph/attachment from alias resolution
without another product run.

