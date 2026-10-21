# WC1 independent assertion/data-safety verdict

## APPROVE bounded candidate

Approve unchanged candidate `c7e392f19b6e6b186c632ed050d8ea6e73b55a34`
(tree `d6aba756208419b9bdfa17e11c7b08710ad5399c`) for the narrow WC1
false-positive assertion repair. The prior 2-case HTTP result remains
unqualified because it ran before this commit/tree; no duplicate HTTP run was
requested.

The checker is source-correct: it filters only `product` phase, exact legacy
mutating methods `POST/PUT/PATCH/DELETE`, and exact terminal paths
`/composition-revisions` or `/publish`. It returns the original request tuples
unchanged. The product positive is an exact immutable
`GET .../composition-revisions/{accepted_revision_id}` assertion. The planted
negative calls this same checker directly, with fixture and immutable-read
controls present.
