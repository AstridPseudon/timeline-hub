# R2 native and derived partition continuation

Base fb97d24bf. Assessed interface: `_nested_mirrors` currently partitions only compiler writes and `_stage_restoration_orders` uses their first/last endpoints. Actual split native aggregates follow four mirrors, so partition attribution and order helper endpoints require narrow changes. Detached native observation replay will supply completed stage endpoints; native inverse execution and strict canonical effect comparison remain authoritative. No contract/caller shape change.

Permanent inputs copied before validation into own worker evidence: split-before-validation.json, split-classification.json, retained-actual-A-image.json. Source modules captured before edits. Final results pending.
