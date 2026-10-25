# handoff-rt-D100-30890-0543

Safe flat export for PLAN3F/G3/R1,C0 D100 Runtime candidate body 30890, with exact old-RED control 7351. This is a mechanical per-ID export of retained producer XML/log/manifests only; it is not a semantic verdict and does not qualify the candidate for merge.

Candidate body outcomes are exactly 38 PASS, 16 FAIL, 5 ERROR across 59 IDs. The baseline is exactly 12 PASS and 14 FAIL across the same 26 new-regression IDs. per-id.tsv and per-id.json preserve every candidate outcome and the one-for-one baseline comparison; firstexceptions.tsv preserves only sanitized first exception class/category/path/frame data.

Groups are kept separate: newexacttime (4), newshareditem (22), originalTEN (10), docpatchphysicalcontrol (1), and historicalneighbors (22). The original TEN remains the exact source with all 29 assertions and source facts unchanged. Failure IDs remain separate for source-offset authoring refusal, at_ms Fraction handling, Runtime internal-timeline scope mismatch, inverse materialization, and historical text binding. No broad common-cause or product-blame claim is made.

Old-RED classification is retained per ID only where the XML/log frame establishes it: production assertion, input/refusal, setup/refusal, or UNKNOWN. No historical proxy, source-only prediction, count sum, rerun, collection, diagnosis, classifier, or semantic NO-GO was added. The existing producer report's NO-GO is referenced as existing evidence only.

The immutable four-repo tuple, source/test/helper hashes, argv/XML/body-log hashes, profile/import facts, controls 17+1, registry restoration and later unrelated-row preservation are in run-identity.json and source-hashes.tsv. Raw XML/log/argv/request/body/media/auth/key/URL artifacts remain private.
