# Handoff: AP2 P1 v2 seed review — FAIL

Independent review of `8e09a143c7cc70f9416e631f6f094537325311a` against
Runtime `49ce53289bc37d9387a7d9e6b9c9b16072162181` and Agent
`ce1d1cca87379029924b0be6f98564f556597107` found a blocking native-init seam.

`seedOneClip` preserves the original clip, including `app.astrid.for: 8`, but
passes it to Agent `capture_clip_add_media`. Agent `ce1d1cca` rejects that
field as a non-literal timing relation in
`native_occurrence_media_commands.py:158-165`, so the seed fails before the
Runtime v2 commit is sent. Stripping the field would violate the no-weakening
payload/source-field requirement.

The migration has the correct one-file scope and public Runtime bootstrap,
media-import, selection/verified-custody, and authenticated Agent facade
shape. Its seed proof nevertheless only checks parent payload equality and
prints `accepted_revision_id`; it lacks explicit accepted publication,
receipt/result binding, and complete canonical-closure assertions before App
open.

Dependency HOLD: shared `harness.ts` base seeding remains legacy and is owned
by Sol-1116; it was not edited and was not used as the rejection basis.

Checks: P1 list 2 PASS; scoped ESLint PASS; embedded Python AST PASS; Agent
init/emitter control FAIL as above; Node typecheck PASS; App typecheck timed
out at 30s (124, no diagnostics); diff/EOF/one-file scope PASS. No browser,
HTTP/body, full, build, service, ops/request-test, native-14, or live
qualification run.

Next owner: supply a supported exact-field-preserving native birth/import seam,
then re-run the bounded control and strengthen receipt/publication/closure
assertions before live P1 qualification.
