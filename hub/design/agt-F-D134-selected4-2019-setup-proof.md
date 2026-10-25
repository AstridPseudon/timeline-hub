# D134 selected-schema setup proof

The retired HTTP fixture setup now registers the existing Agent commit provider,
reads the pristine Runtime head, and submits one normal `commitTimeline` request
with a guarded `doc.patch` root set whose `before` and `value` are deep copies of
the exact pristine parent payload. The fixture asserts the accepted parent
payload is unchanged before closing the in-process service and starting the real
Runtime HTTP daemon.

No source mapping, accepted history, item allocation, pin, or downstream live
readback/restart/undo purpose was fabricated or removed. The seven UNKNOWN cases
in the reviewed partition were not edited.
