# OPS-bench-store creator package1924 independent review

**SOURCE FAIL: packet integrity.** Current exported source passes the permitted static checks, but the durable 1924 packet evidence is stale: recorded final hashes/log sizes do not match the flat files currently exported. Combined **FAIL / UNQUALIFIED / STOPPED** remains; STOP1905 is pending.

Evidence:

- Current manifest self-check: all 13 entries pass. Current manifest SHA256: `26719b729c5f84fe72b421b3d69192fe0a8d9d544a6bc934058b6748d33f1c66`.
- Current `validate-packet.py`: `faf4eaddb3f180099de499f32afebedbb9f78a8539ee6a33d46ecb48b7740ca7`, 5,688 bytes. Recorded before/after hash log says `926d4ecf...`.
- Current `validate-packet-log.txt`: `22b8a19155d24690314c40c5085970addf46a62695f816f69a4e5fe1d0477151`, 9,663 bytes. Artifact summary says 10,163 bytes / `74e038ed...`.
- Flat report says manifest SHA256 `2916b09d...`, and artifact summary records that same digest; neither matches the current manifest.
- The current 5,688-byte validator lacks the broader heredoc/inline compile loop described by the 1924 report; that coverage was independently run and passed, but the exported validator/log pair is not the pair described by the report.

Current manifest entry hashes:

```text
baselines feb8b05574eccee6bc3cf36ef941c7f1d0bf88198970211b58134d8956716295
interface ad47e3dd7011007e70b37d1f848d0c0e221daf7442940a3a00c38349e7146733
make-child-venv.patch 4f453badd875e64851eda6cc0deff754d8ca4649feeaf20b5e14482494e4f8f9
make-child-venv.sh d32ede5ff3de131c0fdc25395bdb3fe934b5bb8aa7f00d3d310f689eee38d5cc
make-runtime.patch 69b7b4df7fda3ff823ac4db67463f922d901e716e9528fc51d79d8c8ff3024f3
make-runtime.sh 9f897619de6872ae399fd42154937d17804178793ed67326835c784d35fd45ca
request-child-venv.patch 777e56d07ed8ef83be6dc992bf592ff13e1ba453b39375ec4e4cfca7e5290a77
request-child-venv.sh 72cafb3a5ec343f648a0e41d59a51e7c803ee51b4d04a394dc2010df828bd731
request-runtime.patch e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
request-runtime.sh f13a1d073699712ccfb05e8463ad97ff69dc210a2617f2c9e0140a242591f7b1
test-adapters.py fbb6b22e4e39ca678daa1f455d71a5ce5d778536cc2528447b6c08249548af2e
test-receipts.py 97b5d9ab62485ade0f39ca85d12dcddc54240e676e62cdef09d7f54de0397cb7
validate-packet.py faf4eaddb3f180099de499f32afebedbb9f78a8539ee6a33d46ecb48b7740ca7
```

Required reruns:

- `TMPDIR=/tmp/rt-ops-1929-Wx2q6g python3 -I /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-runtime-OPS-bench-store-creators-package-sol-1924-validate-packet.py`: exit 0, 16 PASS lines; four installed baseline hashes, four patch dry-run/replay/cmp checks, shell syntax, old1850 immutability/guards and Runtime cleanliness passed.
- `TMPDIR=/tmp/rt-ops-1929-Wx2q6g python3 -I /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-runtime-OPS-bench-store-creators-package-sol-1924-test-receipts.py`: exit 0, 7 PASS lines; created/reused exact parser controls, report declaration, tamper/no-verification/no-projection controls, legacy reuse and refusal-without-success passed.
- Independent compile: all 10 heredoc/inline blocks and three anchored provenance/identity scripts passed; TMPDIR allocation was 10,147 bytes.

Current exported source hashes are recorded in the worker report. Static review confirms the 1924 changes address 1921's anchored extraction and patch replay findings while retaining exact report bytes, D21c tuple/tree custody, old1850 guards, and combined STOPPED limitations. No product/test fix, install, combined Store.ensure/build/publication, permission-sensitive action, or tracked deletion was performed.

Qualification is blocked by the stale packet evidence, not by a failing underlying static source check. Re-export all final files and hash/log records cohesively, then rerun both validators before qualification.
