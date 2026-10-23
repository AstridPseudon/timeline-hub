# A2/P1 independent review — FAIL

Reviewed candidate `76a4bc64773ed9bbfeec393e4b0888594029f7d0` (tree
`17f9b81cad39f803eb6b0e2f3f24336fa05c3d20`) against base
`9dd59025d6aba6b37112c498b479e3f36c7b4bbb`.

The authenticated public GET pairing, identity checks, bounded revision
mismatch refusal, legacy-null preservation, and captured-pair CAS retention are
mounted and source-correct. However, the candidate fails the settled C0
publication semantics: `dataProvider.ts:1427-1429` reuses the old
`parentComposition` whenever the revision is equal, and `1445-1447` leaves the
version unchanged, both ignoring publication identity. Its immutable basis key
at `1432-1434` is revision-only. Thus after `(R,P1)` becomes `(R,P2)` with equal
bytes, load/poll reports `(R,P2)` while retaining the old original basis and
version instead of treating P2 as a new base. No test covers this transition.

Targeted 4-file Vitest: **152 passed**. `npm exec tsc -- --noEmit`, scoped
ESLint, `git diff --check`, exact private `819acf` graph checks, and the
three-file outside-blob allowlist all **passed**. No product changes were made;
no browser/build/full/socket/service/original-chain run was performed. Return to
the App owner for a publication-aware cache/version refresh and regression test.
