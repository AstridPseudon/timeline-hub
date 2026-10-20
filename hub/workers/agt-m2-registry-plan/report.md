Appended one section to [port-manifest.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/port-manifest.md), preserving M0 evidence.

- Eight slices follow the separately owned drag contract, mapping retained commands, timing semantics, writer replacements, regression nodes and deletion triggers.
- Sources: Agent `7a7acc0eea47b372e15bb7921563b281ada00fb4`; frozen SDK `11caf1d9de291d76f491cf69f7942606b7471d7a`.
- Compiler seam: `compiler.compile_timing(TimingInputs) → TimingResult`, composed with main’s graph materializer.
- Static validation: 30 regression names checked; zero unmatched. `git diff --exit-code` and `git diff --cached --exit-code` passed; worktree clean. **No tests run**, as required.
- M2 remains held pending recorded M1 closure, including authorized restore preservation. Group ownership and cross-manager boundaries remain unresolved.

[Report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-registry-plan/notes/report) and required harness commit message written. No product changes or merge request.