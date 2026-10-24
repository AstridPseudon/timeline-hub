## PASS — F-normal-publish-remainder integrated review

- Agent: `1f15f274824fadca722feb8676e6746dbd237f64`, tree `1ac5f2d6…`
- Runtime: `1d9ddba546f8fb1300f55ff62607ed492719cbaa`, tree `f56c396c…`
- `e149` `store.py` blob and regression-test blob match HOME exactly.
- Worktree clean; `git diff --check HEAD^1 HEAD` passed.

### Exact eight membership mapping

| Original selector | Evidence | Result |
|---|---|---|
| `test_nudge_disjoint_clips_merge_onto_peer_head` | 0557 JUnit | PASS |
| `test_ordinary_publish_changed_key_payload_and_force_never_write` | 0557 JUnit | PASS |
| `test_ordinary_publish_exact_retry_and_narration_resume[1]` | 0557 JUnit | PASS |
| `test_ordinary_publish_exact_retry_and_narration_resume[2]` | 0557 JUnit | PASS |
| `test_ordinary_publish_preserves_complete_closure_and_followups` | HOME JUnit | PASS, `1 passed in 6.34s` |
| `test_ordinary_publish_recovers_narration_before_flight` | 0557 JUnit | PASS |
| `test_a_publish_with_a_client_writes_through_that_client` | 0557 JUnit | PASS |
| `test_a_publish_with_no_client_writes_through_the_connection_it_opens` | 0557 JUnit | PASS |

The seven 0557 receipts remain scoped to their named selectors; no missing memberships were inferred.

The original normal-publish source is unchanged versus `2007cf…`: file, module AST, target body, and all 22 predicate AST hashes match exactly.

### Publication path

`Checkout.publish → _commit_document → TimelineSession.open → resolve_ids → open_composition(_raw_projection=True) → normal submit/flush → client.timelines.commit → WorkspaceClient.commit_timeline`.

The raw reader avoids renderer timing imports while preserving the authenticated project/timeline/head pair.

### Limits

No HTTP/socket, installed-profile, full-suite, browser, provisioning, or complete reply-variant qualification is claimed. C0 wire semantics and all optional reply fields remain unverified beyond static source/mock boundaries. No original body or 21-control repeat was run.

Commit message and `DONE` marker created.