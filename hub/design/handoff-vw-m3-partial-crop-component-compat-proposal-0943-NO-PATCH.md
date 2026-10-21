# No unapplied patch

No git-applicable proposal patch was produced. The existing component-owned
`mouthInspectionRect` helper is already the smallest same-drawing geometry
seam, but the public scene has no existing compatibility carrier. Adding one
would change the public `ComponentDiagnostics` type/API; replacing
`diagnostics.mouth` would violate independent semantic capability UNKNOWN
rules. See the adjacent `*-REPORT.md` for the exact source and evidence.
