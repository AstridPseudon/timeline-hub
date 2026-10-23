# Runtime G5 historical fixture handoff

Disposition: **no qualified exact historical fixture found**.

The existing Runtime path is `tests/precut_realm_fixture.py::load_precut_realm_fixture`
followed by `tests/timeline_commit_film_fixture.py::build_film_fixture`. It is
an authenticated backup/restore tool and preserves source bytes, but the
existing archive catalog has no carrier whose canonical parent payload is
`sha256:b6069d1ddccc0279e871b142773b63b73b107ebf9d0adc11ab73832b69097afb`.

The required carrier must preserve the exact parent JSON, including the
`music-other` track/clip, registry, `word:word-1` legacy app declarations,
explicit nulls versus absent fields, nested opaque values and config mirrors;
all three shots and three internals with their physical sharing/occurrences;
dependency manifest; media/CAS; reference and text-binding roots; and genuine
publication/idempotency receipt plus predecessor ancestry. Its actual verified
revision/publication pair may use any authentic revision spelling; the literal
`m1-journey-baseline` is not required.

Agent’s read-only audit searched all 28 retained parent images across the 12
existing Runtime 9ce archives and found no match. The four authenticated
carriers were verified but are non-matches: `anchor` changes timing and lacks
the second track/clip and original null/opaque fields; `music-documents` uses
`music-2` and lacks the app declarations; `raw` changes output/null/opaque data
and child pins; default `original` lacks the required additions. Current
semantic creation cannot reproduce the legacy authority without changing the
fixture or creating an invalid orphan anchor.

Consumer/caller identity is the normal Agent production path: generated
`WorkspaceClient` over a real Runtime daemon, with `TimelineSession`,
`Checkout`, catalog `archive/recover`, CLI redo, and transport closure reads.
The M1 fixture’s direct `RuntimeService.publish_parent_composition` is only a
test setup and must not be treated as historical authority.

The future fixture qualification must exercise the normal V2 request shape
(`api_version`, scope, base pair, commands, label, steps, merge, reads,
`dry_run`, source, rationale, `group_id`, idempotency) and preserve the normal
outcome vocabulary: `accepted`/`merged`,
`historical_rebased{data,receipt}`, conflict reason/head, invalid code/path/
hint/suggested-command, and receipt-free preview with `would` status. This
handoff does not claim those bodies passed; it only records that the fixture
must support the production caller rather than an alternate executor.

Owner seam: Runtime fixture owner must locate and custody an existing
authenticated pre-cut/operator capture outside the inspected catalog. Validate
it only through the existing restore/baseline helpers on a disposable duplicate;
do not add a writer, API, guard, revision override, SQL/direct-store injection,
or new fixture content. If no carrier exists, report that custody fact and keep
G5 gated. The original four bodies remain unverified.

Evidence details and exact archive hashes are in:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-G5-historical-fixture-1621/report.md`

