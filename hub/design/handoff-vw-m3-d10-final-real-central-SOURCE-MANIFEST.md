# D10 final Home normal-refresh source manifest

- App base commit: `8ffd2164b`
- Central snapshot tree: `d1a770fb1c3a960b6de84bab837b184fb4c6b16b`
- Owner packet: `OWNER-READY.patch`
- Owner packet SHA-256: `4e6f792360a175a2d7ce6fc3685a4c11c1ddd77bbd2e4b189e42f119d2bfe1fa`
- Owner packet paths: 13 (updater, vendor manifest, Home host, provenance, nine deleted implementations)
- Astrid checkout: `/home/user/peteromallet/astrid-agent`
- Astrid source commit: `680d1aa4f1f9576d65a603472f1dd7fc0ae9ccd1`
- Astrid source tree: `07ce61f24ec38a1a60c4a981b6bd666f4971bd67`
- Central normal output: 156 files including provenance; 146 recorded vendor files
- Central packet output: 147 files including provenance; 146 recorded vendor files
- Exclusions: exactly the nine package-owned implementations listed in `REAL-CENTRAL-EVIDENCE.json`
- Central result: `vw-m3-d10-final-central-without-preload-integration-viewing-pack-wrapper-unit-1020183621-31017` PASS

The central test applied the flat packet only inside a disposable private root,
ran the packet's original generator with real `git` against the exact source
commit, and compared the resulting vendor tree byte-for-byte with the packet.
The working tree was not changed and no source checkout or shared dependency
was modified.
