App requests a narrow ownership grant for src/pages/Home/astrid-public-host.tsx, outside this brief's assigned paths.
Concrete change: replace nine builtin imports/map entries with reviewed bridge 27ee90ac1; keep custom components, catalog/schema/revision authority, assets and both Vite checkout seams.
Reviewable patch: design/handoff-vw-m3-d10-owner-packet.patch (apply Home hunk only initially); full evidence in the matching REPORT.md.
Viewing independent checks passed 2+12 registry/host cases, vendor/boundary and lint; the App source bridge is queued as its own unit.
Recommendation: authorize the Home import hunk as the D10 consumer migration. Keep nine vendor deletions held until Agent source removal plus normal provenance refresh.
The Agent source-side dependency is a peer request; no new version, wire, DTO, loader or authority is proposed here.
Not covered because: Home is outside the App editing paths and the donor explicitly carried no Home ownership grant.
Rule that would let me decide next time: App may migrate an existing public-host import for planned package adoption when catalog authority and custom packs are preserved.
