# G4/R2 timeline scope inverse repair

The two inverse binding existence checks now distinguish an authenticated whole-timeline closure binding from an entity reference. The scope is accepted only when its existing physical revision/content pin matches the record's captured `timeline` read. Its captured scope read remains guarded against intervening writes; the inverse's new publication revision is not incorrectly treated as an entity change. Unknown and mismatched references still refuse.

Evidence: unchanged real Runtime bootstrap positives **3 passed** against Runtime `780da6d605033ca71dbe2ad48c10ec2870ea4865`; provider/doc.patch/inverse/source/later-write neighbors **238 passed, 46 deselected**; provider file **112 passed**; Ruff **2150/2150**; private focused mypy passed; `git diff --check` passed. Normal mypy baseline remains environment-blocked by missing YAML/NumPy stubs. No full suite was run. Independent review is still required before merge.
