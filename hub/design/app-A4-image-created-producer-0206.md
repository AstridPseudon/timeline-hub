## Report

Produced [a4-image-created-0154-output.json](/home/user/work/wt/app-A4-image-created-producer-0206/a4-image-created-0154-output.json) with exactly one producer attempt.

- Source HEAD: `1c5cc47bf6841c140587f6e1b9164ffb76d433a7`
- Input: 8,957 bytes; SHA-256 `c0a3b6570b8ed5a40b4ef6cf32a7774768a8bd719942e8c5e2daa1053c83eb1e`
- Hub fallback matched the same hash.
- Output: 1,492 bytes; SHA-256 `af1a9a845d4b6cc43315385e149072ef20f57af885c53c4fa5c546a68fc809ad`
- Handoff blob: `f4f6b4f95c430956b1a5c05750ac3e4573286785`
- Producer blob: `8f686e3e3be448995eae1c43a9e86d1dee217aeb`
- Runtime acceptance: **NOT RUN**

Producer command used the approved external Vitest `createVitest` invocation with normal aliases and a private cache. Structural validation passed: one `clip.add-media` parent command, empty intent, exact five-field selection, created claims, new-input identity, authored-registry absence, and opaque value/location preservation. No Runtime/HTTP submission.

Exact output:

```json
{"request":{"api_version":1,"project_id":"7b6f2bae8ffe42bf925216c38249ed79","timeline_id":"film","base_revision_id":"authoring-parent-revision-038ec4093d414e55d51ef6d29eead099b6fc0fed1821c46d9c354ad321db8cff","base_publication_id":"txn-297b037663374fcfac8b1097964942af","commands":[{"schema_version":1,"op":"clip.add-media","version":"1","select":"parent","args":{"row":{"id":"clip-0","at":2,"track":"visual","asset":"variant-0753676861c9a4dd6a775abff10db408008b14978f247e9adf3a6acb8d18aa0b","clipType":"hold","hold":5,"opacity":1},"media":{"asset":"variant-0753676861c9a4dd6a775abff10db408008b14978f247e9adf3a6acb8d18aa0b","generation_id":"generation-5fdd98a846da5596444b9f316914e01f02d3055e08dc64ff5a169724bd29794d","variant_id":"variant-0753676861c9a4dd6a775abff10db408008b14978f247e9adf3a6acb8d18aa0b","object_id":"sha256:11507a0e2f5e69d5dfa40a62a1bd7b6ee57e6bcd85c67c9b8431b36fff21c437","catalog_digest":"sha256:61dcac09fca1f7141cc1e8925fb8a648580fa8d8cc5b08a89e5e90ff10ce01b7"}},"intent":{},"created":["parent/asset:variant-0753676861c9a4dd6a775abff10db408008b14978f247e9adf3a6acb8d18aa0b","parent/clip:clip-0"]}],"source":{"via":"app"},"label":"Add media","dry_run":false,"steps":[{"id":"41ad0c81-8942-4878-b003-a5e2fcf33b8f","label":"Add media","intent":"Add media","tags":[],"command_ordinals":[0],"patch":[]}],"merge":"fields"},"idempotency_key":"a2d58264-14a2-4d16-ad7d-84f6dbd68015","request_body_sha256":"sha256:d27b8f7b86145efb985651ad93d8079204ae621c49ffe9def775078888074abb"}
```

Commit message and `DONE` marker were written.