Normal API data loss: Main ClipAction → useStaleVariants → patchRegistry → shotTimelineDataProvider.saveTimeline visibly refuses but recovery loses chosen replacement (variant-new becomes variant-old).
Evidence: app-m2-popup-main-swap-refusal-draft-proof, permanent RED test1FAIL/7PASS, original real caller; no production edits or fake media binding.
Recommend smallest existing registry argument threading into draft/save recovery, preserving raw child/root and zero canonical writes on refusal. No new store/DTO/writer and no inferred owner/oldMedia.
Candidate fix worker is active; independent data-safety review and actual route proof precede merge. Other writers/gates continue.
Not covered because: this is a newly reproduced normal-path recoverable-draft data-loss finding, an explicit escalation category despite the settled preservation direction.
Rule that would let me decide next time: existing draft-carrier threading that preserves a visibly refused user edit without any new writer, authority or storage may land after independent review and regression proof.
