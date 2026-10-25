# D139 coverage

Static AST/metadata census against Agent 4c4ee35d5687c4cd40a0e5395efda53aa56f939d and Runtime producer ab1e4f6141987706132916e2da16477f5a019464.

- Exact command roots: 22 selectors, 431 Python files; no filtering/deselection.
- Reachable local source modules: 1001; unique imports: 1146; EXACTMISSING: 17.
- D73 preflight: embedded Python in tools/p4-d73-pinned-launch.sh, read only.

Limits: no collection, imports, preflight, controls, child/request/maker/install, configuration/plugin mutation, or product suite. Data-dependent dynamic imports are listed only when source literals/config calls expose them.
