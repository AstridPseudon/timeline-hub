# App stored-cap final project typecheck

## Source identity

- Assigned worktree: `/home/user/work/wt/app-m3-stored-cap-final-project-tsc`
- Commit SHA: `93696b62f30cf86eac632f975a80de4851489c17`
- Tree SHA: `8465cfeec6a77ed66b6a150205ddca768476e8e4`
- Branch: `tl/app-m3-stored-cap-final-project-tsc`
- Worktree status after the run: clean; no uncommitted source/config changes.
- `tsconfig.app.json`: `target: ES2020`, `lib: ["ES2020", "DOM", "DOM.Iterable"]`.
- Required imports verified before typecheck:
  - `config/hosted-origin.json`
  - `supabase/functions/create-task/resolvers/shared/lineage.ts`

Source hashes for the reviewed ES2020-safe delta:

- `src/tools/video-editor/lib/serialize.ts`: `7bdf715abaa480b8170c6b4ab079db316a162891b938855511dc6423eb464864`
- `src/tools/travel-between-images/components/shotTimelineDataProvider.ts`: `70d6d5e845065a361c0088ccc4974262fe9978042344a891847b5ecee3ebfd4c`

## Private installed inputs

The compiler used the worker-owned overlay at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-stored-cap-final-project-tsc/private12`

- `package.json` SHA256: `0c77703dab8eeb46e05fa7555bbaf5e9ea4fbef077b4759610049fe110894090`
- `package-lock.json` SHA256: `310d447508a2f0c023176a3283724455cd5823b6ffe116177f8e30d541de82a0`
- `vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz` SHA256: `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`
- Composition archive: 77 regular tar members.
- Overlay: 32,280 regular dependency files and 39 internal symlinks; no external symlink targets.
- TypeScript: `5.9.3`.
- Peer versions: React/ReactDOM `18.3.1`; Remotion, `@remotion/media`, `@remotion/player`, and `@remotion/layout-utils` `4.0.509`.
- Peer tree SHA256 values: React `2f56e0708f2b43ad352087679b7b728e13d873197949013aa1d3362cd19dcb07`; ReactDOM `9ca1761200e64fb5671d26f2772453571bafc53eda3e3b66fe83bf35c0cd97c2`; Remotion `d2db38902658bec64dbaf9fe24c53cd2eedd03fd9a0ead4dcecacf04d24199ea`; `@remotion/media` `7c7117a5de0d5f4653acaafbf907be49f467e6b9e97c1e9bc931152b87d112d4`; `@remotion/player` `6de5135118e232772317773a1ec65eca97ed25d74e231a521e55ca73568493d7`; `@remotion/layout-utils` `76a94579d6f198109e5f2b35ee9ae3e44ff6cb2505b20532281979acd059581a`.

## Typecheck

Exact command, run once under the requested lock:

```sh
flock -x /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-stored-cap-final-project-tsc/private12/node_modules/typescript/bin/tsc --noEmit -p tsconfig.app.json
```

Result: **exit 0**. stdout and stderr were empty; there were no diagnostics. No retry or blind rerun was made.

This verifies the stored-occurrence cap on b1/public12. PCM13 and the later cold-start fix are outside this run. No Vitest/full suite, build, browser, socket, install, merge, or parity claim was made.
