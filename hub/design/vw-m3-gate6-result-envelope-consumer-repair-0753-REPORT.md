# Gate 6 result-envelope consumer repair handoff

The retained 0739 runner had one wrapper-consumer defect exposed by central
27901: the real validator emitted `result.tuple.appSource`, while `run.sh`
read `result.appSource` in its assertion and success summary. Both reads were
corrected to `result.tuple.appSource`; producer/controller code was unchanged.

The actual captured validator JSON was parsed offline successfully, and a
planted wrong nested App-source digest failed closed. Static syntax and the
updated checksum manifest pass. The central 27901 FAIL classification is
preserved: real validation passed, exactly five cases were collected, and no
issuance, Runtime, browser, physical namespace, grant, marker, or output was
created. No new central request was made.

See the worker REPORT for the compact consumer contract map, exact diff and
hashes, commands, and the later conditional preflight/physical executor.
