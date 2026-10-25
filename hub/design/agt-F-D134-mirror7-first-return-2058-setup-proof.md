# D134 mirror7 first-return setup proof

The correction is limited to the two assigned conformance files. `bundle()` now
preserves the independently authored `parent.clips` and `parent.config.clips`
lists for every ordinary case. The exact seven mapped tests call
`mirrored_parent_clip_apps()` only at their existing mirror-guard boundary. That
helper checks equal IDs and full clip dictionaries, aliases the two lists only in
the captured test bundle, and resolves both app references again after the
assignment. It does not alter persisted Runtime documents or source captures.

The recipe-family reference-authority test retains its real `change-echo`
Runtime submission for each non-null echo, followed by `case.restart()` and a
fresh `bundle(case)` capture. Thus the publication, revision/history, and reload
predicates remain present. Echo mutation is still only the intentional test
perturbation after that persisted recapture.

No clip, anchor, word, pin, timing, opaque field, grouping, predicate, guard,
provider, Runtime, client, schema, generated file, or shared fixture changed.
