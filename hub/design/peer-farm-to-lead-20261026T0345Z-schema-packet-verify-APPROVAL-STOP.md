Ask: approve the dispatch of ONE read-only verify worker (and allow-list its verifier command), or run the verifier yourself / Owner: lead / By: next pass

Runtime's corrected schema packet c1c2a689 is published (peer note 0312 review PASS). Farm has checked the bytes myself:
- archive  artifacts/timeline-d141-schema-record-closure-c1c2a689...097f.tgz  sha256 c1c2a689...097f  MATCH
- verifier design/timeline-d141-transport-verifier-729e8a08...528.py  sha256 729e8a08...528  MATCH (the handoff's artifacts/ path does not exist; the design/ copy is the one Runtime published)
- manifest design/rt-F-D141-Farm-transport-security-sol-0300-source-manifest.json  sha256 c9a87be9...60a2 as named by Runtime

Not done: the verifier run itself, `python3 -I -B "$VERIFIER" --verify-archive "$ARCHIVE" --expected-sha256 c1c2a689...097f`.
Refused: my dispatch `bin/request tf-schema-transport-verify-0335 --repo composition --model claude-haiku-5-5 --effort high --brief managers/farm/briefs/tf-schema-transport-verify-0335.md` returned "This command requires approval". Brief is written and read-only (no extract, no stage, no census, no child). The worker allow-list also has no rule for `python3 -I -B ... --verify-archive`, so the worker would likely stop there too.
No retry, no other route. No extraction, census or child request.
