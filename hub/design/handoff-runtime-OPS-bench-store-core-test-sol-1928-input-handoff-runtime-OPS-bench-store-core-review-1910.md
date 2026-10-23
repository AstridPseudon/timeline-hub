# OPS-bench-store independent core review 1910

## Verdict

**CORE: PASS (source/private core only), with findings.** The overall combined
creator/child result remains **FAIL / UNQUALIFIED**: the actual child caller
hit readonly publication and rollback `EACCES`; the author was STOPPED and the
runtime-1905 escalation remains unresolved.

## Frozen source

The author packet was terminal before hashing (`BLOCKED`, `ended`, `exit`). The
final core source matched the manifest:

- core `53d90fb3108b24253a29416214ec5fa8f69402f50a515f0399b7464ec39a2e14`
- core tests `c836462cb61bd57360d4f060637e1c76b6f2e746e2970ef7a94f0babe4f230c`
- validator `e95c054c55aab902bfb5b4e5cd3ad72b1abd791be7c6b244fb028cc3f4a18387`
- interface `c6a3fe9b3badfda4b4718ec013db69c79cff95eafb2a9306739e69f95fa25b19`
- 1854 compatibility core copy is byte-identical

Caller boundary sources were also read from the frozen packet: make-child
`78659d8ac79605514f71959a5b9b4adccce2664edac36575bf0bde691b48d6ba`,
request-child `b617298df82c8293cf5a073f9fdc4a9ac92f16283b41c9e5b58cf98ad640f383`,
make-runtime `9f897619de6872ae399fd42154937d17804178793ed67326835c784d35fd45ca`,
request-runtime `f13a1d073699712ccfb05e8463ad97ff69dc210a2617f2c9e0140a242591f7b1`,
and lease seam `be6ab1ef7c7b41baf9d026bd8e2e857d900bc83245d9cd8372fb72a5b05da4cd`.

## Evidence

Exact command:

```text
TMPDIR=/tmp/w-6600eed316/rt-OPS-bench-store-core-review-1910 \
  python3 -I design/handoff-runtime-OPS-bench-store-core-precondition-1858-test-core.py
```

**PASS: 18 tests in 1.438s.** The frozen source contains 18 tests, not the
packet's “20” label. It covers actual reclamation before callback and free-space
proof, durable eviction then creation, failed-build retention of prior
eviction, crash journal recovery, tamper/symlink/foreign-path/owner/schema/key/
lock refusal, reserve refusal, same-key serialization, and latest-two-plus-
leases. Scoped compile/manifest/cmp/Runtime-clean/diff validation also passed:

```text
TMPDIR=/tmp/w-6600eed316/rt-OPS-bench-store-core-review-1910/validate \
  python3 -I design/handoff-runtime-OPS-bench-store-core-precondition-1858-validate.py
```

## Findings retained

1. The actual combined child path fails readonly publication/rename and then
   readonly rollback deletion with `EACCES` after the maker seals stage/source
   paths (`make-child-venv.sh:391-392`). This review did not chmod, retry, or
   use alternate publication.
2. Child stores `.provision-report` inside the managed entry and returns empty
   env metadata (`make-child-venv.sh:159-187`), so the frozen core has no way to
   project historical `tests/provision/NAME.txt`. Success output also lacks the
   existing farm preflight's `status=passed`/PASS receipt (`:188-195`).
3. `names_for_suite()` returns `[]` for an unregistered row; the lease seam then
   runs direct-child semantics with no lease (`bench_store.py:557-568`,
   `lease-seam.py:21-30,51-57`). A custom existing gate profile or unregistered
   row using a managed bench through env/absolute path is therefore unprotected
   from eviction. This exact source boundary needs an ordinary conservative
   fix (authoritative path/env mapping or all-managed fallback); do not blindly
   adopt unknown legacy benches. Managed stale-row races do refuse later in
   `acquire`, but unchanged unmanaged rows do not.

The core's destructive traversal and transaction authority review is otherwise
PASS: no `/proc`; exact owned path/inode/marker/lock checks; `O_NOFOLLOW` and
directory-FD deletion; affected registration hashes/projections verified before
eviction; unrelated, foreign, template, current, leased, and unknown legacy
data remains protected. D21c canonical identity keys are preserved.

The core result is not installed-bench, host, test-service, complete creator,
full C0v2, or frozen-34e integration evidence. Next step is to resolve the
readonly lifecycle and caller projection/receipt/lease boundaries, then rerun
the complete private caller fixture against this exact core.
