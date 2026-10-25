# D69 review/evidence JOIN handoff

Result: `NOT_WHOLE_AUDIT_PASS`.

The immutable master remains 129 changed function bodies, 113 removed assertion fingerprints, and 287 added assertion fingerprints (multiplicity). The exact joined map is in `workers/agt-F-D69-review-join-1042/evidence/d69-join.json` and the prose report is in `workers/agt-F-D69-review-join-1042/report.md`.

The joined function-index sets are disjoint (64 unique scopes). Current normal Agent is `7b96e1effa550635fa795a17839d47116e4d2906`; source blob differences against captured are indexes 8–11 and 90, while AST body differences are only faithful repairs at 9 and 90. Index 90 remains behavior-pending because the Remotion dependency was unavailable.

The odd-b prose count is corrected only in this derivative: machine membership is five functions, indexes `37,39,47,57,59`, with five removed and eight added. Indexes 57 and 59 remain unresolved because generic “D69-approved” advisory prose is not an exact scoped approval. Index 107 remains unresolved for the two concrete Windows XML guards `xml.startswith("<Task ")` and `"<?xml" not in xml`; additive repair belongs in `tests/test_installer_platforms.py`.

The 66-row residual artifacts remain source-only and are not semantic PASS. D07/Windows actual behavior, D116, PARAM, and capture remain separate. Tests/typecheck/lint are N/A by instruction.
