# Theme normal file-input delta review

Verdict: **BLOCKED — do not approve**.

`tests/integrations/test_generic_host_remotion_render.py:572-583` directly
calls `WorkspaceClient.admit_task` and hand-authors
`[timeline, assets_registry, theme, black, silence]`. This is not the
ordinary Main SDK file-mode caller. The existing source path is
`astrid/sdk/invocation.py:1221-1240` plus
`:2639-2657`; its manifest producer emits present file-port IDs in sorted
port-name order (`assets_registry`, `theme`, `timeline` here) and does not
derive registry-media IDs for ordinary file mode. The candidate's extra media
IDs are manually introduced at test lines `493-506` and `575-580`.

Smallest correction: use the existing `sdk.invoke("rendering.render", ...)`
caller documented at `astrid/packs/rendering/actions/render/STAGE.md:86-154`
and capture its actual manifest. If that caller still lacks registry-media
authorization, report that existing SDK/source gap rather than inventing a
second carrier or certifying the low-level host case as normal file mode.

Static checks passed: Ruff, AST parse, and `git diff --check`. No actual proof,
Runtime admission, browser/export, full suite, dependency copy/readiness rerun,
or duplicate CAS proof was run.
