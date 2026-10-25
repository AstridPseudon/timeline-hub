# D127 verdict: RETAINED PASS WITH RAW-CAPTURE CUSTODY LIMIT

The exact App source is independently qualified: reviewed commit `9bf465285ccf57be31570c800d4a1f86855ebc4e` and donor commit `54c91d77fa51cb8d21dd86a76d8297d13d8d19e9` have the same tree `7be73e2cbbcf89d627bf7b9da940b4ce17968c20`, and the target blob is byte-identical at SHA256 `92586e7fb9603bec32b6fbee03aeb0fff9176d7cf16a35534ae8a2287e4ad48c`.

The retained 1731 log contains the exact selector invocation, environment, module origins, TAP output, source hashes, and validator summary. It records `P2 Runtime observer bootstrap` PASS: exit 0, one passed, four skipped, zero failed. The Agent/Runtime commits and helper source blob are independently present and hash-verified.

The raw selector log, helper copy, and JSONL capture were under recycled `/tmp/w-52d29f4d54` paths and are now absent. Therefore the result may qualify the targeted control as a retained Node TAP result and exact source receipt, but the 102-event count, `0600` mode, capture hash, phase list, completed-summary count, and privacy-marker result are explicitly retained-log assertions—not current raw-byte custody.

No tests or code edits were performed by D127-1738, and no evidence was invented or reconstructed.
