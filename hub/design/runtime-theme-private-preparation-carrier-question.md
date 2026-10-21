# Runtime private Theme preparation — historical Agent agreement question

> **DEFERRED — owner ruling 2026-10-21 02:04 UTC.** This Runtime carrier
> question is historical design evidence, not an M0–M4 requirement. It must
> not hold current save, render, or peer work. M0–M4 uses the ordinary Main
> path: `media.import_file -> project CAS -> inputs.theme -> theme.json -> ONE resolver -> props.theme`. Ordinary proof is green; canonical
> positive proof remains red pending `rt-m3-main-theme-canonical-caller-
> reconcile`, and this does not claim physical parity or current canonical
> positive green. Preserve the exact source and validator findings below; no
> further private/provenance-only source request is pending. See [the ordinary-versus-canonical proof distinction](handoff-rt-m3-main-theme-canonical-caller-reconcile.md).

Worker rt-m3-theme-private-preparation-owned-source; Runtime base 95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c.

The original owner request authorized a private mode on an EXISTING managed
invocation and asked for an exact existing private mode/input/result carrier
with source paths. The historical constraint was to start with trusted
captured pack/host Theme bytes plus Runtime-frozen config, call the ONE
`_resolved_theme_for_render`, and settle canonical complete `{id, visual}`
bytes through an EXISTING declared output port and its validator before final
render. No already-authorized theme.json prerequisite, invented Theme output
port, public DTO/provider/store/resolver/certificate, or worker projects:write
was allowed.

Historical source trace: rendering.render declares `video` (clip/visual) and
`provenance` (metadata/provenance), not Theme. `_include_internal` returns
private data; it does not by itself change execution mode. Normal host named
theme read requires pre-admitted CAS input, so it was circular as the FIRST
source. The requested source selector, private mode, and output carrier were
left unresolved; Runtime would have owned only admission/retention/recheck.
Existing boundary ACKs did not settle those concrete details.

No product code was written while that concrete agreement was pending. This
note remains a bounded historical cross-area source question, not a public API
proposal or a current implementation wait.

Additional historical source trace (01:23 UTC): `provenance` is an existing
declared file port (`metadata/provenance`) and the normal universal
receipt/harvester checks containment, hashes, sizes and port membership,
without a Theme/provenance payload schema. This could have offered an existing
carrier only if Agent explicitly agreed to its private semantics; Runtime had
not invented a port or chosen a mode alias. `rendering.timeline_visualize` is
already private, but its `manifest_path`/`filmstrip_manifest` ports are
navigation manifests and are not a priori Theme outputs. Normal source fencing
`_admitted_source_roots` / `_verify_admitted_source` binds whole captured pack
bytes; it does not select a Theme file. `active_theme` SDK arguments are
unused in the invocation path; the only host Theme materialization found is the
pre-authorized CAS branch. The historical request to identify an exact source
selection rather than assume these guards provide it is closed by the owner
ruling.

Restart source finding (rt-m3-theme-owned-source-restart-r1, Agent 57d663561):
`GenericHost.run_task` does a second, mandatory check AFTER harvest and
`_typed_outputs`: `generic_host.py:9665-9686` derives `media_ports` from all
declared output artifact types and refuses any missing result file. The
unchanged `rendering.render` definition has `video` of `clip/visual`, so a
provenance-only preparation result is rejected with `produced no result files
for declared media port(s): video`. The provenance file validator alone is
therefore NOT a complete existing preparation result path. No private-context
exemption exists at this check. We must not weaken it or emit a fake video.
An agreed private dispatch must also explain how normal required-output
validation remains intact; merely naming provenance is insufficient.
