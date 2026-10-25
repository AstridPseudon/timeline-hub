# D127d bounded offline commit cost probe — UNAPPLIED

Production source is unchanged. No lifecycle-size root cause, before/after improvement, or fix is claimed.

Command (completed; measurements.json contains all samples and safe local cProfile rows):

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-runtime/bin/python tools/benchmark_timeline_commit_cost.py --repeats 3 --output /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D127d-element-cost-sol-2123/evidence/measurements.json
```

The existing retained fixture is used unchanged: file 200611 bytes,
canonical JSON 200610 bytes, 2 submitted commands.
It explicitly qualifies transport evidence only, not a production join
(tests/test_timeline_commit_sequential_verifier.py:234). The benchmark invokes both existing
production authentication functions with that fixture's original ancestry, without opening
Runtime/Store, fabricating history, mutating captures, loading credentials, or replaying requests.
First verifier call with freshly cleared schema setup caches: 175.998 ms.
Warm median of three: 123.437 ms.
Separate instrumented run: 388.182 ms.
Validation calls: {"Recorder": 2, "CanonicalDocument": 54}. Profile cumulative rows overlap;
they cannot be summed and are not unprofiled wall measurements.

Synthetic documents follow the P2 element seed's shape in App's harness.ts: two parent clips,
three child clips, one occurrence/shot/internal image and two tracks per config. IDs, media and
payload details are synthetic. No actual mounted document byte count, retained-command count,
accepted-history length or lifecycle state was available in the permitted safe packet.
Media references are deliberately unauthoritative and are not Store-validated closures.
Scaling multiplies clip/asset rows, keeping three physical images. The repeated check counts
1/8/54 are explicit synthetic workload factors; 54 is observed in the DIFFERENT retained
fixture, not established for the mounted element. Each check calls real
_capture_document_images (schema + image hashes + uniqueness); each copy calls real detached.
All synthetic timing rows are warm-process helper measurements. Three repetitions per row.

| Synthetic scale | Canonical bytes | Checks | Validation + image digests (ms) | Detached copies (ms) |
| --- | ---: | ---: | ---: | ---: |
| 1 | 5279 | 1 | 0.902 | 0.203 |
| 1 | 5279 | 8 | 6.784 | 1.647 |
| 1 | 5279 | 54 | 50.948 | 12.492 |
| 4 | 15086 | 1 | 1.680 | 0.586 |
| 4 | 15086 | 8 | 12.881 | 4.679 |
| 4 | 15086 | 54 | 100.579 | 36.392 |
| 16 | 54643 | 1 | 4.817 | 1.692 |
| 16 | 54643 | 8 | 37.556 | 13.563 |
| 16 | 54643 | 54 | 267.160 | 102.245 |

Increasing document rows and the number of independent checks increases traversal/copy cost.
These bounded results do not reproduce 21,740.631 ms handler / 13,780.929 ms provider time,
nor establish a superlinear cause, cache-thrashing cause, or accepted-history growth defect.
The source has repeated document traversal in timeline_commit_auth.py, outside the permitted
production mutation seams. Removing validation or identity/custody copies would violate the brief.
Measured warm schema setup misses alone do not justify a cache rewrite. The 1.75-second direct
replay has a different lifecycle; no ratio against it or this benchmark is valid.

No guessed optimization was applied. Source/result durability: tools/benchmark_timeline_commit_cost.py
and this evidence directory. No new profiling body, HTTP, Store, browser, full suite or heavy fixture run.
