# App M2 locked-wrapper type-source attribution

**STATUS: LOCKED WRAPPER RED — its ten diagnostics are from the frozen 48576 source archive; graph guards and the ordinary probe pass, but the wrapper must not be called green.**

## Conclusion

With no arguments, the wrapper compiles the frozen source archive, not a
checkout. Lines 18 and 28–31 of
`app-ap2-m2-locked-graph-wrapper.sh` untar
`app-ap2-m2-locked-graph-source.tar` into a private run directory, `cd` there,
symlink only `node_modules` from the locked graph, and invoke `tsc -p
tsconfig.app.json` there. It does not read `/home/user/work/app/src` as its
source input.

The relevant archive members byte-match App commit
`48576cfa2783331f2c7c8309ff4069162a3afd11` (tree
`126983e329d1ab85a59d7a62ebb96676f8aab622`). They do not byte-match the
current HOME snapshot or the integrated fixes `39751fadd` and `b0efbffae`.
Therefore the rerun's exit 2 is historical-source attribution, not evidence
that current App source still has these ten errors.

## Ten diagnostics -> exact source and owner

The ten sites are five unique App files. Hashes are SHA-256 of the complete
file contents. `HOME` is the current `/home/user/work/app` file; its content
matches the current integration source for these files.

| Diagnostic sites | Archive / 48576 | HOME | 39751fadd | b0efbffae | Smallest owner fix |
|---|---|---|---|---|---|
| `elementCapture.ts:236` TS2345 | `a7f5468ed4795a934398ac67ab1a25bd7525ee5749666162754b4ad70e93c2b7` | `e7e1630a88abf5e8fa06f569bcc0000f7ebf9a43e15e1abba596865426fd76fc` | `e7e1630a88abf5e8fa06f569bcc0000f7ebf9a43e15e1abba596865426fd76fc` | same | App helper fix in `commands/elementCapture.ts` |
| `elementGesture.ts:89,93,112` TS2345/TS18048/TS2345 | `ffc458f34c191d614735e23b8c2886fced3fcbe110ef066f3154d779c68c095e` | `7ab18452e1854038e27456369613eb0b0ac13f0fc3d4ffb44f512e10d39c3a5e` | `ffc458f34c191d614735e23b8c2886fced3fcbe110ef066f3154d779c68c095e` | `2d19314331451e513a8d49902b45e3fd59d9db1f217c191ea8ce4c696dde87d8` | App consumer fix in `commands/elementGesture.ts` |
| `genericPatchCapture.ts:306` TS2345 | `23290b1ee2dbfaf9090c7ec76f78ba3768f8e34e7546876283e514f41eecf1fc` | `fc1d25b4c58120485bfc1155c69d8abf7afb4277532d95b30530fafb4ebea506` | `d5b0aa679f7d837bcc4c062590f23fc54f5e916ef33297b8cc6b3ade4b97904a` | same | App helper fix in `commands/genericPatchCapture.ts` |
| `occurrenceDuplicateCapture.ts:83,195,199` TS2322/TS2345/TS2345 | `55eb0ad12155e03efe1faa872c68c7b792990c6b4c6a214446ceb5418df6d69d` | `af20aaf634cfd9998bdd20e4476341c62288b2e52dfdd21473c8711d24015bb5` | `af20aaf634cfd9998bdd20e4476341c62288b2e52dfdd21473c8711d24015bb5` | same | App helper fix in `commands/occurrenceDuplicateCapture.ts` |
| `AstridElementParams.tsx:49,50` TS2345/TS2345 | `2d7f3890d0223c8057a07c897fb06ddb7011d11e8babd7479774d9d00a67ffbe` | `19b696ad6580ae99d33e84b00264f3fe7e369f39176cc1754ade94da0562b567` | `2d7f3890d0223c8057a07c897fb06ddb7011d11e8babd7479774d9d00a67ffbe` | `19b696ad6580ae99d33e84b00264f3fe7e369f39176cc1754ade94da0562b567` | App consumer fix in `components/PropertiesPanel/AstridElementParams.tsx` |

The exact integrated changes explain all ten sites: `39751fadd` carries the
three helper-file fixes (five diagnostics), and `b0efbffae` carries the
`elementGesture.ts` type predicate plus mutable `clear: []` consumer fix (five
diagnostics). The smallest operational repair is to regenerate/refresh the
locked source archive from the current integrated App tree (or apply exactly
those two source fixes to the archive), while leaving the locked dependency
graph untouched. No product edit was made here.

## Type/package qualification

The archive's local type inputs were also checked in place:

| Input | Archive | Current HOME / 397 / b0 |
|---|---|---|
| `src/integrations/runtime/timeline-commit-types.ts` | `e3d625cea11e5e0318c1a3020b1baba62c3726c4d7fe4b3d03d810d48743331d` | identical |
| `src/sdk/video/timeline/patch.ts` | `4252bbae9e5167d24a0e14e76c4d20d35c35f20930ab1cdc7005da0443b23480` | `577b90da0ddd338887681d30f5081a9f93b9972254bc855d7f08efbb68e3b958` |
| `vendor/timeline-schema/typescript/dist/src/index.d.ts` | `1941ab792d32e2f67cf92d9aef2c915cf9100cecc96367c9f1b4563d64f3326a` | identical |
| `vendor/timeline-ops/typescript/dist/src/index.d.ts` | `6f3beba118aecb4bc34d6c91f9d0fba13fd7093958e36b69a306c41a721de859` | identical |

The `patch.ts` difference is historical source drift, not one of the ten
reported diagnostic locations. The vendored schema/ops declaration packages
are byte-identical.

The wrapper's `node_modules` is the locked graph. Its TypeScript package is
5.9.3 and its `package.json` hash
`822ef7ca6452205657b6288b066481ecf508bfbf43455d715cf7d3ec457561e6`; HOME
has the same version and hash. `@types/react` is 18.3.28 and has the same
package hash
`be92045d849a5cadcdae48f1cd53c094a6645359380b3aea911a23a9e83c77e7`. The graph's Composition package is intentionally
different from HOME: graph `@banodoco/timeline-composition` is 0.0.13,
package hash `7c806b07...c7c1aa61`, and its 58 declaration files match all
members of the locked 0.0.13 tar exactly. HOME's installed package is 0.0.8,
package hash `3d93e0bbc1fd3cd5666a5e83e11da76b81a169b9423f90f1f8e7dd2cb733868b`; 11 of the 58 declaration files differ.
This package distinction is graph integrity/source qualification, not the
owner of the ten diagnostics: every reported diagnostic path is under `src/`
and none is under a package declaration.

## Existing rerun evidence and gate effect

I did not rerun the wrapper, `tsc`, a suite, browser/native tests, or install
anything. The completed central rerun was:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-ap2-m2-locked-graph-wrapper.sh
```

It exited `2`; `tsc` exited `2`, the ordinary probe exited `0`, and the
archive/lock/package/425-symlink/0-broken/77-Composition-file/no-writable
guards passed. Current gate implication: retain a RED typecheck/wrapper gate
until the locked source artifact is refreshed and one later authorized run
proves the current source; keep graph-integrity PASS and ordinary-probe PASS
separate from that qualification. No claim about a full suite or any other
gate is made here.
