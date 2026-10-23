# App F vendor-resolution handoff — BLOCKED

The current App baseline `7e0af6c9cda5a81a89505b006fcd653d4a5fc770` vendors
Astrid `3f1ceaed144d33a7b14c76164ea3c6e6d92bda61` / tree
`b8beca33526a177d699041ca44318687bfa60640`. The producer commit `c1d49291a`
removed the nine duplicate Composition wrapper sources while retaining
source-less public catalog descriptors. App `1b4ac8b68` removed those nine
vendor files and excluded them from the normal manifest. The production bridge
from `058d10d4f` that used `publicCompositionElementRegistry` was later removed
by `606bd1461` and is outside this task's allowlist.

Focused baseline: 4 tests, 1 passed and 3 original failures. The exact normal
refresh against `3f1ceaed…` passes but produces no nine component files. Vendor
verification passes: 65 pinned source files, 159 vendored files, 11 public
imports. No worktree changes were made. Composition archive `819acf…` remains
unchanged. Next step requires either an authoritative current producer source
for the nine files or authorization for the App Composition-registry caller
bridge; do not resurrect wrappers from `7c17cc9`.
