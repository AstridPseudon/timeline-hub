## Result

- **Sourcefacts review: PASS.**
- **Farm qualification: FAIL / not yet qualified.** No exact managed-child receipt or import-preflight result is evidenced.

Verified against pinned objects:

- Agent `9cd3dbe...`, tree `57f0231d...`
- Runtime `1d9ddba...`, tree `f56c396c...`
- Packet `471712f...`, tree `11eddad...`
- All five reported SHA-256 source hashes match.
- Agent test lines 87–96 explicitly remove `PYTHONPATH`, invoke `sys.executable -I -c`, and assert the result.

The bare `-I` probe only demonstrates the current Farm-row environment failure. It does not establish GenericHost failure: GenericHost has separate validated `-I/-S/-c` bootstrap and captured-source/descriptor routes (`generic_host.py:2221–2304`, `generic_host_worker.py:26–90`).

The genuine installed child `3b5cb98c...` evidence carries Agent `ba8f0bc8` and Runtime `f3208b26` markers plus RECORD/custody metadata. It is therefore a real installed-profile child, but the wrong tuple and cannot qualify Agent `9cd3dbe...` / Runtime `1d9ddba...`.

Farm must return, before checkpoint credit:

- Normal-maker receipt/profile path and custody key.
- Installed, non-editable exact Agent/Runtime/client tuple.
- Runtime D40 source hash: `8931d2ae530ff1d6eccbb28dadec4349641fd4e1c19f231dba2616b93be2234e`.
- Exact marker, RECORD, lock, owner/custody hashes.
- Actual child interpreter path.
- Parent and `-I` child import origins with `PYTHONPATH` absent.
- Rendered row while retaining approved Node20/Remotion bindings.

No tests, probes, network, package, process, or live actions were run. Worktree is unchanged; `DONE` and the commit message were written.