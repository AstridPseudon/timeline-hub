# F-D86 packet validation

This worker performed source-only evidence handling. No pytest, collection,
helper/fixture, CLI, service, browser, build, or reproduction execution was
performed.

- JSON parse, TSV shape, selector-set, A `EXACTMISSING` accounting, B branch
  byte comparison, and B flat-copy comparison: PASS (111 checks).
- B source: `tl/rt-D86-20-22-exact-return-0358`, commit
  `2e81b898cbf1512e040a85bb8d5cc847e9baea56`; 48 safe files byte-identical.
- B producer XML provenance retained in the copied superseding packet: Runtime
  commit `350058edc5b830215c7d915e09024e2362a0b429`, run
  `fd86-exact22-body-20261025-034159`, 4 PASS / 18 ERROR.
- Redaction scan: PASS. No URL, credential, raw request/body, or dump content;
  the safe metadata key `raw_request_or_body_exported` was allowlisted.
- Evidence size: under 2 MB.

Raw XML, logs, commands, captures, credentials, and private dumps were not
copied into these outputs.
