# P3 snapshot graph OPS handoff

Status: STATIC PASS for the requested harness custody correction; Farm remains
the sole P3/P2 runner. The original Gate-5 body is NOTRUN.

## Exact row correction

Only the existing app row ap2-P3-gate5-h6-0348 in
tests/suites.conf:36 changed. The final post-eval source boundary now accepts:

    ( test "$(git rev-parse HEAD)" = 2107e1870e51c650d59315f4cc1ab6af338f198c ||
      test "$(git show -s --format=%P HEAD)" = 2107e1870e51c650d59315f4cc1ab6af338f198c ) &&
    test "$(git rev-parse HEAD^{tree})" = a3ff3584e9b559bbb3c3a82b77be7516ed8e761c

The complete %P string is compared, giving the synthetic form exactly one
parent. The exact direct 2107 source remains accepted. Arbitrary descendants,
equal-tree commits, wrong sources, multiple parents, merge parents, and old
source identities remain rejected. Existing source, tree, cleanliness,
ancestry, hash, producer, resolver, pin, and body guards are retained.
The original Gate-5 caller and full v2 request/reply shapes remain untouched:
api_version, scope/base pair, commands, label, steps and their id/label/intent/
tags/command_ordinals/patch/reads, merge, reads, key, dry_run, source,
rationale, group_id, plus full data/receipt accepted/merged/historical/
conflict/invalid/preview fields and their head/document/records/dependencies/
effects/steps/history/undo_steps/would_status/conflict-reason-head/invalid
code-path-hint-command values.

Current row SHA-256 including its newline:
6a1934adad23a6233ba96cce84feffeaa8bf320ff046c843052d92a5171989c4.
Outside-P3 config digest:
e6d4d240181975d560f6c8e7177911dcc231ae7229fabd89eee5653bd5de0153.

## Farm graph instructions

Do not execute graph setup here. Reuse the existing
scripts/testing/auto-real-proxy-main95.mjs prepareNodeModulesOverlay helper
on Farm with a private root outside shared node_modules. Start from the
tracked Composition archive:

    vendor/artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz

Its required identity is version 0.0.14, 73,451 bytes, SHA-256
819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234, and 80
regular files. Keep the package as a physical archive extraction. The helper
owns physical Vite/Rollup copies; ordinary/scoped dependencies remain links
to the read-only shared install. Preserve every existing archive-byte, SRI,
package-version, public-export, resolver-origin, source-pin, and clean-source
guard. Generated exports must resolve to dist/*.js, and package-root
generated modules, package-root typescript, source fallback links, repacks,
pin changes, and shared-install mutations are forbidden.

The 0407 absolute graph path is proof-only. After real qualification Farm
must substitute its own durable private graph path in its invocation; never
point at the Remotion graph or skip the original 80-file/export checks. The
retained 3794/29449 evidence has provisioning, report-all preflight,
actual-beforeAll, and native-21 seed GREEN; the original 37ca journey was
NOTRUN. Diagnostic 30416 skipped guards and is not acceptance evidence.

## Verification boundary

Outer and inner bash syntax checks pass. Actual direct App source/tree checks
pass. Clearly marked offline identity fixtures pass for direct source and
synthetic single-parent/same-tree, and reject wrong source/tree, multiple
parents, and old source; a failed source check does not reach the body marker.
The reviewed 55 protected checks and 21 AST assertions remain retained.

See the worker report and small custody records under
workers/ap2-P3-snapshot-graph-1845/.
