# D139 independent Luna review — FAIL_SOURCE

Reviewed candidate `02b6a412a47bd2f884b823271b8ddd0de544539d` against
`managers/runtime/briefs/rt-OPS-store-retire-2222.md`, with the terminal donor
base `tl/rt-OPS-D131-kind-reserve-1558` (`4ec5b05960af6008542037f74e757b02ca548bcf`).

## Findings

1. **D139-1 — critical: age authorization and production `--now` are caller-controlled.**
   `entry` has no persisted registration/age state (`bench_store.py:192-199`).
   `_retirement_authorization` accepts `registered_at` and `not_before` solely
   from authorization JSON (`604-625`), and the API/CLI accepts a caller-supplied
   `now` (`638-653`, `retire_entry.py:18-19`). A private fixture retired a young
   entry using caller-supplied 2099 timestamps and 2099 `now`; the real entry had
   no persisted age field. The production route can therefore self-assert age or
   pass a future clock. The fix must bind age to authenticated Store state and
   make deterministic time fixture-only.

2. **D139-2 — critical: reference and KEEP/ACTIVE authorization fields are
   self-asserted.** `worker_refs`, `queue_refs`, `registration_refs`,
   `suite_refs`, `keep`, and `active` are caller JSON (`604-630`). The code only
   requires empty lists/false booleans; it has no actual worker/queue/service
   audit or persisted KEEP/ACTIVE state. Store index registrations and suite
   projections are derived later (`677-695`), but that does not authenticate the
   other claims. A Store-owned live audit bound to the current generation must
   replace caller evidence and fail closed when its source is unavailable.

3. **D139-3 — critical: process-reference audit has a deletion race.** The final
   `/proc` scan returns at `664-675`; the journal and destructive `_roll` happen
   afterward (`696-703`, `747-760`) without an admission guard. In a private
   fixture, a process was started with cwd in the entry after the second scan
   returned; retirement still returned `retired` and deleted the directory.
   A second scan alone cannot enforce the concurrent process/cwd/fd/cmdline
   requirement.

4. **D139-4 — high: corrupt retirement receipts are accepted.** Receipt
   validation (`230-238`) checks the key set, derived identity/owner, and only
   list-ness for registrations/suites. It does not validate path/node/lock/seq
   types or receipt list element schemas/consistency. A private fixture with
   `path=7`, `node=null`, `lock="corrupt"`, `seq="not-an-int"`, and
   `suites=[null]` was accepted by `Store.registered()`. Malformed evidence must
   fail closed.

## Preserved behavior

The fixed-two child retention policy was exercised with three private fixture
entries and retained exactly two. No changes to `ensure`/`_evict` policy were
observed. The normal author tests and all specified static checks pass, but the
source candidate fails the lifecycle safety contract because of the findings
above.

No live Store, entry, registration, suite, child, cleanup, installation, or
refusal retry was performed.
