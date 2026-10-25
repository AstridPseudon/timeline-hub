# D116 report

- Source PASS: HEAD `795608e1b9d8077487b26eea50b65c1e79c3f522`; Runtime pin `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`, tree `de2954a0ceadb4455903d9abdfec3b773318a50f`.
- Admission passed at `5,005,950,976` bytes.
- Ran exactly the four required NEW4 nodes once:
  `3 failed, 1 error in 28.85s`; no passes.
- Failures: three exact transcript-pin admission errors; gate3 setup errored on closure membership requiring semantic commands.
- No source changes, retries, broader tests, or central requests.

Evidence is under the assigned worker `evidence/` directory, with raw `own4.xml` and `own4.log` retained privately. `DONE` and conventional `commit-msg` were created.

Next step: Runtime/Agent owner diagnosis; this proof is not behavior-qualified.