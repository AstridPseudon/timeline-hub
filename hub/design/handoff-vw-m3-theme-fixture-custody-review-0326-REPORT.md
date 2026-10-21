# Theme fixture custody review handoff

Candidate `37006ab9c9586739ffc0956d9a8fe1581f73be69` is fixture-custody
approved: the fresh `_prepare_render_validation`/`GenericPackHost.preflight`
path, owner-vs-worker credentials, `copy2` isolation, and reused frozen graph
evidence are sound. The focused regression was already `1 passed, 2
deselected`; no heavy run was repeated.

The later normal Theme proof is **not cleared**. Its candidate task spec still
contains both `inputs.timeline` and `inputs.timeline_ref`, and its timeline is
not a managed imported descriptor (`input_object_ids` contains only the theme).
That violates the ordinary Main file-mode contract in
`astrid/packs/rendering/actions/render/STAGE.md:192-194`. Before the proof,
import the timeline with the existing owner client, pass its descriptor and
object ID with the imported theme, and omit `timeline_ref`.

No product change was made. No actual Theme proof, Runtime service, MP4,
browser, or full suite was run.
