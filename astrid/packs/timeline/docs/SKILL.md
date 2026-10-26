---
name: timeline-transfer-actions
description: Read-only Runtime actions for planning timeline exports and preparing imports.
---

# Timeline transfer actions

Use `timeline.export_plan` to read the saved timeline and receive a task
artifact containing the full export plan. Fetch the `plan` task output through
the existing task managed-output API; the action does not assemble an archive
or create project objects.

Use `timeline.prepare_import` in two passes. First pass `manifest` (or the
`manifest_file` fallback) with `check_only=true` before uploading any media.
After successful compatibility checks and client-side uploads, pass the
manifest and a JSON `payload` file containing
`{ "timeline": ..., "transcripts": ... }`
to receive a `prepared` commit-body artifact. The
prepared body is still only a proposal; the client owns upload/commit and any
target-project object management.

These actions do not publish timelines, write project documents, or associate
task artifacts with a project.
