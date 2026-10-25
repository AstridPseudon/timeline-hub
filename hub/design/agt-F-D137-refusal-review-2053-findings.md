# D137 refusal review

Verdict: **PASS_EVIDENCE**.

This is a finite custody/result review, not a product or core qualification.

## Authenticated facts

- The live maker is a regular non-symlink file, mode `0755`, 75,503 bytes, SHA-256 `4435d49953f583234e17a549b4df9896d9d45aa8aa7242ea51a61560ad1d0a36`.
- The exact clean carriers are Agent `a4e016b6a9f91fbe372672bdcf382c630bf59186` / tree `60d45288145414ee4702fcce61af7c7810c2a3df` and Runtime `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344` / tree `de2954a0ceadb4455903d9abdfec3b773318a50f`.
- Admission recorded 6,157,840,384 free bytes before the ordinary request; the stop witness recorded 6,262,321,152 bytes. Both exceed the configured reserve/stop thresholds.
- The single public refusal record has SHA-256 `81b7747ced6d6543ae6e6fc63217edd21367cf5b3493a905f64db4b590e5f4f3`, matching the worker's evidence and its mode-0600 private refusal copy.
- The result is `REFUSED`, stage `venv-log-setup`, exit `2`, with first error `environment: line 60: stage_stderr_path: command not found`.
- `EXACTMISSING` is correct for stage stderr: the live source calls `stage_stderr_path` before creating the stage file, and the named child/stage-log paths are absent.
- The requested child path, pending/done child queue records, and named stage stderr are absent. The worker's service record is `NOTRUN`, with null service ID, null runner/XML, and no registered child interpreter. No exact-name reference was found under the bench store.
- No retry, alternate profile, fallback interpreter, fixture body, Store registration, core service, or ship-grade run occurred.

## Source qualification

The authenticated live maker defines `stage_stderr_path` and invokes it from
`run_stage` at line 304. Its child-shell context export at line 385 includes
`failure run_stage progress source_state`, but omits `stage_stderr_path`.
Therefore the child shell can enter `run_stage` while resolving
`stage_stderr_path` as an unavailable command. This precisely accounts for the
recorded command-not-found at log setup and for the absence of a stage stderr
file. This review did not execute the maker or alter the source.

## Limits and custody note

`EXACTMISSING` means the actual stage stderr cannot be recovered and is not
reconstructed here. Raw refusal/wrapper material was not copied into this safe
packet or reprinted. The original wrapper/log artifacts remain outside this
review's evidence; their OS-level mode is not asserted as private. No
permission change was made.

No tests were run, per the task. This result grants no regression, core,
registration, or ship credit. Runtime owns the source-boundary repair and any
future request requires a new explicit authorization; this review does not
authorize a retry.
