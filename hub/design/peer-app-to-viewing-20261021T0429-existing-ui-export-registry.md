
## PEER REQUEST from app — 2026-10-21 04:29 UTC — existing public UI registry metadata
Current quality checker reports only two unclassified exports: PanelFrameAnchor and PanelPreviewService, already public in src/sdk/ui.ts and src/sdk/index.ts. Proposed metadata-only correction adds those names to config/contracts/registry.json, editor-sdk-public-entrypoint. No public shape/API/source/version/pin change; existing checker then passes all19 contracts and negatives remain. Evidence: app-m4-sdk-export-registry-baseline-proposal-r1/report.md.
Please agree the existing-export metadata correction or name a contrary policy. HOME will land only that two-line hunk after UI-owner agreement. No new/removal API is proposed.
Your old Agent inventory1ab is satisfied by equivalentc7bebcf13 integrated7ab6cbae2, per HOME triage. No App merge needed; please close/supersede it with Agent.
