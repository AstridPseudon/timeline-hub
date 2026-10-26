# F D141z Main receiving findings

Status: candidate ready for independent review; no canonical mutation or installation was attempted.

The accepted App source remains byte-identifiable and unchanged:

- caller run-final-delivery.py: 71ad92fae4dbe70dd2f0b8b7977bc72d0c2d5c583fd7bedf67b93f3a971af154, 12,812 bytes;
- lifecycle helper delivery_lifecycle.py: 7607908a006fbedff58112ffbc4cb0bb68112615250c00de325b3e2e49fd63d3, 23,186 bytes;
- accepted check.sh: 0486a6e6d6fd5f548f39accfb1ac3866a79b65606c74de9649a67eb2262f6099;
- accepted install-map.json: 4b42c9e355c03be688e5fd763646b0415ea385086862e2854aa1d64d64467618.

The guarded receiver binds the exact caller and helper as one closure, then verifies the genuine Runtime core runner, inventory, D68 wrapper, and current builder before any later install. The three replacement rows are generated only from the reviewed predecessor rows with the caller path/hash closure refreshed. The old runner pin 45a50639 is not silently retained; the actual reviewed caller is 71ad92....

Main’s real current registry is tests/suites.conf, mode 0600, hash 7b1ffdd7225ad9db6a21dd3f2ced1ae7aa3335249ae9994f529aec6d15fd98df. It contains four disjoint Runtime D141 rows, not only the three named in the historical note: full-d141-cut, full-d141-pristine, d141-p5-cut, and full-d141-pristine-targeted15. The candidate explicitly guards and conserves all four. This is the only source-state discrepancy found; no decision was changed beyond preserving the additional real row.

The current builder hash is ef9cd915a4c64f45c179e9ed8aa2ded6e29123847e8018db88ba8b0b680fd9ca; the historical predecessor pin f25dfab13bbfb090bf26cf97a85e59bd4818859f5b974dac94aae7e6f2272708 is not used. This is an existing reviewed receiving adaptation, not a source semantic change.

The source-only map distinguishes prospective live admission from present controls. Admission remains owned by normal test-run; final source/gate tuples, live F1/dispatcher admission, real builder/main/rehearsal, registry write, and final build/ZIP remain unverified and intentionally unclaimed.
