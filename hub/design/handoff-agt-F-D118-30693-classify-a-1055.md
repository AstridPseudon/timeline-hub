# D118 terminal30693 accounting — Part A

The terminal XML has 450 bad nodes: 159 failures and 291 errors. Immutable full-XML enumeration assigns 365 bad nodes to Part A (`tests/editing_conformance/`) and 85 to the disjoint Part B complement; the exact-ID union is 450.

Part A has 364 `NEW-OURS core` nodes and one `UNKNOWN` node. All 365 are core scope and current core open. Regression count is zero. Fourteen exact 2016 source/exception/location tuples were reused; all were already `NEW-OURS CORE`. The former ENV row was not exact and therefore remains UNKNOWN. Each row was mapped to the XML classname/source file, its test function was verified by AST at Agent commit `120d71202a9ebafa99011aec417cfca6d67fafc2`, and only safe exception/location fields and hashes were emitted.

See the worker evidence JSON files for exact IDs, ordinals, hashes, safe locations, and partition digests. No tests or runtime behavior were executed; this was static XML/JSON/source/AST validation only.
