# Per-record comparison: runtime4913 source vs reviewed stage1054

Compared source `/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/node_modules` with stage `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-storage-cleared-complete-runtime-stage-1054/owned-stage/remotion/node_modules` using the existing controller record shape and the packet's record traversal. There are 23,014 source records and 23,014 stage records, including directories, regular files, and symlinks.

## Record/key and metadata differences

| Field | Differences | Finding |
| --- | ---: | --- |
| relative path/key set | 0 | Same keys; no missing or extra record |
| record kind | 0 | Same file, symlink, and directory kinds |
| canonical kind/mode tuple | 0 | Same executable/file and symlink serialization |
| mode | 0 | No permission drift |
| size | 0 | No size drift |
| regular-file content digest | 0 | No byte drift |
| symlink target | 0 | No link-target drift |
| uid / gid | 0 / 0 | No ownership drift |
| device | 0 | No device-field drift |
| inode | 23,014 | Independent stage copy identity; expected |
| hardlink count | 2 | Only the known esbuild pair differs: source 2, stage 1 |
| atime / mtime / ctime / birthtime | 0 / 0 / 0 / 0 | No timestamp drift |
| root path | differs | Source and stage have intentionally different absolute roots; root path is not in the canonical record tuple |

The two `nlink` differences are exactly:

| Relative path | Source inode / nlink | Stage inode / nlink |
| --- | ---: | ---: |
| `@esbuild/linux-x64/bin/esbuild` | `1385077 / 2` | `4934571 / 1` |
| `esbuild/bin/esbuild` | `1385077 / 2` | `4942379 / 1` |

Both entries remain mode `0555`, size `11,407,472`, and have the same content digest and timestamps. The stage intentionally breaks the source hardlink pair while preserving bytes and mode; this cannot explain `f06d7fe9` because neither inode nor nlink is serialized by either fingerprint implementation.

## Serialization-order difference

The packet traversal and controller record sets are equal, but their sequence differs. The first divergence is at record index 859:

| Index | Packet traversal | Controller final lexical sort |
| ---: | --- | --- |
| 859 | `@babel/helpers/lib/helpers/AwaitValue.js` | `@babel/helpers/lib/helpers-generated.js` |
| 860 | `@babel/helpers/lib/helpers/AwaitValue.js.map` | `@babel/helpers/lib/helpers-generated.js.map` |
| 861 | `@babel/helpers/lib/helpers/OverloadYield.js` | `@babel/helpers/lib/helpers/AwaitValue.js` |
| 862 | `@babel/helpers/lib/helpers/OverloadYield.js.map` | `@babel/helpers/lib/helpers/AwaitValue.js.map` |

Across 21,455 records, 14,624 positions are equal and 6,831 positions differ. JSON serialization of these equal-but-differently-ordered tuples therefore yields the two hashes:

- Recursive traversal without final whole-list sort: `f06d7fe955f936e7a6370cee1900bd4d32a5676d65a8f9a7f46f8b4ce8ec352a`.
- Existing controller with final lexical path sort: `4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c`.

This establishes an algorithm mismatch, not a genuine source/stage graph mismatch.

