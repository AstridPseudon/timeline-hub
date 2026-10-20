# Runtime ordinary014 independent final review

## Verdict: REJECT

Review target: the committed-candidate worker report identifies the actual candidate test-service snapshot tree as `06de9476db4a9b7f11f6adeb4cb8003fa942f651`, based on Runtime commit `7f6dd8920e1ceec41b137358df5e7fecc304888d` / tree `4cccb2d643194df7df95d624e89a6cd9f6f268fc`. The worker report does not emit a separate candidate commit SHA; this review therefore cites the immutable candidate tree and exact patch identity rather than a moving worktree. Prepared patch SHA-256: `06ecdfcb17cc975f8bed9e3c62677bbcaa8873b5c5cb1e1d65dbf9ff3c1c719`.

The artifact/schema side is otherwise acceptable:

- Frozen Agent source `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3` / content tree `c5a8a3ec7e9e01c61c5ae31834da53bed4be406a` matches the candidate raw schema SHA-256 `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`; the candidate and embedded Runtime bundle contain the same 55-definition, 29-operation schema.
- The patch applies cleanly and is restricted to the declared 17 generated/contract paths. No new public schema fixture, endpoint, port, private carrier, version-2 path, custody/attestation machinery, or authority/source change was found. Public fixture `agent-26ef2bbb.json` remains unchanged at SHA-256 `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`.
- Candidate metadata is internally consistent: contract `0.2.14` (unpublished), Runtime schema digest `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`, artifact version `sha256:8023c665f0e32835cf06b793c6f5ffa0a278a7ca5aadbfe971d52d163d66c7a3`, 75 artifacts, and 133 unique HTTP operations.

## Blocking finding

The successor changes `tests/test_timeline_current_union_contract.py` so that the prior positive invariant—every schema `*Args`/producer type is exported from the public Python client and identity-matches the DTO module—is conditional on the name already appearing in `client.__all__`. The candidate’s own report confirms that seven newly generated ordinary DTO names are absent from the package initializer, and the relaxed test now lets those missing exports pass. This violates the settled requirement that all old positive assertions remain and that tests are not weakened. It also leaves the generated Python client’s public API incomplete for the new schema cohort.

Do not pin, merge, publish, or activate `0.2.14` until this is repaired. Restore the exact export/identity assertion and either generate/export the seven DTOs through the intended package API or document and test a precise, non-weakening public/private boundary with an explicit allowlist.

## Evidence

The committed-candidate worker reports these actual-candidate results:

- bounded contract/schema/retention lane: `300 passed`;
- central socket-capable commit integration: `9 passed`;
- central TypeScript client check: `61 passed, 0 failed`;
- frozen Agent310 ordinary native cohort against the exact candidate Runtime: `11 passed`.

Independent archive checks performed here:

- `git apply --check` of the prepared patch: PASS;
- patch SHA-256 and 17-path inventory: PASS;
- frozen Agent raw schema and candidate schema hash: exact match;
- candidate operation order/set versus frozen Agent: exact 29-operation match;
- Runtime bundle’s embedded edit-command schema versus candidate schema: exact match;
- forbidden private-carrier/version2/attestation/gateway scan of changed artifacts: no matches.

No full suite was run. No consumer pin, merge, publication, or product-code edit was performed.

