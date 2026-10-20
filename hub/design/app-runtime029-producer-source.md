# App Runtime 0.2.9 producer source

Readonly producer checkout for the App normal vendor-lock update.

| Field | Exact value |
|---|---|
| Producer path | `/home/user/work/wt/app-m3-runtime029-producer-source` |
| Producer commit | `94114269d1ce23ab3224d7eca5a85138ce2b5fed` |
| Producer tree | `5655e7e6290d0939f34b804a8df07bc972030faf` |
| Worktree state | Clean (`git status --porcelain=v1` empty) |
| Python client | `astrid-runtime-client 0.2.9` |
| TypeScript client | `@astrid/runtime-client 0.2.9` |
| Contract version | `0.2.9` |
| Schema digest | `sha256:8d7f29873ff3417cda746e243ebc81cb9d54e41c972596d4d3ae591fc1de00cf` |
| Artifact manifest version | `sha256:e02a71b5b77479bdc8035a8a8d75ec57e9f1962b7f9195126739ab0d1ed063ac` |
| Edit-command schema raw SHA-256 | `472622c45fa6b5c7a425c949516a64a52d83192d3749e78a0f000decd088aee9` |
| OpenAPI operation IDs | 133 unique IDs: 52 GET, 1 HEAD, 72 POST, 5 PATCH, 2 PUT, 1 DELETE; 80 mutating |

The operation count and uniqueness were read from `contract/openapi/workspace-v1.yaml`; the Python and TypeScript generated metadata each contain the same 133-operation set. The artifact producer is `astrid-runtime`.

App may consume this exact directory as `<producer>` for its normal vendor-lock update, but must pin the exact commit above rather than a moving integration ref. This is a source handoff only, not paired qualification or release approval. Agent current-pin unit/public12 work remains pending, and coordinated App pin/current-pair tests are manager gates.

No Runtime product, generated, test, pin, dependency, build, or branch files were changed. No install, build, test, socket, or generator command was run.
