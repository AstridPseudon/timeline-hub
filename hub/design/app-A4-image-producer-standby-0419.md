## Report

Produced [a4-image-standby-0419-output.json](/home/user/work/wt/app-A4-image-producer-standby-0419/a4-image-standby-0419-output.json).

- READY peer: `peer-agent-to-app-20261024T0440-image-READY.md`
- Source base: `1c5cc47bf6841c140587f6e1b9164ffb76d433a7`
- Input: 8,957 bytes; SHA-256 `15fa6ca85874232e090dd15610583a4ebf817cafb7ce29b1f84a8e982829a354`
- Deadline: `2026-10-24T05:05:03.447728Z`
- Output: 1,492 bytes; SHA-256 `56566d2fd278415ab8974b9945b61aa1d6e95bc69f849663df3f51b15729e288`
- Node: `v22.22.0`
- Exactly one producer attempt; Runtime/HTTP acceptance not run.
- Structural validation: PASS.
- No source, dependency, graph, or test changes.

Invocation used the qualified external Vitest `createVitest` resolver with private cache. The hub input was used because the ORCH mirror lagged; bytes/hash matched READY metadata.

Commit message and `DONE` marker written. Harness should commit the artifact.

```json
{"request":{"api_version":1,"project_id":"7b6f2bae8ffe42bf925216c38249ed79","timeline_id":"film","base_revision_id":"authoring-parent-revision-038ec4093d414e55d51ef6d29eead099b6fc0fed1821c46d9c354ad321db8cff","base_publication_id":"txn-c4d9e2449545499ea5d1e27141138a58","commands":[{"schema_version":1,"op":"clip.add-media","version":"1","select":"parent","args":{"row":{"id":"clip-0","at":2,"track":"visual","asset":"variant-cd28223ffc6ec7213058801fa3f7aab21c47efbd1910baf590a52f0ce11c04b3","clipType":"hold","hold":5,"opacity":1},"media":{"asset":"variant-cd28223ffc6ec7213058801fa3f7aab21c47efbd1910baf590a52f0ce11c04b3","generation_id":"generation-7b42569a6c8c701a6b03c7d4d52f740bce5a13f7d53dbbc19607364e91a77e7b","variant_id":"variant-cd28223ffc6ec7213058801fa3f7aab21c47efbd1910baf590a52f0ce11c04b3","object_id":"sha256:11507a0e2f5e69d5dfa40a62a1bd7b6ee57e6bcd85c67c9b8431b36fff21c437","catalog_digest":"sha256:774e8df98b091d27e0a40e2e4310a8bab8907bd5bccd538dbbd7d10721e45fd8"}},"intent":{},"created":["parent/asset:variant-cd28223ffc6ec7213058801fa3f7aab21c47efbd1910baf590a52f0ce11c04b3","parent/clip:clip-0"]}],"source":{"via":"app"},"label":"Add media","dry_run":false,"steps":[{"id":"665610a6-aa7e-43af-9d3f-323c9d922cde","label":"Add media","intent":"Add media","tags":[],"command_ordinals":[0],"patch":[]}],"merge":"fields"},"idempotency_key":"8d322a78-0ca7-47a7-bb17-5d7c3a941298","request_body_sha256":"sha256:d52871265f799530c0a3425d50eb20241cfee83198c28916dd2e3a2979be76ef"}
```